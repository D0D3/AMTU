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
   - Select a folder containing your MP3 files (or use drag & drop)
   - Start processing

## 📝 Logs and Reports

AMTU generates several log files:
- `error_log.csv`: List of encountered errors
- `not_found_log.csv`: List of files not found
- Exportable processing logs with timestamps

## ⚙️ Configuration

Services can be enabled/disabled individually:
- MusicBrainz (enabled by default)
- Spotify (requires API keys)
- Discogs (requires token)

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the project
2. Create a branch for your feature
3. Commit your changes
4. Push to your fork
5. Open a Pull Request

## 📄 License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.
