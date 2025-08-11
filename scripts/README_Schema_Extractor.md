# MongoDB Schema Extractor

A comprehensive tool to extract and document MongoDB database schemas in markdown format.

## Overview

The MongoDB Schema Extractor analyzes all collections in a MongoDB database, samples documents to understand the data structure, and generates detailed documentation in markdown format. This is particularly useful for:

- **Database Documentation**: Automatically generate up-to-date schema documentation
- **Data Analysis**: Understand the structure and relationships of your data
- **Migration Planning**: Document existing schemas before database migrations
- **Team Onboarding**: Provide clear documentation for new team members

## Features

- ✅ **Comprehensive Analysis**: Analyzes all collections in the database
- ✅ **Type Detection**: Automatically detects and documents field types
- ✅ **Nested Objects**: Handles complex nested document structures
- ✅ **Array Analysis**: Analyzes array contents and types
- ✅ **Index Documentation**: Documents all indexes on collections
- ✅ **Sample Data**: Provides example values for better understanding
- ✅ **Statistics**: Includes document counts and collection statistics
- ✅ **Markdown Output**: Clean, readable markdown documentation

## Generated Documentation

The script generated a comprehensive schema for the `pepagora_dev` database with **36 collections**:

### Key Collections Analyzed:

- `users` - User account information
- `businessprofiles` - Business profile data
- `adminusers` - Administrative user accounts
- `categories` - Product/service categories
- `products` - Product catalog data
- `orders` - Order management
- `payments` - Payment processing data
- And 29 more collections...

### Documentation Structure:

1. **Table of Contents** - Quick navigation to all collections
2. **Collection Details** - Document counts and sample sizes
3. **Field Analysis** - Complete field listing with types and examples
4. **Index Information** - All indexes with their configurations

## Installation

### Prerequisites

```bash
# Install required packages
pip install motor pymongo pydantic-settings python-dotenv
```

### Environment Setup

Create a `.env` file with your MongoDB connection details:

```env
MONGODB_URI=mongodb://localhost:27017/
PEPAGORA_DB_NAME=pepagora_dev
SAMPLE_SIZE=100
OUTPUT_FILE=pepagora_dev.md
```

## Usage

### Basic Usage

```bash
# Run the schema extraction
python scripts/extract_pepagora_schema.py
```

### Configuration Options

The script accepts the following configuration parameters:

| Parameter          | Default                      | Description                                  |
| ------------------ | ---------------------------- | -------------------------------------------- |
| `mongodb_uri`      | `mongodb://localhost:27017/` | MongoDB connection string                    |
| `pepagora_db_name` | `pepagora_dev`               | Database name to analyze                     |
| `sample_size`      | `100`                        | Number of documents to sample per collection |
| `output_file`      | `pepagora_dev.md`            | Output markdown file name                    |

### Custom Configuration

```python
from extract_pepagora_schema import MongoSchemaExtractor, SchemaExtractorSettings

# Custom settings
settings = SchemaExtractorSettings(
    mongodb_uri="mongodb+srv://user:pass@cluster.mongodb.net/",
    pepagora_db_name="your_database",
    sample_size=50,
    output_file="custom_schema.md"
)

extractor = MongoSchemaExtractor(settings)
await extractor.run()
```

## Output Format

The generated markdown file includes:

### Collection Overview

```markdown
## collection_name

**Document Count:** 1,234
**Sample Size:** 100
```

### Field Documentation

```markdown
### Fields

| Field         | Type          | Example          |
| ------------- | ------------- | ---------------- |
| `_id`         | ObjectId      |                  |
| `name`        | string        | John Doe         |
| `email`       | string        | john@example.com |
| `profile`     | object        |                  |
| `profile.age` | integer       | 25               |
| `tags`        | array<string> |                  |
```

### Index Information

```markdown
### Indexes

**email_1**

- Type: Unique
- Keys:
  - `email`: ascending
```

## Type Detection

The extractor automatically detects and documents various data types:

- **Primitive Types**: `string`, `integer`, `number`, `boolean`, `null`
- **MongoDB Types**: `ObjectId`, `date`
- **Complex Types**: `object`, `array<type>`
- **Mixed Arrays**: `array<string | integer>`
- **Nested Objects**: Full path documentation like `profile.address.city`

## Performance

- **Sampling Strategy**: Configurable sampling size to balance accuracy vs. speed
- **Async Processing**: Non-blocking analysis of collections
- **Memory Efficient**: Processes documents in batches
- **Progress Logging**: Real-time progress updates

## Example Output

The tool generated a comprehensive 2,418-line documentation file covering:

- 36 collections
- Hundreds of fields with types and examples
- Complete index documentation
- Nested object analysis up to multiple levels deep

## Error Handling

The script includes robust error handling for:

- Connection failures
- Permission issues
- Malformed documents
- Missing collections
- Index access problems

## Extending the Tool

The code is designed to be extensible:

```python
# Add custom field analysis
def custom_field_analyzer(self, value):
    # Your custom logic here
    return custom_type

# Add collection filtering
def filter_collections(self, collection_names):
    # Filter logic
    return filtered_names
```

## MongoDB Atlas Support

Works seamlessly with MongoDB Atlas:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

## Contributing

Feel free to extend this tool with additional features:

- Custom field analyzers
- Different output formats (JSON, HTML)
- Collection filtering
- Advanced type inference
- Schema comparison utilities

## Generated Files

- `pepagora_dev.md` - Complete schema documentation (2,418 lines)
- `extract_pepagora_schema.py` - Main extraction script
- `extract_schema_usage.py` - Usage examples

The generated schema documentation is now available and provides a complete overview of your `pepagora_dev` database structure!
