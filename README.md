[English version](README.en.md)
# AMTU (Apple Music Tag Updater)

AMTU est un outil graphique Python permettant de mettre à jour automatiquement les tags des fichiers MP3 en utilisant plusieurs sources de données musicales (MusicBrainz, Spotify, Discogs) pour une meilleure organisation de votre bibliothèque Apple Music.

⚠️ **Important**: Cet outil est conçu uniquement pour les fichiers MP3 que vous possédez légalement (achetés ou téléchargés) destinée a l'organisation via la bibliothèque Apple Music. Il n'est pas compatible avec les morceaux streamés ou faisant partie d'un service d'abonnement Apple Music ou autres. AMTU est destiné à l'organisation et à la gestion de votre bibliothèque musicale personnelle dans Apple Music, en améliorant spécifiquement les métadonnées pour une meilleure expérience avec l'application.

## 🌟 Fonctionnalités Principales

- **Optimisation pour Apple Music** :
  - Mise à jour de l'artiste d'album pour un meilleur regroupement des albums dans Apple Music
  - Nettoyage automatique des noms d'albums (suppression du suffixe "- Single")
  - Organisation intelligente de la bibliothèque pour une meilleure expérience visuelle

- **Enrichissement des métadonnées** :
  - Label (stocké dans le champ Composer)
  - Numéro de catalogue (stocké dans le champ Grouping)
  - Artiste de l'album (stocké dans le champ Band)

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

## 📦 Installation et Configuration des APIs

1. Clonez le repository :
```bash
git clone https://github.com/votre-username/AMTU.git
cd AMTU
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configuration des APIs :

- **MusicBrainz** : Pas de configuration nécessaire (activé par défaut)

- **Spotify API** [(Créer une app)](https://developer.spotify.com/dashboard) :
  - Créez un compte développeur Spotify
  - Créez une nouvelle application
  - Récupérez vos `client_id` et `client_secret`

- **Discogs API** [(Créer un token)](https://www.discogs.com/settings/developers) :
  - Créez un compte Discogs
  - Allez dans les paramètres développeur
  - Générez un nouveau token personnel

4. Créez un fichier `api_keys.json` avec vos clés d'API :
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
python AMTU.py
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
