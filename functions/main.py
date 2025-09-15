from firebase_functions import https_fn , pubsub_fn
from firebase_admin import initialize_app
from scraping.medlineplus import scrape_and_save
import json
from firebase_functions.https_fn import Request, Response
from api_gene.get_gene_data import get_gene_data_logic
from api_gene.get_gene_data import api_logic

initialize_app()

@https_fn.on_request(timeout_sec=360) 
def crawling_genes(req: https_fn.Request) -> https_fn.Response: 
    total_genes, msg = scrape_and_save() 
    return https_fn.Response( 
        json.dumps({"status": "success", "Total_genes": total_genes, "message": msg}), 
        mimetype="application/json" 
    ) 
 
@pubsub_fn.on_message_published(topic="weekly-crawl-genes", timeout_sec=540) 
def scheduled_genes_files(event: pubsub_fn.CloudEvent[pubsub_fn.MessagePublishedData]) -> None: 
    total_genes, msg = scrape_and_save() 
    print(f"Scheduled completed, total genes: {total_genes}") 
    
    
@https_fn.on_request()
def api(req:Request) -> Response:
    return get_gene_data_logic(req)



   
@https_fn.on_request()
def api2(req:Request) -> Response:
    return api_logic(req)