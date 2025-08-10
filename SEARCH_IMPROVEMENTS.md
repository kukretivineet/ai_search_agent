# Search Quality Improvements

## Overview

Enhanced the search system to provide more accurate and relevant results by implementing strict filtering and better query understanding.

## Key Improvements

### 1. Enhanced Query Intent Parsing

- **Price Constraints**: Now supports various formats:

  - "under 500", "below 1000", "less than 800"
  - "above 600", "over 1200"
  - Symbolic operators: "<500", ">600", "<=1000", ">=800"
  - Currency variations: "under rs 500", "above rs. 1000"

- **Category Detection**: Improved keyword matching for:

  - Shoes: shoe, shoes, footwear, sneaker, sneakers, boots, sandals
  - Shirts: shirt, shirts, tshirt, t-shirt, top, blouse, polo
  - Pants: pant, pants, trouser, trousers, jeans, bottoms, chinos
  - Dresses: dress, gown, frock, maxi, midi
  - Jackets: jacket, blazer, coat, outerwear, hoodie

- **Color Recognition**: Enhanced color keyword detection for accurate matching

### 2. Strict MongoDB Filtering

- **Category Enforcement**: Search results MUST match at least one detected category
- **Price Range Enforcement**: Strict adherence to price constraints (under/above)
- **Color Preference**: Colors boost relevance but don't exclude results (configurable)

### 3. Repository Layer Enhancements

- Added `filters` parameter to all search methods:

  - `search_products_text(query, limit, filters=None)`
  - `search_products_vector(vector, limit, filters=None)`
  - `search_products_hybrid(query, vector, limit, filters=None)`

- **Vector Search Optimization**:
  - Increased candidate sampling (limit \* 60)
  - Post-filtering with MongoDB $match
  - Proper sorting and final limiting

### 4. Search Service Integration

- Parse intent for every search request
- Build strict MongoDB filters from intent
- Apply filters at database level for efficiency
- Additional color boosting for hybrid search results

## Example Query Processing

**Query**: "red shoes under 500"

1. **Intent Parsing**:

   ```json
   {
     "categories": ["shoes"],
     "colors": ["red"],
     "price_constraints": { "under": 500 },
     "keywords": ["red", "shoes"]
   }
   ```

2. **MongoDB Filters**:

   ```json
   {
     "$and": [
       {
         "$or": [
           { "category": { "$regex": "shoes", "$options": "i" } },
           { "sub_category": { "$regex": "shoes", "$options": "i" } },
           { "title": { "$regex": "shoes", "$options": "i" } }
         ]
       },
       {
         "$or": [
           { "selling_price_numeric": { "$lte": 500 } },
           { "price_inr": { "$lte": 500 } }
         ]
       }
     ]
   }
   ```

3. **Results**: Only products that:
   - Are shoes (category/sub_category/title contains "shoes")
   - Cost 500 or less
   - Red color items get relevance boost but aren't filtered out

## Benefits

1. **Accuracy**: Results strictly match user intent (category + price)
2. **Relevance**: Color and other preferences boost ranking
3. **Performance**: Database-level filtering reduces processing overhead
4. **Flexibility**: Easy to add new categories, colors, or constraint types

## File Changes

- `app/domain/search/services.py`: Enhanced intent parsing and filter building
- `app/repositories/product_repository.py`: Added strict filtering support
- `app/services/search_service.py`: Integrated filtering across all search modes
- `test_search_improvements.py`: Comprehensive tests for new functionality

## Usage

The improvements are automatically applied to all existing search endpoints. No API changes required - better results with the same interface.

For "red shoes under 500":

- ✅ Will return: Red shoes under ₹500, other shoes under ₹500 (red boosted)
- ❌ Won't return: Shirts, pants, items over ₹500, non-shoe products

This ensures users get exactly what they're looking for!
