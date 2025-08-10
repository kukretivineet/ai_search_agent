"""
Test search intent parsing and filtering for improved search quality
"""

import pytest
from app.domain.search.services import SearchDomainService


def test_search_intent_parsing():
    """Test that search intent parsing works correctly for various queries"""
    service = SearchDomainService()
    
    # Test red shoes query
    intent = service.parse_search_intent("red shoes")
    assert "shoes" in intent['categories']
    assert "red" in intent['colors']
    assert len(intent['keywords']) >= 2
    
    # Test price constraints
    intent = service.parse_search_intent("shoes under 500")
    assert "shoes" in intent['categories'] 
    assert intent['price_constraints']['under'] == 500
    
    # Test above price
    intent = service.parse_search_intent("shirt above 600")
    assert "shirt" in intent['categories']
    assert intent['price_constraints']['above'] == 600
    
    # Test complex query
    intent = service.parse_search_intent("red t-shirt under rs 1000")
    assert "shirt" in intent['categories']
    assert "red" in intent['colors']
    assert intent['price_constraints']['under'] == 1000


def test_mongo_filter_building():
    """Test that MongoDB filters are built correctly"""
    service = SearchDomainService()
    
    # Test category + price filter
    intent = {
        'categories': ['shoes'],
        'colors': ['red'],
        'price_constraints': {'under': 500},
        'keywords': ['red', 'shoes']
    }
    
    filters = service.build_mongo_filters(intent, strict_color=False)
    
    # Should have category filter
    assert '$and' in filters
    and_conditions = filters['$and']
    
    # Find category filter
    category_filter_found = False
    price_filter_found = False
    
    for condition in and_conditions:
        if '$or' in condition:
            or_conditions = condition['$or']
            # Check if any condition has category/title regex
            for or_cond in or_conditions:
                if 'category' in or_cond and '$regex' in or_cond['category']:
                    category_filter_found = True
                elif ('selling_price_numeric' in or_cond or 'price_inr' in or_cond):
                    price_filter_found = True
    
    assert category_filter_found
    assert price_filter_found


def test_relevance_scoring():
    """Test relevance scoring for color and category matching"""
    service = SearchDomainService()
    
    intent = {
        'categories': ['shoes'],
        'colors': ['red'],
        'price_constraints': {'under': 500},
        'keywords': ['red', 'shoes']
    }
    
    # Perfect match document
    perfect_doc = {
        'title': 'Red Sports Shoes',
        'category': 'Footwear',
        'sub_category': 'shoes',
        'brand': 'Nike',
        'selling_price_numeric': 450
    }
    
    score = service.calculate_relevance_score(perfect_doc, intent)
    assert score > 0.8  # Should have high relevance
    
    # Poor match document
    poor_doc = {
        'title': 'Blue Shirt',
        'category': 'Clothing',
        'brand': 'Zara',
        'selling_price_numeric': 800  # Over budget
    }
    
    score = service.calculate_relevance_score(poor_doc, intent)
    assert score < 0.3  # Should have low relevance


if __name__ == "__main__":
    test_search_intent_parsing()
    test_mongo_filter_building()
    test_relevance_scoring()
    print("All tests passed! Search intent parsing and filtering working correctly.")
