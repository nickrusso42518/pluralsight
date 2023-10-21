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

# Wait 10 minutes (60 retries * 10 second waits) for HTTPS GET to respond.
# We expect a 200 OK response from the top-level restconf endpoint, and be
# sure to include the base64-encoded credentials for basic authentication.
data "http" "wait_for_https" {
  url      = "https://${aws_instance.xe_ec2.public_ip}/restconf"
  insecure = true

  request_headers = {
    accept        = "application/yang-data+json"
    authorization = "Basic ${base64encode("${var.xe_username}:${var.xe_password}")}"
  }

  retry {
    attempts     = 60
    min_delay_ms = 10000
  }

  lifecycle {
    postcondition {
      condition     = contains([200], self.status_code)
      error_message = "Non-200 status code"
    }
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
    data.http.wait_for_https
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
    data.http.wait_for_https
  ]
}

# Save configuration at the end; must happen AFTER config changes!
resource "iosxe_save_config" "save" {
  depends_on = [
    iosxe_logging.logging,
    iosxe_restconf.logging
  ]
}
