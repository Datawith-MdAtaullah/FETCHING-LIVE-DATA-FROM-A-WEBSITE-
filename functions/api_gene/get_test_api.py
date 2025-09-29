from firebase_functions.https_fn import Request, Response
import json
from firebase_admin import storage as s

# api for seaching genes in comma separated style , we can search multiple genes here
# limit 20 genes per time

my_bucket = "enigmagenomics-internship.firebasestorage.app"
file_path = "genes/new_infos_added_to_gene/"

def get_test_api(req: Request) -> Response:
    z = req.args.get("search")
    
    if not z:
        return Response(
            json.dumps({"error": "Missing ?search=Gene(s) to find"}),
            status=400,
            mimetype="application/json"
        )
    
    Total_gene = z.split(",")
    gene_list =[]
    for g in Total_gene:
        if g.strip():
            x = g.strip().upper()
            gene_list.append(x)
    
    if len(gene_list) > 20:
        return Response(
            json.dumps({"error": "Maximum 20 genes allowed per request"}),
            status=400,
            mimetype="application/json"
        )

    results = []
    b = s.bucket(my_bucket)
    for i in gene_list:
        
        try:
            o = b.blob(f"{file_path}{i}.json")
            if o.exists():
                data = o.download_as_text()
                results.append(json.loads(data))
            else:
               results.append({"error": f"Gene '{i}' not found"})
               
        except Exception as e:
            results.append({"error": str(e)})

    return Response(
        json.dumps(results, indent=2),
        status=200,
        mimetype="application/json"
    )
