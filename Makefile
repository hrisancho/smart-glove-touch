venv:
	python3 -m venv ./venv
	source ./venv/bin/activate

req:
	pip install -r requirements.txt

sub:
	git submodule update --init --recursive --remote
	
protoc:
	python3 -m grpc_tools.protoc -I./controllerProto/ --python_out=./controllerProto ./controllerProto/*.proto
	python3 -m grpc_tools.protoc -I./grpcProto --python_out=./ --grpc_python_out=./ ./grpcProto/*.proto

run:
	python3 main.py