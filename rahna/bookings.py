import os
import sqlite3
import uuid
from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime, timedelta
from rahna.dog import Dog

class NotFound(Exception):
    pass

class Booking(BaseModel):
    booking_id: str = Field(default_factory = lambda: str(uuid.uuid4()))
    dog: Dog
    start_date: datetime
    end_date: datetime = None
    total_days: timedelta = None
    price: float = 0.0
    booking_confirmed: str = ""
    
@classmethod
def total_days(start_date, end_date):
    # Return timedelta in days
    return timedelta(end_date - start_date)

@classmethod
def create_table(cls, database_name = "../data/bookings.db"):
    """
    Creates a table of bookings with path database_name.
    """

    conn = sqlite3.connect(database_name)

    conn.execute(
        """CREATE TABLE IF NOT EXISTS bookings (id TEXT, name TEXT, 
        parent_name: TEXT, start_date DATETIME, end_date DATETIME, 
        total_days INT, price FLOAT)"""
    )
    conn.close()
    
    
    def save(self, database_name = "../data/bookings.db")-> "Booking":
        """
        Inserts a row in a database with path database_name. Returns the Booking
        object that called the function (self).
        """

        with sqlite3.connect(os.getenv("DATABASE_NAME", database_name)) as con:
            cur = con.cursor()
            cur.execute(
                f""" INSERT INTO bookings (id, dog_id, name, parent_name, 
                start_date, end_date, total_days, price) 
                VALUES('{self.id}','{Dog.id}', {Dog.name}','{Dog.parent_name}',
                '{self.start_date}','{self.end_date}','{self.total_days}', '{self.price}')"""
            )
            con.commit()
        return self
    

    @classmethod
    def current_bookings(cls, database_name = "../data/bookings.db") -> List["Dog"]:
        """
        Lists rows in a database with path database_name. 
        Returns a list of current and future bookings.
        """

        con = sqlite3.connect(os.getenv("DATABASE_NAME", database_name))
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM bookings WHERE end_date < DATE('now')")

        records = cur.fetchall()
        bookings = [cls(**record) for record in records]
        con.close()

        return bookings
    
    @classmethod
    def get_booking_by_id(cls, booking_id: str, database_name = "../data/bookings.db"):
        """
        Selects booking with booking_id as id in a database with path database_name
        and returns it.
        """

        con = sqlite3.connect(os.getenv("DATABASE_NAME", database_name))
        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute(f"SELECT * FROM dogs WHERE id='{booking_id}'")

        record = cur.fetchone()

        if record is None:
            raise NotFound

        booking = cls(**record)
        con.close()
        return booking
    
    @classmethod
    def get_booking_by_name(cls, dog_name: str, database_name = "../data/bookings.db"):
        """
        Selects booking with dog_name as name in a database with path database_name
        and returns it.
        """

        con = sqlite3.connect(os.getenv("DATABASE_NAME", database_name))

        con.row_factory = sqlite3.Row

        cur = con.cursor()
        cur.execute(f"SELECT * FROM dogs WHERE name = '{dog_name}'")

        record = cur.fetchone()

        if record is None:
            raise NotFound

        booking = cls(**record)
        con.close()
        return booking

    @classmethod
    def delete_booking_by_name(cls, dog_name: str, database_name = "../data/bookings.db"):
        """
        Deletes bookingg with dog_name as name from the database with path database_name
        and returns it.
        """

        con = sqlite3.connect(os.getenv("DATABASE_NAME", database_name))

        cur = con.cursor()
        cur.execute(f"""
                    DELETE
                    FROM bookings
                    WHERE name = '{dog_name}'
                    """)

        con.commit()

        return None