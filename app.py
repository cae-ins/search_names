from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()

# Connexion à Elasticsearch dans Kubernetes
es = Elasticsearch("http://elasticsearch.elasticsearch.svc.cluster.local:9200")

@app.get("/recherche")
def recherche_nom(nom: str = Query(..., min_length=2)):
    query = {
        "query": {
            "term": {
                "nom.keyword": nom 
            }
        }
    }

    result = es.search(index="noms_prenoms", body=query, size=100)
    hits = [hit["_source"] for hit in result["hits"]["hits"]]

    if not hits:
        return {
            "message": f"Aucun document trouvé pour le nom : '{nom}'"
        }

    return {
        "resultats": hits
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
