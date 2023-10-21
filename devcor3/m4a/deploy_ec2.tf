# Tells Terraform what region to use, as this default setting
# from "aws configure" does not carry over
provider "aws" {
  region = "us-east-1"
  access_key = "AKIAQUIXDWMC2BWT3SMX"
  secret_key = "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"
}

# aws ec2 describe-images --filters 'Name=name,Values=Cisco-C8K-17.12.01a-*'
data "aws_ami" "xe_latest" {
  most_recent = true
  owners      = ["aws-marketplace"]  # owner ID 679593333241
  filter {
    name   = "name"
    values = ["Cisco-C8K-${var.xe_version}-*"]
  }
}

output "xe_latest_id" {
  description = "AMI image ID just discovered"
  value       = data.aws_ami.xe_latest.id
}

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

output "xe_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.xe_ec2.public_ip
}