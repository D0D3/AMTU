# Import nécessaire pour genre_manager.py
import json
import logging
from dataclasses import dataclass
from typing import Optional
from models import TrackMetadata

logger = logging.getLogger(__name__)

class GenreManager:
    """Gestionnaire de genres personnalisés."""

    def __init__(self):
        # Mapping de base des genres EDM
        self.genre_mapping = {
            # Drum & Bass et dérivés
            'drum and bass': 'Drum & Bass',
            'dnb': 'Drum & Bass',
            'liquid funk': 'Drum & Bass',
            'neurofunk': 'Drum & Bass',
            'jump up': 'Drum & Bass',
            'jungle': 'Drum & Bass',

            # Dubstep et dérivés
            'dubstep': 'Dubstep',
            'brostep': 'Dubstep',
            'riddim': 'Dubstep',
            'melodic dubstep': 'Melodic Dubstep',

            # House et dérivés
            'house': 'House',
            'deep house': 'Deep House',
            'tech house': 'Tech House',
            'progressive house': 'Progressive House',
            'electro house': 'Electro House',
            'future house': 'Future House',
            'bass house': 'Bass House',

            # Autres genres EDM
            'drumstep': 'Drumstep',
            'breakbeat': 'Breakbeat',
            'trap': 'Trap',
            'future bass': 'Future Bass',
            'hardstyle': 'Hardstyle',
            'trance': 'Trance',
            'psytrance': 'Psytrance',
            'ambient': 'Ambient',
            'synthwave': 'Synthwave'
        }

        # Règles de détection basées sur les labels
        self.label_genre_rules = {
            'hospital records': 'Drum & Bass',
            'ram records': 'Drum & Bass',
            'monstercat': 'EDM',
            'spinnin': 'House',
            'revealed': 'Electro House',
            'mau5trap': 'Progressive House',
            'never say die': 'Dubstep'
        }

        # Règles de détection basées sur les artistes
        self.artist_genre_rules = {
            'noisia': 'Drum & Bass',
            'pendulum': 'Drum & Bass',
            'skrillex': 'Dubstep',
            'deadmau5': 'Progressive House',
            'martin garrix': 'Electro House',
            'andy c': 'Drum & Bass',
            'sub focus': 'Drum & Bass',
            'dj zinc': 'Drum & Bass'
        }

    def load_custom_mappings(self, file_path):
        """Charge des mappings personnalisés depuis un fichier JSON."""
        try:
            with open(file_path, 'r') as f:
                custom_mappings = json.load(f)
                self.genre_mapping.update(custom_mappings.get('genres', {}))
                self.label_genre_rules.update(custom_mappings.get('labels', {}))
                self.artist_genre_rules.update(custom_mappings.get('artists', {}))
            return True
        except Exception as e:
            logger.error(f"Erreur lors du chargement des mappings personnalisés: {e}")
            return False

    def detect_genre(self, metadata: TrackMetadata) -> str:
        """Détecte le genre en fonction des métadonnées disponibles."""
        detected_genre = None

        # 1. Vérification basée sur le label
        if metadata.label:
            label_lower = metadata.label.lower()
            for label_key, genre in self.label_genre_rules.items():
                if label_key in label_lower:
                    detected_genre = genre
                    break

        # 2. Vérification basée sur l'artiste
        if not detected_genre and metadata.artist:
            artist_lower = metadata.artist.lower()
            for artist_key, genre in self.artist_genre_rules.items():
                if artist_key in artist_lower:
                    detected_genre = genre
                    break

        # 3. Vérification basée sur le genre existant
        if not detected_genre and metadata.genre:
            genre_lower = metadata.genre.lower()
            detected_genre = self.genre_mapping.get(genre_lower, metadata.genre)

        return detected_genre or 'Electronic'  # Genre par défaut si rien n'est détecté

# Format exemple pour le fichier de configuration JSON des genres
example_genre_config = {
    "genres": {
        "future garage": "Future Garage",
        "neurohop": "Neurofunk",
        "crossbreed": "Drum & Bass"
    },
    "labels": {
        "vision recordings": "Drum & Bass",
        "critical music": "Drum & Bass",
        "shogun audio": "Drum & Bass"
    },
    "artists": {
        "camo & krooked": "Drum & Bass",
        "metrik": "Drum & Bass",
        "dimension": "Drum & Bass"
    }
}
