#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

def setup_environment():
    """Configure l'environnement de l'application."""
    # Définir les chemins principaux
    ROOT_DIR = Path(__file__).parent
    SRC_DIR = ROOT_DIR / "src"
    DOCS_DIR = ROOT_DIR / "docs"
    
    # Ajouter le dossier src au PYTHONPATH
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))

    # S'assurer que le dossier docs existe
    DOCS_DIR.mkdir(exist_ok=True)
    
    # Import après avoir configuré le PYTHONPATH
    from config import CONFIG_DIR, LOGS_DIR, I18N_DIR, DOCS_DIR, GENRE_MAPPINGS_FILE, API_CONFIG_FILE
    
    # Créer les dossiers nécessaires
    for directory in [CONFIG_DIR, LOGS_DIR, I18N_DIR, DOCS_DIR]:
        directory.mkdir(exist_ok=True)
    
    # Vérifier que les fichiers essentiels existent
    if not API_CONFIG_FILE.exists():
        default_config = {
            "spotify_client_id": "",
            "spotify_client_secret": "",
            "discogs_token": "",
            "services": {
                "musicbrainz": True,
                "spotify": False,
                "discogs": False
            }
        }
        API_CONFIG_FILE.write_text(json.dumps(default_config, indent=2))

    if not GENRE_MAPPINGS_FILE.exists():
        default_mappings = {
            "genres": {},
            "labels": {},
            "artists": {}
        }
        GENRE_MAPPINGS_FILE.write_text(json.dumps(default_mappings, indent=2))

def run_app():
    """Lance l'application AMTU."""
    try:
        from AMTU import MetadataManagerGUI
        app = MetadataManagerGUI()
        app.root.mainloop()
    except Exception as e:
        print(f"Erreur au démarrage de l'application: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    setup_environment()
    run_app()