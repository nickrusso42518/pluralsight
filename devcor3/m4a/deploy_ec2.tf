# Tells Terraform what region to use, along with user-specific
# access credentials from an existing user with API Access
provider "aws" {
  region = "us-east-1"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# Deploy specific version of IOS-XE, choosing the latest from that upload batch
# $ aws ec2 describe-images --filters 'Name=name,Values=Cisco-C8K-17.12.01a-*'
data "aws_ami" "xe_latest" {
  most_recent = true
  owners      = ["aws-marketplace"]  # owner ID 679593333241
  filter {
    name   = "name"
    values = ["Cisco-C8K-${var.xe_version}-*"]
  }
}

# Print the AMI ID for reference so the user can optionally research it
output "xe_latest_id" {
  description = "AMI image ID just discovered"
  value       = data.aws_ami.xe_latest.id
}

# Deploy the EC2 instance using the specified keypair and the discovered
# AMI ID. Include bootstrap/day0 config to add a user for RESTCONF, as well
# as enabling the RESTCONF service (HTTPS is already enabled). Use the
# hostname as the AWS Name key and the device hostname.
resource "aws_instance" "xe_ec2" {
  ami           = data.aws_ami.xe_latest.id
  instance_type = "c5.large"  # minimum size
  key_name      = var.ec2_keypair
  user_data     = <<EOF
hostname=${var.xe_hostname}
login-username=${var.xe_username}
login-password=${var.xe_password}
ios-config-10="restconf"
EOF
  root_block_device {
    delete_on_termination = true
  }
  tags = {
    Name = var.xe_hostname
  }
}

# Print the public IP of the deployed instance for ping/ssh/curl testing.
output "xe_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.xe_ec2.public_ip
}
