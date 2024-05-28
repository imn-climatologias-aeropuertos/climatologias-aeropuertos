STATION=mrlb

SOURCE_FILES=$(shell find . -path "./clima/*.py")
TEST_FILES=$(shell find . -path "./test/*.py")
SOURCES_FOLDER=clima
TESTS_FOLDER=test

BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

check_no_main:
ifeq ($(BRANCH),main)
	echo "You are good to go!"
else
	$(error You are not in the main branch)
endif

patch: check_no_main
	bumpversion patch --verbose
	git push --follow-tags

minor: check_no_main
	bumpversion minor --verbose
	git push --follow-tags

major: check_no_main
	bumpversion major --verbose
	git push --follow-tags

style:
	isort $(SOURCES_FOLDER)
	isort $(TESTS_FOLDER)
	black $(SOURCE_FILES)
	black $(TEST_FILES)

lint:
	isort $(SOURCES_FOLDER) --check-only
	isort $(TESTS_FOLDER) --check-only
	black $(SOURCE_FILES) --check
	black $(TEST_FILES) --check

tests:
	PYTHONPATH=. $(POETRY_RUN) pytest -vv test

run:
	# python -m clima $(STATION) resume-table
	# python -m clima $(STATION) wind-direction
	# python -m clima $(STATION) wind-speed
	python -m clima $(STATION) wind-gust
	python -m clima $(STATION) temperature
	# python -m clima $(STATION) dewpoint
	# python -m clima $(STATION) pressure
	# python -m clima $(STATION) visibility
	# python -m clima $(STATION) weather
	# python -m clima $(STATION) ceiling