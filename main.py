import flask 
from flask import request, jsonify
from flask_cors import CORS

from translate import Translator
from database import Database

app = flask.Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

db = Database()
tr = Translator(to_lang="zh")

@app.route("/api/translate", methods=["GET"])
def translate():
    text = request.args.get("text")
    translation = tr.translate(text)
    return translation

@app.route("/api/add_character", methods=["POST"])
def add_character():
    character = request.json["character"]
    base64_image = request.json["image"]
    db.AddCharacter(character, base64_image)
    return jsonify({"success": True})

@app.route("/api/get_character", methods=["GET"])
def get_character():
    character = request.args.get("character")
    image = db.GetCharacter(character)
    return jsonify({"image": image})

@app.route("/api/get_all_characters", methods=["GET"])
def get_all_characters():
    characters = db.GetAllCharacters()
    return jsonify({"characters": characters})

if __name__ == "__main__":
    app.run(port=5000)


