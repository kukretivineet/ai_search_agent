"""
Search Domain Service
Pure business logic for search operations following DDD patterns
"""

import re
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class SearchDomainService:
    """
    Domain service containing pure business logic for search operations
    No dependencies on external services or infrastructure
    """
    
    def __init__(self):
        self.category_keywords = {
            'shirt': ['shirt', 'shirts', 'tshirt', 't-shirt', 'top', 'blouse', 'polo'],
            'pant': ['pant', 'pants', 'trouser', 'trousers', 'jeans', 'bottoms', 'chinos'],
            'dress': ['dress', 'gown', 'frock', 'maxi', 'midi'],
            'shoes': ['shoe', 'shoes', 'footwear', 'sneaker', 'sneakers', 'boots', 'sandals'],
            'jacket': ['jacket', 'blazer', 'coat', 'outerwear', 'hoodie'],
        }
        
        self.color_keywords = [
            'red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 
            'purple', 'orange', 'brown', 'gray', 'grey', 'navy', 'maroon'
        ]
        
        self.price_patterns = {
            'under': r'under\s+(?:rs\.?\s*)?(\d+)',
            'below': r'below\s+(?:rs\.?\s*)?(\d+)',
            'less_than': r'less\s+than\s+(?:rs\.?\s*)?(\d+)',
            'above': r'above\s+(?:rs\.?\s*)?(\d+)',
            'over': r'over\s+(?:rs\.?\s*)?(\d+)',
            # Common shorthand like ">600", "< 500", "<=1000"
            'lte_symbol': r'<=\s*(\d+)',
            'gte_symbol': r'>=\s*(\d+)',
            'lt_symbol': r'<\s*(\d+)',
            'gt_symbol': r'>\s*(\d+)',
        }
    
    def parse_search_intent(self, query: str) -> Dict[str, Any]:
        """
        Parse search query and extract user intent
        
        Args:
            query: Raw search query string
            
        Returns:
            Dictionary containing parsed intent
        """
        query_lower = query.lower().strip()
        
        intent = {
            'original_query': query,
            'normalized_query': query_lower,
            'categories': [],
            'colors': [],
            'price_constraints': {},
            'keywords': [],
            'filters': {}
        }
        
        # Extract categories
        for category, keywords in self.category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                intent['categories'].append(category)
        
        # Extract colors
        intent['colors'] = [color for color in self.color_keywords if color in query_lower]
        
        # Extract price constraints
        for constraint_type, pattern in self.price_patterns.items():
            match = re.search(pattern, query_lower)
            if match:
                value = int(match.group(1))
                if constraint_type in {'lt_symbol', 'under', 'below', 'less_than'}:
                    intent['price_constraints']['under'] = value
                elif constraint_type in {'lte_symbol'}:
                    intent['price_constraints']['under'] = value
                elif constraint_type in {'gt_symbol', 'above', 'over'}:
                    intent['price_constraints']['above'] = value
                elif constraint_type in {'gte_symbol'}:
                    intent['price_constraints']['above'] = value
        
        # Extract keywords (remove stop words)
        words = re.findall(r'\b\w+\b', query_lower)
        stop_words = {'for', 'and', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'is', 'are', 'with'}
        intent['keywords'] = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Build additional filters
        intent['filters'] = self._build_filters(intent)
        
        return intent
    
    def build_text_query(self, search_intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build MongoDB text search query from parsed intent
        
        Args:
            search_intent: Parsed search intent
            
        Returns:
            MongoDB query dictionary
        """
        query_parts = []
        
        # Add keyword search (regex-based to avoid text index requirement)
        if search_intent['keywords']:
            keyword_filters = []
            for keyword in search_intent['keywords']:
                keyword_filters.extend([
                    {'title': {'$regex': keyword, '$options': 'i'}},
                    {'description': {'$regex': keyword, '$options': 'i'}},
                    {'brand': {'$regex': keyword, '$options': 'i'}}
                ])
            if keyword_filters:
                query_parts.append({'$or': keyword_filters})
        
        # Add category filters
        if search_intent['categories']:
            category_regex = '|'.join(search_intent['categories'])
            query_parts.append({
                '$or': [
                    {'category': {'$regex': category_regex, '$options': 'i'}},
                    {'sub_category': {'$regex': category_regex, '$options': 'i'}}
                ]
            })
        
        # Add color filters
        if search_intent['colors']:
            color_filters = []
            for color in search_intent['colors']:
                color_filters.extend([
                    {'title': {'$regex': color, '$options': 'i'}},
                    {'product_details.Color': {'$regex': color, '$options': 'i'}}
                ])
            if color_filters:
                query_parts.append({'$or': color_filters})
        
        # Add price constraints
        if search_intent['price_constraints']:
            price_query = {}
            for constraint_type, value in search_intent['price_constraints'].items():
                if constraint_type in ['under', 'below', 'less_than']:
                    price_query['$lte'] = value
                elif constraint_type in ['above', 'over']:
                    price_query['$gte'] = value
            
            if price_query:
                query_parts.append({
                    '$or': [
                        {'selling_price_numeric': price_query},
                        {'price_inr': price_query}
                    ]
                })
        
        # Combine all query parts
        if query_parts:
            return {'$and': query_parts} if len(query_parts) > 1 else query_parts[0]
        else:
            # Fallback to regex search on title and description
            return {
                '$or': [
                    {'title': {'$regex': search_intent['original_query'], '$options': 'i'}},
                    {'description': {'$regex': search_intent['original_query'], '$options': 'i'}}
                ]
            }
    
    def build_mongo_filters(self, intent: Dict[str, Any], strict_color: bool = False) -> Dict[str, Any]:
        """Build strict MongoDB filters from intent.
        
        Enforces category and price strictly. Color is optional: when strict_color
        is True, enforce it; otherwise, it will be used only for boosting outside DB.
        
        Args:
            intent: Parsed intent dictionary
            strict_color: Whether to enforce color as a filter
        
        Returns:
            A MongoDB filter document suitable for $match stages.
        """
        filters: List[Dict[str, Any]] = []
        
        # Category: strict – require at least one category keyword to appear
        if intent.get('categories'):
            category_regex = '|'.join(map(re.escape, intent['categories']))
            filters.append({
                '$or': [
                    {'category': {'$regex': category_regex, '$options': 'i'}},
                    {'sub_category': {'$regex': category_regex, '$options': 'i'}},
                    {'title': {'$regex': category_regex, '$options': 'i'}},
                ]
            })
        
        # Price: strict range
        price_constraints = intent.get('price_constraints', {})
        if price_constraints:
            price_query: Dict[str, Any] = {}
            under = price_constraints.get('under')
            above = price_constraints.get('above')
            if under is not None:
                price_query['$lte'] = under
            if above is not None:
                price_query['$gte'] = above
            if price_query:
                filters.append({
                    '$or': [
                        {'selling_price_numeric': price_query},
                        {'price_inr': price_query}
                    ]
                })
        
        # Color: optional strictness
        if strict_color and intent.get('colors'):
            color_regex = '|'.join(map(re.escape, intent['colors']))
            filters.append({
                '$or': [
                    {'title': {'$regex': color_regex, '$options': 'i'}},
                    {'product_details.Color': {'$regex': color_regex, '$options': 'i'}}
                ]
            })
        
        return {'$and': filters} if filters else {}
    
    def _build_filters(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Build additional filters from intent"""
        filters = {}
        
        # Brand filters (if brand names detected in keywords)
        brand_keywords = ['nike', 'adidas', 'puma', 'reebok', 'levis', 'zara']
        detected_brands = [brand for brand in brand_keywords if brand in intent['normalized_query']]
        if detected_brands:
            filters['brands'] = detected_brands
        
        # Size filters (if size mentioned)
        size_patterns = [r'\b(xs|s|m|l|xl|xxl|xxxl)\b', r'\b(\d{2,3})\b']
        for pattern in size_patterns:
            matches = re.findall(pattern, intent['normalized_query'])
            if matches:
                filters['sizes'] = matches
        
        return filters
    
    def calculate_relevance_score(
        self, 
        document: Dict[str, Any], 
        search_intent: Dict[str, Any]
    ) -> float:
        """
        Calculate relevance score for a document based on search intent
        Pure business logic for ranking
        
        Args:
            document: Product document
            search_intent: Parsed search intent
            
        Returns:
            Relevance score (0.0 - 1.0)
        """
        score = 0.0
        max_score = 0.0
        
        # Title match scoring
        title = document.get('title', '').lower()
        for keyword in search_intent['keywords']:
            max_score += 0.3
            if keyword in title:
                score += 0.3
        
        # Category match scoring
        doc_category = document.get('category', '').lower()
        doc_sub_category = document.get('sub_category', '').lower()
        for category in search_intent['categories']:
            max_score += 0.25
            if category in doc_category or category in doc_sub_category or category in title:
                score += 0.25
        
        # Brand match scoring
        doc_brand = document.get('brand', '').lower()
        for keyword in search_intent['keywords']:
            if keyword in doc_brand:
                max_score += 0.1
                score += 0.1
        
        # Color match scoring (preferred but not mandatory)
        for color in search_intent['colors']:
            max_score += 0.2
            if color in title or color in document.get('description', '').lower() or \
               color in str(document.get('product_details', {}).get('Color', '')).lower():
                score += 0.2
        
        # Price relevance
        if search_intent['price_constraints']:
            max_score += 0.2
            doc_price = document.get('selling_price_numeric') or document.get('price_inr') or 0
            try:
                doc_price = float(doc_price)
            except Exception:
                doc_price = 0
            if doc_price > 0:
                under = search_intent['price_constraints'].get('under')
                above = search_intent['price_constraints'].get('above')
                ok = True
                if under is not None and not (doc_price <= under):
                    ok = False
                if above is not None and not (doc_price >= above):
                    ok = False
                if ok:
                    score += 0.2
        
        # Normalize score
        return score / max_score if max_score > 0 else 0.0
    
    def validate_search_query(self, query: str) -> Dict[str, Any]:
        """
        Validate search query and provide suggestions
        
        Args:
            query: Search query to validate
            
        Returns:
            Validation results with suggestions
        """
        validation = {
            'is_valid': True,
            'issues': [],
            'suggestions': [],
            'query_type': 'general'
        }
        
        if not query or not query.strip():
            validation['is_valid'] = False
            validation['issues'].append('Empty query')
            validation['suggestions'].append('Enter a search term')
            return validation
        
        if len(query.strip()) < 2:
            validation['is_valid'] = False
            validation['issues'].append('Query too short')
            validation['suggestions'].append('Enter at least 2 characters')
            return validation
        
        if len(query) > 200:
            validation['issues'].append('Query very long')
            validation['suggestions'].append('Try a shorter, more specific query')
        
        # Detect query type
        intent = self.parse_search_intent(query)
        if intent['categories']:
            validation['query_type'] = 'category'
        elif intent['colors']:
            validation['query_type'] = 'color'
        elif intent['price_constraints']:
            validation['query_type'] = 'price'
        
        return validation
