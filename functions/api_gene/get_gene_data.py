
from firebase_functions.https_fn import Request, Response
import json
from firebase_admin import storage as s

my_bucket = 'enigmagenomics-internship.firebasestorage.app'
file_path = 'genes/new_infos_added_to_gene/'

# this is the api for getting gene data of single file from my bucket       
def get_gene_api(req:Request) -> Response:
    z = req.args.get('search')
    
    if z:
        try:
            b = s.bucket(my_bucket)
            o = b.blob(f'{file_path}{z.upper()}.json')
            
            if o.exists():
                 data = o.download_as_text()
                    
                 return Response(
                        data,
                        status=200,
                        mimetype='application/json'
                    )
            else:
                return Response(
                    json.dumps({"error": f"Gene '{z}' not found"}),
                    status=404,
                    mimetype='application/json'
                )
        except Exception as e:
            return Response(
                json.dumps({'error':str(e)}),
                status=500,
                mimetype='application/json'
            )
    else:
        return Response(
            json.dumps({'error':'Missing ?search=Gene that you want to find'}),
            status=400,
            mimetype='application/json'
        )