VENV_PATH := $(abspath .venv)
VENV := ${VENV_PATH}/bin/activate
PYTHONPATH := $(abspath .)

make-venv:
	python3 -m venv ${VENV_PATH}
	source ${VENV} && pip3 install -r requirements.txt


extract-data:
	source ${VENV} && PYTHONPATH=${PYTHONPATH} python3 ./bot/data/extract.py


train:


evaluate:


