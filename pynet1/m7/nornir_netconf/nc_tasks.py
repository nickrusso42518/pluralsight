#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Collection of Nornir-oriented tasks that wrap existing
ncclient methods. These mimic the look and feel of Netmiko/NAPALM
tasks (in the main Nornir repository) for consistency.
"""


from nornir.core.task import Result
from lxml.etree import fromstring


def netconf_get_config(task, source="running", **kwargs):
    """
    Nornir task to issue a NETCONF get_config RPC with optional keyword
    arguments. The source argument uses "running" by default.
    """

    conn = task.host.get_connection("netconf", task.nornir.config)
    result = conn.get_config(source=source, **kwargs)
    return Result(host=task.host, result=result)


def netconf_edit_config(task, target, config, **kwargs):
    """
    Nornir task to issue a NETCONF edit_config RPC with optional keyword
    arguments. Both the target and config arguments must be specified.
    """

    conn = task.host.get_connection("netconf", task.nornir.config)
    result = conn.edit_config(target=target, config=config, **kwargs)
    return Result(host=task.host, result=result)


def netconf_commit(task, **kwargs):
    """
    Nornir task to issue a NETCONF commit RPC with optional keyword
    arguments. On most platforms, this copies the candidate config
    to the running config.
    """

    conn = task.host.get_connection("netconf", task.nornir.config)
    result = conn.commit(**kwargs)
    return Result(host=task.host, result=result)


def netconf_custom_rpc(task, rpc_text, **kwargs):
    """
    Nornir task to issue a custom NETCONF RPC given an XML-formatted string
    and additional keyword arguments.
    """

    conn = task.host.get_connection("netconf", task.nornir.config)
    result = conn.dispatch(fromstring(rpc_text.strip()), **kwargs)
    return Result(host=task.host, result=result)
