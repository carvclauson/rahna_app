from rahna.dog import Dog
from rahna.queries import ListDogsQuery,GetDogByIDQuery,GetDogByNameQuery

def test_list_dogs():
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

    query = ListDogsQuery()

    assert len(query.execute()) == 2

def test_get_dog_by_id():
    dog = Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    ).save()

    query = GetDogByIDQuery(id = dog.id)

    assert query.execute().id == dog.id

def test_get_dog_by_name():
    dog = Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    ).save()

    query = GetDogByNameQuery(name = dog.name)

    assert query.execute().name == dog.name
