"""
Unit tests for LLM Intent Service
"""

import pytest
from unittest.mock import Mock, AsyncMock
import json
from app.services.intent_service import LLMIntentService, LLMIntent


class TestLLMIntentService:
    """Test cases for LLM Intent Service"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client"""
        mock_client = Mock()
        mock_client.chat = Mock()
        mock_client.chat.completions = Mock()
        return mock_client
    
    @pytest.fixture
    def intent_service(self, mock_openai_client):
        """Create LLM intent service with mocked client"""
        service = LLMIntentService("test-api-key", "gpt-4o-mini")
        service.client = mock_openai_client
        return service
    
    @pytest.mark.asyncio
    async def test_parse_intent_girlfriend_gift(self, intent_service, mock_openai_client):
        """Test parsing intent for girlfriend gift query"""
        # Mock OpenAI response
        mock_response_data = {
            "rephrased_query": "gift ideas for girlfriend under 1500 INR",
            "categories": ["jewellery", "accessories"],
            "colors": [],
            "brands": [],
            "sizes": [],
            "budget_min": None,
            "budget_max": 1500,
            "gifting": True,
            "occasion": None,
            "recipient": {
                "relation": "girlfriend",
                "likely_gender": "female",
                "marital_status": "unmarried"
            },
            "keywords": ["gift", "girlfriend"],
            "locale": "IN",
            "confidence": 0.9
        }
        
        mock_choice = Mock()
        mock_choice.message.content = json.dumps(mock_response_data)
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        
        mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        # Test the method
        result = await intent_service.parse_intent("i want something for my girlfriend under 1500")
        
        # Assertions
        assert result is not None
        assert isinstance(result, LLMIntent)
        assert result.rephrased_query == "gift ideas for girlfriend under 1500 INR"
        assert result.categories == ["jewellery", "accessories"]
        assert result.budget_max == 1500
        assert result.gifting is True
        assert result.recipient is not None
        assert result.recipient["relation"] == "girlfriend"
        assert result.confidence == 0.9
    
    @pytest.mark.asyncio
    async def test_parse_intent_shoes_typo(self, intent_service, mock_openai_client):
        """Test parsing intent for shoes query with typo"""
        # Mock OpenAI response
        mock_response_data = {
            "rephrased_query": "casual shoes",
            "categories": ["shoes"],
            "colors": [],
            "brands": [],
            "sizes": [],
            "budget_min": None,
            "budget_max": None,
            "gifting": False,
            "occasion": None,
            "recipient": None,
            "keywords": ["shoes", "casual"],
            "locale": None,
            "confidence": 0.85
        }
        
        mock_choice = Mock()
        mock_choice.message.content = json.dumps(mock_response_data)
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        
        mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        # Test the method
        result = await intent_service.parse_intent("car asked shoes")
        
        # Assertions
        assert result is not None
        assert isinstance(result, LLMIntent)
        assert result.rephrased_query == "casual shoes"
        assert result.categories == ["shoes"]
        assert result.gifting is False
        assert result.recipient is None
        assert result.confidence == 0.85
    
    @pytest.mark.asyncio
    async def test_parse_intent_openai_error(self, intent_service, mock_openai_client):
        """Test graceful handling of OpenAI API errors"""
        # Mock OpenAI error
        mock_openai_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
        
        # Test the method
        result = await intent_service.parse_intent("test query")
        
        # Should return None on error
        assert result is None
    
    @pytest.mark.asyncio
    async def test_parse_intent_invalid_json(self, intent_service, mock_openai_client):
        """Test handling of invalid JSON response"""
        # Mock invalid JSON response
        mock_choice = Mock()
        mock_choice.message.content = "invalid json content"
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        
        mock_openai_client.chat.completions.create = AsyncMock(return_value=mock_response)
        
        # Test the method
        result = await intent_service.parse_intent("test query")
        
        # Should return None for invalid JSON
        assert result is None
    
    def test_llm_intent_model_validation(self):
        """Test LLMIntent model validation"""
        # Test valid data
        valid_data = {
            "rephrased_query": "blue shirt",
            "categories": ["clothing"],
            "colors": ["blue"],
            "brands": [],
            "sizes": [],
            "gifting": False,
            "keywords": ["blue", "shirt"],
            "confidence": 0.9
        }
        
        intent = LLMIntent(**valid_data)
        assert intent.rephrased_query == "blue shirt"
        assert intent.categories == ["clothing"]
        assert intent.colors == ["blue"]
        assert intent.confidence == 0.9
        
        # Test missing required field should raise validation error
        invalid_data = {
            "categories": ["clothing"],
            "colors": ["blue"],
            "brands": [],
            "sizes": [],
            "gifting": False,
            "keywords": ["blue", "shirt"],
            "confidence": 0.9
            # Missing rephrased_query
        }
        
        with pytest.raises(Exception):  # Pydantic validation error
            LLMIntent(**invalid_data)


if __name__ == "__main__":
    pytest.main([__file__])
