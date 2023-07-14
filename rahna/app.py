from flask import Flask, jsonify, request

from rahna.commands import AddDogCommand

app = Flask(__name__)

@app.route("/add-dog/", methods=["POST"])
def add_dog():
    cmd = AddDogCommand(
        **request.json
    )
    return jsonify(cmd.execute().dict())

if __name__ == "__main__":
    app.run()
