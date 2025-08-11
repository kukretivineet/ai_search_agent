#!/usr/bin/env python3
"""
Extract MongoDB schema from pepagora_dev database and generate markdown documentation.

This script connects to the MongoDB database, analyzes the structure of all collections,
and generates a comprehensive schema documentation in markdown format.
"""

import asyncio
import logging
from typing import Dict, Any, List, Set, Optional, Union
from collections import defaultdict
from datetime import datetime
import json
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import OperationFailure
from bson import ObjectId
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SchemaExtractorSettings(BaseSettings):
    """Settings for schema extraction."""
    
    mongodb_uri: str = "mongodb://localhost:27017/"
    pepagora_db_name: str = "pepagora_dev"
    sample_size: int = 100  # Number of documents to sample per collection
    output_file: str = "pepagora_dev.md"
    
    model_config = {"env_file": ".env", "extra": "ignore"}


class MongoSchemaExtractor:
    """Extract MongoDB schema and generate markdown documentation."""
    
    def __init__(self, settings: SchemaExtractorSettings):
        self.settings = settings
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self) -> None:
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.settings.mongodb_uri)
            self.database = self.client[self.settings.pepagora_db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {self.settings.pepagora_db_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def analyze_value_type(self, value: Any) -> str:
        """Analyze and return the type of a value."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "number"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, ObjectId):
            return "ObjectId"
        elif isinstance(value, datetime):
            return "date"
        elif isinstance(value, list):
            if not value:
                return "array (empty)"
            # Analyze array element types
            element_types = set()
            for item in value[:5]:  # Sample first 5 elements
                element_types.add(self.analyze_value_type(item))
            if len(element_types) == 1:
                return f"array<{list(element_types)[0]}>"
            else:
                return f"array<{' | '.join(sorted(element_types))}>"
        elif isinstance(value, dict):
            return "object"
        else:
            return f"unknown ({type(value).__name__})"
    
    def analyze_document_schema(self, doc: Dict[str, Any], path: str = "") -> Dict[str, Any]:
        """Recursively analyze document schema."""
        schema = {}
        
        for key, value in doc.items():
            full_path = f"{path}.{key}" if path else key
            value_type = self.analyze_value_type(value)
            
            if isinstance(value, dict) and value:
                # Recursively analyze nested objects
                nested_schema = self.analyze_document_schema(value, full_path)
                schema[key] = {
                    "type": "object",
                    "properties": nested_schema
                }
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # Analyze array of objects
                array_schema = {}
                for item in value[:3]:  # Sample first 3 array items
                    if isinstance(item, dict):
                        item_schema = self.analyze_document_schema(item, f"{full_path}[]")
                        # Merge schemas
                        for k, v in item_schema.items():
                            if k not in array_schema:
                                array_schema[k] = v
                            elif array_schema[k] != v:
                                # Handle type variations
                                if isinstance(array_schema[k], dict) and isinstance(v, dict):
                                    if array_schema[k].get("type") != v.get("type"):
                                        array_schema[k]["type"] = f"{array_schema[k].get('type', 'unknown')} | {v.get('type', 'unknown')}"
                
                schema[key] = {
                    "type": "array<object>",
                    "items": array_schema if array_schema else {}
                }
            else:
                schema[key] = {"type": value_type}
                
                # Add sample value for primitive types
                if value_type in ["string", "integer", "number", "boolean"] and value is not None:
                    if isinstance(value, str) and len(str(value)) < 50:
                        schema[key]["example"] = value
                    elif not isinstance(value, str):
                        schema[key]["example"] = value
        
        return schema
    
    def _to_serializable(self, value: Any) -> Any:
        """Convert MongoDB/BSON types to JSON-serializable forms.
        - ObjectId -> str
        - datetime -> ISO string
        - bytes -> base64 or hex (short)
        - Recursively handles dicts and lists
        """
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, bytes):
            return value.hex()[:32] + ("..." if len(value) > 16 else "")
        if isinstance(value, dict):
            return {k: self._to_serializable(v) for k, v in value.items()}
        if isinstance(value, list):
            # Limit very long arrays to keep markdown readable
            limited = value[:5]
            converted = [self._to_serializable(v) for v in limited]
            if len(value) > 5:
                converted.append("[... truncated ...]")
            return converted
        return value

    def _redact_sensitive(self, doc: Any) -> Any:
        """Redact sensitive fields like passwords, tokens, card numbers, secrets.
        Applies recursively to dicts/lists.
        """
        sensitive_keys = {
            "password", "pass", "pwd", "token", "access_token", "refresh_token",
            "api_key", "apikey", "secret", "client_secret", "cvv", "cardNo",
            "card_number", "card", "authorization", "auth", "otp",
        }
        if isinstance(doc, dict):
            redacted: Dict[str, Any] = {}
            for k, v in doc.items():
                lower_k = k.lower()
                if lower_k in sensitive_keys or any(s in lower_k for s in ["token", "secret", "password", "cvv", "card"]):
                    redacted[k] = "[REDACTED]"
                else:
                    redacted[k] = self._redact_sensitive(v)
            return redacted
        if isinstance(doc, list):
            return [self._redact_sensitive(v) for v in doc]
        if isinstance(doc, str):
            # Redact obvious key-like strings (e.g., sk-*, Bearer *, xoxb-*)
            if doc.startswith("sk-") or "Bearer " in doc or doc.startswith("xox"):
                return "[REDACTED]"
        return doc

    async def _get_first_document(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Fetch the first document (by _id ascending) from a collection.
        Returns a sanitized and JSON-serializable dict.
        """
        if self.database is None:
            return None
        col = self.database[collection_name]
        try:
            cursor = col.find({}, projection=None).sort("_id", 1).limit(1)
            docs = await cursor.to_list(length=1)
            if not docs:
                return None
            doc = docs[0]
            doc = self._to_serializable(doc)
            doc = self._redact_sensitive(doc)
            return doc
        except Exception as e:
            logger.warning(f"Could not fetch first document for {collection_name}: {e}")
            return None

    async def get_collection_schema(self, collection_name: str) -> Dict[str, Any]:
        """Extract schema for a specific collection."""
        logger.info(f"Analyzing collection: {collection_name}")
        
        if self.database is None:
            raise RuntimeError("Database connection not established. Call connect() first.")
        
        collection = self.database[collection_name]
        
        try:
            # Get collection stats
            stats = await self.database.command("collStats", collection_name)
            doc_count = stats.get("count", 0)
            
            # Sample documents
            sample_size = min(self.settings.sample_size, doc_count)
            documents = []
            
            if doc_count > 0:
                async for doc in collection.aggregate([{"$sample": {"size": sample_size}}]):
                    documents.append(doc)
            
            # Analyze schema
            field_types = defaultdict(set)
            all_fields = set()
            field_examples = {}
            
            for doc in documents:
                schema = self.analyze_document_schema(doc)
                self._collect_field_info(schema, field_types, all_fields, field_examples)
            
            # Get indexes
            indexes = []
            try:
                async for index in collection.list_indexes():
                    indexes.append(index)
            except Exception as e:
                logger.warning(f"Could not retrieve indexes for {collection_name}: {e}")
            
            # Fetch first document (sanitized)
            first_doc = await self._get_first_document(collection_name)
            
            return {
                "name": collection_name,
                "document_count": doc_count,
                "sample_size": len(documents),
                "fields": self._format_field_info(field_types, field_examples, all_fields),
                "indexes": indexes,
                "first_document": first_doc,
            }
            
        except OperationFailure as e:
            logger.error(f"Failed to analyze collection {collection_name}: {e}")
            return {
                "name": collection_name,
                "error": str(e),
                "document_count": 0,
                "fields": {},
                "indexes": [],
                "first_document": None,
            }
    
    def _collect_field_info(self, schema: Dict[str, Any], field_types: Dict[str, Set], 
                           all_fields: Set[str], field_examples: Dict[str, Any], prefix: str = ""):
        """Recursively collect field information from schema."""
        for field_name, field_info in schema.items():
            full_field_name = f"{prefix}.{field_name}" if prefix else field_name
            all_fields.add(full_field_name)
            
            if isinstance(field_info, dict):
                field_type = field_info.get("type", "unknown")
                field_types[full_field_name].add(field_type)
                
                if "example" in field_info:
                    field_examples[full_field_name] = field_info["example"]
                
                # Handle nested objects
                if field_type == "object" and "properties" in field_info:
                    self._collect_field_info(field_info["properties"], field_types, 
                                           all_fields, field_examples, full_field_name)
                elif field_type == "array<object>" and "items" in field_info:
                    self._collect_field_info(field_info["items"], field_types, 
                                           all_fields, field_examples, f"{full_field_name}[]")
    
    def _format_field_info(self, field_types: Dict[str, Set], field_examples: Dict[str, Any], 
                          all_fields: Set[str]) -> Dict[str, Any]:
        """Format field information for output."""
        formatted_fields = {}
        
        for field in sorted(all_fields):
            types = list(field_types[field])
            formatted_fields[field] = {
                "types": types,
                "type": " | ".join(types) if len(types) > 1 else types[0] if types else "unknown"
            }
            
            if field in field_examples:
                formatted_fields[field]["example"] = field_examples[field]
        
        return formatted_fields
    
    async def extract_all_schemas(self) -> Dict[str, Any]:
        """Extract schemas for all collections in the database."""
        logger.info("Starting schema extraction...")
        
        if self.database is None:
            raise RuntimeError("Database connection not established. Call connect() first.")
        
        # Get list of collections
        collection_names = await self.database.list_collection_names()
        logger.info(f"Found {len(collection_names)} collections: {collection_names}")
        
        schemas = {}
        
        for collection_name in sorted(collection_names):
            try:
                schema = await self.get_collection_schema(collection_name)
                schemas[collection_name] = schema
            except Exception as e:
                logger.error(f"Failed to extract schema for {collection_name}: {e}")
                schemas[collection_name] = {
                    "name": collection_name,
                    "error": str(e),
                    "document_count": 0,
                    "fields": {},
                    "indexes": []
                }
        
        return schemas
    
    def generate_markdown(self, schemas: Dict[str, Any]) -> str:
        """Generate markdown documentation from schemas."""
        md_content = []
        
        # Header
        md_content.append("# MongoDB Schema: `pepagora_dev`")
        md_content.append("")
        md_content.append(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_content.append(f"**Database:** `{self.settings.pepagora_db_name}`")
        md_content.append(f"**Total Collections:** {len(schemas)}")
        md_content.append("")
        
        # Table of Contents
        md_content.append("## Table of Contents")
        md_content.append("")
        for collection_name in sorted(schemas.keys()):
            md_content.append(f"- [{collection_name}](#{collection_name.lower().replace('_', '-')})")
        md_content.append("")
        
        # Collection schemas
        for collection_name, schema in sorted(schemas.items()):
            md_content.append(f"## {collection_name}")
            md_content.append("")
            
            if "error" in schema:
                md_content.append(f"**Error:** {schema['error']}")
                md_content.append("")
                continue
            
            # Collection info
            md_content.append(f"**Document Count:** {schema['document_count']:,}")
            md_content.append(f"**Sample Size:** {schema['sample_size']}")
            md_content.append("")
            
            # Fields
            if schema['fields']:
                md_content.append("### Fields")
                md_content.append("")
                md_content.append("| Field | Type | Example |")
                md_content.append("|-------|------|---------|")
                
                for field_name, field_info in schema['fields'].items():
                    field_type = field_info['type']
                    example = field_info.get('example', '')
                    if isinstance(example, (dict, list)):
                        example = json.dumps(example)[:50] + "..." if len(json.dumps(example)) > 50 else json.dumps(example)
                    elif isinstance(example, str) and len(example) > 50:
                        example = example[:47] + "..."
                    
                    md_content.append(f"| `{field_name}` | {field_type} | {example} |")
                
                md_content.append("")
            
            # First document (sanitized)
            if schema.get('first_document') is not None:
                md_content.append("### First Document (sanitized)")
                md_content.append("")
                pretty = json.dumps(schema['first_document'], indent=2, ensure_ascii=False)
                md_content.append("```json")
                md_content.append(pretty)
                md_content.append("```")
                md_content.append("")
            
            # Indexes
            if schema['indexes']:
                md_content.append("### Indexes")
                md_content.append("")
                
                for idx in schema['indexes']:
                    index_name = idx.get('name', 'unnamed')
                    index_keys = idx.get('key', {})
                    index_unique = idx.get('unique', False)
                    
                    md_content.append(f"**{index_name}**")
                    if index_unique:
                        md_content.append("- Type: Unique")
                    
                    if index_keys:
                        md_content.append("- Keys:")
                        for key, direction in index_keys.items():
                            direction_str = "ascending" if direction == 1 else "descending" if direction == -1 else str(direction)
                            md_content.append(f"  - `{key}`: {direction_str}")
                    
                    md_content.append("")
            
            md_content.append("---")
            md_content.append("")
        
        # Footer
        md_content.append("## Generation Info")
        md_content.append("")
        md_content.append(f"- **MongoDB URI:** `{self.settings.mongodb_uri}`")
        md_content.append(f"- **Sample Size per Collection:** {self.settings.sample_size}")
        md_content.append(f"- **Generated by:** MongoDB Schema Extractor")
        md_content.append("")
        
        return "\n".join(md_content)
    
    async def run(self) -> None:
        """Run the complete schema extraction process."""
        try:
            await self.connect()
            schemas = await self.extract_all_schemas()
            markdown_content = self.generate_markdown(schemas)
            
            # Write to file
            output_path = os.path.join(os.getcwd(), self.settings.output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            logger.info(f"Schema documentation generated: {output_path}")
            logger.info(f"Total collections processed: {len(schemas)}")
            
        except Exception as e:
            logger.error(f"Schema extraction failed: {e}")
            raise
        finally:
            await self.disconnect()


async def main():
    """Main entry point."""
    settings = SchemaExtractorSettings()
    extractor = MongoSchemaExtractor(settings)
    await extractor.run()


if __name__ == "__main__":
    asyncio.run(main())