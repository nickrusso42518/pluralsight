#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple implementation of the Observer design pattern without any
fancy packages or frameworks.
"""


class BusinessCustomer:
    """
    This is a type of observer, which is a business customer. When they
    fall behind on payments, the program should automatically robocall
    their finance department (yes, I know this is evil). Sometimes
    observers are called subscribers, too.
    """

    def __init__(self, acct_id, money_owed):
        """
        Constructor to store the account ID and current amount
        of money owed.
        """
        self.acct_id = acct_id
        self.money_owed = money_owed

    def update(self):
        """
        When the accounting system (the subject, or publisher) needs to notify
        all observers (or subscribers) about some event, this is the method
        that will be invoked. Perhaps it is the end of the month or
        some other important event occurred at Globomantics.
        """
        if self.money_owed > 0:
            print(f"{self.acct_id}: Call the company's finance department")
        else:
            print(f"{self.acct_id}: Corporate balance paid")


class ConsumerCustomer:
    """
    This is another type of observer, a consumer customer. When they
    fall behind on payments, they are just individuals who don't
    have departments working for them, so let's send a simple email
    reminding them their balance is past due.
    """

    def __init__(self, acct_id, money_owed):
        """
        Constructor to store the account ID and current amount
        of money owed.
        """
        self.acct_id = acct_id
        self.money_owed = money_owed

    def update(self):
        """
        When the accounting system (the subject, or publisher) needs to notify
        all observers (or subscribers) about some event, this is the method
        that will be invoked. Perhaps it is the end of the month or
        some other important event occurred at Globomantics.
        """
        if self.money_owed > 0:
            print(f"{self.acct_id}: Send a polite reminder email")
        else:
            print(f"{self.acct_id}: Individual balance paid")


class AccountingSystem:
    """
    This is the subject (or the publisher) that maintains a list of
    observers (or subscribers) and is capable of notifying them. There
    could be a mix of different observers too, as we have both
    business and consumer-grade customers in this example.
    """

    def __init__(self):
        """
        Constructor creates a new, empty accounting system with
        an empty set of customers (observers/subscribers).
        """
        self.customers = set()

    def register(self, customer):
        """
        A new customer has signed up, so add them to the set.
        """
        self.customers.add(customer)

    def unregister(self, customer):
        """
        An existing customer has closed their account. Remove
        them from the set.
        """
        self.customers.remove(customer)

    def notify(self):
        """
        Notify all current customers about some event. This iteratively
        steps through the set and invokes the "update()" method on
        each type of customer.
        """
        for customer in self.customers:
            customer.update()


def main():
    """
    Execution starts here.
    """

    # Create a mix of business and consumer customers with varying balances
    cust1 = BusinessCustomer("ACCT100", 10)
    cust2 = BusinessCustomer("ACCT200", 0)
    cust3 = ConsumerCustomer("ACCT300", -10)
    cust4 = ConsumerCustomer("ACCT400", 20)

    # Create the account system (subject) and register our new customers
    accounting_sys = AccountingSystem()
    accounting_sys.register(cust1)
    accounting_sys.register(cust2)
    accounting_sys.register(cust3)
    accounting_sys.register(cust4)

    # Some event occurred; notify all subscribers about their bills
    accounting_sys.notify()

    # One customer has cancelled their account; unregister them
    print("** cust2 has cancelled their account")
    accounting_sys.unregister(cust2)

    # Event occurrred again, and notice how cust2 isn't displayed
    accounting_sys.notify()


if __name__ == "__main__":
    main()
