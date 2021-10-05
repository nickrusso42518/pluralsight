## site.pp ##

# This file (/etc/puppetlabs/puppet/manifests/site.pp) is the main entry point
# used when an agent connects to a master and asks for an updated configuration.
#
# Global objects like filebuckets and resource defaults should go in this file,
# as should the default node definition. (The default node can be omitted
# if you use the console and don't define any other nodes in site.pp. See
# http://docs.puppetlabs.com/guides/language_guide.html#nodes for more on
# node definitions.)

## Active Configurations ##

# Disable filebucket by default for all File resources:
File { backup => false }

# DEFAULT NODE
# Node definitions in this file are merged with node data from the console. See
# http://docs.puppetlabs.com/guides/language_guide.html#nodes for more on
# node definitions.

# The default node definition matches any node lacking a more specific node
# definition. If there are no other nodes in this file, classes declared here
# will be included in every node's catalog, *in addition* to any classes
# specified in the console for that node.

node default {
  # This is where you can declare classes for all nodes.
  # Example:
  #   class { 'my_class': }
}

# Define the local puppet master (puppet manages itself)
# Includes connection handlers for network devices
node "ip-10-125-0-45.ec2.internal" {
  include ciscopuppet::proxy
  include device_manager::devices

  # Hostname and credentials came from always-on
  # NXOS DevNet sandbox
  device_manager {'nxos_sandbox':
  type           => 'cisco_nexus',
    credentials    => {
      host            => 'sbx-nxos-mgmt.cisco.com',
      port            => 443,
      user            => 'admin',
      password        => 'Admin_1234!',
      transport       =>  'https',
    },
    include_module => false,
  }
}

# Define our NXOS node and the declarative configuration items
# we want to manage. This creates three VLANs with different IDs
# and different names.
node 'nxos_sandbox'{
  cisco_vlan { '171':
    ensure    => 'present',
    shutdown  => 'false',
    state     => 'active',
    vlan_name => 'DATA',
  }
  cisco_vlan { '172':
    ensure    => 'present',
    shutdown  => 'false',
    state     => 'active',
    vlan_name => 'VOICE',
  }
  cisco_vlan { '173':
    ensure    => 'present',
    shutdown  => 'false',
    state     => 'active',
    vlan_name => 'MGMT',
  }
}
