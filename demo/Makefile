PYTHON_EXEC := python3.10
VENV_DIR := venv
VENV_EXEC_DIR := bin

setup:
	${PYTHON_EXEC} -m venv ${VENV_DIR}
	${VENV_DIR}/${VENV_EXEC_DIR}/${PYTHON_EXEC} -m pip install --upgrade pip
	${VENV_DIR}/${VENV_EXEC_DIR}/pip install requests httpx websockets pyyaml pyjwt accelbyte-py-sdk

run:
	@test -n "$(GRPC_SERVER_URL)" || (echo "GRPC_SERVER_URL is not set"; exit 1)
	${VENV_DIR}/${VENV_EXEC_DIR}/${PYTHON_EXEC} demo.py ${GRPC_SERVER_URL} rotation
