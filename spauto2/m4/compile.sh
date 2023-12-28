#!/bin/bash
# Compiles the protobuf definition and generates two Python files
#  1. gnmi_pb2.py: generated request and response classes
#  2. gnmi_pb2_grpc.py: generated client and server classes

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. gnmi.proto
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. gnmi_ext.proto
