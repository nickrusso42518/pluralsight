# export TF_VAR_aws_access_key=...
variable "aws_access_key" {
  type        = string
  description = "AWS access key with programmatic access to EC2"
}

# export TF_VAR_aws_secret_key=...
variable "aws_secret_key" {
  type        = string
  description = "AWS secret key with programmatic access to EC2"
  sensitive   = true
}

# Can override these use env vars as well
variable "xe_username" {
  type        = string
  description = "Login username for Cat8000v"
  default     = "ec2-user"
}

variable "xe_password" {
  type        = string
  description = "Login password for Cat8000v"
  default     = "password123!"
  sensitive   = true
}

variable "xe_version" {
  type        = string
  description = "Software version of XE device to deploy"
  default     = "17.12.01a"  # newest at time of recording
}

variable "xe_hostname" {
  type        = string
  description = "Device hostname and AWS Name tag"
  default     = "C8K"
}

variable "ec2_keypair" {
  type        = string
  description = "EC2 keypair name for SSH public key authentication"
  default     = "EC2-key-pair"
}
