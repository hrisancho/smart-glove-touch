venv:
	python3 -m venv ./venv
	source ./venv/bin/activate

req:
	pip install -r requirements.txt

sub:
	git submodule update --init --recursive --remote
	
protoc:
	protoc --proto_path=./proto --python_out=./pythonProto ./proto/*.proto

run:
	uvicorn main:app