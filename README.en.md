[Version française](README.md)
# AMTU (Apple Music Tag Updater)

AMTU is a Python GUI tool designed to automatically update MP3 file tags using multiple music data sources (MusicBrainz, Spotify, Discogs) for better organization of your Apple Music library.

⚠️ **Important**: This tool is designed exclusively for MP3 files that you legally own (purchased or downloaded) intended for organization through the Apple Music library. It is not compatible with streamed tracks or those that are part of an Apple Music subscription service or others. AMTU is intended for organizing and managing your personal music library in Apple Music, specifically improving metadata for a better experience with the application.

## 🌟 Main Features

- **Apple Music Optimization**:
  - Album artist update for better album grouping in Apple Music
  - Automatic album name cleaning (removing "- Single" suffix)
  - Smart library organization for better visual experience

- **Metadata Enrichment**:
  - Label (stored in Composer field)
  - Catalog number (stored in Grouping field)
  - Album artist (stored in Band field)

- User-friendly GUI with drag & drop support
- Multi-source search (MusicBrainz, Spotify, Discogs)
- Automatic tag updates:
  - Label (stored in Composer field)
  - Catalog number (stored in Grouping field)
  - Album artist (stored in Band field)
- Preservation of existing metadata
- Error handling and detailed logs
- Results and logs export
- Batch processing support
- Smart album/EP grouping

- **Intelligent Genre Management**:
  - Automatic genre detection based on label and artist
  - Customizable genre mapping through GUI
  - Flexible genre rules configuration by label and artist
  - Automatic genre updates according to your preferences

- **Integrated Genre Mapping Editor**:
  - GUI for managing genre mappings
  - Configuration of mapping rules for:
    - Genres (e.g., "dnb" → "Drum & Bass")
    - Labels (e.g., "Hospital Records" → "Drum & Bass")
    - Artists (e.g., "Netsky" → "Drum & Bass")
  - Real-time rule updates
  - Automatic configuration saving

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

2. In the GUI:
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
- Exportable processing logs with timestamps

## ⚙️ Configuration

### API Services
Services can be enabled/disabled individually:
- MusicBrainz (enabled by default)
- Spotify (requires API keys)
- Discogs (requires token)

### Genre Configuration
The genre mapping editor allows you to:
1. Define genre mapping rules through the GUI
2. Manage three types of rules:
   - Genre mappings (converting one genre to another)
   - Label-based rules (assigning genre based on label)
   - Artist-based rules (assigning genre based on artist)
3. Configurations are saved in `genre_mappings.json`

To access the editor:
1. Launch AMTU
2. Click the "Edit Mappings" button
3. Use tabs to manage each type of mapping
4. Double-click an entry to modify it
5. Use Add/Delete/Edit buttons to manage your rules
6. Don't forget to save your changes

## 📁 Configuration Files

- `api_keys.json`: API keys configuration
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

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

## 📄 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.
