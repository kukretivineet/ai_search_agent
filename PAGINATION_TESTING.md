# Testing Pagination

## Manual Testing Steps

### 1. Start the Application

```bash
cd /home/vineet/Desktop/southguild\ /search_agent
python -m uvicorn app.main_search_only:app --reload --host 0.0.0.0 --port 8000
```

### 2. Open the Web Interface

Navigate to `http://localhost:8000` in your browser.

### 3. Test Basic Pagination

#### Test Search with Results

1. Search for: `"shirt"`
2. Verify you see pagination controls at the bottom
3. Check that total results and page information are displayed
4. Click "Next" to go to page 2
5. Verify results update and page counter changes
6. Click "Previous" to go back
7. Try the "Load More Results" button

#### Test API Directly

```bash
# Test page 1
curl -X POST "http://localhost:8000/api/search/" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "shirt",
       "mode": "hybrid",
       "page": 1,
       "limit": 5,
       "use_reranking": true
     }'

# Test page 2
curl -X POST "http://localhost:8000/api/search/" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "shirt",
       "mode": "hybrid",
       "page": 2,
       "limit": 5,
       "use_reranking": true
     }'
```

### 4. Test Edge Cases

#### Empty Results

- Search for: `"xyzabc12345nonexistent"`
- Verify pagination handles empty results gracefully

#### Large Result Sets

- Search for: `"clothing"`
- Test pagination with many results
- Try different page sizes (5, 10, 20)

#### Invalid Pages

- Test API with invalid page numbers
- Should handle gracefully and return valid pages

### 5. Performance Testing

#### Compare Before/After

- Search for broad terms like "fashion" or "electronics"
- Note response times for paginated vs non-paginated searches
- Verify memory usage is lower with pagination

#### Load Testing

```bash
# Install Apache Bench if not available
sudo apt-get install apache2-utils

# Test pagination performance
ab -n 100 -c 10 -T application/json -p test_payload.json http://localhost:8000/api/search/
```

Where `test_payload.json` contains:

```json
{
  "query": "shirt",
  "mode": "hybrid",
  "page": 1,
  "limit": 12,
  "use_reranking": true
}
```

## Expected Behavior

### UI Behavior

- ✅ Results load faster on first search
- ✅ Pagination controls appear when there are multiple pages
- ✅ "Load More" progressively adds results without losing current ones
- ✅ Page navigation replaces current results
- ✅ Loading indicators show during requests
- ✅ Error messages appear if requests fail

### API Behavior

- ✅ Returns proper pagination metadata
- ✅ `total` shows total available results
- ✅ `returned` shows results in current response
- ✅ `has_next` and `has_prev` indicate navigation availability
- ✅ `page` and `total_pages` show current position

### Database Behavior

- ✅ Only requested results are fetched from database
- ✅ Total count is calculated efficiently
- ✅ Memory usage remains constant regardless of total results
- ✅ Query performance is optimized for pagination

## Troubleshooting

### Common Issues

1. **Pagination controls not showing**

   - Check if `total_pages > 1` in API response
   - Verify JavaScript is loading correctly

2. **"Load More" not working**

   - Check browser console for JavaScript errors
   - Verify `has_next` is true in API response

3. **Slow pagination**

   - Check database indexes are properly set up
   - Monitor MongoDB query performance
   - Verify vector search indexes are optimized

4. **Incorrect total counts**
   - Check MongoDB aggregation pipeline
   - Verify filters are applied correctly
   - Test with simple queries first

### Debug Information

Enable logging to see pagination debug info:

```python
import logging
logging.getLogger('app.services.search_service').setLevel(logging.DEBUG)
logging.getLogger('app.repositories.product_repository').setLevel(logging.DEBUG)
```

This will show:

- Search execution details
- Pagination parameters used
- Query performance metrics
- Result counts at each stage
