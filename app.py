from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()

es = Elasticsearch("http://elasticsearch.elasticsearch.svc.cluster.local:9200")

@app.get("/recherche")
def recherche_nom(nom: str = Query(..., min_length=2)):
    try:
        # On fait une recherche exacte sur le nom
        query = {
            "query": {
                "term": {
                    "nom.keyword": nom  
                }
            }
        }

        result = es.search(index="noms_prenoms", query=query["query"], size=100)
        hits = [hit["_source"] for hit in result["hits"]["hits"]]

        if not hits:
            return {
                "message": f"Aucun document trouvé pour le nom exact : '{nom}'"
            }

        return {
            "resultats": hits
        }

    except Exception as e:
        return {"error": str(e)}
