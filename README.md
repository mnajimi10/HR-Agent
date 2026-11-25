# hr-agent

> ⚠️ **Projet d'apprentissage uniquement.**
> Ce dépôt est un simple test pour s'exercer à construire un agent IA (API Flask, appel LLM, RAG, isolation par tenant). Il n'est **pas prêt pour la production** et ne doit pas être utilisé avec de vraies données.

## Objectif

Mettre en pratique, étape par étape, les notions d'un agent IA industrialisé :

- appel d'un LLM avec timeout, retries et gestion d'erreurs
- validation des entrées et sorties avec Pydantic
- logs structurés (durée, tokens)
- à venir : RAG avec PostgreSQL + pgvector, isolation par `tenant_id`, authentification JWT, mémoire de conversation, outil et boucle d'agent

## Limites connues

- Pas d'authentification réelle (le JWT sera simulé)
- Données fictives uniquement
- Modèle local (Ollama) peu performant, choisi pour éviter les coûts
- Pas de déploiement, pas de monitoring, pas de sécurité renforcée

## Stack

Python, Flask, Pydantic, OpenAI SDK (compatible Ollama), pytest.
PostgreSQL + pgvector prévus pour l'étape suivante.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Crée un fichier `.env` (jamais commité) :

```
LLM_API_KEY=ollama
LLM_MODEL=llama3.2
```

## Lancer

Avec Ollama installé et le modèle téléchargé (`ollama pull llama3.2`) :

```bash
python app.py
```

## Tester

Dans un second terminal :

```powershell
# PowerShell
Invoke-RestMethod -Uri http://127.0.0.1:5000/ask -Method Post -ContentType "application/json" -Body '{"question": "Bonjour"}'
```

Tests automatiques (le LLM est simulé) :

```bash
pytest -v
```

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/health` | Vérifie que le serveur tourne |
| POST | `/ask` | Pose une question à l'agent (`{"question": "..."}`) |

## Statut

Étape 1 sur 6 : appel LLM de base. Projet d'entraînement, sans garantie.