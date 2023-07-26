########################## PACKAGE ACTIONS #####################
reinstall_package:
	@pip install --upgrade pip
	@pip uninstall -y rahna || : # -y flag avoids asking for confirmation
	@pip install -e .

create_database:
	python -c 'from rahna.dog import Dog; Dog.create_table("./data/dog.db")'

########################## TESTS #####################
tests_commands:
	@pytest tests/test_dog/test_commands.py

tests_queries:
	@pytest tests/test_dog/test_queries.py

test_all: tests_commands tests_queries

########################## CLEAN #####################
clean:
	rm -rf __pycache__
