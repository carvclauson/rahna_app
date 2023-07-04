from pydantic import BaseModel
from typing import List
from rahna.dog import Dog


class ListDogsQuery(BaseModel):

    def execute(self) ->List[Dog]:
        dogs = Dog.list_dogs()

        return dogs

class GetDogByIDQuery(BaseModel):
    id: str

    def execute(self) -> Dog:
        dog = Dog.get_by_id(self.id)

        return dog
