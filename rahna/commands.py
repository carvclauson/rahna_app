from pydantic import BaseModel, EmailStr

from rahna.dog import Dog, NotFound

class AlreadyExists(Exception):
    pass

class AddDogCommand(BaseModel):
    name: str
    age: int
    weight: float
    parent_name: str
    phone: str
    email: EmailStr

    def execute(self, test_ext = False) -> Dog:

        db_name = "../data/test_dog.db" if test_ext else "../data/dog.db"
        try:
            Dog.get_by_name(self.name, database_name = db_name)
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
        ).save(database_name = db_name)

        return dog

class DeleteDogByNameCommand(BaseModel):
    name : str

    def execute(self, test_ext = False) -> None:
        db_name = "../data/test_dog.db" if test_ext else "../data/dog.db"

        # raises exception NotFound in case dog is not found
        Dog.get_by_name(self.name, database_name = db_name)

        Dog.delete_by_name(self.name, database_name = db_name)

        return None
