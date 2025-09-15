from firebase_functions import https_fn
from firebase_functions.https_fn import Request, Response
import json

@https_fn.on_request()
def my_api(req: Request) -> Response:
    name = req.args.get("name", "World")
    return Response(
        json.dumps({"message": f"Hello, {name} from Firebase API!"}),
        status=200,
        mimetype="application/json"
    )