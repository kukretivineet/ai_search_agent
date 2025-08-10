#!/usr/bin/env python3
"""
OpenAI Embedding Text Generation for MongoDB Atlas Vector Search

This module generates consistent, structured text for OpenAI embeddings following
the exact specifications in detail_prompt_instruction_for_creatingEmdeddings.txt

Key Features:
- Fixed order embedding text generation: title | brand | category | attributes | price | desc
- Category-agnostic with support for fashion, electronics, home-decor, etc.
- Deterministic output for consistent re-embedding logic
- Boilerplate removal and text normalization
"""

import re
from typing import Dict, Any, Optional, List


# Boilerplate patterns to remove from descriptions
BOILERPLATE_PATTERNS = [
    r"proudly made in [a-z\s]+?(?=\s+[a-z]|$)",  # Less greedy
    r"great for all year( round)?\s+use",
    r"best in class\s*",
    r"perfect for\s*",
    r"ideal choice\s*",
    r"must have(\s+item)?\s*",
    r"specially designed(\s+for)?\s*",
    r"premium quality\s*",
    r"high quality\s*",
    r"excellent quality\s*"
]


def _to_snake(s: str) -> str:
    """Convert string to snake_case format for category normalization."""
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def _pd_to_map(product_details: Optional[List[Dict[str, str]]]) -> Dict[str, str]:
    """Flatten product_details array to a single dictionary with lowercased keys."""
    out = {}
    if not product_details:
        return out
    
    for kv in product_details:
        if isinstance(kv, dict):
            for k, v in kv.items():
                if k and v:  # Skip None or empty keys/values
                    out[k.strip().lower()] = str(v).strip()
    return out


def _clean_desc(text: Optional[str], max_words: int = 12) -> Optional[str]:
    """Clean description text by removing boilerplate and limiting words."""
    if not text or not text.strip():
        return None
        
    t = text
    
    # Remove boilerplate patterns
    for pat in BOILERPLATE_PATTERNS:
        t = re.sub(pat, "", t, flags=re.IGNORECASE)
    
    # Extract meaningful words (alphanumeric, %, +, -, ')
    # Also handle special characters like % in "100%" properly
    words = re.findall(r"[A-Za-z0-9%+\-']+", t.lower())
    
    # Return first max_words or None if empty
    return " ".join(words[:max_words]) if words else None


def _normalize_material(pd: Dict[str, str]) -> Optional[str]:
    """Extract and normalize material from product details."""
    # Check multiple possible keys for material/fabric
    for key in ["fabric", "material", "composition", "material type"]:
        if key in pd:
            material = pd[key].lower().strip()
            if material and material != "n/a" and material != "not specified":
                return material
    return None


def _normalize_electronics_attrs(pd: Dict[str, str], doc: Dict[str, Any]) -> Dict[str, Optional[str]]:
    """Extract electronics-specific attributes like RAM, storage, 5G support."""
    attrs = {}
    
    # RAM - look in product_details and title/description
    ram_gb = None
    for key in ["ram", "memory", "ram size"]:
        if key in pd:
            ram_match = re.search(r"(\d+)\s*gb", pd[key].lower())
            if ram_match:
                ram_gb = ram_match.group(1)
                break
    
    # Also check title for RAM info
    if not ram_gb:
        title = doc.get("title", "").lower()
        ram_match = re.search(r"(\d+)\s*gb.*ram|ram.*(\d+)\s*gb", title)
        if ram_match:
            ram_gb = ram_match.group(1) or ram_match.group(2)
    
    attrs["ram_gb"] = ram_gb
    
    # Storage
    storage_gb = None
    for key in ["storage", "internal storage", "memory"]:
        if key in pd:
            storage_match = re.search(r"(\d+)\s*gb", pd[key].lower())
            if storage_match and key != "ram":  # Don't confuse RAM with storage
                storage_gb = storage_match.group(1)
                break
    
    # Check title for storage
    if not storage_gb:
        title = doc.get("title", "").lower()
        storage_match = re.search(r"(\d+)\s*gb(?!.*ram)", title)  # GB not followed by RAM
        if storage_match:
            storage_gb = storage_match.group(1)
    
    attrs["storage_gb"] = storage_gb
    
    # 5G support
    supports_5g = None
    title_desc = f"{doc.get('title', '')} {doc.get('description', '')}".lower()
    if "5g" in title_desc:
        supports_5g = "true"
    
    attrs["supports_5g"] = supports_5g
    
    # Screen size (for phones/tablets)
    screen_size = None
    for key in ["screen size", "display", "screen"]:
        if key in pd:
            screen_match = re.search(r"(\d+\.?\d*)\s*inch", pd[key].lower())
            if screen_match:
                screen_size = screen_match.group(1)
                break
    
    attrs["screen_size_in"] = screen_size
    
    return attrs


def _is_electronics_category(category: str, sub_category: str = "") -> bool:
    """Check if this is an electronics product."""
    electronics_terms = [
        "electronics", "phone", "mobile", "smartphone", "tablet", "laptop", 
        "computer", "gadget", "device", "tech", "gaming"
    ]
    
    combined = f"{category} {sub_category}".lower()
    return any(term in combined for term in electronics_terms)


def _extract_dimensions(pd: Dict[str, str]) -> Optional[str]:
    """Extract dimensions for home decor items."""
    for key in ["dimensions", "size", "dimension"]:
        if key in pd:
            dim_text = pd[key]
            # Look for LxWxH pattern
            dim_match = re.search(r"(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)", dim_text)
            if dim_match:
                l, w, h = dim_match.groups()
                return f"{l}x{w}x{h}"
    return None


def build_embedding_text(doc: Dict[str, Any]) -> str:
    """
    Build structured embedding text for OpenAI text-embedding-3-small.
    
    Format: {title} | brand:{brand} | category:{main}>{leaf} | {attrs} | price_inr:{price} | desc:{desc}
    
    Args:
        doc: Product document with fields like title, brand, category, sub_category,
             product_details, selling_price_numeric, description
             
    Returns:
        Formatted embedding text string following the exact specification
    """
    # Extract basic fields
    title = (doc.get("title") or "").strip()
    brand = (doc.get("brand") or "").strip().lower() or None
    
    # Category normalization
    category_main = _to_snake(doc.get("category") or "general")
    category_leaf = _to_snake(doc.get("sub_category") or "") or None
    
    # Flatten product_details
    pd = _pd_to_map(doc.get("product_details"))
    
    # Price handling
    price = doc.get("selling_price_numeric") or doc.get("price_inr")
    if price is not None:
        try:
            price = int(float(str(price).replace(",", "")))
        except (ValueError, TypeError):
            price = None
    
    # Short descriptor from description
    short_desc = _clean_desc(doc.get("description") or "")
    
    # Determine category type for attribute extraction
    is_electronics = _is_electronics_category(doc.get("category", ""), doc.get("sub_category", ""))
    
    # Start building the parts list
    parts = []
    
    # 1. Title (preserve original case)
    if title:
        parts.append(title)
    
    # 2. Brand
    if brand:
        parts.append(f"brand:{brand}")
    
    # 3. Category
    if category_main and category_leaf:
        parts.append(f"category:{category_main}>{category_leaf}")
    elif category_main:
        parts.append(f"category:{category_main}")
    
    # 4. Category-specific attributes (maintaining fixed order)
    if is_electronics:
        # Electronics: ram_gb, storage_gb, supports_5g, screen_size_in
        electronics_attrs = _normalize_electronics_attrs(pd, doc)
        
        if electronics_attrs.get("ram_gb"):
            parts.append(f"ram_gb:{electronics_attrs['ram_gb']}")
        if electronics_attrs.get("storage_gb"):
            parts.append(f"storage_gb:{electronics_attrs['storage_gb']}")
        if electronics_attrs.get("supports_5g"):
            parts.append(f"supports_5g:{electronics_attrs['supports_5g']}")
        if electronics_attrs.get("screen_size_in"):
            parts.append(f"screen_size_in:{electronics_attrs['screen_size_in']}")
        
        # Color for electronics (if applicable)
        color = (pd.get("color") or "").lower() or None
        if color:
            parts.append(f"color:{color}")
            
    else:
        # Fashion/Home-decor: color, material, pattern, size
        color = (pd.get("color") or "").lower() or None
        material = _normalize_material(pd)
        pattern = (pd.get("pattern") or "").lower() or None
        size = (pd.get("size") or "").lower() or None
        
        if color:
            parts.append(f"color:{color}")
        if material:
            parts.append(f"material:{material}")
        if pattern:
            parts.append(f"pattern:{pattern}")
        if size:
            parts.append(f"size:{size}")
        
        # For home decor, add dimensions if available
        if "home" in category_main or "decor" in category_main:
            dimensions = _extract_dimensions(pd)
            if dimensions:
                parts.append(f"dimensions_cm:{dimensions}")
    
    # 5. Price
    if price is not None:
        parts.append(f"price_inr:{price}")
    
    # 6. Description
    if short_desc:
        parts.append(f"desc:{short_desc}")
    
    # Join all parts
    return " | ".join(parts)


def build_embedding_text_batch(docs: List[Dict[str, Any]]) -> List[str]:
    """
    Build embedding text for multiple documents efficiently.
    
    Args:
        docs: List of product documents
        
    Returns:
        List of formatted embedding text strings in the same order
    """
    return [build_embedding_text(doc) for doc in docs]


def should_regenerate_embedding(doc: Dict[str, Any], current_embedding_text: str) -> bool:
    """
    Check if the embedding should be regenerated by comparing the current
    stored embedding_text with the newly generated one.
    
    Args:
        doc: Product document
        current_embedding_text: Currently stored openai_embedding_text
        
    Returns:
        True if regeneration is needed, False otherwise
    """
    new_embedding_text = build_embedding_text(doc)
    return new_embedding_text != current_embedding_text


if __name__ == "__main__":
    # Example usage
    sample_doc = {
        "_id": "893e6980-f2a0-531f-b056-34dd63fe912c",
        "title": "Solid Men Blue Track Pants",
        "brand": "York",
        "category": "Clothing and Accessories",
        "sub_category": "Bottomwear",
        "description": "Yorker trackpants made from 100% rich combed cotton ... Proudly made in India",
        "product_details": [
            {"Style Code": "1005BLUE"},
            {"Closure": "Drawstring, Elastic"},
            {"Pockets": "Side Pockets"},
            {"Fabric": "Cotton Blend"},
            {"Pattern": "Solid"},
            {"Color": "Blue"}
        ],
        "selling_price_numeric": 499,
        "actual_price_numeric": 1499,
        "out_of_stock": False
    }
    
    result = build_embedding_text(sample_doc)
    print("Sample embedding text:")
    print(result)
