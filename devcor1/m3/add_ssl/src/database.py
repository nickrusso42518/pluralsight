#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A simple Flask web app that demonstrates the Model View Controller
(MVC) pattern in a meaningful and somewhat realistic way.
"""

import json
import time
from sqlalchemy import create_engine, Table, Column, Float, String, MetaData


class Database:
    """
    Represents a generic SQL Database object.
    """

    def __init__(self, db_url, seed_path):
        """
        Constructor builds the object. Path determines what kind of SQL
        database should be used. Can be MySQL, sqlite, postgreSQL, etc.
        """

        # Try to initialize the DB 10 times; docker-compose doesn't have
        # a good built-in mechanism to sequence container startup
        for _ in range(10):
            try:
                # Initial sqlalchemy setup; create engine and metadata
                self.engine = create_engine(db_url)
                self.meta = MetaData(self.engine)

                # Create table named "account" along with columns for the
                # account ID (unique key), amount paid, and amount due.
                # The paid and due values cannot be null (constraint).
                self.table = Table(
                    "account",
                    self.meta,
                    Column("acctid", String(15), primary_key=True),
                    Column("paid", Float, nullable=False),
                    Column("due", Float, nullable=False),
                )

                # Connect to the database, and if everything works, stop loop
                self.meta.create_all()
                self.connect()
                break
            except:
                # Wait 5 seconds to try again
                time.sleep(5)

        # If the "conn" attribute does not exist, or it is closed, raise error
        if not hasattr(self, "conn") or self.conn.closed:
            raise TimeoutError("Could not establish session to mysql db")

        # Use the JSON data to seed the database. Note that the JSON file
        # has been converted from a hierarchical dictionary into a list of
        # 3-key dictionaries. This makes it easier to consume by sqlalchemy.
        with open(seed_path, "r") as handle:
            data = json.load(handle)

        # Perform a bulk INSERT of all seed accounts into the db, then close
        self.result = self.conn.execute(self.table.insert(), data)
        self.disconnect()

    def connect(self):
        """
        Open (connect) the connection to the database.
        """
        self.conn = self.engine.connect()
        if self.conn.closed:
            raise OSError("connect() succeeded but session is still closed")

    def disconnect(self):
        """
        Close (disconnect) the connection to the database.
        """
        if hasattr(self, "conn") and not self.conn.closed:
            self.conn.close()
            if not self.conn.closed:
                raise OSError("close() succeeded but session is still open")

    def balance(self, acct_id):
        """
        Determines the customer balance by finding the difference between
        what has been paid and what is still owed on the account. Uses
        SQL queries to find the specified account ID. A positive number means
        the customer owes us money and a negative number means they overpaid.
        """

        select_acct = self.table.select().where(
            self.table.c.acctid == acct_id.upper()
        )
        result = self.conn.execute(select_acct)
        acct = result.fetchone()
        if acct:
            bal = acct["due"] - acct["paid"]
            return f"{bal:.2f} USD"

        return None
