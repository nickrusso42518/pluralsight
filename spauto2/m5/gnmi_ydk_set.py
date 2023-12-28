#!/usr/bin/python

"""
Author: Nick Russo
Purpose: Demonstrate YDK using gNMI provider + CRUD service.
"""

from ydk.models.xr_staticroute import Cisco_IOS_XR_ip_static_cfg as top_static
from ydk.services import CRUDService
from ydk.gnmi.providers import gNMIServiceProvider
from ydk.path import Repository
import logging

# Route tag used for bogon routes
BOGON_TAG = 888

def main():
    """
    Execution starts here.
    """

    # Copy/paste recommended YDK logging config
    logger = logging.getLogger("ydk")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Define gNMI provider to access route server
    repo = Repository("/root/ydk-gen/gen-api/python/xr_staticroute-bundle/ydk/models/xr_staticroute/_yang")
    gnmi_prov = gNMIServiceProvider(address="10.0.90.41",
                                      port=57777,
                                      username="labadmin",
                                      password="labadmin",
                                      repo=repo)
    
    # Define CRUD service to issue RPCs
    crud_serv = CRUDService()

    # Load bogons from file into list of strings
    with open(f"inputs/bogons_gnmi.txt", "r") as handle:
        bogons = [line.strip() for line in handle]

    # Instantiate top-level YANG container
    na_static = top_static.RouterStatic()
    
    # Iterate over each bogon to configure
    for bogon in bogons:
        print(f"Processing {bogon}")
    
        # Set AFI based on whether prefix is IPv4 or IPv6
        if ":" in bogon:
            afi = na_static.default_vrf.address_family.vrfipv6
        else:
            afi = na_static.default_vrf.address_family.vrfipv4
    
        print(f"Using AFI: {afi.yang_name}")
        
        # Create the prefix in the default routing table (aka topology)
        prefix = afi.vrf_unicast.vrf_prefixes.VrfPrefix()
        pfx = bogon.split("/")
        prefix.prefix, prefix.prefix_length = pfx[0], int(pfx[1])
        print(f"Prefix leaf values: {prefix._leafs}")
        
        # Set null0 as the egress interface with the bogon tag of 888
        nhop = prefix.vrf_route.vrf_next_hop_table.VrfNextHopInterfaceName()
        nhop.interface_name = "Null0"
        nhop.description = "YDK_GNMI"
        nhop.tag = BOGON_TAG
        prefix.vrf_route.vrf_next_hop_table.vrf_next_hop_interface_name.append(nhop)
    
        # Send individual gNMI Set request per prefix
        resp = crud_serv.update(gnmi_prov, prefix)
    

if __name__ == "__main__":
    main()
