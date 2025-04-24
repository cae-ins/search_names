import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

# Réponse simulée (nouvelle structure des documents Elasticsearch)
fake_es_response = {
    "hits": {
        "hits": [
            {
                "_source": {
                    "nom": "Diallo",
                    "partie_prenom": 5,
                    "nom_famille": 3,
                    "prenom_unique": 2,
                    "nombre_homme_prenom": 10,
                    "nombre_homme_nom_famille": 7,
                    "nombre_femme_prenom": 8,
                    "nombre_femme_nom_famille": 4,
                    "frequences": {
                        "annee_1950": 0.0,
                        "annee_1951": 1.0,
                        "annee_1952": 0.0
                    }
                }
            }
        ]
    }
}


@patch("app.es.search", return_value=fake_es_response)
def test_recherche_nom(mock_es):
    response = client.get("/recherche?nom=Diallo")
    assert response.status_code == 200

    data = response.json()
    assert "resultats" in data
    assert isinstance(data["resultats"], list)
    assert len(data["resultats"]) == 1

    doc = data["resultats"][0]
    assert doc["nom"] == "Diallo"
    assert doc["partie_prenom"] == 5
    assert doc["nombre_femme_nom_famille"] == 4

    assert "frequences" in doc
    assert isinstance(doc["frequences"], dict)
    assert "annee_1951" in doc["frequences"]
    assert doc["frequences"]["annee_1951"] == 1.0
