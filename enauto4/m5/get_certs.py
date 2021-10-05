#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Consume the custom CiscoSDWAN mini-SDK and
and test its Certificate Management API methods.
"""

import os
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cisco_sdwan import CiscoSDWAN


def main():
    """
    Execution begins here.
    """

    # Create SD-WAN object to DevNet sandbox host
    sdwan = CiscoSDWAN.get_instance_reserved()

    # Create a backup_certs/ directory if it doesn't already exist
    cert_path = "backup_certs"
    if not os.path.exists(cert_path):
        os.makedirs(cert_path)

    # For each controller (vBond, vSmart, vManage) cert, perform
    # backup and information display
    for cert in sdwan.get_controller_certs().json()["data"]:
        backup_and_print_cert(
            cert_path, cert["host-name"], cert["deviceEnterpriseCertificate"]
        )

    # Perform backup and information display of the root cert also
    root_cert = sdwan.get_root_cert().json()["rootcertificate"]
    backup_and_print_cert(cert_path, "root", root_cert)


def backup_and_print_cert(path, name, data):
    """
    User-written helper function (could be in SDK too) to backup a certificate
    given a path, name, and certificate data. It also prints a summary of
    the certificate by including the serial number and subject name details.
    """

    # Open new file for writing, and write the cert data
    with open(f"{path}/{name}.pem", "w") as handle:
        handle.write(data)

    # Use cryptography to load the cert data into memory after converting
    # the text to a byte string
    cert = x509.load_pem_x509_certificate(bytes(data, "utf-8"), default_backend())

    # Print basic information about certificate
    print(f"Cert info for {name} / serial {cert.serial_number}")
    subject_items = cert.subject.rfc4514_string().replace(",", "\n")
    print(subject_items + "\n")


if __name__ == "__main__":
    main()
