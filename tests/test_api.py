import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app import app

client = TestClient(app)

# Réponse simulée 
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

fake_mapping = {
    "noms_prenoms": {
        "mappings": {
            "properties": {
                "nom": {
                    "type": "keyword"
                }
            }
        }
    }
}


@patch("app.get_es_client")
def test_recherche_nom(mock_get_es):
    # Création du mock client Elasticsearch
    mock_es = MagicMock()
    mock_es.search.return_value = fake_es_response
    mock_es.indices.get_mapping.return_value = fake_mapping
    mock_get_es.return_value = mock_es

    # Appel de l'API avec le client simulé
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
