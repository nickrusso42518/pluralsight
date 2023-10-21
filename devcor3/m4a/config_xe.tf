# Tell TF where to find the provider so `terraform init` can install it.
# Specify minimum and/or exact versions; a good idea for new providers.
# https://registry.terraform.io/providers/CiscoDevNet/iosxe/latest
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    iosxe = {
      source = "CiscoDevNet/iosxe"
      version = ">= 0.5.1"
    }
  }
}

# Provider for IOS-XE, creating a mechanism to interact via RESTCONF
provider "iosxe" {
  username = var.xe_username
  password = var.xe_password
  url      = "https://${aws_instance.xe_ec2.public_ip}"
}

# Wait 10 minutes (60 iterations of 10 second waits) for RESTCONF to respond
resource "null_resource" "wait_for_https" {
  provisioner "local-exec" {
    command = "./wait_for_rc.sh 60 ${aws_instance.xe_ec2.public_ip} ${var.xe_username} ${var.xe_password}"
  }
}

# Configure system logging (syslog) information
resource "iosxe_logging" "logging" {
  trap_severity     = "informational"
  source_interface  = "GigabitEthernet1"
  ipv4_hosts = [
    {
      ipv4_host = "203.0.113.1"
    },
    {
      ipv4_host = "203.0.113.2"
    }
  ]
  depends_on = [
    null_resource.wait_for_https
  ]
}

# Configure highly niche option not available in previous logging resource
# YANG structure: { "logging": { "persistent": { "immediate": [null] } } }
resource "iosxe_restconf" "logging" {
  path = "Cisco-IOS-XE-native:native/logging/persistent"
  attributes = {
    immediate = ""
  }
  depends_on = [
    null_resource.wait_for_https
  ]
}

# Save configuration at the end; must happen AFTER config changes!
resource "iosxe_save_config" "save" {
  depends_on = [
    iosxe_logging.logging,
    iosxe_restconf.logging
  ]
}
