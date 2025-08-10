#!/usr/bin/env python3
"""
Domain services for embedding text generation and processing.
"""

import re
from typing import Dict, Any, Optional, List
from app.domain.embeddings.models import EmbeddingText


class EmbeddingTextService:
    """Service for generating structured embedding text."""
    
    # Boilerplate patterns to remove from descriptions
    BOILERPLATE_PATTERNS = [
        r'\b(?:buy|shop|online|store|sale|offer|deal|discount|price|₹|rs\.?|inr)\b',
        r'\b(?:free|delivery|shipping|return|exchange|warranty|guarantee)\b',
        r'\b(?:best|top|great|amazing|awesome|fantastic|excellent|quality)\b',
        r'\b(?:latest|new|trending|popular|hot|featured)\b',
        r'\s{2,}',  # Multiple spaces
    ]
    
    @classmethod
    def build_embedding_text(cls, product_data: Dict[str, Any]) -> str:
        """Build structured embedding text from product data."""
        
        # Extract basic fields
        title = cls._clean_text(product_data.get("title", ""))
        brand = cls._extract_brand(product_data)
        category = cls._extract_category(product_data)
        description = cls._clean_description(product_data.get("description", ""))
        price = cls._extract_price(product_data)
        
        # Extract attributes based on category
        attributes = cls._extract_attributes(product_data, category)
        
        # Create embedding text object
        embedding_text = EmbeddingText(
            title=title,
            brand=brand,
            category=category,
            attributes=attributes,
            price_inr=price,
            description=description
        )
        
        return embedding_text.to_structured_text()
    
    @classmethod
    def _clean_text(cls, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Convert to lowercase and strip
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    @classmethod
    def _clean_description(cls, description: str) -> str:
        """Clean product description by removing boilerplate."""
        if not description:
            return ""
        
        cleaned = description.lower()
        
        # Remove boilerplate patterns
        for pattern in cls.BOILERPLATE_PATTERNS:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Remove common prefixes/suffixes
        cleaned = re.sub(r'^(description|about|details?):\s*', '', cleaned)
        cleaned = re.sub(r'\s*(read more|view details|see more).*$', '', cleaned)
        
        return cleaned[:200] if len(cleaned) > 200 else cleaned
    
    @classmethod
    def _extract_brand(cls, product_data: Dict[str, Any]) -> Optional[str]:
        """Extract brand from product data."""
        brand = product_data.get("brand", "").strip()
        if brand and brand.lower() not in ["unknown", "na", "n/a", ""]:
            return cls._clean_text(brand)
        return None
    
    @classmethod
    def _extract_category(cls, product_data: Dict[str, Any]) -> str:
        """Extract hierarchical category."""
        category = cls._clean_text(product_data.get("category", ""))
        sub_category = cls._clean_text(product_data.get("sub_category", ""))
        
        if category and sub_category:
            return f"{category}>{sub_category}"
        elif category:
            return category
        else:
            return "unknown"
    
    @classmethod
    def _extract_price(cls, product_data: Dict[str, Any]) -> Optional[float]:
        """Extract numeric price."""
        price_fields = ["selling_price_numeric", "selling_price", "actual_price_numeric", "actual_price"]
        
        for field in price_fields:
            price_value = product_data.get(field)
            if price_value:
                if isinstance(price_value, (int, float)):
                    return float(price_value)
                elif isinstance(price_value, str):
                    # Extract numeric value from string
                    price_match = re.search(r'[\d,]+', price_value.replace(',', ''))
                    if price_match:
                        try:
                            return float(price_match.group())
                        except ValueError:
                            continue
        return None
    
    @classmethod
    def _extract_attributes(cls, product_data: Dict[str, Any], category: str) -> Dict[str, str]:
        """Extract category-specific attributes."""
        attributes = {}
        
        # Get product details
        product_details = product_data.get("product_details", [])
        if isinstance(product_details, list):
            for detail in product_details:
                if isinstance(detail, dict):
                    for key, value in detail.items():
                        key_clean = cls._to_snake_case(key)
                        value_clean = cls._clean_text(str(value))
                        if value_clean and value_clean not in ["na", "n/a", "unknown"]:
                            attributes[key_clean] = value_clean
        
        # Category-specific attribute extraction
        if "clothing" in category.lower():
            attributes.update(cls._extract_fashion_attributes(product_data))
        elif "electronics" in category.lower():
            attributes.update(cls._extract_electronics_attributes(product_data))
        elif "home" in category.lower():
            attributes.update(cls._extract_home_attributes(product_data))
        
        return attributes
    
    @classmethod
    def _extract_fashion_attributes(cls, product_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract fashion-specific attributes."""
        attributes = {}
        
        # Common fashion attributes
        fashion_fields = [
            "color", "colour", "size", "material", "fabric", "pattern", 
            "fit", "occasion", "sleeve", "neck", "style"
        ]
        
        for field in fashion_fields:
            value = product_data.get(field)
            if value:
                attributes[field] = cls._clean_text(str(value))
        
        return attributes
    
    @classmethod
    def _extract_electronics_attributes(cls, product_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract electronics-specific attributes."""
        attributes = {}
        
        # Common electronics attributes
        electronics_fields = [
            "brand", "model", "color", "storage", "ram", "processor", 
            "screen_size", "battery", "camera", "connectivity"
        ]
        
        for field in electronics_fields:
            value = product_data.get(field)
            if value:
                attributes[field] = cls._normalize_electronics_value(str(value))
        
        return attributes
    
    @classmethod
    def _extract_home_attributes(cls, product_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract home & kitchen attributes."""
        attributes = {}
        
        # Common home attributes
        home_fields = [
            "color", "material", "size", "capacity", "power", "warranty",
            "brand", "type", "style", "finish"
        ]
        
        for field in home_fields:
            value = product_data.get(field)
            if value:
                attributes[field] = cls._clean_text(str(value))
        
        return attributes
    
    @classmethod
    def _normalize_electronics_value(cls, value: str) -> str:
        """Normalize electronics attribute values."""
        value = cls._clean_text(value)
        
        # Normalize storage units
        value = re.sub(r'\b(\d+)\s*gb\b', r'\1gb', value)
        value = re.sub(r'\b(\d+)\s*tb\b', r'\1tb', value)
        value = re.sub(r'\b(\d+)\s*mb\b', r'\1mb', value)
        
        # Normalize RAM
        value = re.sub(r'\b(\d+)\s*gb\s*ram\b', r'\1gb ram', value)
        
        # Normalize screen size
        value = re.sub(r'\b(\d+(?:\.\d+)?)\s*inch\b', r'\1"', value)
        
        return value
    
    @classmethod
    def _to_snake_case(cls, text: str) -> str:
        """Convert text to snake_case."""
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        text = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', text)
        text = re.sub(r'[\s\-\.]+', '_', text)
        return text.lower().strip('_')
