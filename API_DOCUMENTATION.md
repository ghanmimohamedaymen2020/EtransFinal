# API Documentation - E-Trans

## Base URL
```
http://localhost:5000/api
```

## Authentification

Toutes les routes API nécessitent une authentification. Deux méthodes:

### 1. Session (Flask-Login)
Utilisée automatiquement lors de la connexion web.

### 2. JWT Token
Pour les appels API:
```
Authorization: Bearer <JWT_TOKEN>
```

## Endpoints

### Dossiers

#### Récupérer la liste des dossiers
```http
GET /api/dossiers
Query Parameters:
  - page: int (default: 1)
  - per_page: int (default: 10)
```

**Response:**
```json
{
  "dossiers": [
    {
      "id": 1,
      "numero": "DOS001",
      "type_conteneur": "FCL",
      "date_arrivee": "2026-02-04T10:30:00",
      "status": "nouveau",
      "avis_envoye": false,
      "contient_imo": true
    }
  ],
  "total": 42,
  "pages": 5,
  "current_page": 1
}
```

---

#### Récupérer un dossier spécifique
```http
GET /api/dossiers/<id>
```

**Response:**
```json
{
  "id": 1,
  "numero": "DOS001",
  "type_conteneur": "FCL",
  "date_arrivee": "2026-02-04T10:30:00",
  "status": "nouveau",
  "avis_envoye": false,
  "contient_imo": true,
  "validé_transit": false,
  "validé_documentation": false
}
```

---

#### Créer un dossier
```http
POST /api/dossiers
Content-Type: application/json

{
  "numero": "DOS001",
  "type_conteneur": "FCL",
  "date_arrivee": "2026-02-04T10:30:00",
  "contient_imo": true,
  "contient_escale": true,
  "contient_fret": true
}
```

**Response:**
```json
{
  "message": "Dossier créé",
  "id": 1
}
```

---

#### Valider un dossier (Transit)
```http
PUT /api/dossiers/<id>/valider-transit
```

**Response:**
```json
{
  "message": "Dossier validé par Transit"
}
```

---

#### Valider un dossier (Documentation)
```http
PUT /api/dossiers/<id>/valider-doc
```

**Response:**
```json
{
  "message": "Dossier validé par Documentation"
}
```

---

### Avis d'Arrivée

#### Envoyer un avis
```http
PUT /api/avis/<id>/envoyer
```

**Response:**
```json
{
  "message": "Avis envoyé"
}
```

---

### Profil

#### Récupérer le profil utilisateur
```http
GET /api/profile
```

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "role": "Timbrage",
  "is_active": true,
  "created_at": "2026-02-04T10:00:00",
  "last_login": "2026-02-04T14:30:00"
}
```

---

## Codes de statut HTTP

| Code | Signification |
|------|---------------|
| 200 | ✓ Succès |
| 201 | ✓ Ressource créée |
| 400 | ✗ Mauvaise requête |
| 401 | ✗ Non authentifié |
| 403 | ✗ Accès refusé |
| 404 | ✗ Ressource non trouvée |
| 500 | ✗ Erreur serveur |

---

## Exemples d'utilisation

### Python (requests)
```python
import requests

BASE_URL = "http://localhost:5000/api"

# Récupérer un JWT token (après login)
response = requests.get(
    f"{BASE_URL}/profile",
    headers={"Authorization": f"Bearer {token}"}
)

print(response.json())
```

### cURL
```bash
# Récupérer la liste des dossiers
curl -H "Authorization: Bearer <TOKEN>" \
  http://localhost:5000/api/dossiers

# Créer un dossier
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"numero":"DOS001","type_conteneur":"FCL"}' \
  http://localhost:5000/api/dossiers
```

### JavaScript (fetch)
```javascript
const token = "your-jwt-token";

fetch("http://localhost:5000/api/profile", {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Modèles de données

### Dossier
```
{
  id: integer,
  numero: string (unique),
  type_conteneur: "FCL" | "LCL",
  date_arrivee: datetime,
  status: "nouveau" | "validé" | "avis_envoyé",
  contient_imo: boolean,
  avis_envoye: boolean,
  avis_a_envoyer: boolean,
  version_avis: integer,
  validé_transit: boolean,
  validé_documentation: boolean,
  contient_escale: boolean,
  contient_fret: boolean,
  created_at: datetime,
  updated_at: datetime
}
```

### AvisArrivee
```
{
  id: integer,
  dossier_id: integer,
  numero_bl: string (unique),
  contenu: text,
  statut: "brouillon" | "envoyé",
  version: integer,
  date_creation: datetime,
  date_envoi: datetime
}
```

### User
```
{
  id: integer,
  username: string (unique),
  email: string (unique),
  role: Role,
  is_active: boolean,
  created_at: datetime,
  last_login: datetime
}
```

### Role
```
{
  id: integer,
  name: "Timbrage" | "Transit" | "Documentation" | "Commercial" | "Admin",
  description: string,
  created_at: datetime
}
```

---

## Erreurs

### Réponses d'erreur

```json
{
  "message": "Description de l'erreur",
  "code": "ERROR_CODE"
}
```

### Codes d'erreur courants

- `UNAUTHORIZED` - Authentification requise
- `FORBIDDEN` - Accès refusé pour ce rôle
- `NOT_FOUND` - Ressource non trouvée
- `INVALID_REQUEST` - Données invalides
- `SERVER_ERROR` - Erreur serveur

---

## Rate Limiting

Pas de limite de débit actuellement implémentée.

## Version

API Version: **1.0.0**
