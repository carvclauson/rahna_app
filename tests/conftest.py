import os
import tempfile

import pytest

from rahna.dog import Dog

@pytest.fixture(autouse=True)
def database():
    #'before test' block
    _,file_name = tempfile.mkstemp()
    os.environ["DATABASE_NAME"] = file_name #creates environment variable
    Dog.create_table(database_name = file_name)
    yield
    #'after test' block
    os.unlink(file_name)
