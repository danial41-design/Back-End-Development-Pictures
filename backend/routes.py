
from . import app
import os
import json
from flask import jsonify, request

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")

with open(json_url, encoding="utf-8") as f:
    data = json.load(f)


@app.route("/health")
def health():
    return jsonify(status="OK"), 200


@app.route("/count")
def count():
    return jsonify(length=len(data)), 200


@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    return jsonify(message="picture not found"), 404


@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if any(p["id"] == picture["id"] for p in data):
        return jsonify(
            Message=f"picture with id {picture['id']} already present"
        ), 302
    data.append(picture)
    return jsonify(picture), 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    incoming = request.get_json()
    for index, picture in enumerate(data):
        if picture["id"] == id:
            incoming["id"] = id
            data[index] = incoming
            return jsonify(incoming), 200
    return jsonify(message="picture not found"), 404
    


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data.pop(index)
            return "", 204
    return jsonify(message="picture not found"), 404
