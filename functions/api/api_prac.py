from flask import Flask , jsonify , request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    name = request.args.get("name", "World")
    return jsonify({"message": f"Hello, {name} from Flask API!"})