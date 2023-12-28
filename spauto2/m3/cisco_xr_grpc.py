#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Define a simple Cisco IOS-XR gRPC interface using OOP.
"""

from enum import IntEnum
import json
import grpc
import xr_pb2
import xr_pb2_grpc

class Encode(IntEnum):
    """
    Enumerated encoding types for streaming telemetry.
    This isn't well documented today ...
    """
    TEST = 1
    GPB = 2
    KVGPB = 3
    JSON = 4

class CiscoXRgRPC:
    """
    Define a simple Cisco IOS-XR gRPC interface using OOP.
    """

    def __init__(self, host, port, username, password):
        """
        Create a new object with the specific hostname/IP, gRPC port,
        username, and password.
        """
        self.creds = [("username", username), ("password", password)]
        self.host = host
        self.port = port

    def __enter__(self):
        """
        Establish a gRPC connection to the device and instantiate the
        stub object from which RPCs can be issued.
        """
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.stub = xr_pb2_grpc.gRPCConfigOperStub(self.channel)
        return self

    def __exit__(self, type, value, traceback):
        """
        Gracefully close the gRPC connection.
        """
        self.channel.close()

    def get_config(self, yangpathjson_dict):
        """
        Issue a GetConfig RPC and transform result into a list of
        ConfigGetReply objects for each consumption.
        """
        responses = self.stub.GetConfig(
            xr_pb2.ConfigGetArgs(yangpathjson=json.dumps(yangpathjson_dict)),
            metadata=self.creds,
        )
        return [json.loads(resp.yangjson) for resp in responses if resp.yangjson]

    def merge_config(self, yangjson_dict):
        """
        Issue a MergeConfig RPC based on the YANG data supplied.
        """
        config_args = xr_pb2.ConfigArgs(yangjson=json.dumps(yangjson_dict))
        response = self.stub.MergeConfig(config_args, metadata=self.creds)
        return response

    def create_subs(self, sub_id, encode):
        """
        Subscribe to a telemetry topic using a specific encoding
        (see Encode class for options) and unique subscription ID.
        Returns a generator object which is built as messages arrive.
        """
        sub_args = xr_pb2.CreateSubsArgs(ReqId=1, encode=encode, subidstr=sub_id)
        stream = self.stub.CreateSubs(sub_args, metadata=self.creds)
        for segment in stream:
            yield segment
