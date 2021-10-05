#!/bin/bash

# Initial installation of NSO in sandbox. Run these commands on NSO directly.
# Cisco Network Services Orchestrator 4.7.3.2 Sandbox v1
sh nso-4.7.3.2.linux.x86_64.installer.bin $HOME/ncs-4.7.3.2 --local-install
source ncs-4.7.3.2/ncsrc
ncs-setup --dest $HOME/ncs-run

# This step is not in the install guide but is necessary. NSO comes
# with many Network Element Drivers (NEDs) but they start off in a
# staging area. To use them, copy the required NED folders into
# ncs-run/packages. We only need Cisco IOS for this demo.
cp -R ncs-4.7.3.2/packages/neds/cisco-ios ncs-run/packages/cisco-ios

# Switch into the ncs-run directory and start the application
cd $HOME/ncs-run
ncs
