# AMTU (Apple Music Tag Updater)

[Version en français](README.md) | [English version](README.en.md) | [Versione italiana](README.it.md) | [Versión española](README.es.md) | [Versão em português](README.pt.md)

AMTU è uno strumento grafico Python per aggiornare automaticamente i tag dei file MP3 utilizzando diverse fonti di dati musicali (MusicBrainz, Spotify, Discogs) per una migliore organizzazione della tua libreria Apple Music.

⚠️ **Importante**: Questo strumento è progettato solo per i file MP3 di cui si è legalmente proprietari (acquistati o scaricati) destinati all'organizzazione tramite la libreria Apple Music. Non è compatibile con brani in streaming o che fanno parte di un servizio in abbonamento Apple Music o altri. AMTU è destinato all'organizzazione e alla gestione della tua libreria musicale personale in Apple Music, migliorando specificamente i metadati per una migliore esperienza con l'applicazione.

## 🌟 Caratteristiche Principali

- **Ottimizzazione per Apple Music**:
  - Aggiornamento dell'artista dell'album per un migliore raggruppamento degli album in Apple Music
  - Pulizia automatica dei nomi degli album (rimozione del suffisso "- Single")
  - Organizzazione intelligente della libreria per una migliore esperienza visiva

- **Arricchimento dei Metadati**:
  - Etichetta (memorizzata nel campo Compositore)
  - Numero di catalogo (memorizzato nel campo Raggruppamento)
  - Artista dell'album (memorizzato nel campo Band)

- Interfaccia grafica intuitiva con supporto drag & drop
- Ricerca multi-fonte (MusicBrainz, Spotify, Discogs)
- Aggiornamenti automatici dei tag
- Conservazione dei metadati esistenti
- Gestione degli errori e log dettagliati
- Esportazione dei risultati e dei log
- Supporto per l'elaborazione batch
- Raggruppamento intelligente album/EP

- **Gestione Intelligente dei Generi**:
  - Rilevamento automatico del genere basato su etichetta e artista
  - Mappatura personalizzabile dei generi tramite interfaccia grafica
  - Configurazione flessibile delle regole di genere per etichetta e artista
  - Aggiornamento automatico dei generi secondo le tue preferenze

## 🌍 Supporto Multilingua

AMTU è disponibile nelle seguenti lingue:
- 🇫🇷 Francese
- 🇬🇧 Inglese
- 🇮🇹 Italiano
- 🇪🇸 Spagnolo
- 🇵🇹 Portoghese

Caratteristiche del supporto multilingua:
- Interfaccia utente completamente tradotta
- Cambio lingua dinamico senza riavvio
- Conservazione delle preferenze linguistiche
- Messaggi di errore e log localizzati
- Documentazione disponibile in tutte le lingue supportate

Per cambiare lingua:
1. Avvia AMTU
2. Nel menu principale, seleziona "Lingua"
3. Scegli la lingua preferita
4. L'interfaccia si aggiorna automaticamente

## 🔧 Prerequisiti

- Python 3.7 o superiore
- Le seguenti librerie Python:
  - tkinter
  - tkinterdnd2
  - mutagen
  - spotipy
  - discogs-client
  - musicbrainzngs
  - requests

## 📦 Installazione e Configurazione API

1. Clona il repository:
```bash
git clone https://github.com/your-username/AMTU.git
cd AMTU
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configurazione API:

- **MusicBrainz**: Nessuna configurazione necessaria (abilitato di default)

- **Spotify API** [(Crea un'app)](https://developer.spotify.com/dashboard):
  - Crea un account sviluppatore Spotify
  - Crea una nuova applicazione
  - Ottieni il tuo `client_id` e `client_secret`

- **Discogs API** [(Crea un token)](https://www.discogs.com/settings/developers):
  - Crea un account Discogs
  - Vai alle impostazioni sviluppatore
  - Genera un nuovo token personale

4. Crea un file `api_keys.json` con le tue chiavi API:
```json
{
    "spotify": {
        "client_id": "tuo_client_id",
        "client_secret": "tuo_client_secret"
    },
    "discogs": {
        "token": "tuo_token"
    }
}
```

## 🚀 Utilizzo

1. Avvia il programma:
```bash
python AMTU.py
```

2. Nell'interfaccia grafica:
   - Carica le tue chiavi API
   - Seleziona i servizi da utilizzare (MusicBrainz, Spotify, Discogs)
   - Inizializza le API
   - [Opzionale] Configura le tue regole di mappatura dei generi
   - Seleziona una cartella contenente i tuoi file MP3 (o usa il drag & drop)
   - Avvia l'elaborazione

## 📝 Log e Report

AMTU genera diversi file di log:
- `error_log.csv`: Elenco degli errori riscontrati
- `not_found_log.csv`: Elenco dei file non trovati
- Log di elaborazione esportabili con timestamp

## ⚙️ Configurazione

### Servizi API
I servizi possono essere abilitati/disabilitati individualmente:
- MusicBrainz (abilitato di default)
- Spotify (richiede chiavi API)
- Discogs (richiede token)

### Configurazione dei Generi
L'editor di mappatura dei generi permette di:
1. Definire regole di mappatura dei generi tramite interfaccia grafica
2. Gestire tre tipi di regole:
   - Mappature dei generi (conversione da un genere all'altro)
   - Regole basate sull'etichetta (assegnazione del genere basata sull'etichetta)
   - Regole basate sull'artista (assegnazione del genere basata sull'artista)
3. Le configurazioni vengono salvate in `genre_mappings.json`

Per accedere all'editor:
1. Avvia AMTU
2. Clicca sul pulsante "Modifica Mappature"
3. Usa le schede per gestire ogni tipo di mappatura
4. Fai doppio clic su una voce per modificarla
5. Usa i pulsanti Aggiungi/Elimina/Modifica per gestire le tue regole
6. Non dimenticare di salvare le modifiche

## 📁 File di Configurazione

- `api_keys.json`: Configurazione delle chiavi API
- `genre_mappings.json`: Configurazione delle regole di mappatura dei generi
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
- `locales/`: Cartella contenente i file di traduzione
  ```
  locales/
  ├── en.json    # Inglese
  ├── fr.json    # Francese
  ├── it.json    # Italiano
  ├── es.json    # Spagnolo
  └── pt.json    # Portoghese
  ```

## 🔨 Per gli Sviluppatori

### Struttura del Codice
- **AMTU.py**: Programma principale e interfaccia grafica
- **genre_manager.py**: Gestione e rilevamento dei generi
- **models.py**: Modelli di dati e strutture
  ```python
  @dataclass
  class TrackMetadata:
      title: str               # Titolo della traccia
      artist: str             # Artista principale
      album: str              # Nome dell'album
      label: Optional[str]    # Etichetta (memorizzata in Compositore)
      catalog_number: Optional[str]  # Numero di catalogo
      artist_sort: Optional[str]     # Nome di ordinamento dell'artista
      is_single: bool = False        # Indicatore di singolo
      confidence: float = 0.0        # Punteggio di confidenza
      source: str = ""              # Fonte dei metadati (MusicBrainz, Spotify, Discogs)
      genre: Optional[str] = None   # Genere musicale
  ```

## 🤝 Contribuire

I contributi sono benvenuti! Sentiti libero di:
1. Fare il fork del progetto
2. Creare un ramo per la tua funzionalità
3. Committare le tue modifiche
4. Fare il push sul tuo fork
5. Aprire una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.