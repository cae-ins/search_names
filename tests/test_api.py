import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

# Faux résultat simulé pour Elasticsearch
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
                    "nombre_femme_nom_famille": 4
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
    assert "resume" in data
    assert "noms_utilises" in data
    assert data["resume"]["nom_recherche"] == "Diallo"
    assert "partie_prenom" in data["resume"]
    assert "nombre_homme_nom_famille" in data["resume"]
