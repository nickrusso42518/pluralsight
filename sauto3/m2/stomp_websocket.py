#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Create a child WebSocketApp that is specific to PxGrid using
STOMP to subscribe to a topic, printing each message as it arrives.
"""

import time
import websocket


class StompWebsocket(websocket.WebSocketApp):
    """
    Extends WebSocketApp to add STOMP-specific functionality for PxGrid.
    """

    def __init__(self, ws_url, header, sslopt):
        """
        Creates a new websocket with a given URL, header dictionary, and
        SSL options.
        """

        # Low-level debugging can be helpful for development, but sloppy
        # websocket.enableTrace(True)

        # Call the base class constructor to handle the heavy lifting
        super().__init__(
            ws_url,
            on_message=StompWebsocket._on_message,
            on_close=StompWebsocket._on_close,
            on_open=StompWebsocket._on_open,
            header=header,
        )

        # Store the SSL options for use when starting the websocket app
        self.sslopt = sslopt

    def start(self, pub_node, topic):
        """
        Runs the websocket app forever using the services on a given PxGrid
        publisher node and subscribing to a given topic.
        """
        self.pub_node = pub_node
        self.topic = topic
        self.run_forever(sslopt=self.sslopt)

    def _send_stomp_command(self, command, headers):
        """
        Internal method to issue a STOMP command, such as CONNECT
        or SUBSCRIBE, with the appropriate headers. Some STOMP commands
        have body content as well, but for simplicity, this method
        does not support STOMP body content.
        """

        # The command text goes first, followed by a newline
        text = f"{command}\n"

        # Print headers in "key:value" format on separate lines
        for key, value in headers.items():
            text += f"{key}:{value}\n"

        # Add newline and null terminator to signify end of command
        text += "\n\0"

        # Print status message so we can see the STOMP exchanges
        # preceded by >>
        print(f">> {text}")

        # Very important to set BINARY mode with UTF-8 (buried in pxGrid docs)
        self.send(text.encode("utf-8"), opcode=websocket.ABNF.OPCODE_BINARY)
        time.sleep(1)

    @staticmethod
    def _on_message(ws, message):
        """
        Print all received messages preceded by <<
        """
        print(f"<< {message.decode('utf-8')}")

    @staticmethod
    def _on_close(ws):
        """
        Notify user that websocket is closed
        """
        print("** WEBSOCKET CLOSED")

    @staticmethod
    def _on_open(ws):
        """
        Notify user that websocket is open, then issue the appropriate STOMP
        CONNECT and SUBSCRIBE commands. See STOMP spec for details:
        https://stomp.github.io/stomp-specification-1.2.html
        """
        print("** WEBSOCKET OPEN")

        # Send the CONNECT command with the proper version and pub node
        connect_headers = {"accept-version": "1.2", "host": ws.pub_node}
        ws._send_stomp_command("CONNECT", connect_headers)

        # Secnd the SUBSCRIBE command with the topic and conversation ID
        subscribe_headers = {"destination": ws.topic, "id": "0"}
        ws._send_stomp_command("SUBSCRIBE", subscribe_headers)
