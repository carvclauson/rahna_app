import pytest

from rahna.dog import Dog, NotFound
from rahna.commands import AddDogCommand, AlreadyExists, DeleteDogByNameCommand

def test_add_dog():

    cmd = AddDogCommand(
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


def test_delete_dog_by_name():
    Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'

    ).save()

    cmd = DeleteDogByNameCommand(name = 'Falafel')
    cmd.execute()
    with pytest.raises(NotFound):
        Dog.get_by_name('Falafel')


def test_add_dog_already_exists():

    dog = Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    ).save()

    cmd = AddDogCommand(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'
    )
    with pytest.raises(AlreadyExists):
        cmd.execute()

def test_delete_dog_by_name_not_found():
    Dog(
        name = 'Falafel',
        age = 3,
        weight = 6.5,
        parent_name = 'Raquel Brasileiro',
        phone = '+55 21 98888 7777',
        email = 'raquel@brasileiro.com'

    ).save()

    cmd = DeleteDogByNameCommand(name = 'Halloumi')
    with pytest.raises(NotFound):
        cmd.execute()
