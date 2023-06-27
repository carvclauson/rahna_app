import os
import sqlite3
import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import List

class NotFound(Exception):
    pass

class Dog(BaseModel):
    # Pydantic performs the parsing of the attributes and validation
    id: str = Field(default_factory = lambda: str(uuid.uuid4()))
    name: str = ""
    age: int = 0
    weight: float = 0.0
    parent_name: str = ""
    phone: str = ""
    email: EmailStr  = "noemail@domain.com"


    @classmethod
    def create_table(cls, database_name = "../data/dog.db"):
        """
        Creates a table of dogs with path database_name.
        """

        conn = sqlite3.connect(database_name)

        conn.execute(
            """CREATE TABLE IF NOT EXISTS dogs (id TEXT, name TEXT, age INTEGER,
            weight REAL, parent_name TEXT, phone TEXT , email TEXT)"""
        )
        conn.close()


    def save(self, database_name = "../data/dog.db")-> "Dog":
        """
        Inserts a row in a database with path database_name. Returns the Dog
        object that called the function (self).
        """

        #more general case where we have a environment virable "DATABASE_NAME"
        #with sqlite3.connect(os.getenv("DATABASE_NAME", "../data/dog.db"))
        # as con:
        with sqlite3.connect(database_name) as con:
            cur = con.cursor()
            cur.execute(
                f""" INSERT INTO dogs (id, name, age, weight, parent_name,
                phone, email) VALUES('{self.id}','{self.name}','{self.age}',
                '{self.weight}','{self.parent_name}','{self.phone}',
                '{self.email}')"""
            )
            con.commit()
        return self


    @classmethod
    def list_dogs(cls, database_name = "../data/dog.db") -> List["Dog"]:
        """
        Lists rows in a database with path database_name. Returns a list with
        Dog objects.
        """

        #more general case where we have a environment virable "DATABASE_NAME"
        #con = sqlite3.connect(os.getenv("DATABASE_NAME", "../data/dog.db"))
        con = sqlite3.connect(database_name)
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM dogs")

        records = cur.fetchall()
        articles = [cls(**record) for record in records]
        con.close()

        return articles


    @classmethod
    def get_by_id(cls, dog_id: str, database_name = "../data/dog.db"):
        """
        Selects Dog with dog_id as id in a database with path database_name
        and returns it.
        """

        #more general case where we have a environment virable "DATABASE_NAME"
        #con = sqlite3.connect(os.getenv("DATABASE_NAME", "../data/dog.db"))
        con = sqlite3.connect(database_name)
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute(f"SELECT * FROM dogs WHERE id='{dog_id}'")

        record = cur.fetchone()

        if record is None:
            raise NotFound

        dog = cls(**record)
        con.close()
        return dog


    @classmethod
    def get_by_name(cls, dog_name: str, database_name = "../data/dog.db"):
        """
        Selects Dog with dog_name as name in a database with path database_name
        and returns it.
        """

        #more general case where we have a environment virable "DATABASE_NAME"
        #con = sqlite3.connect(os.getenv("DATABASE_NAME", "../data/dog.db"))
        con = sqlite3.connect(database_name)
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute(f"SELECT * FROM dogs WHERE name = '{dog_name}'")

        record = cur.fetchone()

        if record is None:
            raise NotFound

        dog = cls(**record)
        con.close()
        return dog
