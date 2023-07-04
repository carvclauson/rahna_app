import pytest

from rahna.dog import Dog
from rahna.commands import SaveDogCommand, AlreadyExists

def test_save_dog():

    cmd = SaveDogCommand(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    )

    dog = cmd.execute()

    db_dog = Dog.get_by_id(dog.id)
    assert db_dog.name == dog.name
    assert db_dog.age == dog.age
    assert db_dog.weight == dog.weight
    assert db_dog.parent_name == dog.parent_name
    assert db_dog.phone == dog.phone
    assert db_dog.email == dog.email



def test_save_dog_already_exists():

    dog = Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    ).save()

    cmd = SaveDogCommand(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    )
    with pytest.raises(AlreadyExists):
        cmd.execute()
