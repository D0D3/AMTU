# src/config.py
from pathlib import Path

# Chemin racine du projet (2 niveaux au-dessus car nous sommes dans src/config.py)
ROOT_DIR = Path(__file__).parent.parent

# Chemins des dossiers
CONFIG_DIR = ROOT_DIR / 'config'
LOGS_DIR = ROOT_DIR / 'logs'
I18N_DIR = ROOT_DIR / 'i18n'
SRC_DIR = ROOT_DIR / 'src'
DOCS_DIR = ROOT_DIR / 'docs'

# Chemins des fichiers de configuration
GENRE_MAPPINGS_FILE = CONFIG_DIR / 'genre_mappings.json'
API_CONFIG_FILE = CONFIG_DIR / 'set_api_config.json'
API_KEYS_FILE = CONFIG_DIR / 'api_keys.json'