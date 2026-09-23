.PHONY: run test migrate seed
run:
	python manage.py runserver
test:
	pytest
migrate:
	python manage.py migrate
seed:
	python manage.py seed_detection_rules
