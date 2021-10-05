#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate basic HTTP cache-control mechanisms usinga variety
of URLs with different cache-control characteristics.
"""

import logging
import time
import requests
from cachecontrol import CacheControl


def main():
    """
    Execution begins here.
    """

    # Create a logger object to let us see what is happening behind the
    # scenes with the HTTP URLs
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Specify list of URLs to perform an HTTP GET against
    # Author's note: These files don't have "Cache-Control" anymore as I removed
    # them after the demo. Please replace these URLs with your own!
    url_list = [
        "http://njrusmc.net/jobaid/wlan_pcap.zip",  # Cache-Control: public (300s)
        "http://njrusmc.net/jobaid/lmnop_answers.pdf",  # Cache-Control: no-store
    ]

    # For each URL, run two GET requests, and use the logger to print out
    # the relevant information as requests are processed
    for url in url_list:

        # Create the cached session object, which automatically intereprets
        # caching-related headers (requests doesn't do it natively)
        cached_sess = CacheControl(requests.session())

        # Print information from first run, include key headers
        logger.info("---------------------------------------------------------")
        logger.info("First GET to URL: %s", url)
        resp = cached_sess.get(url)
        logger.info("Response %s / %s", resp.status_code, resp.reason)
        logger.info("Cache-Control: %s", resp.headers.get("Cache-Control"))
        logger.info("ETag: %s", resp.headers.get("ETag"))

        # Slight delay just to show the cache timer countdown
        # Print information from second run, but focus is on background debugs
        time.sleep(1.5)
        logger.info("Second GET to URL: %s", url)
        resp = cached_sess.get(url)
        logger.info("Response %s / %s", resp.status_code, resp.reason)


if __name__ == "__main__":
    main()
