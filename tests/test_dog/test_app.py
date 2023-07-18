import json
import pathlib
import pytest
from jsonschema import validate, RefResolver

from rahna.app import app
from rahna.dog import Dog

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def validate_payload(payload, schema_name):
    """
    Validate payload with selected schema
    """
    schemas_dir = str(
        f"{pathlib.Path(__file__).parent.absolute()}/schemas"
    )
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            "file://"+str(pathlib.Path(f"{schemas_dir}/{schema_name}").absolute()),
            schema
        )
    )

def test_add_dog(client):

    data= {'name' : 'Falafel',
        'age' : 3,
        'weight' : 6.5,
        'parent_name' : 'Raquel Brasileiro',
        'phone' : '+55 21 98888 7777',
        'email' : 'raquel@brasileiro.com'}

    response = client.post("/add-dog/", data = json.dumps(data), content_type="application/json")
    validate_payload(response.json, "Dog.json")
