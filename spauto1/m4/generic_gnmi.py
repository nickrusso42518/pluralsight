#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Define a simple and generic gNMI interface using OOP.
"""

from enum import IntEnum
import json
import grpc
import gnmi_pb2
import gnmi_pb2_grpc


class Encoding(IntEnum):
    """
    Enumerated encoding types for streaming telemetry.
    BYTES_VAL and ASCII_VAL are not supported on IOS-XR today.
    """

    JSON = 0
    BYTES = 1
    PROTO = 2
    ASCII = 3
    JSON_IETF = 4


class SubscriptionMode(IntEnum):
    """
    Enumerated telemetry subscription modes.
    """

    TARGET_DEFINED = 0
    ON_CHANGE = 1
    SAMPLE = 2


class TelemetryMode(IntEnum):
    """
    Enumerated telemetry modes applying to entire session.
    """

    STREAM = 0
    ONCE = 1
    POLL = 2


class DataType(IntEnum):
    """
    Enumerated data types for "Get" RPCs.
    """

    ALL = 0
    CONFIG = 1
    STATE = 2
    OPERATIONAL = 3


class GenericgNMI:
    """
    Define a simple generic gNMI interface using OOP.
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
        self.stub = gnmi_pb2_grpc.gNMIStub(self.channel)
        return self

    def __exit__(self, type, value, traceback):
        """
        Gracefully close the gRPC connection.
        """
        self.channel.close()

    @staticmethod
    def _make_path(path_str):
        """
        Given a resource path (ie /some:input/data/path), transform the string
        into a gNMI Path object, consisting of a list of PathElem objects.
        """

        # Use list comprehension to iterate over /-split path elements,
        # creating a new PathElem for each one
        elem_list = [gnmi_pb2.PathElem(name=p) for p in path_str.split("/")]

        # Create a Path and assign list of PathElems, then return it
        path = gnmi_pb2.Path(elem=elem_list)
        return path

    def get(self, path_str, encoding=Encoding.JSON_IETF, type=DataType.ALL):
        """
        Assemble a GetRequest consisting of a Path (which has PathElements
        mapped to each hierarchical YANG container in the path_str) to pass
        into the Get RPC. Return the response data.
        """

        # Generate the Path object
        path = self._make_path(path_str)

        # Generate the GetRequest object using the Path
        get_req = gnmi_pb2.GetRequest(path=[path], encoding=encoding, type=type)

        # Issue the Get RPC and return the response
        response = self.stub.Get(get_req, metadata=self.creds)
        return response

    def set_update(self, path_str, json_data):
        """
        Assemble a SetRequest consisting of an Update, which contains a
        Path and TypedValue to pass into the Get RPC. Return the response data.
        """

        # Generate the Path object
        path = self._make_path(path_str)

        # Convert the input data to a UTF-8 encoded byte object
        json_ietf = bytes(json.dumps(json_data), encoding="utf-8")

        # Assemble payload dictionary; the dict key is the type
        val = {"json_ietf_val": json_ietf}

        # Create the Update object using the Path and value to add
        update = gnmi_pb2.Update(path=path, val=val)

        # Create the SeqRequest object using the Update
        set_req = gnmi_pb2.SetRequest(update=[update])

        # Issue the Set RPC and return the response
        response = self.stub.Set(set_req, metadata=self.creds)
        return response

    def subscribe(
        self,
        path_str,
        encoding=Encoding.JSON_IETF,
        telmode=TelemetryMode.STREAM,
        submode=SubscriptionMode.SAMPLE,
        interval_ns=3000000000,
    ):
        """
        Subscribe to a telemetry topic using a specific encoding
        (see Encoding class for options) and YANG path string.
        Returns a generator object which is built as messages arrive.
        """
        # Generate the Path object
        path = self._make_path(path_str)

        # Generate the Subscription object (what we want and how often)
        sub = gnmi_pb2.Subscription(
            path=path,
            mode=submode,
            sample_interval=interval_ns,
            suppress_redundant=False,
        )

        # Generate the SubscriptionList (encoding and update frequency)
        sub_list = gnmi_pb2.SubscriptionList(
            subscription=[sub],
            mode=telmode,
            encoding=encoding,
            updates_only=False,
        )

        # Generate the SubscribeRequest containing the sub_list
        sub_req = gnmi_pb2.SubscribeRequest(subscribe=sub_list)

        # Subscribe() expects a next()-able iterable object containing
        # SubscribeRequest objects (iterator/generator). Can't use a list.
        sub_req_iter = iter([sub_req])

        # Send the Subscribe RPC with the input iterator, then stream results
        stream = self.stub.Subscribe(sub_req_iter, metadata=self.creds)
        for segment in stream:
            yield segment
