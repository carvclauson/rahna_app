import json
import pathlib
import pytest
import requests
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

@pytest.mark.parametrize(
    "data",
    [
        {
            'name' : 'Falafel',
            'age' : 3,
            'weight' : 6.5,
            'parent_name' : 'Raquel Brasileiro',
            'phone' : '+55 21 98888 7777',
            'email' : 'Raquel Br'
        },
        {
            'name' : 'Falafel',
            'age' : 3,
            'weight' : 6.5,
            'parent_name' : 'Raquel Brasileiro',
            'phone' : '+55 21 98888 7777',
        },
        {
            'name' : 'Falafel',
            'age' : 3,
            'weight' : 6.5,
            'parent_name' : None,
            'phone' : '+55 21 98888 7777',
            'email' : 'raquel@brasileiro.com'
        }
    ]
)
def test_add_dog_bad_request(client, data):

    response = client.post("/add-dog/",
        data=json.dumps(data),content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json is not None

def test_add_dog(client):

    data= {'name' : 'Falafel',
        'age' : 3,
        'weight' : 6.5,
        'parent_name' : 'Raquel Brasileiro',
        'phone' : '+55 21 98888 7777',
        'email' : 'raquel@brasileiro.com'}

    response = client.post("/add-dog/", data = json.dumps(data), content_type="application/json")
    validate_payload(response.json, "Dog.json")

def test_get_dog_by_name(client):
    dog = Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    ).save()

    response = client.get(f"/dog/{dog.name}/", content_type = "application.json")
    validate_payload(response.json, "Dog.json")

def test_list_dogs(client):
    Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    ).save()
    Dog(
        name = 'Halloumi',
        age = 5,
        weight = 8.5,
        parent_name = 'Maria Gomes',
        phone = '+55 21 98888 6666',
        email = 'maria@gomes.com'
    ).save()
    response = client.get("/list-dogs/", content_type = "application/json")
    validate_payload(response.json, "DogList.json")

@pytest.mark.e2e
def test_add_list_get(client):
    data= {'name' : 'Falafel',
        'age' : 3,
        'weight' : 6.5,
        'parent_name' : 'Raquel Brasileiro',
        'phone' : '+55 21 98888 7777',
        'email' : 'raquel@brasileiro.com'}

    requests.post(
        "http://localhost:5000/add-dog",
    json = data
    )
    response = requests.get(
        "http://localhost:5000/list-dogs/"
        )
    dogs = response.json()
    response = requests.get(
        f"http://localhost:5000/dog/{dogs[0]['name']}/"
    )
    assert response.status_code == 200
