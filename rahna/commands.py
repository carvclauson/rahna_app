from pydantic import BaseModel, EmailStr

from rahna.dog import Dog, NotFound

class AlreadyExists(Exception):
    pass

class SaveDogCommand(BaseModel):
    name: str
    age: int
    weight: float
    parent_name: str
    phone: str
    email: EmailStr

    def execute(self) -> Dog:
        try:
            #notice the tests are called at /rahna_app and therefore ./
            #means ./rahna_app (it probably should be better than this)
            Dog.get_by_name(self.name, database_name = "./data/db_test_dog.db")
            raise AlreadyExists
        except NotFound:
            pass

        dog = Dog(
            name = self.name,
            age = self.age,
            weight = self.weight,
            parent_name = self.parent_name,
            phone = self.phone,
            email = self.email
        ).save(database_name = "./data/db_test_dog.db")

        return dog

class DeleteDogByNameCommand(BaseModel):
    name : str

    def execute(self) -> None:
        # raises exception NotFound in case dog is not found
        Dog.get_by_name(self.name, database_name = "./data/db_test_dog.db")

        Dog.delete_by_name(self.name, database_name = "./data/db_test_dog.db")

        return None
