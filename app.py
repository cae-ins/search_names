from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from collections import defaultdict

app = FastAPI()
#es = Elasticsearch("http://192.168.1.230:30920")
es = Elasticsearch("http://elasticsearch.elasticsearch.svc.cluster.local:9200")

@app.get("/recherche")
def recherche_nom(nom: str = Query(..., min_length=2)):
    prefix_letter = nom[0].lower()

    query = {
        "query": {
            "match": {
                "nom": {
                    "query": nom,
                    "fuzziness": 2
                }
            }
        }
    }

    result = es.search(index="noms_prenoms", body=query, size=1000)
    hits = [hit["_source"] for hit in result["hits"]["hits"]]

    filtered_hits = [
        doc for doc in hits if doc["nom"].lower().startswith(prefix_letter)
    ]

    if not filtered_hits:
        return {
            "message": f"Aucun nom correspondant trouvé pour : '{nom}'"
        }

    # Agrégation manuelle des valeurs numériques
    numeric_fields = [
        "partie_prenom", "nom_famille", "prenom_unique",
        "nombre_homme_prenom", "nombre_homme_nom_famille",
        "nombre_femme_prenom", "nombre_femme_nom_famille"
    ]

    aggregated = defaultdict(int)
    noms_distincts = set()

    for doc in filtered_hits:
        noms_distincts.add(doc["nom"])
        for field in numeric_fields:
            aggregated[field] += int(doc.get(field, 0))

    doc_final = {
        "nom_recherche": nom,
        **aggregated
    }

    return {
        "resume": doc_final,
        "noms_utilises": sorted(noms_distincts)
    }

'''
from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()

#es = Elasticsearch("http://192.168.1.230:30920")
es = Elasticsearch("http://elasticsearch.elasticsearch.svc.cluster.local:9200")


@app.get("/recherche")
def recherche_nom(nom: str = Query(..., min_length=2)):
    query = {
        "query": {
            "match": {
                "nom": {
                    "query": nom,
                    "fuzziness": 2
                }
            }
        }
    }

    result = es.search(index="noms_prenoms", body=query)
    hits = [hit["_source"] for hit in result["hits"]["hits"]]
    return {"resultats": hits}
'''
