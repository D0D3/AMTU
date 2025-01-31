# locales/locale_manager.py
import json
import os
from typing import Dict, Optional, Any

class LocaleManager:
    def __init__(self, locales_dir: str = "locales"):
        self.locales_dir = locales_dir
        self.current_locale = "fr"  # Langue par défaut
        self.translations: Dict[str, Dict[str, Any]] = {}

        # Créer le dossier des locales s'il n'existe pas
        os.makedirs(self.locales_dir, exist_ok=True)

        self.available_locales = self._load_available_locales()
        self._load_translations()

    def _load_available_locales(self) -> Dict[str, str]:
        """Charge la liste des langues disponibles."""
        default_locales = {
            "fr": "Français",
            "en": "English",
            "es": "Español",
            "it": "Italiano",
            "pt": "Português"
        }

        config_file = os.path.join(self.locales_dir, "available_locales.json")

        try:
            if os.path.exists(config_file):
                with open(config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(config_file, "w", encoding="utf-8") as f:
                    json.dump(default_locales, f, ensure_ascii=False, indent=2)
                return default_locales
        except Exception as e:
            return default_locales

    def _load_translations(self):
        for locale_code in self.available_locales.keys():
            self._load_locale(locale_code)

    def _load_locale(self, locale_code: str) -> None:
        """Charge les traductions pour une langue spécifique."""
        file_path = os.path.join(self.locales_dir, f"{locale_code}.json")

        if not os.path.exists(file_path):
            # Créer le fichier avec des traductions par défaut
            default_translations = self._create_default_translations(locale_code)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(default_translations, f, ensure_ascii=False, indent=2)
            self.translations[locale_code] = default_translations
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations[locale_code] = json.load(f)
        except Exception as e:
            self.translations[locale_code] = self._create_default_translations(locale_code)

    def _create_default_translations(self, locale_code: str) -> Dict[str, Any]:
        """Crée les traductions par défaut."""
        # Retourne les traductions françaises par défaut pour l'exemple
        if locale_code == "fr":
            return {
                "interface": {
                    "app_title": "AMTU - Apple Music Tag Updater MP3",
                    "menu": {"language": "Langue"}
                },
                # ... autres traductions par défaut ...
            }
        # Pour les autres langues, retourne une copie des traductions anglaises
        return {
            "interface": {
                "app_title": "AMTU - Apple Music Tag Updater MP3",
                "menu": {"language": "Language"}
            },
            # ... autres traductions par défaut en anglais ...
        }

    def get_text(self, key: str, default: Optional[str] = None, *args) -> str:
        """
        Récupère une traduction avec support des clés hiérarchiques et du formatage.

        Args:
            key: Clé de traduction (ex: "messages.error.api_config")
            default: Texte par défaut si la clé n'existe pas
            *args: Arguments de formatage pour les placeholders {0}, {1}, etc.
        """
        try:
            # Séparation de la clé en parties
            parts = key.split('.')
            current = self.translations[self.current_locale]

            # Navigation dans la structure imbriquée
            for part in parts:
                current = current[part]

            # Si on a une chaîne, on la formate avec les arguments
            if isinstance(current, str):
                try:
                    if args:
                        return current.format(*args)
                    return current
                except Exception as e:
                    print(f"Erreur de formatage pour la clé {key}: {e}")
                    return current

            # Si ce n'est pas une chaîne, on retourne la clé ou la valeur par défaut
            return default or key

        except (KeyError, AttributeError, TypeError) as e:
            return default or key

    def set_locale(self, locale_code: str) -> bool:
        """Change la langue courante."""
        if locale_code in self.available_locales:
            self.current_locale = locale_code
            return True
        return False

    def get_available_locales(self) -> Dict[str, str]:
        """Retourne la liste des langues disponibles."""
        try:
            with open(os.path.join(self.locales_dir, "available_locales.json"), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"fr": "Français", "it": "Italiano"}
