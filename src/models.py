# models.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class TrackMetadata:
    """Structure pour stocker les métadonnées d'une piste."""
    title: str
    artist: str
    album: str
    label: Optional[str] = None
    catalog_number: Optional[str] = None
    artist_sort: Optional[str] = None
    is_single: bool = False
    confidence: float = 0.0
    source: str = ""
    year: Optional[int] = None
    genre: Optional[str] = None
