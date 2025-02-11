# AMTU (Apple Music Tag Updater)

[Version en français](../README.md) | [English version](README.en.md) | [Versione italiana](README.it.md) | [Versión española](README.es.md) | [Versão em português](README.pt.md) | [Deutsch Version](README.de.md)

AMTU ist ein grafisches Python-Tool zum automatischen Aktualisieren von MP3-Tag-Informationen unter Verwendung verschiedener Musikdatenquellen (MusicBrainz, Spotify, Discogs) für eine bessere Organisation Ihrer Apple Music-Bibliothek.

⚠️ **Wichtig**: Dieses Tool ist ausschließlich für MP3-Dateien gedacht, die Sie legal besitzen (gekauft oder heruntergeladen) und die für die Organisation über die Apple Music-Bibliothek bestimmt sind. Es ist nicht kompatibel mit gestreamten Titeln oder Titeln, die Teil eines Apple Music- oder anderen Abonnementdienstes sind. AMTU dient der Organisation und Verwaltung Ihrer persönlichen Musikbibliothek in Apple Music, insbesondere der Verbesserung von Metadaten für eine bessere Erfahrung mit der Anwendung.

## 🌟 Hauptfunktionen

- **Apple Music-Optimierung**:
  - Aktualisierung des Album-Interpreten für bessere Albumgruppierung in Apple Music
  - Automatische Bereinigung von Albumnamen (Entfernung des Suffixes "- Single")
  - Intelligente Bibliotheksorganisation für bessere visuelle Erfahrung

- **Metadaten-Anreicherung**:
  - Label (gespeichert im Komponisten-Feld)
  - Katalognummer (gespeichert im Gruppierungs-Feld)
  - Album-Interpret (gespeichert im Band-Feld)

- Benutzerfreundliche Oberfläche mit Drag & Drop-Unterstützung
- Multi-Quellen-Suche (MusicBrainz, Spotify, Discogs)
- Automatische Tag-Aktualisierungen
- Erhaltung bestehender Metadaten
- Fehlerbehandlung und detaillierte Protokolle
- Export von Ergebnissen und Protokollen
- Unterstützung für Stapelverarbeitung
- Intelligente Album/EP-Gruppierung

- **Intelligente Genre-Verwaltung**:
  - Automatische Genre-Erkennung basierend auf Label und Künstler
  - Anpassbare Genre-Zuordnung über grafische Oberfläche
  - Flexible Genre-Regelkonfiguration nach Label und Künstler
  - Automatische Genre-Aktualisierungen nach Ihren Präferenzen

- **Integrierter Genre-Mapping-Editor**:
  - Grafische Oberfläche zur Verwaltung von Genre-Zuordnungen
  - Konfiguration von Zuordnungsregeln für:
    - Genres (z.B. "dnb" → "Drum & Bass")
    - Labels (z.B. "Hospital Records" → "Drum & Bass")
    - Künstler (z.B. "Netsky" → "Drum & Bass")
  - Echtzeit-Regelaktualisierungen
  - Automatische Konfigurationsspeicherung

## 🌍 Mehrsprachige Unterstützung

AMTU ist in folgenden Sprachen verfügbar:
- 🇫🇷 Französisch
- 🇬🇧 Englisch
- 🇮🇹 Italienisch
- 🇪🇸 Spanisch
- 🇵🇹 Portugiesisch
- 🇩🇪 Deutsch

Funktionen der mehrsprachigen Unterstützung:
- Vollständig übersetzte Benutzeroberfläche
- Dynamischer Sprachwechsel ohne Neustart
- Speicherung der Spracheinstellung
- Lokalisierte Fehlermeldungen und Protokolle
- Dokumentation in allen unterstützten Sprachen

Zum Ändern der Sprache:
1. Starten Sie AMTU
2. Wählen Sie im Hauptmenü "Sprache"
3. Wählen Sie Ihre bevorzugte Sprache
4. Die Oberfläche wird automatisch aktualisiert

## 🔧 Voraussetzungen

- Python 3.7 oder höher
- Die folgenden Python-Bibliotheken:
  - tkinter
  - tkinterdnd2
  - mutagen
  - spotipy
  - discogs-client
  - musicbrainzngs
  - requests

## 📦 Installation und API-Konfiguration

1. Repository klonen:
```bash
git clone https://github.com/your-username/AMTU.git
cd AMTU
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. API-Konfiguration:

- **MusicBrainz**: Keine Konfiguration erforderlich (standardmäßig aktiviert)

- **Spotify API** [(App erstellen)](https://developer.spotify.com/dashboard):
  - Erstellen Sie ein Spotify-Entwicklerkonto
  - Erstellen Sie eine neue Anwendung
  - Holen Sie sich Ihre `client_id` und `client_secret`

- **Discogs API** [(Token erstellen)](https://www.discogs.com/settings/developers):
  - Erstellen Sie ein Discogs-Konto
  - Gehen Sie zu den Entwicklereinstellungen
  - Generieren Sie ein neues persönliches Token

4. Erstellen Sie eine `api_keys.json`-Datei mit Ihren API-Schlüsseln:
```json
{
    "spotify": {
        "client_id": "ihre_client_id",
        "client_secret": "ihr_client_secret"
    },
    "discogs": {
        "token": "ihr_token"
    }
}
```

## 🚀 Verwendung

1. Programm starten:
```bash
python AMTU.py
```

2. In der grafischen Oberfläche:
   - Laden Sie Ihre API-Schlüssel
   - Wählen Sie die zu verwendenden Dienste (MusicBrainz, Spotify, Discogs)
   - Initialisieren Sie die APIs
   - [Optional] Konfigurieren Sie Ihre Genre-Zuordnungsregeln
   - Wählen Sie einen Ordner mit Ihren MP3-Dateien (oder nutzen Sie Drag & Drop)
   - Starten Sie die Verarbeitung

## 📝 Protokolle und Berichte

AMTU generiert verschiedene Protokolldateien:
- `error_log.csv`: Liste aufgetretener Fehler
- `not_found_log.csv`: Liste nicht gefundener Dateien
- Exportierbare Verarbeitungsprotokolle mit Zeitstempel

## ⚙️ Konfiguration

### API-Dienste
Dienste können einzeln aktiviert/deaktiviert werden:
- MusicBrainz (standardmäßig aktiviert)
- Spotify (erfordert API-Schlüssel)
- Discogs (erfordert Token)

### Genre-Konfiguration
Der Genre-Mapping-Editor ermöglicht:
1. Definition von Genre-Zuordnungsregeln über grafische Oberfläche
2. Verwaltung von drei Regeltypen:
   - Genre-Zuordnungen (Umwandlung von einem Genre in ein anderes)
   - Label-basierte Regeln (Genre-Zuweisung basierend auf Label)
   - Künstler-basierte Regeln (Genre-Zuweisung basierend auf Künstler)
3. Konfigurationen werden in `genre_mappings.json` gespeichert

Zugriff auf den Editor:
1. Starten Sie AMTU
2. Klicken Sie auf "Zuordnungen bearbeiten"
3. Verwenden Sie Registerkarten zur Verwaltung jedes Zuordnungstyps
4. Doppelklicken Sie auf einen Eintrag, um ihn zu ändern
5. Verwenden Sie Hinzufügen/Löschen/Bearbeiten-Schaltflächen zur Verwaltung Ihrer Regeln
6. Vergessen Sie nicht, Ihre Änderungen zu speichern

## 📁 Konfigurationsdateien

- `api_keys.json`: API-Schlüssel-Konfiguration
- `genre_mappings.json`: Genre-Zuordnungsregeln-Konfiguration
  ```json
  {
    "genres": {
      "dnb": "Drum & Bass",
      "jungle": "Drum & Bass"
    },
    "labels": {
      "hospital records": "Drum & Bass",
      "ram records": "Drum & Bass"
    },
    "artists": {
      "netsky": "Drum & Bass",
      "high contrast": "Drum & Bass"
    }
  }
  ```
- `locales/`: Ordner mit Übersetzungsdateien
  ```
  locales/
  ├── en.json    # Englisch
  ├── fr.json    # Französisch
  ├── it.json    # Italienisch
  ├── es.json    # Spanisch
  ├── pt.json    # Portugiesisch
  └── de.json    # Deutsch
  ```

## 🔨 Für Entwickler

### Code-Struktur
- **AMTU.py**: Hauptprogramm und grafische Oberfläche
- **genre_manager.py**: Genre-Verwaltung und -Erkennung
- **models.py**: Datenmodelle und -strukturen
  ```python
  @dataclass
  class TrackMetadata:
      title: str               # Titel des Tracks
      artist: str             # Hauptkünstler
      album: str              # Albumname
      label: Optional[str]    # Label (gespeichert in Komponist)
      catalog_number: Optional[str]  # Katalognummer
      artist_sort: Optional[str]     # Künstler-Sortiername
      is_single: bool = False        # Single-Indikator
      confidence: float = 0.0        # Match-Konfidenzwert
      source: str = ""              # Metadatenquelle (MusicBrainz, Spotify, Discogs)
      genre: Optional[str] = None   # Musikgenre
  ```

## 🤝 Mitwirken

Beiträge sind willkommen! Sie können:
1. Das Projekt forken
2. Einen Feature-Branch erstellen
3. Ihre Änderungen committen
4. In Ihren Fork pushen
5. Einen Pull Request öffnen

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die [LICENSE](LICENSE)-Datei für Details.