STATION=mroc

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

run-all: resume-table wind-dir wind-spd wind-gust temp dewpt press vis weather ceiling

resume-table:
	python -m clima $(STATION) resume-table

wind-dir:
	python -m clima $(STATION) wind-direction

wind-spd:
	python -m clima $(STATION) wind-speed

wind-gust:
	python -m clima $(STATION) wind-gust

temp:
	python -m clima $(STATION) temperature

dewpt:
	python -m clima $(STATION) dewpoint

press:
	python -m clima $(STATION) pressure

vis:
	python -m clima $(STATION) visibility

weather:
	python -m clima $(STATION) weather

ceiling:
	python -m clima $(STATION) ceiling