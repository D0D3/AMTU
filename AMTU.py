#!/usr/bin/env python3
# -*- coding: utf-8 -*-

{
  "app": {
    "name": "Apple Music Tag Updater (AMTU)",
    "description": "Un outil pour mettre à jour automatiquement les tags des fichiers MP3."
  }
}

# Imports standards
from typing import Dict, List, Optional, Tuple, Any
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinterdnd2 import *  # Pour le drag & drop
from tkinterdnd2 import TkinterDnD, DND_FILES
from genre_manager import GenreManager
from models import TrackMetadata
from locales.locale_manager import LocaleManager
import json
from pathlib import Path
import logging
from dataclasses import dataclass
import requests
import time
import csv
import threading
from queue import Queue, Empty
import os

# Imports tiers
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import discogs_client
import musicbrainzngs
import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TCON, TXXX, TGID, TDRC, TPE2, TPE1, TALB, TIT2, TMCL

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConfigManager:
    """Gère la configuration et la validation des APIs."""
    CONFIG_FILE = "set_api_config.json"

    def __init__(self, locale_manager):
        self.locale_manager = locale_manager
        self.config: Dict[str, Any] = self.load_config()

    def load_config(self) -> Dict[str, Any]:
            default_config = {
                'spotify_client_id': '',
                'spotify_client_secret': '',
                'discogs_token': '',
                'services': {
                    'musicbrainz': True,     # MusicBrainz activé par défaut
                    'spotify': False,         # Spotify désactivé par défaut
                    'discogs': False          # Discogs désactivé par défaut
                }
            }
            try:
                if Path(self.CONFIG_FILE).exists():
                    with open(self.CONFIG_FILE, 'r') as f:
                        loaded_config = json.load(f)
                        # S'assurer que la section services existe avec les valeurs par défaut
                        if 'services' not in loaded_config:
                            loaded_config['services'] = default_config['services']
                        return loaded_config
            except Exception as e:
                logger.error(self.locale_manager.get_text("messages.error.config_loading", None, str(e)))

            return default_config

    def load_api_keys(self):
        try:
            with open('api_keys.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self, config: Dict[str, Any]) -> None:
        try:
            # S'assurer que la section services existe
            if 'services' not in config:
                config['services'] = {
                    'musicbrainz': True,
                    'spotify': False,
                    'discogs': True
                }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            logger.error(self.locale_manager.get_text(
                "messages.error.config_save",
                None,
                str(e)
            ))

    def save_api_keys(self, config: Dict[str, Any]) -> None:
        try:
            with open('api_keys.json', 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error(self.locale_manager.get_text(
                "messages.error.api_keys_save",
                None,
                str(e)
            ))

    def is_service_enabled(self, service_name: str) -> bool:
        """Vérifie si un service est activé."""
        return self.config.get('services', {}).get(service_name, False)

    def set_service_state(self, service_name: str, enabled: bool) -> None:
        """Active ou désactive un service."""
        if 'services' not in self.config:
            self.config['services'] = {}
        self.config['services'][service_name] = enabled
        self.save_config(self.config)

    def export_config(self, filename: str) -> None:
        try:
            config = {
                'spotify': {
                    'client_id': self.config.get('spotify_client_id', ''),
                    'client_secret': self.config.get('spotify_client_secret', '')
                },
                'discogs': {
                    'consumer_key': self.config.get('discogs_consumer_key', ''),
                    'consumer_secret': self.config.get('discogs_consumer_secret', ''),
                    'token': self.config.get('discogs_token', '')
                }
            }
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            logger.error(self.locale_manager.get_text(
                "messages.error.config_export",
                None,
                str(e)
            ))

class APIManager:
    """Gestionnaire centralisé des APIs musicales."""

    def __init__(self, config: Dict[str, str], locale_manager):
        self.config = config
        self.locale_manager = locale_manager
        self.spotify = None
        self.discogs = None
        self.musicbrainz = None
        self._init_apis()

    def _init_apis(self):
        """Initialise toutes les connexions APIs."""
        self._init_spotify()
        self._init_discogs()
        self._init_musicbrainz()

    def _init_spotify(self):
        try:
            auth_manager = SpotifyClientCredentials(
                client_id=self.config['spotify_client_id'],
                client_secret=self.config['spotify_client_secret']
            )
            self.spotify = spotipy.Spotify(auth_manager=auth_manager)
        except Exception as e:
            logger.error(self.locale_manager.get_text(
                "api.initialization.error.spotify",
                None,
                str(e)
            ))
            raise

    def _init_discogs(self):
        try:
            api_keys = self.config_manager.load_api_keys() if hasattr(self, 'config_manager') else {}
            discogs_config = api_keys.get('discogs', {})

            self.discogs = discogs_client.Client(
                'AMTU/1.0',
                consumer_key=self.config.get('discogs_consumer_key', discogs_config.get('consumer_key', '')),
                consumer_secret=self.config.get('discogs_consumer_secret', discogs_config.get('consumer_secret', '')),
                token=self.config.get('discogs_token', discogs_config.get('token', ''))
            )
        except Exception as e:
            logger.error(self.locale_manager.get_text(
                "api.initialization.error.discogs",
                None,
                str(e)
            ))
            raise

    def _init_musicbrainz(self):
        try:
            logging.getLogger('musicbrainzngs').setLevel(logging.WARNING)
            musicbrainzngs.set_useragent(
                "MetadataManager",
                "1.0",
                "https://github.com/yourusername/metadata-manager"
            )
            self.musicbrainz = musicbrainzngs
            logging.info(self.locale_manager.get_text("api.initialization.success.musicbrainz"))
        except Exception as e:
            logging.error(self.locale_manager.get_text(
                "api.initialization.error.musicbrainz",
                None,
                str(e)
            ))
            raise

    def search_track(self, title: str, artist: str, retries: int = 3) -> List[TrackMetadata]:
        """Recherche les métadonnées avec plusieurs tentatives en cas d'échec."""
        logger.info(self.locale_manager.get_text(
            "api.initialization.search.start",
            None,
            title,
            artist
        ))
        for attempt in range(retries):
            try:
                results = self._execute_search(title, artist)
                if results:
                    return results
            except Exception as e:
                logger.warning(self.locale_manager.get_text(
                    "api.initialization.search.attempt_failed",
                    None,
                    attempt + 1,
                    retries,
                    str(e)
                ))
                if attempt == retries - 1:
                    logger.error(self.locale_manager.get_text(
                        "api.initialization.search.all_attempts_failed",
                        None,
                        title,
                        artist
                    ))
                    raise
                time.sleep(1)
        return []

    def _execute_search(self, title: str, artist: str) -> List[TrackMetadata]:
        """Exécute la recherche sur les APIs activées."""
        best_result = None
        enabled_services = self.config.get('services', {})

        for service_name, search_func, display_name in [
            ('musicbrainz', self._search_musicbrainz, "MusicBrainz"),
            ('spotify', self._search_spotify, "Spotify"),
            ('discogs', self._search_discogs, "Discogs")
        ]:
            if not enabled_services.get(service_name, False):
                continue

            logger.info(f"Recherche sur {display_name}...")
            try:
                results = search_func(title, artist)

                if not results:
                    continue

                logger.info(f"Résultats trouvés sur {display_name}: {len(results)}")

                # Trouve le meilleur résultat pour ce service
                current_best = max(results, key=lambda x: x.confidence)

                if current_best.label:  # On vérifie seulement la présence du label
                    # Si c'est notre premier résultat valide ou s'il est meilleur que le précédent
                    if not best_result or current_best.confidence > best_result.confidence:
                        best_result = current_best
                        logger.info(f"Nouveau meilleur résultat trouvé sur {display_name} "
                                  f"(confiance: {current_best.confidence}%)")

            except Exception as e:
                logger.warning(f"Erreur lors de la recherche sur {display_name}: {e}")
                continue

        if best_result:
            logger.info(f"Meilleur résultat final : {best_result.source} "
                       f"(confiance: {best_result.confidence}%)")
            return [best_result]

        logger.info("Aucun résultat valide trouvé")
        return []

    def _search_spotify(self, title: str, artist: str) -> List[TrackMetadata]:
        results = []
        query = f"track:\"{title}\" artist:\"{artist}\""

        try:
            search_results = self.spotify.search(query, type='track', limit=5)

            if 'tracks' in search_results and 'items' in search_results['tracks']:
                for track in search_results['tracks']['items']:
                    album = track['album']
                    confidence = self._calculate_confidence(
                        title, artist,
                        track['name'], track['artists'][0]['name']
                    )

                    album_detail = self.spotify.album(album['id'])
                    label = album_detail.get('label')

                    logger.info(f"Spotify - Détails album - Titre: {album_detail.get('name')}, Label: {label}")

                    metadata = TrackMetadata(
                        title=track['name'],
                        artist=track['artists'][0]['name'],
                        album=album['name'],
                        label=label,
                        confidence=confidence,
                        source="Spotify"
                    )
                    results.append(metadata)

            logger.info(f"Spotify - Nombre de résultats: {len(results)}")
            for result in results:
                logger.info(f"Spotify - Résultat: Label={result.label}, Album={result.album}")

        except Exception as e:
            logger.error(f"Erreur Spotify: {e}")

        return results

    def _search_discogs(self, title: str, artist: str) -> List[TrackMetadata]:
        results = []

        try:
            search_results = self.discogs.search(
                f"{title} {artist}",
                type='release',
                format='album'
            )

            for release in list(search_results)[:5]:
                try:
                    artist_name = release.artists[0].name if release.artists else "Unknown Artist"
                    label_name = release.labels[0].name if release.labels else None
                    catalog_num = release.labels[0].catno if release.labels else None

                    confidence = self._calculate_confidence(
                        title, artist,
                        release.title,
                        artist_name
                    )

                    metadata = TrackMetadata(
                        title=release.title,
                        artist=artist_name,
                        album=release.title,
                        label=label_name,
                        catalog_number=catalog_num,
                        confidence=confidence,
                        source="Discogs"
                    )
                    results.append(metadata)

                except (AttributeError, IndexError) as e:
                    logger.debug(f"Erreur lors du traitement d'un résultat Discogs: {e}")
                    continue

        except Exception as e:
            logger.warning(f"Erreur Discogs: {e}")

        return results

    def _search_musicbrainz(self, title: str, artist: str) -> List[TrackMetadata]:
            """Recherche sur MusicBrainz avec nettoyage des titres."""
            logger.info(f"MusicBrainz - Début de recherche pour titre='{title}' artist='{artist}'")
            results = []

            try:
                # Nettoyer le titre pour la recherche
                clean_title = title.split('(')[0].strip()  # Enlever tout ce qui est entre parenthèses
                clean_artist = artist.split('&')[0].strip()  # Prendre seulement le premier artiste

                logger.info(f"MusicBrainz - Recherche avec titre nettoyé: '{clean_title}' artiste: '{clean_artist}'")

                search_results = self.musicbrainz.search_recordings(
                    query=f'recording:"{clean_title}" AND artist:"{clean_artist}"',
                    limit=5
                )

                # Recherche de l'artiste pour le tri
                artist_result = self.musicbrainz.search_artists(clean_artist, limit=1)
                artist_sort_name = None
                if 'artist-list' in artist_result and artist_result['artist-list']:
                    artist_sort_name = artist_result['artist-list'][0].get('sort-name', clean_artist)
                    logger.info(f"MusicBrainz - Nom de tri trouvé: {artist_sort_name}")

                if 'recording-list' in search_results:
                    for recording in search_results['recording-list']:
                        if 'release-list' in recording and recording['release-list']:
                            release = recording['release-list'][0]
                            release_id = release['id']
                            logger.info(f"MusicBrainz - ID de la release trouvé: {release_id}")

                            # Récupération des détails de la release
                            release_details = self.musicbrainz.get_release_by_id(
                                release_id,
                                includes=['labels']
                            )

                            actual_release = release_details.get('release', {})
                            logger.info(f"MusicBrainz - Détails de la release récupérés")

                            # Extraire le label et le numéro de catalogue
                            label = None
                            catalog_number = None

                            if 'label-info-list' in actual_release:
                                label_info = actual_release['label-info-list'][0]
                                if 'label' in label_info:
                                    label = label_info['label']['name']
                                    logger.info(f"MusicBrainz - Label trouvé: {label}")
                                if 'catalog-number' in label_info:
                                    catalog_number = label_info['catalog-number']
                                    logger.info(f"MusicBrainz - Numéro de catalogue trouvé: {catalog_number}")

                            # Calculer la confiance avec le titre original
                            confidence = self._calculate_confidence(
                                title,
                                artist,
                                recording['title'],
                                recording['artist-credit'][0]['artist']['name']
                            )

                            metadata = TrackMetadata(
                                title=recording['title'],
                                artist=recording['artist-credit'][0]['artist']['name'],
                                album=release.get('title', ''),
                                label=label,
                                catalog_number=catalog_number,
                                confidence=confidence,
                                source="MusicBrainz",
                                artist_sort=artist_sort_name  # Ajout du champ de tri
                            )

                            results.append(metadata)
                            logger.info(f"MusicBrainz - Résultat ajouté: {metadata}")

                # Trier les résultats par confiance
                results.sort(key=lambda x: x.confidence, reverse=True)
                if results:
                    logger.info(f"MusicBrainz - Meilleur résultat: {results[0]}")

            except Exception as e:
                logger.error(f"MusicBrainz - Erreur: {str(e)}")

            return results

    def _calculate_confidence(self, query_title: str, query_artist: str,
                               result_title: str, result_artist: str) -> float:
            """Calcule un score de confiance pour les résultats en nettoyant les titres."""
            if not all([query_title, query_artist, result_title, result_artist]):
                return 0.0

            def clean_text(text: str) -> str:
                """Nettoie le texte pour la comparaison."""
                # Enlever tout ce qui est entre parenthèses
                while '(' in text and ')' in text:
                    start = text.find('(')
                    end = text.find(')')
                    if start < end:
                        text = text[:start] + text[end + 1:]
                    else:
                        break

                # Nettoyer et normaliser le texte
                text = text.lower().strip()
                text = ''.join(c for c in text if c.isalnum() or c.isspace())
                return text.strip()

            # Nettoyer les textes pour la comparaison
            query_title_clean = clean_text(query_title)
            query_artist_clean = clean_text(query_artist.split('&')[0])  # Prendre le premier artiste
            result_title_clean = clean_text(result_title)
            result_artist_clean = clean_text(result_artist.split('&')[0])

            logger.info(f"Comparaison de titres: '{query_title_clean}' vs '{result_title_clean}'")
            logger.info(f"Comparaison d'artistes: '{query_artist_clean}' vs '{result_artist_clean}'")

            # Ratio de similarité
            title_ratio = self._levenshtein_ratio(query_title_clean, result_title_clean)
            artist_ratio = self._levenshtein_ratio(query_artist_clean, result_artist_clean)

            logger.info(f"Ratios - Titre: {title_ratio}, Artiste: {artist_ratio}")

            # Pondération : titre (60%) + artiste (40%)
            confidence = (title_ratio * 0.6 + artist_ratio * 0.4) * 100

            # Bonus si l'album correspond exactement
            if query_title_clean in result_title_clean or result_title_clean in query_title_clean:
                confidence = min(100, confidence + 20)

            logger.info(f"Score de confiance final: {confidence}")
            return confidence

    def _levenshtein_ratio(self, s1: str, s2: str) -> float:
        """Calcule le ratio de similarité entre deux chaînes."""
        if not s1 or not s2:
            return 0.0

        distances = {}
        len1, len2 = len(s1), len(s2)

        for i in range(len1 + 1):
            distances[i] = {}
            distances[i][0] = i

        for j in range(len2 + 1):
            distances[0][j] = j

        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if s1[i-1] == s2[j-1]:
                    distances[i][j] = distances[i-1][j-1]
                else:
                    distances[i][j] = min(distances[i-1][j],
                                      distances[i][j-1],
                                      distances[i-1][j-1]) + 1

        max_length = max(len1, len2)
        if max_length == 0:
            return 1.0

        return 1 - (distances[len1][len2] / max_length)


class MP3Processor:
    """Gère le traitement des fichiers MP3."""

    def __init__(self, api_manager: APIManager, locale_manager):
            self.api_manager = api_manager
            self.locale_manager = locale_manager
            self.genre_manager = GenreManager()
            self.error_records = []
            self.not_found_records = []
            self.processing_canceled = False
            self.update_summary = {
                'total_files': 0,
                'updated_files': 0,
                'label_updates': 0,
                'catalog_updates': 0,
                'genre_updates':0,
                'source_used': None,  # Source API utilisée
                'labels_found': set(),  # Ensemble des labels trouvés
                'catalogs_found': set(),  # Ensemble des numéros de catalogue trouvés
                'genres_found': set()  # Correction de genre_found -> genres_found
            }

    def _is_valid_mp3_file(self, file_path: Path) -> bool:
        """Vérifie si le fichier est un MP3 valide et non un fichier caché."""
        # Ignore les fichiers cachés Mac OS et système
        if file_path.name.startswith('._') or file_path.name.startswith('.'):
            return False
        # Vérifie si le fichier est accessible et valide
        try:
            EasyID3(str(file_path))
            return True
        except Exception:
            return False

    def _read_metadata_safe(self, file_path: Path) -> Optional[TrackMetadata]:
        """Version sécurisée de read_metadata sans récursion."""
        if not self._is_valid_mp3_file(file_path):
            return None

        try:
            audio = EasyID3(str(file_path))
            return TrackMetadata(
                title=audio.get('title', [''])[0],
                artist=audio.get('artist', [''])[0],
                album=audio.get('album', [''])[0],
                label=audio.get('composer', [''])[0],
                catalog_number=audio.get('grouping', [''])[0],
                genre=audio.get('genre', [''])[0]
            )
        except Exception as e:
            # Log direct sans récursion
            error_record = {
                'file': str(file_path),
                'title': '',
                'artist': '',
                'album': '',
                'error': self.locale_manager.get_text("processor.metadata.error.read", None, str(e))
            }
            self.error_records.append(error_record)
            return None

    def group_files_by_album(self, files: List[Path], progress_callback) -> Dict[Tuple[str, bool], List[Path]]:
        """Version améliorée du groupement de fichiers."""
        if progress_callback:
            progress_callback(None, self.locale_manager.get_text("processor.analysis.file_grouping"))

        grouped = {}
        # Filtrer d'abord les fichiers valides
        valid_files = [f for f in files if self._is_valid_mp3_file(f)]

        for file_path in valid_files:
            metadata = self._read_metadata_safe(file_path)
            if metadata and metadata.album:
                # Utiliser _read_metadata_safe pour éviter la récursion
                album_files = [f for f in valid_files
                             if (meta := self._read_metadata_safe(f))
                             and meta.album == metadata.album]

                is_ep = len(album_files) < 7
                album_info = (metadata.album, is_ep)

                if album_info not in grouped:
                    grouped[album_info] = []
                if file_path not in grouped[album_info]:
                    grouped[album_info].append(file_path)

        return grouped

    def _get_album_metadata(self, file_path: Path, progress_callback) -> Optional[TrackMetadata]:
        """Obtient les métadonnées pour un album entier à partir d'un fichier."""
        current_metadata = self._read_metadata(file_path)

        if not current_metadata or not (current_metadata.title and current_metadata.artist):
            if progress_callback:
                progress_callback(None, self.locale_manager.get_text("processor.analysis.metadata_missing"))
            return None

        if progress_callback:
            progress_callback(
                None,
                self.locale_manager.get_text(
                    "processor.analysis.metadata_search",
                    None,
                    current_metadata.title,
                    current_metadata.artist
                )
            )

        # Délai pour éviter de surcharger les APIs
        time.sleep(0.5)

        api_results = self.api_manager.search_track(current_metadata.title, current_metadata.artist)

        if not api_results:
            if progress_callback:
                progress_callback(None, self.locale_manager.get_text("processor.analysis.no_results"))
            return None

        best_match = api_results[0]

        if progress_callback:
            progress_callback(
                None,
                self.locale_manager.get_text(
                    "processor.analysis.best_match",
                    None,
                    best_match.source,
                    best_match.confidence
                )
            )
            progress_callback(
                None,
                self.locale_manager.get_text(
                    "processor.analysis.label_info",
                    None,
                    best_match.label if best_match.label else self.locale_manager.get_text("messages.common.not_found")
                )
            )

        # Simplifie la condition de validation
        if best_match.confidence >= 60:
            if best_match.label:
                logger.info(f"Résultat accepté - Score: {best_match.confidence}, Label: {best_match.label}")
                best_match.genre = self.genre_manager.detect_genre(best_match)
                return best_match
            else:
                logger.info("Résultat rejeté - Pas de label trouvé")
        else:
            logger.info(f"Résultat rejeté - Score trop faible: {best_match.confidence}")

        return None

    def _log_error(self, file_path: Path, error_message: str) -> None:
        """Enregistre une erreur dans le fichier CSV."""
        try:
            metadata = self._read_metadata(file_path)
            error_record = {
                'file': str(file_path),
                'title': metadata.title if metadata else '',
                'artist': metadata.artist if metadata else '',
                'album': metadata.album if metadata else '',
                'error': error_message
            }
            self.error_records.append(error_record)
            self._write_error_log()
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement de l'erreur pour {file_path}: {e}")

    def _write_error_log(self):
        """Écrit les erreurs dans un fichier CSV."""
        try:
            with open('error_log.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f, fieldnames=['file', 'title', 'artist', 'album', 'error'])
                writer.writeheader()
                writer.writerows(self.error_records)
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du fichier d'erreurs: {e}")

    # Voici la version corrigée de la méthode _update_metadata
    def _update_metadata(self, file_path: Path, metadata: TrackMetadata) -> None:
        """Met à jour uniquement le label et le numéro de catalogue dans les champs appropriés."""
        try:
            from mutagen.id3 import ID3, TCOM, GRP1, TPE1, TALB, TIT2, TCON, TDTG, TPE2, COMM

            try:
                audio = ID3(str(file_path))
            except:
                audio = ID3()
                audio.save(str(file_path))
                audio = ID3(str(file_path))

            updated = False

            # Sauvegarder les métadonnées existantes
            existing_metadata = {
                'title': str(audio.get('TIT2', [''])[0]) if 'TIT2' in audio else '',
                'artist': str(audio.get('TPE1', [''])[0]) if 'TPE1' in audio else '',
                'album': str(audio.get('TALB', [''])[0]) if 'TALB' in audio else '',
                'genre': str(audio.get('TCON', [''])[0]) if 'TCON' in audio else '',
                'date': str(audio.get('TDTG', [''])[0]) if 'TDTG' in audio else ''
            }

            # Mise à jour du label (composer)
            if metadata.label:
                current_label = str(audio.get('TCOM', [''])[0]) if 'TCOM' in audio else ''
                if current_label.lower() != metadata.label.lower():
                    composer_frame = TCOM(encoding=3, text=[metadata.label])
                    audio['TCOM'] = composer_frame
                    logger.info(f"Label mis à jour: '{current_label}' → '{metadata.label}'")
                    updated = True
                    self.update_summary['label_updates'] += 1
                    self.update_summary['labels_found'].add(metadata.label)

            # Mise à jour du numéro de catalogue (grouping)
            if metadata.catalog_number:
                current_grouping = str(audio.get('GRP1', [''])[0]) if 'GRP1' in audio else ''
                if current_grouping.lower() != metadata.catalog_number.lower():
                    audio['GRP1'] = GRP1(encoding=3, text=[metadata.catalog_number])
                    logger.info(f"Numéro de catalogue mis à jour: '{current_grouping}' → '{metadata.catalog_number}'")
                    updated = True
                    self.update_summary['catalog_updates'] += 1
                    self.update_summary['catalogs_found'].add(metadata.catalog_number)

            # Gestion du genre
            try:
                # Déterminer le nouveau genre
                new_genre = None
                should_update = False
                current_genre = str(audio.get('TCON', [''])[0]) if 'TCON' in audio else ''

                if metadata.label and metadata.label.lower() in self.genre_manager.label_genre_rules:
                    new_genre = self.genre_manager.label_genre_rules[metadata.label.lower()]
                    should_update = True
                    logger.info(f"Genre déterminé par le label: '{new_genre}' (label: {metadata.label})")

                elif metadata.artist and metadata.artist.lower() in self.genre_manager.artist_genre_rules:
                    new_genre = self.genre_manager.artist_genre_rules[metadata.artist.lower()]
                    should_update = True
                    logger.info(f"Genre déterminé par l'artiste: '{new_genre}' (artiste: {metadata.artist})")

                elif current_genre:
                    current_genre_lower = current_genre.lower()
                    if current_genre_lower in self.genre_manager.genre_mapping:
                        mapped_genre = self.genre_manager.genre_mapping[current_genre_lower]
                        if mapped_genre != current_genre:
                            new_genre = mapped_genre
                            should_update = True
                            logger.info(f"Genre remappé: '{current_genre}' → '{new_genre}'")

                elif not current_genre:
                    detected_genre = self.genre_manager.detect_genre(metadata)
                    if detected_genre:
                        new_genre = detected_genre
                        should_update = True
                        logger.info(f"Nouveau genre détecté: '{new_genre}'")

                # Mise à jour du genre si nécessaire
                if should_update and new_genre:
                    # Supprimer tous les tags de genre existants
                    for key in list(audio.keys()):
                        if any(tag in key for tag in ['TCON', 'GENRE']):
                            audio.delall(key)

                    # Ajouter le nouveau genre
                    audio['TCON'] = TCON(encoding=3, text=[new_genre])

                    logger.info(f"Genre mis à jour: '{current_genre}' → '{new_genre}'")
                    self.update_summary['genre_updates'] += 1
                    self.update_summary['genres_found'].add(new_genre)
                    updated = True

            except Exception as e:
                logger.error(f"Erreur lors de la mise à jour du genre: {str(e)}")

            # Nettoyer le titre de l'album
            current_album = existing_metadata['album']
            new_album = current_album

            # Supprime le suffixe "- Single"
            single_patterns = [
                r'\s*-\s*Single\s*$',
                r'\s*\(Single\)\s*$',
                r'\s*-\s*single\s*$',
                r'\s*\(single\)\s*$'
            ]

            for pattern in single_patterns:
                new_album = re.sub(pattern, '', new_album, flags=re.IGNORECASE)

            new_album = new_album.strip()

            if new_album != current_album:
                audio['TALB'] = TALB(encoding=3, text=[new_album])
                logger.info(f"Album nettoyé: '{current_album}' → '{new_album}'")
                updated = True
                existing_metadata['album'] = new_album

            # Mise à jour de l'artiste de l'album (Band)
            if metadata.artist:
                current_album_artist = str(audio.get('TPE2', [''])[0]) if 'TPE2' in audio else ''
                if current_album_artist != metadata.artist:
                    audio['TPE2'] = TPE2(encoding=3, text=[metadata.artist])
                    logger.info(f"Album Artist mis à jour: '{current_album_artist}' → '{metadata.artist}'")
                    updated = True

            # Sauvegarder les modifications si nécessaire
            if updated:
                original_time = os.path.getmtime(file_path)
                self.update_summary['updated_files'] += 1
                self.update_summary['source_used'] = metadata.source
                audio.save(v2_version=4)
                os.utime(file_path, (original_time, original_time))
                logger.info(f"Fichier sauvegardé avec succès: {file_path.name}")

            self.update_summary['total_files'] += 1

        except Exception as e:
            error_msg = f"Erreur de mise à jour des tags: {str(e)}"
            logger.error(error_msg)
            self._log_error(file_path, error_msg)
            raise

    def _read_metadata(self, file_path: Path) -> Optional[TrackMetadata]:
        """Lit les métadonnées existantes d'un fichier MP3."""
        try:
            audio = EasyID3(str(file_path))
            return TrackMetadata(
                title=audio.get('title', [''])[0],
                artist=audio.get('artist', [''])[0],
                album=audio.get('album', [''])[0],
                label=audio.get('composer', [''])[0],
                catalog_number=audio.get('grouping', [''])[0]
            )
        except Exception as e:
            error_msg = f"Erreur de lecture des tags: {str(e)}"
            self._log_error(file_path, error_msg)
            return None

    def _log_not_found(self, file_path: Path, metadata: TrackMetadata, reason: str) -> None:
        """Enregistre les fichiers non trouvés ou non mis à jour."""
        try:
            not_found_record = {
                'file': str(file_path),
                'title': metadata.title if metadata else '',
                'artist': metadata.artist if metadata else '',
                'album': metadata.album if metadata else '',
                'reason': reason
            }
            self.not_found_records.append(not_found_record)
            self._write_not_found_log()
        except Exception as e:
                logger.error(f"Erreur lors de l'enregistrement des non trouvés pour {file_path}: {e}")

    def _write_not_found_log(self):
        """Écrit les fichiers non trouvés dans un CSV séparé."""
        try:
            with open('not_found_log.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(
                    f, fieldnames=['file', 'title', 'artist', 'album', 'reason'])
                writer.writeheader()
                writer.writerows(self.not_found_records)
        except Exception as e:
            logger.error(f"Erreur lors de l'écriture du fichier des non trouvés: {e}")

    def cancel_processing(self):
        """Annule le traitement en cours."""
        self.processing_canceled = True

    def _get_album_metadata(self, file_path: Path, progress_callback) -> Optional[TrackMetadata]:
        """Obtient les métadonnées pour un album entier à partir d'un fichier."""
        current_metadata = self._read_metadata(file_path)

        if not current_metadata or not (current_metadata.title and current_metadata.artist):
            if progress_callback:
                progress_callback(None, "    └─ ⚠️ Métadonnées manquantes ou incomplètes")
            return None

        if progress_callback:
            progress_callback(
                None,
                f"    └─ Recherche pour '{current_metadata.title}' - {current_metadata.artist}..."
            )

        # Délai pour éviter de surcharger les APIs
        time.sleep(0.5)

        api_results = self.api_manager.search_track(
            current_metadata.title,
            current_metadata.artist
        )

        if not api_results:
            if progress_callback:
                progress_callback(None, "    └─ ❌ Aucun résultat trouvé")
            return None

        best_match = api_results[0]

        if progress_callback:
            progress_callback(
                None,
                f"    └─ Meilleure correspondance ({best_match.source}): {best_match.confidence:.1f}%"
            )
            progress_callback(
                None,
                f"    └─ Label : {best_match.label if best_match.label else 'Non trouvé'}"
            )
            progress_callback(
                None,
                f"    └─ No Catalogue : {best_match.catalog_number if best_match.catalog_number else 'Non trouvé'}"
            )

        # Modification de la condition pour accepter les résultats avec au moins un label
        should_use_result = (best_match.confidence >= 60 and best_match.label)

        # Log détaillé pour le débogage
        logger.info(f"Évaluation du résultat - Score: {best_match.confidence}, "
                   f"Label: {best_match.label}, "
                   f"Catalogue: {best_match.catalog_number}")

        if should_use_result:
            logger.info("Résultat accepté - Label trouvé avec score suffisant")
            return best_match
        else:
            logger.info(f"Résultat ignoré - Score insuffisant ou pas de label")
            return None

    def process_directory(self, directory: Path, progress_callback=None) -> None:
        """Traite tous les fichiers MP3 dans un dossier et ses sous-dossiers."""
        try:
            # Gestion des genres personnalisés
            try:
                self.genre_manager.load_custom_mappings('genre_mappings.json')
                if progress_callback:
                    progress_callback(None, "✅ Configuration des genres chargée")
            except Exception as e:
                if progress_callback:
                    progress_callback(None, f"⚠️ Erreur lors du chargement des genres : {str(e)}")
                logger.warning(f"Erreur lors du chargement des mappings de genre : {str(e)}")

            # Filtrer les fichiers MP3 valides dès le début
            mp3_files = [f for f in directory.rglob("*.mp3")
                        if self._is_valid_mp3_file(f)]

            total_files = len(mp3_files)
            if total_files == 0:
                if progress_callback:
                    progress_callback(None, self.locale_manager.get_text("folder.status.no_mp3"))
                return

            if progress_callback:
                progress_callback(
                    0,
                    self.locale_manager.get_text("processor.progress.start", None, total_files)
                )

            self.error_records = []
            self.not_found_records = []
            grouped_files = self.group_files_by_album(mp3_files, progress_callback)

            processed_count = 0
            for (album_name, is_ep), files in grouped_files.items():
                if self.processing_canceled:
                    if progress_callback:
                        progress_callback(None, self.locale_manager.get_text("processor.progress.canceled"))
                    break

                if progress_callback:
                    progress_callback(None, self.locale_manager.get_text(
                        "processor.progress.processing_album",
                        None,
                        album_name
                    ))

                first_file = files[0]
                try:
                    metadata = self._get_album_metadata(first_file, progress_callback)

                    # Vérifie seulement si metadata existe et a un label
                    if metadata and metadata.label:
                        logger.info(f"Traitement des fichiers pour {album_name} avec le label {metadata.label}")
                        for file in files:
                            try:
                                self._update_metadata(file, metadata)
                                processed_count += 1
                                if progress_callback:
                                    progress_callback(
                                        (processed_count / total_files) * 100,
                                        f"[{processed_count}/{total_files}] Mise à jour de {file.name}"
                                    )
                            except Exception as e:
                                error_msg = f"Erreur lors de la mise à jour du fichier {file.name}: {str(e)}"
                                self._log_error(file, error_msg)
                                if progress_callback:
                                    progress_callback(None, f"❌ {error_msg}")
                    else:
                        reason = "Pas de label trouvé" if metadata else "Aucun résultat trouvé"
                        logger.info(f"Fichiers ignorés pour {album_name}: {reason}")
                        for file in files:
                            current_metadata = self._read_metadata(file)
                            self._log_not_found(file, current_metadata, reason)

                except Exception as e:
                    error_msg = f"Erreur lors du traitement de l'album {album_name}: {str(e)}"
                    self._log_error(first_file, error_msg)
                    if progress_callback:
                        progress_callback(None, f"❌ {error_msg}")

            if not self.processing_canceled and progress_callback:
                progress_callback(100, "✅ Traitement terminé!")
                update_summary = self.get_update_summary()
                progress_callback(None, update_summary)

                not_found_count = len(self.not_found_records)
                error_count = len(self.error_records)
                progress_callback(None, "\n📈 Statistiques:")
                progress_callback(None, f"  • Fichiers non trouvés: {not_found_count}")
                progress_callback(None, f"  • Erreurs: {error_count}")

        except Exception as e:
            if progress_callback:
                progress_callback(None, f"❌ Erreur critique: {str(e)}")
            raise

    def get_update_summary(self) -> str:
            """Génère un résumé détaillé des mises à jour effectuées."""
            summary = []
            summary.append("\n📊 Résumé des mises à jour:")
            summary.append(f"  • Source utilisée: {self.update_summary['source_used']}")
            summary.append(f"  • Fichiers traités: {self.update_summary['total_files']}")
            summary.append(f"  • Fichiers mis à jour: {self.update_summary['updated_files']}")

            if self.update_summary['labels_found']:
                summary.append(f"  • Labels trouvés ({self.update_summary['label_updates']} mises à jour):")
                for label in self.update_summary['labels_found']:
                    summary.append(f"    - {label}")

            if self.update_summary['catalogs_found']:
                summary.append(f"  • Numéros de catalogue trouvés ({self.update_summary['catalog_updates']} mises à jour):")
                for catalog in self.update_summary['catalogs_found']:
                    summary.append(f"    - {catalog}")

            if self.update_summary.get('genres_found'):
                    summary.append(f"  • Genres mis à jour ({self.update_summary['genre_updates']} mises à jour):")
                    for genre in self.update_summary['genres_found']:
                        summary.append(f"    - {genre}")

            return "\n".join(summary)

class MetadataManagerGUI:
    """Interface graphique principale du gestionnaire de métadonnées."""

    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.minsize(800, 600)
        self.locale_manager = LocaleManager()
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.root.title(self.locale_manager.get_text("gui.app_title"))

        # Gestionnaires
        self.config_manager = ConfigManager(self.locale_manager)
        self.api_manager = None
        self.mp3_processor = None

        # Variables d'interface
        self.spotify_client_id = tk.StringVar()
        self.spotify_client_secret = tk.StringVar()
        self.discogs_consumer_key = tk.StringVar()
        self.discogs_consumer_secret = tk.StringVar()
        self.discogs_token = tk.StringVar()
        self.selected_directory = tk.StringVar()
        self.show_log = tk.BooleanVar(value=True)

        # Variables pour les services API
        self.musicbrainz_enabled = tk.BooleanVar(value=self.config_manager.is_service_enabled('musicbrainz'))
        self.spotify_enabled = tk.BooleanVar(value=self.config_manager.is_service_enabled('spotify'))
        self.discogs_enabled = tk.BooleanVar(value=self.config_manager.is_service_enabled('discogs'))

        # File d'événements pour le threading
        self.event_queue = Queue()

        self.processing = False
        self.setup_ui()
        self.load_saved_config()
        self.start_event_processing()

    def setup_ui(self):
        """Configuration du menu"""
        self.setup_language_menu()

        """Configure l'interface utilisateur complète."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        style = ttk.Style()
        style.configure('Drop.TFrame', background='gray75', relief='solid', borderwidth=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        self.setup_api_config(main_frame)
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=10)

        self.setup_directory_selection(main_frame)
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=10)

        self.setup_log_section(main_frame)

    def setup_language_menu(self):
        """Configure le menu de sélection de langue."""
        language_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
                label="Language",  # Texte par défaut en cas d'erreur de traduction
                menu=language_menu
        )

        available_locales = self.locale_manager.get_available_locales()

        for code, name in available_locales.items():
            language_menu.add_command(
                label=name,
                command=lambda c=code: self.change_language(c)
            )

    def setup_api_config(self, parent):
        self.api_frame = ttk.LabelFrame(parent, text=self.locale_manager.get_text("gui.layout.api_config"), padding="5")
        self.api_frame.grid(row=0, column=0, columnspan=2, sticky="nsew" )
    
        self.services_frame = ttk.LabelFrame(self.api_frame, text=self.locale_manager.get_text("gui.layout.active_services"), padding="5")
        self.services_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # Checkbuttons
        ttk.Checkbutton(self.services_frame, text=self.locale_manager.get_text("gui.layout.services.musicbrainz"), 
                        variable=self.musicbrainz_enabled).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(self.services_frame, text=self.locale_manager.get_text("gui.layout.services.spotify"), 
                        variable=self.spotify_enabled).grid(row=0, column=1, padx=5)
        ttk.Checkbutton(self.services_frame, text=self.locale_manager.get_text("gui.layout.services.discogs"), 
                        variable=self.discogs_enabled).grid(row=0, column=2, padx=5)

        # Bouton genres
        self.edit_genres_button = ttk.Button(self.services_frame, 
                                        text=self.locale_manager.get_text("gui.buttons.edit_genres"),
                                        command=self.open_mapping_editor)
        self.edit_genres_button.grid(row=0, column=3, padx=5)

        self.load_keys_button = ttk.Button(self.services_frame, 
                                        text=self.locale_manager.get_text("gui.buttons.load_keys"),
                                        command=self.load_api_keys_file)
        self.load_keys_button.grid(row=0, column=4, padx=5)

        self.init_api_button = ttk.Button(self.services_frame, 
                                        text=self.locale_manager.get_text("gui.buttons.init_api"),
                                        command=self.initialize_apis)
        self.init_api_button.grid(row=0, column=5, padx=5)

    def setup_directory_selection(self, parent):
        self.dir_frame = ttk.LabelFrame(parent, text=self.locale_manager.get_text("gui.layout.folder_selection"), padding="5")
        self.dir_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # Zone navigation classique
        self.nav_frame = ttk.Frame(self.dir_frame)
        self.nav_frame.grid(row=0, column=0, sticky="ew", padx=5)

        ttk.Entry(self.nav_frame, textvariable=self.selected_directory, state='readonly').pack(side="left", fill="x", expand=True)
        ttk.Button(self.nav_frame, text=self.locale_manager.get_text("gui.buttons.browse"), command=self.browse_directory).pack(side="left", padx=5)

        # Zone drag & drop
        self.drop_frame = ttk.Frame(self.dir_frame, style='Drop.TFrame', height=100)
        self.drop_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.drop_frame.grid_propagate(False)  # Maintient la hauteur fixe

        self.drop_label = ttk.Label(self.drop_frame, text=self.locale_manager.get_text("gui.dropzone.hint"))
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)

        # Bouton traitement
        self.process_button = ttk.Button(self.dir_frame, text=self.locale_manager.get_text("gui.buttons.start_processing"),
                                       command=self.process_directory,
                                       state="disabled")
        self.process_button.grid(row=2, column=0, pady=5)

        self.dir_frame.columnconfigure(0, weight=1)
    
    def setup_log_section(self, parent):
        """Configure la section de log et progression."""
        log_frame = ttk.LabelFrame(parent, text=self.locale_manager.get_text("gui.layout.progress"), padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=5)

        progress_info_frame = ttk.Frame(log_frame)
        progress_info_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=2)

        self.progress_label = ttk.Label(progress_info_frame, text=self.locale_manager.get_text("gui.status.waiting"))
        self.progress_label.pack(side="left", padx=5)

        self.progress_percent = ttk.Label(progress_info_frame, text="0%")
        self.progress_percent.pack(side="right", padx=5)

        self.log_text = tk.Text(log_frame, height=15, width=80, wrap=tk.WORD)
        self.log_text.grid(row=1, column=0, sticky="nsew", pady=5)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical",
                                command=self.log_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.log_text['yscrollcommand'] = scrollbar.set

        # Barre de progression
        self.progress = ttk.Progressbar(log_frame, mode='determinate', length=300)
        self.progress.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)

        # Boutons de contrôle
        button_frame = ttk.Frame(log_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

        self.cancel_button = ttk.Button(button_frame, text=self.locale_manager.get_text("gui.buttons.cancel"),
                                      command=self.cancel_processing,
                                      state="disabled")
        self.cancel_button.pack(side="left", padx=5)

        self.clear_button = ttk.Button(button_frame, text=self.locale_manager.get_text("gui.buttons.clear_log"),
                                     command=self.clear_log)
        self.clear_button.pack(side="left", padx=5)

        self.export_button = ttk.Button(button_frame, text=self.locale_manager.get_text("gui.buttons.export_logs"),
                                    command=self.export_logs)
        self.export_button.pack(side="left", padx=5)

        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(1, weight=1)
        parent.rowconfigure(4, weight=1)

    def start_event_processing(self):
        """Démarre le traitement des événements en arrière-plan."""
        def process_events():
            while True:
                try:
                    event = self.event_queue.get_nowait()
                    if event[0] == "progress":
                        self.handle_progress_update(event[1], event[2])
                    elif event[0] == "log":
                        self.log_message(event[1])
                except Empty:
                    break
            self.root.after(100, process_events)

        self.root.after(100, process_events)

    def change_language(self, locale_code):
        """Change la langue de l'interface."""
        if self.locale_manager.set_locale(locale_code):
            self.update_ui_texts()

    def update_ui_texts(self):
        self.root.title(self.locale_manager.get_text("gui.app_title"))
        
        if hasattr(self, 'services_frame'):
            for checkbox in self.services_frame.winfo_children():
                if isinstance(checkbox, ttk.Checkbutton):
                    service = checkbox["text"].lower()
                    checkbox.configure(text=self.locale_manager.get_text(f"gui.layout.services.{service}"))
                elif isinstance(checkbox, ttk.Button):
                    if "edit_genres" in str(checkbox):
                        checkbox.configure(text=self.locale_manager.get_text("gui.buttons.edit_genres"))
                    elif "load_keys" in str(checkbox):
                        checkbox.configure(text=self.locale_manager.get_text("gui.buttons.load_keys"))
                    elif "init_api" in str(checkbox):
                        checkbox.configure(text=self.locale_manager.get_text("gui.buttons.init_api"))

        if hasattr(self, 'api_frame'):
            self.api_frame.configure(text=self.locale_manager.get_text("gui.layout.api_config"))
            self.services_frame.configure(text=self.locale_manager.get_text("gui.layout.active_services"))

        if hasattr(self, 'dir_frame'):
            self.dir_frame.configure(text=self.locale_manager.get_text("gui.layout.folder_selection"))
            self.drop_label.configure(text=self.locale_manager.get_text("gui.dropzone.hint"))
            for child in self.nav_frame.winfo_children():
                if isinstance(child, ttk.Button):
                    child.configure(text=self.locale_manager.get_text("gui.buttons.browse"))

        if hasattr(self, 'edit_genres_button'):
            self.edit_genres_button.configure(text=self.locale_manager.get_text("gui.buttons.edit_genres"))
        if hasattr(self, 'load_keys_button'):
            self.load_keys_button.configure(text=self.locale_manager.get_text("gui.buttons.load_keys"))
        if hasattr(self, 'init_api_button'):
            self.init_api_button.configure(text=self.locale_manager.get_text("gui.buttons.init_api"))
        if hasattr(self, 'progress_label'):
            self.progress_label.configure(text=self.locale_manager.get_text("gui.status.waiting"))
        if hasattr(self, 'process_button'):
            self.process_button.configure(text=self.locale_manager.get_text("gui.buttons.start_processing"))
        if hasattr(self, 'cancel_button'):
            self.cancel_button.configure(text=self.locale_manager.get_text("gui.buttons.cancel"))
        if hasattr(self, 'clear_button'):
            self.clear_button.configure(text=self.locale_manager.get_text("gui.buttons.clear_log"))
        if hasattr(self, 'export_button'):
            self.export_button.configure(text=self.locale_manager.get_text("gui.buttons.export_logs"))

    def open_mapping_editor(self):
        """Ouvre l'éditeur de mapping de genres."""
        GenreMappingEditor(self.root, self.locale_manager)

    def load_api_keys_file(self):
        filename = filedialog.askopenfilename(
            title="Sélectionner le fichier de configuration",
            filetypes=[("JSON files", "*.json")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)

                if 'spotify' in config:
                    self.spotify_client_id.set(config['spotify'].get('client_id', ''))
                    self.spotify_client_secret.set(config['spotify'].get('client_secret', ''))

                if 'discogs' in config:
                    self.discogs_consumer_key.set(config['discogs'].get('consumer_key', ''))
                    self.discogs_consumer_secret.set(config['discogs'].get('consumer_secret', ''))
                    self.discogs_token.set(config['discogs'].get('token', ''))

                self.log_message("✅ Configuration chargée avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")

    def handle_drop(self, event):
        path = event.data
        # Nettoyer le chemin des caractères spéciaux
        path = path.strip('{}').strip('"')

        if os.path.exists(path):
            if os.path.isfile(path):
                if path.lower().endswith('.mp3'):
                    directory = os.path.dirname(path)
                else:
                    self.log_message(self.locale_manager.get_text("messages.error.mp3_only"))
                    return
            else:
                directory = path

            self.selected_directory.set(directory)
            self.process_button['state'] = 'normal'
            self.log_message(self.locale_manager.get_text("logs.folder.added", None, directory))

    def initialize_apis(self):
            """Initialise les APIs avec les informations fournies."""
            config = {
                'spotify_client_id': self.spotify_client_id.get(),
                'spotify_client_secret': self.spotify_client_secret.get(),
                'discogs_token': self.discogs_token.get(),
                'services': {
                    'musicbrainz': self.musicbrainz_enabled.get(),
                    'spotify': self.spotify_enabled.get(),
                    'discogs': self.discogs_enabled.get()
                }
            }

            enabled_services = [name for name, enabled in config['services'].items() if enabled]
            if not enabled_services:
                messagebox.showerror(
                    self.locale_manager.get_text("messages.error.api_config"),
                    self.locale_manager.get_text("messages.error.api_required")
                )
                return

            try:
                self.log_message(self.locale_manager.get_text("api.initialization.start"))
                self.config_manager.save_config(config)
                self.progress['value'] = 0

                # Création préalable de la liste des étapes
                services_steps = []
                if config['services']['musicbrainz']:
                    services_steps.append((self.locale_manager.get_text("api.initialization.connection.musicbrainz"), 33))

                self.api_manager = APIManager(config, self.locale_manager)

                if config['services']['spotify']:
                    services_steps.append((self.locale_manager.get_text("api.initialization.connection.spotify"), 66))
                if config['services']['discogs']:
                    services_steps.append((self.locale_manager.get_text("api.initialization.connection.discogs"), 100))

                def init_step(step):
                    if step < len(services_steps):
                        message, progress = services_steps[step]
                        if self.log_text:  # Vérification que log_text existe
                            self.log_message(message)
                        self.progress['value'] = progress

                        if step == 0:  # Initialisation des APIs au premier pas
                            self.api_manager = APIManager(config, self.locale_manager)

                        self.root.after(500, lambda: init_step(step + 1))
                    else:
                        if self.log_text:  # Vérification que log_text existe
                            self.log_message(self.locale_manager.get_text("api.initialization.complete"))
                            self.log_message(self.locale_manager.get_text("api.initialization.success_final"))

                # Démarrer l'initialisation uniquement s'il y a des services à initialiser
                if services_steps:
                    init_step(0)
                else:
                    self.log_message("Aucun service à initialiser")

            except Exception as e:
                error_msg = self.locale_manager.get_text(
                    "api.initialization.error.message",
                    None,
                    str(e)
                )
                messagebox.showerror(
                    self.locale_manager.get_text("api.initialization.error.title"),
                    error_msg
                )
                if self.log_text:  # Vérification que log_text existe
                    self.log_message(
                        self.locale_manager.get_text(
                            "api.initialization.error.log",
                            None,
                            str(e)
                        )
                    )

    def toggle_service(self, service_name: str, var: tk.BooleanVar):
        """Active ou désactive un service API."""
        self.config_manager.set_service_state(service_name, var.get())
        self.log_message(f"Service {service_name}: {'activé' if var.get() else 'désactivé'}")

    def browse_directory(self):
        """Ouvre une boîte de dialogue pour sélectionner un dossier."""
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory.set(directory)
            self.process_button['state'] = 'normal'
            self.log_message(f"Dossier sélectionné : {directory}")

    def process_directory(self):
        """Lance le traitement des fichiers MP3 du dossier sélectionné."""
        if not self.api_manager:
            messagebox.showerror(
            self.locale_manager.get_text("messages.error.api_config"),
            self.locale_manager.get_text("messages.error.initialize_first")
            )
            return

        directory = Path(self.selected_directory.get())
        if not directory.exists():
            self.log_message(self.locale_manager.get_text("logs.folder.not_found"))
            return

        self.log_message(self.locale_manager.get_text("logs.processing.start", None, str(directory)))
        self.log_message(self.locale_manager.get_text("logs.processing.analyzing"))

        self.processing = True
        self.process_button['state'] = 'disabled'
        self.cancel_button['state'] = 'normal'
        self.progress['value'] = 0
        self.progress_percent['text'] = "0%"
        self.progress_label['text'] = self.locale_manager.get_text("gui.status.waiting")

        def process_thread():
            try:
                self.log_message(self.locale_manager.get_text("processor.analysis.creating_processor"))
                self.mp3_processor = MP3Processor(self.api_manager, self.locale_manager)
                self.log_message(self.locale_manager.get_text("processor.progress.processor_ready"))

                self.log_message(self.locale_manager.get_text(
                    "processor.progress.processing_directory",
                    None,
                    str(directory)
                ))

                self.mp3_processor.process_directory(directory, self.update_progress)

            except Exception as e:
                error_msg = self.locale_manager.get_text(
                    "messages.error.critical",
                    None,
                    str(e)
                )
                self.log_message(error_msg)
                import traceback
                self.log_message(self.locale_manager.get_text(
                    "messages.error.details",
                    None,
                    ''.join(traceback.format_tb(e.__traceback__))
                ))
            finally:
                self.processing = False
                self.root.after(0, self.reset_ui_after_processing)

        threading.Thread(target=process_thread, daemon=True).start()

    def load_saved_config(self):
            """Charge la configuration sauvegardée."""
            config = self.config_manager.load_config()
            self.spotify_client_id.set(config.get('spotify_client_id', ''))
            self.spotify_client_secret.set(config.get('spotify_client_secret', ''))
            self.discogs_token.set(config.get('discogs_token', ''))

            # Charger l'état des services
            services = config.get('services', {})
            self.musicbrainz_enabled.set(services.get('musicbrainz', True))
            self.spotify_enabled.set(services.get('spotify', False))
            self.discogs_enabled.set(services.get('discogs', False))

    def cancel_processing(self):
        """Annule le traitement en cours."""
        if self.mp3_processor and self.processing:
            self.mp3_processor.cancel_processing()
            self.log_message(self.locale_manager.get_text("logs.processing.cancel"))
            self.cancel_button['state'] = 'disabled'

    def reset_ui_after_processing(self):
        """Réinitialise l'interface après le traitement."""
        self.process_button['state'] = 'normal'
        self.cancel_button['state'] = 'disabled'
        if (hasattr(self, 'mp3_processor') and
            self.mp3_processor is not None and
            hasattr(self.mp3_processor, 'error_records') and
            self.mp3_processor.error_records):
            self.log_message(
                self.locale_manager.get_text(
                    "logs.processing.errors",
                    None,
                    len(self.mp3_processor.error_records)
            )
            )

    def clear_log(self):
        """Efface le contenu de la zone de log."""
        self.log_text.delete(1.0, tk.END)
        self.progress['value'] = 0
        self.progress_percent['text'] = "0%"
        self.progress_label['text'] = self.locale_manager.get_text("waiting")

    def log_message(self, message: str):
        """Ajoute un message au log."""
        if self.show_log.get():
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)

    def update_progress(self, value, message):
        """Met à jour la progression et le log."""
        self.event_queue.put(("progress", value, message))

    def handle_progress_update(self, value, message):
        """Gère la mise à jour de l'interface pour la progression."""
        if value is not None:
            self.progress['value'] = value
            self.progress_percent['text'] = f"{value:.1f}%"

            if "[" in message and "/" in message and "]" in message:
                try:
                    count_info = message.split("[")[1].split("]")[0]
                    current, total = map(int, count_info.split("/"))
                    self.progress_label['text'] = f"Fichier {current}/{total}"
                except:
                    self.progress_label['text'] = message
            else:
                self.progress_label['text'] = message

        self.log_message(message)

    def export_logs(self):
        """Exporte les logs dans un fichier."""
        try:
            # Crée le dossier logs s'il n'existe pas
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)

            # Timestamp pour le nom du fichier
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # Sauvegarde du log de traitement
            log_content = self.log_text.get(1.0, tk.END)
            log_file = logs_dir / f"processing_log_{timestamp}.txt"
            log_file.write_text(log_content, encoding='utf-8')

            # Copie des fichiers de résultats s'ils existent
            if hasattr(self, 'mp3_processor') and self.mp3_processor is not None:
                if hasattr(self.mp3_processor, 'error_records') and self.mp3_processor.error_records:
                    error_file = logs_dir / f"error_log_{timestamp}.csv"
                    with open(error_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=['file', 'title', 'artist', 'album', 'error'])
                        writer.writeheader()
                        writer.writerows(self.mp3_processor.error_records)

                if hasattr(self.mp3_processor, 'not_found_records') and self.mp3_processor.not_found_records:
                    not_found_file = logs_dir / f"not_found_{timestamp}.csv"
                    with open(not_found_file, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=['file', 'title', 'artist', 'album', 'reason'])
                        writer.writeheader()
                        writer.writerows(self.mp3_processor.not_found_records)

            self.log_message(self.locale_manager.get_text("logs.export.success"))
        except Exception as e:
            messagebox.showerror(
                self.locale_manager.get_text("logs.export.error.title"),
                self.locale_manager.get_text("logs.export.error.message", None, str(e))
            )
            self.log_message(self.locale_manager.get_text("logs.export.error.log", None, str(e)))

class GenreMappingEditor:
    def __init__(self, parent, locale_manager):
        self.locale_manager = locale_manager
        self.window = tk.Toplevel(parent)
        self.window.title(self.locale_manager.get_text("gui.genre_editor.title"))
        self.window.geometry("800x600")
        self.window.minsize(800, 600)

        # Définition des en-têtes pour chaque type de mapping
        self.headers = {
            'genres': (
                self.locale_manager.get_text("gui.genre_editor.columns.source_genre"),
                self.locale_manager.get_text("gui.genre_editor.columns.mapped_genre")
            ),
            'labels': ('Label', 'Genre'),
            'artists': ('Artiste', 'Genre')
        }

        # Création des onglets
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        # Création des trois frames pour chaque type de mapping
        self.genres_frame = ttk.Frame(self.notebook)
        self.labels_frame = ttk.Frame(self.notebook)
        self.artists_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.genres_frame, text=self.locale_manager.get_text("gui.genre_editor.tabs.genres"))
        self.notebook.add(self.labels_frame, text=self.locale_manager.get_text("gui.genre_editor.tabs.labels"))
        self.notebook.add(self.artists_frame, text=self.locale_manager.get_text("gui.genre_editor.tabs.artists"))

        # Initialisation des tableaux
        self.setup_treeview(self.genres_frame, 'genres')
        self.setup_treeview(self.labels_frame, 'labels')
        self.setup_treeview(self.artists_frame, 'artists')

        # Boutons de contrôle
        self.setup_control_buttons()

        # Chargement des données
        self.load_mappings()

    def setup_treeview(self, parent, mapping_type):
        # Frame pour les boutons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=5, pady=5)

        ttk.Button(button_frame, text=self.locale_manager.get_text("gui.genre_editor.buttons.add"),
                  command=lambda: self.add_item(mapping_type)).pack(side='left', padx=2)
        ttk.Button(button_frame, text=self.locale_manager.get_text("gui.genre_editor.buttons.delete"),
                  command=lambda: self.delete_item(mapping_type)).pack(side='left', padx=2)
        ttk.Button(button_frame, text=self.locale_manager.get_text("gui.genre_editor.buttons.edit"),
                  command=lambda: self.edit_item(mapping_type)).pack(side='left', padx=2)

        # Création du Treeview
        columns = ('source', 'mapped')
        tree = ttk.Treeview(parent, columns=columns, show='headings')

        # Définition des en-têtes
        tree.heading('source', text=self.headers[mapping_type][0])
        tree.heading('mapped', text=self.headers[mapping_type][1])

        # Configuration des colonnes
        tree.column('source', width=200)
        tree.column('mapped', width=200)

        # Scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Placement des éléments
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Stocker la référence au Treeview
        setattr(self, f"{mapping_type}_tree", tree)

        # Double-clic pour éditer
        tree.bind('<Double-1>', lambda e: self.edit_item(mapping_type))

    def add_item(self, mapping_type):
        dialog = EditMappingDialog(
            parent=self.window,
            source="",
            mapped="",
            headers=self.headers[mapping_type],
            locale_manager=self.locale_manager
        )
        if dialog.result:
            source, mapped = dialog.result
            tree = getattr(self, f"{mapping_type}_tree")
            tree.insert('', 'end', values=(source, mapped))

    def edit_item(self, mapping_type):
        tree = getattr(self, f"{mapping_type}_tree")
        selected = tree.selection()
        if not selected:
            return

        current_values = tree.item(selected[0])['values']
        dialog = EditMappingDialog(
            parent=self.window,
            source=current_values[0],
            mapped=current_values[1],
            headers=self.headers[mapping_type],
            locale_manager=self.locale_manager
        )
        if dialog.result:
            source, mapped = dialog.result
            tree.item(selected[0], values=(source, mapped))

    def delete_item(self, mapping_type):
        tree = getattr(self, f"{mapping_type}_tree")
        selected = tree.selection()
        if selected:
            if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élément ?"):
                tree.delete(selected[0])

    def setup_control_buttons(self):
        control_frame = ttk.Frame(self.window)
        control_frame.pack(fill='x', padx=5, pady=5)

        save_btn = ttk.Button(control_frame, 
                            text=self.locale_manager.get_text("gui.genre_editor.buttons.save"),
                            command=self.save_mappings)
        save_btn.pack(side='left', padx=5)

        close_btn = ttk.Button(control_frame, 
                             text=self.locale_manager.get_text("gui.genre_editor.buttons.close"),
                             command=self.window.destroy)
        close_btn.pack(side='right', padx=5)

    def load_mappings(self):
        try:
            with open('genre_mappings.json', 'r', encoding='utf-8') as f:
                mappings = json.load(f)

            # Chargement des données dans chaque Treeview
            for mapping_type in ['genres', 'labels', 'artists']:
                tree = getattr(self, f"{mapping_type}_tree")
                tree.delete(*tree.get_children())

                for source, mapped in mappings.get(mapping_type, {}).items():
                    tree.insert('', 'end', values=(source, mapped))

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des mappings: {str(e)}")

    def save_mappings(self):
        try:
            mappings = {}

            # Récupération des données de chaque Treeview
            for mapping_type in ['genres', 'labels', 'artists']:
                tree = getattr(self, f"{mapping_type}_tree")
                mapping_dict = {}

                for item in tree.get_children():
                    source, mapped = tree.item(item)['values']
                    mapping_dict[source.lower()] = mapped

                mappings[mapping_type] = mapping_dict

            # Sauvegarde dans le fichier
            with open('genre_mappings.json', 'w', encoding='utf-8') as f:
                json.dump(mappings, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Succès", "Mappings sauvegardés avec succès!")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")

class EditMappingDialog:
    def __init__(self, parent, source="", mapped="", headers=('Source', 'Mapped'),locale_manager=None):
        if locale_manager is None:
            raise ValueError("locale_manager cannot be None")
        self.locale_manager = locale_manager
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(self.locale_manager.get_text("gui.genre_editor.dialog.title"))
        self.dialog.geometry("400x200")
        self.result = None

        # Champs de saisie
        ttk.Label(self.dialog, text=headers[0]).pack(pady=5)
        self.source_entry = ttk.Entry(self.dialog, width=40)
        self.source_entry.insert(0, source)
        self.source_entry.pack(pady=5)

        ttk.Label(self.dialog, text=headers[1]).pack(pady=5)
        self.mapped_entry = ttk.Entry(self.dialog, width=40)
        self.mapped_entry.insert(0, mapped)
        self.mapped_entry.pack(pady=5)

        # Boutons
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill='x', padx=5, pady=10)

        ttk.Button(button_frame, text=self.locale_manager.get_text("gui.genre_editor.dialog.buttons.ok"), command=self.ok).pack(side='left', padx=5)
        ttk.Button(button_frame, text=self.locale_manager.get_text("gui.genre_editor.dialog.buttons.cancel"), command=self.cancel).pack(side='right', padx=5)

        self.dialog.transient(parent)
        self.dialog.grab_set()
        parent.wait_window(self.dialog)

    def ok(self):
        source = self.source_entry.get().strip()
        mapped = self.mapped_entry.get().strip()
        if source and mapped:
            self.result = (source, mapped)
            self.dialog.destroy()

    def cancel(self):
        self.dialog.destroy()

def main():
    """Point d'entrée principal du programme."""
    app = MetadataManagerGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
