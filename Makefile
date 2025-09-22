VENV_PATH := $(abspath .venv)
VENV := ${VENV_PATH}/bin/activate
PYTHONPATH := $(abspath .)

include .env

make-venv:
	python3 -m venv ${VENV_PATH}
	source ${VENV} && pip3 install -r requirements.txt -r requirements.dev.txt

check-code:
	source ${VENV} && \
	ruff check && \
	ruff format --check && \
	isort --check-only .


format-code:
	source ${VENV} && \
	ruff check --fix && \
	ruff format && \
	isort .


extract-data:
	source ${VENV} && PYTHONPATH=${PYTHONPATH} python3 ./bot/data/extract.py \
	--telegram-data ${TG_DATA_PATH} \
	--telegram-user-id ${TG_USER_ID} \
	--output-file ${OUTPUT_FILE}


train:


evaluate:


