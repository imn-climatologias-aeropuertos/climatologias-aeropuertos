STATION=mroc

SOURCE_FILES=$(shell find . -path "./clima/*.py")
TEST_FILES=$(shell find . -path "./test/*.py")
SOURCES_FOLDER=clima
TESTS_FOLDER=test

CLIMA=python -m clima
ADD_SUPTITLE=false

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

check_if_add_suptitle:
ifeq ($(ADD_SUPTITLE),true)
	@echo Adding SUPTITLE to visualizations
CLIMA_RUN:=$(CLIMA) --add-suptitle
else
	@echo SUPTITLE no will be added to visualizations
CLIMA_RUN:=$(CLIMA)
endif

run-all: check_if_add_suptitle resume-table wind-dir wind-spd wind-gust temp dewpt press vis weather ceiling

resume-table: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) resume-table

wind-dir: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) wind-direction

wind-spd: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) wind-speed

wind-gust: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) wind-gust

temp: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) temperature

dewpt: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) dewpoint

press: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) pressure

vis: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) visibility

weather: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) weather

ceiling: check_if_add_suptitle
	$(CLIMA_RUN) $(STATION) ceiling