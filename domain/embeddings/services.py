"""
Domain service for building embedding text strings from product documents.
Following the specification in detail_prompt_instruction_for_creatingEmdeddings.txt
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Optional

# Boilerplate phrases to strip from descriptions
BOILERPLATE_PATTERNS = [
    r"proudly made in [a-z\s]+",
    r"great for all year( round)? use",
    r"best in class",
    r"top quality",
    r"premium quality",
]

def _to_snake(s: str) -> str:
    """Normalize a string to snake_case: lowercase and non-alphanumerics to underscores."""
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s

def _pd_to_map(product_details: Optional[Iterable[Dict[str, Any]]]) -> Dict[str, str]:
    """Flatten product_details (list of 1-key dicts) into a lowercase-keyed dict."""
    out: Dict[str, str] = {}
    for kv in (product_details or []):
        for k, v in kv.items():
            out[k.strip().lower()] = str(v).strip()
    return out

def _clean_desc(text: str, max_words: int = 8) -> Optional[str]:
    """Clean description: remove boilerplate and keep first N informative words."""
    if not text:
        return None
    t = text
    for pat in BOILERPLATE_PATTERNS:
        t = re.sub(pat, "", t, flags=re.I)
    words = re.findall(r"[A-Za-z0-9%+\-']+", t.lower())
    return " ".join(words[:max_words]) if words else None

def _int_from_str(s: str) -> Optional[int]:
    """Extract first integer from string."""
    if s is None:
        return None
    m = re.search(r"(\d+)", str(s))
    return int(m.group(1)) if m else None

def _float_from_str(s: str) -> Optional[float]:
    """Extract first float from string."""
    if s is None:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", str(s))
    return float(m.group(1)) if m else None

def _parse_price(value: Any) -> Optional[int]:
    """Parse price to integer (strip commas/currency)."""
    if value is None:
        return None
    s = str(value)
    m = re.search(r"(\d[\d,]*)", s)
    if not m:
        return None
    return int(m.group(1).replace(",", ""))

def _extract_electronics_attrs(title: str, pd: Dict[str, str]) -> Dict[str, Any]:
    """Extract RAM/Storage/5G/screen size from title or details for electronics."""
    lower_title = title.lower()

    ram_gb = None
    storage_gb = None
    # Common patterns: "8GB RAM", "(8GB,128GB)", "8 gb/128 gb"
    m = re.search(r"(\d+)\s*gb[^a-z0-9]+(\d+)\s*gb", lower_title)
    if m:
        ram_gb, storage_gb = int(m.group(1)), int(m.group(2))
    else:
        m1 = re.search(r"(\d+)\s*gb\s*ram", lower_title)
        m2 = re.search(r"(\d+)\s*gb\s*(rom|storage)", lower_title)
        if m1:
            ram_gb = int(m1.group(1))
        if m2:
            storage_gb = int(m2.group(1))

    # Try product_details fallbacks
    if ram_gb is None:
        ram_gb = _int_from_str(pd.get("ram") or pd.get("memory"))
    if storage_gb is None:
        storage_gb = _int_from_str(pd.get("storage") or pd.get("rom"))

    supports_5g = None
    if "5g" in lower_title or "supports 5g" in lower_title:
        supports_5g = True
    elif any("5g" in str(v).lower() for v in pd.values()):
        supports_5g = True
    elif pd.get("5g support") and str(pd.get("5g support")).lower() in ("yes", "true", "1"):
        supports_5g = True

    screen_size_in = _float_from_str(pd.get("screen size") or pd.get("display size") or "")
    if screen_size_in is None:
        mm = re.search(r"(\d+(?:\.\d+)?)\s*(?:inches|inch|\"|in)\b", lower_title)
        if mm:
            screen_size_in = float(mm.group(1))

    out: Dict[str, Any] = {}
    if ram_gb is not None:
        out["ram_gb"] = ram_gb
    if storage_gb is not None:
        out["storage_gb"] = storage_gb
    if supports_5g is True:
        out["supports_5g"] = True
    if screen_size_in is not None:
        out["screen_size_in"] = screen_size_in
    return out

def build_embedding_text(doc: Dict[str, Any]) -> str:
    """Build a deterministic, compact embedding text string for a product document.

    Args:
        doc: Product document (fields may vary by category).

    Returns:
        Deterministic single-line string with key:value tokens in fixed order.
        
    Example:
        Solid Men Blue Track Pants | brand:york | category:clothing_and_accessories>bottomwear | 
        color:blue | material:cotton blend | pattern:solid | price_inr:499 | 
        desc:skin-friendly itch-free waistband breathable cotton
    """
    title = (doc.get("title") or "").strip()
    brand = (doc.get("brand") or "").strip().lower() or None

    # categories
    category_main = _to_snake(doc.get("category") or "general")
    category_leaf = _to_snake(doc.get("sub_category") or "") or None

    # flatten product_details and map keys
    pd = _pd_to_map(doc.get("product_details"))
    color = (pd.get("color") or "").strip().lower() or None
    material = (pd.get("fabric") or pd.get("material") or "").strip().lower() or None
    pattern = (pd.get("pattern") or "").strip().lower() or None
    size = (pd.get("size") or "").strip().lower() or None

    # price
    price = (
        doc.get("selling_price_numeric")
        or doc.get("price_inr")
        or doc.get("price")
        or doc.get("actual_price_numeric")
    )
    price = _parse_price(price)

    # short descriptor
    short_desc = _clean_desc(doc.get("description") or "")

    # Choose attribute order: electronics vs general
    is_electronics = "electronics" in category_main
    electronics_attrs = _extract_electronics_attrs(title, pd) if is_electronics else {}

    parts: List[str] = []
    if title:
        parts.append(title)
    if brand:
        parts.append(f"brand:{brand}")

    if category_main and category_leaf:
        parts.append(f"category:{category_main}>{category_leaf}")
    elif category_main:
        parts.append(f"category:{category_main}")

    if is_electronics:
        # Example order from spec: ram_gb, storage_gb, supports_5g, screen_size_in
        if "ram_gb" in electronics_attrs:
            parts.append(f"ram_gb:{electronics_attrs['ram_gb']}")
        if "storage_gb" in electronics_attrs:
            parts.append(f"storage_gb:{electronics_attrs['storage_gb']}")
        if "supports_5g" in electronics_attrs and electronics_attrs["supports_5g"]:
            parts.append("supports_5g:true")
        if "screen_size_in" in electronics_attrs:
            parts.append(f"screen_size_in:{electronics_attrs['screen_size_in']}")
        # Optional color if present
        if color:
            parts.append(f"color:{color}")
    else:
        # Fashion/home-decor attrs
        if color:
            parts.append(f"color:{color}")
        if material:
            parts.append(f"material:{material}")
        if pattern:
            parts.append(f"pattern:{pattern}")
        if size:
            parts.append(f"size:{size}")

    if price is not None:
        parts.append(f"price_inr:{price}")
    if short_desc:
        parts.append(f"desc:{short_desc}")

    return " | ".join(parts)
