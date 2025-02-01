# AMTU (Apple Music Tag Updater)

[Version en français](README.md) | [English version](README.en.md) | [Versione italiana](README.it.md) | [Versión española](README.es.md) | [Versão em português](README.pt.md)

AMTU é uma ferramenta gráfica Python para atualizar automaticamente as tags de arquivos MP3 usando múltiplas fontes de dados musicais (MusicBrainz, Spotify, Discogs) para uma melhor organização da sua biblioteca Apple Music.

⚠️ **Importante**: Esta ferramenta é projetada apenas para arquivos MP3 que você possui legalmente (comprados ou baixados) destinados à organização através da biblioteca Apple Music. Não é compatível com faixas transmitidas ou que fazem parte de um serviço de assinatura Apple Music ou outros. O AMTU é destinado a organizar e gerenciar sua biblioteca musical pessoal no Apple Music, melhorando especificamente os metadados para uma melhor experiência com o aplicativo.

## 🌟 Recursos Principais

- **Otimização para Apple Music**:
  - Atualização do artista do álbum para melhor agrupamento de álbuns no Apple Music
  - Limpeza automática de nomes de álbuns (remoção do sufixo "- Single")
  - Organização inteligente da biblioteca para uma melhor experiência visual

- **Enriquecimento de Metadados**:
  - Gravadora (armazenada no campo Compositor)
  - Número do catálogo (armazenado no campo Agrupamento)
  - Artista do álbum (armazenado no campo Banda)

- Interface gráfica amigável com suporte a arrastar e soltar
- Pesquisa multi-fonte (MusicBrainz, Spotify, Discogs)
- Atualizações automáticas de tags
- Preservação de metadados existentes
- Gestão de erros e logs detalhados
- Exportação de resultados e logs
- Suporte a processamento em lote
- Agrupamento inteligente de álbuns/EP

## 🌍 Suporte Multilíngue

AMTU está disponível nos seguintes idiomas:
- 🇫🇷 Francês
- 🇬🇧 Inglês
- 🇮🇹 Italiano
- 🇪🇸 Espanhol
- 🇵🇹 Português

Características do suporte multilíngue:
- Interface do usuário totalmente traduzida
- Mudança dinâmica de idioma sem reinicialização
- Preservação das preferências de idioma
- Mensagens de erro e logs localizados
- Documentação disponível em todos os idiomas suportados

Para mudar o idioma:
1. Inicie o AMTU
2. No menu principal, selecione "Idioma"
3. Escolha seu idioma preferido
4. A interface é atualizada automaticamente

## 🔧 Pré-requisitos

- Python 3.7 ou superior
- As seguintes bibliotecas Python:
  - tkinter
  - tkinterdnd2
  - mutagen
  - spotipy
  - discogs-client
  - musicbrainzngs
  - requests

## 📦 Instalação e Configuração de APIs

1. Clone o repositório:
```bash
git clone https://github.com/your-username/AMTU.git
cd AMTU
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configuração das APIs:

- **MusicBrainz**: Não requer configuração (habilitado por padrão)

- **API do Spotify** [(Criar um app)](https://developer.spotify.com/dashboard):
  - Crie uma conta de desenvolvedor Spotify
  - Crie uma nova aplicação
  - Obtenha seu `client_id` e `client_secret`

- **API do Discogs** [(Criar um token)](https://www.discogs.com/settings/developers):
  - Crie uma conta no Discogs
  - Acesse as configurações de desenvolvedor
  - Gere um novo token pessoal

4. Crie um arquivo `api_keys.json` com suas chaves API:
```json
{
    "spotify": {
        "client_id": "seu_client_id",
        "client_secret": "seu_client_secret"
    },
    "discogs": {
        "token": "seu_token"
    }
}
```

## 🚀 Uso

1. Inicie o programa:
```bash
python AMTU.py
```

2. Na interface gráfica:
   - Carregue suas chaves API
   - Selecione os serviços a utilizar (MusicBrainz, Spotify, Discogs)
   - Inicialize as APIs
   - [Opcional] Configure suas regras de mapeamento de gêneros
   - Selecione uma pasta contendo seus arquivos MP3 (ou use arrastar e soltar)
   - Inicie o processamento

## 📝 Logs e Relatórios

AMTU gera vários arquivos de log:
- `error_log.csv`: Lista de erros encontrados
- `not_found_log.csv`: Lista de arquivos não encontrados
- Logs de processamento exportáveis com registro de data e hora

## ⚙️ Configuração

### Serviços API
Os serviços podem ser habilitados/desabilitados individualmente:
- MusicBrainz (habilitado por padrão)
- Spotify (requer chaves API)
- Discogs (requer token)

### Configuração de Gêneros
O editor de mapeamento de gêneros permite:
1. Definir regras de mapeamento de gêneros via interface gráfica
2. Gerenciar três tipos de regras:
   - Mapeamentos de gêneros (conversão de um gênero para outro)
   - Regras baseadas em gravadoras (atribuição de gênero por gravadora)
   - Regras baseadas em artistas (atribuição de gênero por artista)
3. As configurações são salvas em `genre_mappings.json`

Para acessar o editor:
1. Inicie o AMTU
2. Clique no botão "Editar Mapeamentos"
3. Use as abas para gerenciar cada tipo de mapeamento
4. Faça duplo clique em uma entrada para modificá-la
5. Use os botões Adicionar/Excluir/Editar para gerenciar suas regras
6. Não se esqueça de salvar suas alterações

## 📁 Arquivos de Configuração

- `api_keys.json`: Configuração das chaves API
- `genre_mappings.json`: Configuração das regras de mapeamento de gêneros
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
- `locales/`: Pasta contendo os arquivos de tradução
  ```
  locales/
  ├── en.json    # Inglês
  ├── fr.json    # Francês
  ├── it.json    # Italiano
  ├── es.json    # Espanhol
  └── pt.json    # Português
  ```

## 🔨 Para Desenvolvedores

### Estrutura do Código
- **AMTU.py**: Programa principal e interface gráfica
- **genre_manager.py**: Gerenciamento e detecção de gêneros
- **models.py**: Modelos de dados e estruturas
  ```python
  @dataclass
  class TrackMetadata:
      title: str               # Título da faixa
      artist: str             # Artista principal
      album: str              # Nome do álbum
      label: Optional[str]    # Gravadora (armazenada em Compositor)
      catalog_number: Optional[str]  # Número do catálogo
      artist_sort: Optional[str]     # Nome de ordenação do artista
      is_single: bool = False        # Indicador de single
      confidence: float = 0.0        # Pontuação de confiança
      source: str = ""              # Fonte dos metadados (MusicBrainz, Spotify, Discogs)
      genre: Optional[str] = None   # Gênero musical
  ```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer fork do projeto
2. Criar um branch para sua funcionalidade
3. Fazer commit de suas alterações
4. Fazer push para seu fork
5. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.