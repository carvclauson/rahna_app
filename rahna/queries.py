from pydantic import BaseModel
from typing import List
from rahna.dog import Dog


class ListDogsQuery(BaseModel):

    def execute(self, test_ext = False) ->List[Dog]:
        db_name = "../data/test_dog.db" if test_ext else "../data/dog.db"
        dogs = Dog.list_dogs(database_name = db_name)

        return dogs

class GetDogByIDQuery(BaseModel):
    id: str

    def execute(self, test_ext = False) -> Dog:
        db_name = "../data/test_dog.db" if test_ext else "../data/dog.db"
        dog = Dog.get_by_id(self.id, database_name = db_name)

        return dog

class GetDogByNameQuery(BaseModel):
    name: str

    def execute(self, test_ext = False) -> Dog:
        db_name = "../data/test_dog.db" if test_ext else "../data/dog.db"
        dog = Dog.get_by_name(self.name, database_name = db_name)

        return dog
