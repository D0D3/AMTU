# AMTU (Apple Music Tag Updater)

[Version en français](README.md) | [English version](README.en.md) | [Versione italiana](README.it.md) | [Versión española](README.es.md) | [Versão em português](README.pt.md)

AMTU es una herramienta gráfica Python para actualizar automáticamente las etiquetas de archivos MP3 utilizando múltiples fuentes de datos musicales (MusicBrainz, Spotify, Discogs) para una mejor organización de tu biblioteca de Apple Music.

⚠️ **Importante**: Esta herramienta está diseñada únicamente para archivos MP3 que poseas legalmente (comprados o descargados) destinados a la organización a través de la biblioteca de Apple Music. No es compatible con pistas transmitidas o que forman parte de un servicio de suscripción de Apple Music u otros. AMTU está destinado a organizar y gestionar tu biblioteca musical personal en Apple Music, mejorando específicamente los metadatos para una mejor experiencia con la aplicación.

## 🌟 Características Principales

- **Optimización para Apple Music**:
  - Actualización del artista del álbum para una mejor agrupación de álbumes en Apple Music
  - Limpieza automática de nombres de álbumes (eliminación del sufijo "- Single")
  - Organización inteligente de la biblioteca para una mejor experiencia visual

- **Enriquecimiento de Metadatos**:
  - Sello discográfico (almacenado en el campo Compositor)
  - Número de catálogo (almacenado en el campo Agrupación)
  - Artista del álbum (almacenado en el campo Banda)

- Interfaz gráfica amigable con soporte de arrastrar y soltar
- Búsqueda multi-fuente (MusicBrainz, Spotify, Discogs)
- Actualizaciones automáticas de etiquetas
- Preservación de metadatos existentes
- Gestión de errores y registros detallados
- Exportación de resultados y registros
- Soporte de procesamiento por lotes
- Agrupación inteligente de álbumes/EP

## 🌍 Soporte Multilingüe

AMTU está disponible en los siguientes idiomas:
- 🇫🇷 Francés
- 🇬🇧 Inglés
- 🇮🇹 Italiano
- 🇪🇸 Español
- 🇵🇹 Portugués

Características del soporte multilingüe:
- Interfaz de usuario completamente traducida
- Cambio dinámico de idioma sin reinicio
- Conservación de preferencias de idioma
- Mensajes de error y registros localizados
- Documentación disponible en todos los idiomas soportados

Para cambiar el idioma:
1. Inicia AMTU
2. En el menú principal, selecciona "Idioma"
3. Elige tu idioma preferido
4. La interfaz se actualiza automáticamente

## 🔧 Requisitos Previos

- Python 3.7 o superior
- Las siguientes bibliotecas Python:
  - tkinter
  - tkinterdnd2
  - mutagen
  - spotipy
  - discogs-client
  - musicbrainzngs
  - requests

## 📦 Instalación y Configuración de APIs

1. Clona el repositorio:
```bash
git clone https://github.com/your-username/AMTU.git
cd AMTU
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configuración de APIs:

- **MusicBrainz**: No requiere configuración (habilitado por defecto)

- **API de Spotify** [(Crear una app)](https://developer.spotify.com/dashboard):
  - Crea una cuenta de desarrollador de Spotify
  - Crea una nueva aplicación
  - Obtén tu `client_id` y `client_secret`

- **API de Discogs** [(Crear un token)](https://www.discogs.com/settings/developers):
  - Crea una cuenta de Discogs
  - Ve a la configuración de desarrollador
  - Genera un nuevo token personal

4. Crea un archivo `api_keys.json` con tus claves API:
```json
{
    "spotify": {
        "client_id": "tu_client_id",
        "client_secret": "tu_client_secret"
    },
    "discogs": {
        "token": "tu_token"
    }
}
```

## 🚀 Uso

1. Inicia el programa:
```bash
python AMTU.py
```

2. En la interfaz gráfica:
   - Carga tus claves API
   - Selecciona los servicios a utilizar (MusicBrainz, Spotify, Discogs)
   - Inicializa las APIs
   - [Opcional] Configura tus reglas de mapeo de géneros
   - Selecciona una carpeta que contenga tus archivos MP3 (o usa arrastrar y soltar)
   - Inicia el procesamiento

## 📝 Registros e Informes

AMTU genera varios archivos de registro:
- `error_log.csv`: Lista de errores encontrados
- `not_found_log.csv`: Lista de archivos no encontrados
- Registros de procesamiento exportables con marca de tiempo

## ⚙️ Configuración

### Servicios API
Los servicios pueden ser habilitados/deshabilitados individualmente:
- MusicBrainz (habilitado por defecto)
- Spotify (requiere claves API)
- Discogs (requiere token)

### Configuración de Géneros
El editor de mapeo de géneros permite:
1. Definir reglas de mapeo de géneros a través de la interfaz gráfica
2. Gestionar tres tipos de reglas:
   - Mapeos de géneros (conversión de un género a otro)
   - Reglas basadas en sellos (asignación de género según el sello)
   - Reglas basadas en artistas (asignación de género según el artista)
3. Las configuraciones se guardan en `genre_mappings.json`

Para acceder al editor:
1. Inicia AMTU
2. Haz clic en el botón "Editar Mapeos"
3. Usa las pestañas para gestionar cada tipo de mapeo
4. Haz doble clic en una entrada para modificarla
5. Usa los botones Agregar/Eliminar/Editar para gestionar tus reglas
6. No olvides guardar tus cambios

## 📁 Archivos de Configuración

- `api_keys.json`: Configuración de claves API
- `genre_mappings.json`: Configuración de reglas de mapeo de géneros
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
- `locales/`: Carpeta que contiene los archivos de traducción
  ```
  locales/
  ├── en.json    # Inglés
  ├── fr.json    # Francés
  ├── it.json    # Italiano
  ├── es.json    # Español
  └── pt.json    # Portugués
  ```

## 🔨 Para Desarrolladores

### Estructura del Código
- **AMTU.py**: Programa principal e interfaz gráfica
- **genre_manager.py**: Gestión y detección de géneros
- **models.py**: Modelos de datos y estructuras
  ```python
  @dataclass
  class TrackMetadata:
      title: str               # Título de la pista
      artist: str             # Artista principal
      album: str              # Nombre del álbum
      label: Optional[str]    # Sello (almacenado en Compositor)
      catalog_number: Optional[str]  # Número de catálogo
      artist_sort: Optional[str]     # Nombre de ordenación del artista
      is_single: bool = False        # Indicador de single
      confidence: float = 0.0        # Puntuación de confianza
      source: str = ""              # Fuente de metadatos (MusicBrainz, Spotify, Discogs)
      genre: Optional[str] = None   # Género musical
  ```

## 🤝 Contribución

¡Las contribuciones son bienvenidas! No dudes en:
1. Hacer fork del proyecto
2. Crear una rama para tu funcionalidad
3. Hacer commit de tus cambios
4. Hacer push a tu fork
5. Abrir una Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.