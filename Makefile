run:
	python3 main.py

update:
	pip3 freeze > requirements.txt

test:
	python3 -m unittest discover -s tests