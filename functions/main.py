from firebase_functions import https_fn , pubsub_fn 
from firebase_admin import initialize_app
from scraping.medlineplus import crawling_function
import json
from firebase_functions.https_fn import Request, Response
from api_gene.get_gene_data import get_gene_api
from api_gene.get_test_api import get_test_api

initialize_app()

#function to crawl data and save it into firebase bucket
@https_fn.on_request(timeout_sec=360) 
def crawling_genes_updated(req:Request) -> Response: 
    
    total_genes, msg = crawling_function() 
    return Response( 
        json.dumps({"status": "success", "Total_genes": total_genes, "message": msg}), 
        mimetype="application/json" 
    ) 
    
# applying schedular to run automatically per week 
@pubsub_fn.on_message_published(topic="weekly-crawl-genes_updated", timeout_sec=540) 
def scheduled_weekly_run_updated(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None: 
        
    print("Crawling Started...")
    total_genes, msg = crawling_function() 
    print(f"Crawling Finished...& Scheduled completed, total genes: {total_genes}") 
   
    
# API for single searching genes     
@https_fn.on_request()
def gene_api(req:Request) -> Response:
    return get_gene_api(req)

# API FOR multiple searching genes
@https_fn.on_request()
def test_api(req:Request) -> Response:
    return get_test_api(req)