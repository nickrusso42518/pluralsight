# Module 4 - Managing Cisco NX-OS using Puppet
This directory contains the reference Puppet manifest generated in
the course. The file does not stand alone and should be integrated into
a functional Puppet deployment. I've provided it in the course files for
reference.

## Puppet Installation
Installing puppet is more involved than a simple `pip install`,
and using the bootstrap process from this DevNet demo is
one of the simplest ways to get started. These are the high-level steps:

  1. Open a web browswer to 
     `https://github.com/shermdog/devnet_demo/wiki/Cisco-Live-US-2019-DevNet-Workshop`
     and use the site as a guide/reference if you get stuck.
  2. Follow the "Bootstrapping" section which includes cloning the repo
     and running a Bash script. I recommend being root for these actions.
  3. Install the NXOS puppet module using 
     `puppet module install puppetlabs-ciscopuppet`
  4. Verify correct installation with `puppet module list`
  5. Reference this documentation to learn how to use this Cisco NXOS
     module: `https://forge.puppet.com/puppetlabs/ciscopuppet`
  6. Copy `site.pp` from this directory into the following path:
     `/etc/puppetlabs/code/environments/production/manifests/site.pp`
  7. Update `site.pp` with your puppet master hostname and network devices.
  8. Run `puppet agent -t` to update puppet.
  9. Run `puppet device -v` to apply the configuration changes.

Note that this repo is very specific to Cisco DevNet's IOS-XE sandbox, so if
you aren't using that specific sandbox, the IP addresses may change. In the
course, I used a standalone AWS instance due to DevNet's current restrictions
on sandbox Internet access. This restriction may be lifted by the time you
read this.

## Transport schema
You may need access to the minor options available with the NXOS transport
handler. Looking at the source code is the simplest approach:

`https://github.com/cisco/cisco-network-puppet-module/blob/develop/lib/puppet/transport/schema/cisco_nexus.rb`

## Quick tips
Here is some additional information advice to help you get started:

  * Whenever `site.pp` is modified, the puppet master needs to update itself
    with the new desired state. Use `puppet agent -tv` to update it. You
    must do this before trying to apply the changes to network devices.
  * The command `puppet device -v` is like running an Ansible playbook
    with medium-level verbosity for debugging. This is how the puppet
    configuration is applied to the nodes specified in the `site.pp` manifest.
  * You can use `puppet device -d` for more verbosity, but be warned this
    will generate a ton of output.
  * To retrieve information quickly use the
    `puppet device -t nxos_sandbox --resource cisco_vlan` command as an
    example. This targets the `nxos_sandbox` device and only collects the
    `cisco_vlan` resource to save time.
