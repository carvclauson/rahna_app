from flask import Flask, jsonify, request
from pydantic import ValidationError

from rahna.commands import AddDogCommand
from rahna.queries import GetDogByNameQuery

app = Flask(__name__)

@app.errorhandler(ValidationError)
def handle_validation_exception(error):
    response = jsonify(error.errors())
    response.status_code = 400
    return response

@app.route("/add-dog/", methods=["POST"])
def add_dog():
    cmd = AddDogCommand(
        **request.json
    )
    return jsonify(cmd.execute().dict())

@app.route("/dog/<dog_name>/", methods=["GET"])
def get_dog(dog_name):
    query = GetDogByNameQuery(name = dog_name)
    return jsonify(query.execute().dict())

if __name__ == "__main__":
    app.run()
