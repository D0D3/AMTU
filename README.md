# AMTU (Apple Music Tag Updater)

AMTU est un outil graphique Python permettant de mettre à jour automatiquement les tags des fichiers MP3 en utilisant plusieurs sources de données musicales (MusicBrainz, Spotify, Discogs).

## 🌟 Fonctionnalités

- Interface graphique conviviale avec support du drag & drop
- Recherche multi-sources (MusicBrainz, Spotify, Discogs)
- Mise à jour automatique des tags :
  - Label (stocké dans le champ Composer)
  - Numéro de catalogue (stocké dans le champ Grouping)
  - Artiste de l'album (stocké dans le champ Band)
- Préservation des métadonnées existantes
- Gestion des erreurs et logs détaillés
- Export des résultats et des logs
- Support du traitement par lots
- Regroupement intelligent par album/EP

## 🔧 Prérequis

- Python 3.7 ou supérieur
- Les bibliothèques Python suivantes :
  - tkinter
  - tkinterdnd2
  - mutagen
  - spotipy
  - discogs-client
  - musicbrainzngs
  - requests

## 📦 Installation

1. Clonez le repository :
```bash
git clone https://github.com/votre-username/AMTU.git
cd AMTU
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez un fichier `api_keys.json` avec vos clés d'API :
```json
{
    "spotify": {
        "client_id": "votre_client_id",
        "client_secret": "votre_client_secret"
    },
    "discogs": {
        "token": "votre_token"
    }
}
```

## 🚀 Utilisation

1. Lancez le programme :
```bash
python AMTU_ver2.14.py
```

2. Dans l'interface graphique :
   - Chargez vos clés API
   - Sélectionnez les services à utiliser (MusicBrainz, Spotify, Discogs)
   - Initialisez les APIs
   - Sélectionnez un dossier contenant vos fichiers MP3 (ou utilisez le drag & drop)
   - Lancez le traitement

## 📝 Logs et Rapports

AMTU génère plusieurs fichiers de logs :
- `error_log.csv` : Liste des erreurs rencontrées
- `not_found_log.csv` : Liste des fichiers non trouvés
- Logs de traitement exportables avec horodatage

## ⚙️ Configuration

Les services peuvent être activés/désactivés individuellement :
- MusicBrainz (activé par défaut)
- Spotify (nécessite des clés API)
- Discogs (nécessite un token)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser sur votre fork
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

