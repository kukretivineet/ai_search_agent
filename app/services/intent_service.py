"""
LLM Intent Service
Extracts structured user intent and rephrased query using an LLM.
Follows application layer responsibilities (calls external API) and returns
pure data structures consumable by domain services.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from openai import AsyncOpenAI


logger = logging.getLogger(__name__)


class LLMIntent(BaseModel):
    """Structured intent extracted by LLM."""

    rephrased_query: str = Field(
        ..., description="Short, clear reformulation of the user's query for retrieval"
    )
    categories: List[str] = Field(default_factory=list, description="Inferred product categories")
    colors: List[str] = Field(default_factory=list, description="Mentioned or inferred colors")
    brands: List[str] = Field(default_factory=list, description="Mentioned brands")
    sizes: List[str] = Field(default_factory=list, description="Mentioned sizes, e.g., S, M, 42")
    budget_min: Optional[float] = Field(None, description="Minimum budget in INR or local currency")
    budget_max: Optional[float] = Field(None, description="Maximum budget in INR or local currency")
    gifting: bool = Field(default=False, description="Whether query implies a gift use-case")
    occasion: Optional[str] = Field(None, description="Occasion like birthday, anniversary, diwali")
    recipient: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Recipient info e.g., relation, likely gender, age range, marital status",
    )
    keywords: List[str] = Field(default_factory=list, description="Key terms for matching")
    locale: Optional[str] = Field(None, description="Locale if inferred")
    confidence: float = Field(
        0.0, description="Extractor confidence 0.0-1.0 for downstream fallback decisions"
    )


class LLMIntentService:
    """LLM-based intent extraction and query rewriting.

    Note: Do not use this in the domain layer. Keep external calls in the application layer.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self._logger = logging.getLogger(self.__class__.__name__)

    async def parse_intent(self, query: str) -> Optional[LLMIntent]:
        """Parse search intent using an LLM and return a structured object.

        Args:
            query: User's raw query

        Returns:
            LLMIntent or None on failure
        """
        system_prompt = (
            "You are an e-commerce search intent parser. Return ONLY valid JSON matching the schema. "
            "Infer recipient details (relation, likely gender, age_range, marital_status) when gifting. "
            "Infer categories, colors, brands, sizes, and budget range if present. "
            "Keep rephrased_query short and retrieval-friendly. Use INR if currency not specified. "
            "Set confidence low (<0.8) if uncertain."
        )

        schema = {
            "type": "object",
            "properties": {
                "rephrased_query": {"type": "string"},
                "categories": {"type": "array", "items": {"type": "string"}},
                "colors": {"type": "array", "items": {"type": "string"}},
                "brands": {"type": "array", "items": {"type": "string"}},
                "sizes": {"type": "array", "items": {"type": "string"}},
                "budget_min": {"type": ["number", "null"]},
                "budget_max": {"type": ["number", "null"]},
                "gifting": {"type": "boolean"},
                "occasion": {"type": ["string", "null"]},
                "recipient": {"type": ["object", "null"]},
                "keywords": {"type": "array", "items": {"type": "string"}},
                "locale": {"type": ["string", "null"]},
                "confidence": {"type": "number"},
            },
            "required": [
                "rephrased_query",
                "categories",
                "colors",
                "brands",
                "sizes",
                "gifting",
                "keywords",
                "confidence",
            ],
            "additionalProperties": True,
        }

        user_prompt = (
            "Query: \n" + query.strip() + "\n\n"
            "Return a JSON object only. Examples:\n\n"
            "Example 1 Input: 'i want something for my girlfriend under 1500'\n"
            "Example 1 Output: {\n"
            "  \"rephrased_query\": \"gift ideas for girlfriend under 1500 INR\",\n"
            "  \"categories\": [\"jewellery\", \"accessories\"],\n"
            "  \"colors\": [],\n"
            "  \"brands\": [],\n"
            "  \"sizes\": [],\n"
            "  \"budget_min\": null,\n"
            "  \"budget_max\": 1500,\n"
            "  \"gifting\": true,\n"
            "  \"occasion\": null,\n"
            "  \"recipient\": {\"relation\": \"girlfriend\", \"likely_gender\": \"female\", \"marital_status\": \"unmarried\"},\n"
            "  \"keywords\": [\"gift\", \"girlfriend\"],\n"
            "  \"locale\": \"IN\",\n"
            "  \"confidence\": 0.9\n"
            "}\n\n"
            "Example 2 Input: 'car asked shoes'\n"
            "Example 2 Output: {\n"
            "  \"rephrased_query\": \"casual shoes\",\n"
            "  \"categories\": [\"shoes\"],\n"
            "  \"colors\": [],\n"
            "  \"brands\": [],\n"
            "  \"sizes\": [],\n"
            "  \"budget_min\": null,\n"
            "  \"budget_max\": null,\n"
            "  \"gifting\": false,\n"
            "  \"occasion\": null,\n"
            "  \"recipient\": null,\n"
            "  \"keywords\": [\"shoes\", \"casual\"],\n"
            "  \"locale\": null,\n"
            "  \"confidence\": 0.85\n"
            "}"
        )

        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            content = resp.choices[0].message.content or "{}"
            data = json.loads(content)
            return LLMIntent(**data)
        except Exception as e:
            # Log only high-level error, no sensitive info
            self._logger.warning("LLM intent parse failed: %s", e)
            return None
