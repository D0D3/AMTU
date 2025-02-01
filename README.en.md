# AMTU (Apple Music Tag Updater)

[Version en français](README.md) | [English version](README.en.md) | [Versione italiana](README.it.md) | [Versión española](README.es.md) | [Versão em português](README.pt.md)

AMTU is a Python graphical tool for automatically updating MP3 file tags using multiple music data sources (MusicBrainz, Spotify, Discogs) for better organization of your Apple Music library.

⚠️ **Important**: This tool is designed only for MP3 files that you legally own (purchased or downloaded) intended for organization via the Apple Music library. It is not compatible with streamed tracks or tracks that are part of an Apple Music or other subscription service. AMTU is intended for organizing and managing your personal music library in Apple Music, specifically improving metadata for a better experience with the application.

## 🌟 Main Features

- **Apple Music Optimization**:
  - Album artist update for better album grouping in Apple Music
  - Automatic album name cleaning (removal of "- Single" suffix)
  - Intelligent library organization for better visual experience

- **Metadata Enrichment**:
  - Label (stored in Composer field)
  - Catalog number (stored in Grouping field)
  - Album artist (stored in Band field)

- User-friendly interface with drag & drop support
- Multi-source search (MusicBrainz, Spotify, Discogs)
- Automatic tag updates
- Preservation of existing metadata
- Error handling and detailed logs
- Results and logs export
- Batch processing support
- Smart album/EP grouping

- **Smart Genre Management**:
  - Automatic genre detection based on label and artist
  - Customizable genre mapping via graphical interface
  - Flexible genre rules configuration by label and artist
  - Automatic genre updates according to your preferences

- **Integrated Genre Mapping Editor**:
  - Graphical interface for managing genre mappings
  - Mapping rules configuration for:
    - Genres (e.g., "dnb" → "Drum & Bass")
    - Labels (e.g., "Hospital Records" → "Drum & Bass")
    - Artists (e.g., "Netsky" → "Drum & Bass")
  - Real-time rule updates
  - Automatic configuration saving

## 🌍 Multilingual Support

AMTU is available in the following languages:
- 🇫🇷 French
- 🇬🇧 English
- 🇮🇹 Italian
- 🇪🇸 Spanish
- 🇵🇹 Portuguese

Multilingual support features:
- Fully translated user interface
- Dynamic language switching without restart
- Language preference preservation
- Localized error messages and logs
- Documentation available in all supported languages

To change the language:
1. Launch AMTU
2. In the main menu, select "Language"
3. Choose your preferred language
4. The interface updates automatically

## 🔧 Prerequisites

- Python 3.7 or higher
- The following Python libraries:
  - tkinter
  - tkinterdnd2
  - mutagen
  - spotipy
  - discogs-client
  - musicbrainzngs
  - requests

## 📦 Installation and API Configuration

1. Clone the repository:
```bash
git clone https://github.com/your-username/AMTU.git
cd AMTU
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. API Configuration:

- **MusicBrainz**: No configuration needed (enabled by default)

- **Spotify API** [(Create an app)](https://developer.spotify.com/dashboard):
  - Create a Spotify developer account
  - Create a new application
  - Get your `client_id` and `client_secret`

- **Discogs API** [(Create a token)](https://www.discogs.com/settings/developers):
  - Create a Discogs account
  - Go to developer settings
  - Generate a new personal token

4. Create an `api_keys.json` file with your API keys:
```json
{
    "spotify": {
        "client_id": "your_client_id",
        "client_secret": "your_client_secret"
    },
    "discogs": {
        "token": "your_token"
    }
}
```

## 🚀 Usage

1. Launch the program:
```bash
python AMTU.py
```

2. In the graphical interface:
   - Load your API keys
   - Select services to use (MusicBrainz, Spotify, Discogs)
   - Initialize APIs
   - [Optional] Configure your genre mapping rules
   - Select a folder containing your MP3 files (or use drag & drop)
   - Start processing

## 📝 Logs and Reports

AMTU generates several log files:
- `error_log.csv`: List of encountered errors
- `not_found_log.csv`: List of files not found
- Exportable processing logs with timestamp

## ⚙️ Configuration

### API Services
Services can be enabled/disabled individually:
- MusicBrainz (enabled by default)
- Spotify (requires API keys)
- Discogs (requires token)

### Genre Configuration
The genre mapping editor allows you to:
1. Define genre mapping rules via graphical interface
2. Manage three types of rules:
   - Genre mappings (conversion from one genre to another)
   - Label-based rules (genre assignment based on label)
   - Artist-based rules (genre assignment based on artist)
3. Configurations are saved in `genre_mappings.json`

To access the editor:
1. Launch AMTU
2. Click the "Edit Mappings" button
3. Use tabs to manage each type of mapping
4. Double-click an entry to modify it
5. Use Add/Delete/Edit buttons to manage your rules
6. Don't forget to save your changes

## 📁 Configuration Files

- `api_keys.json`: API key configuration
- `genre_mappings.json`: Genre mapping rules configuration
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
- `locales/`: Folder containing translation files
  ```
  locales/
  ├── en.json    # English
  ├── fr.json    # French
  ├── it.json    # Italian
  ├── es.json    # Spanish
  └── pt.json    # Portuguese
  ```

## 🔨 For Developers

### Code Structure
- **AMTU.py**: Main program and graphical interface
- **genre_manager.py**: Genre management and detection
- **models.py**: Data models and structures
  ```python
  @dataclass
  class TrackMetadata:
      title: str               # Track title
      artist: str             # Main artist
      album: str              # Album name
      label: Optional[str]    # Label (stored in Composer)
      catalog_number: Optional[str]  # Catalog number
      artist_sort: Optional[str]     # Artist sort name
      is_single: bool = False        # Single indicator
      confidence: float = 0.0        # Match confidence score
      source: str = ""              # Metadata source (MusicBrainz, Spotify, Discogs)
      genre: Optional[str] = None   # Musical genre
  ```

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

## 📄 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for details.