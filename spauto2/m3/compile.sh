#!/bin/bash
# Compiles the protobuf definition and generates two Python files
#  1. xr_pb2.py: generated request and response classes
#  2. xr_pb2_grpc.py: generated client and server classes

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. xr.proto
