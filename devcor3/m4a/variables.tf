# Easy and secure way to override these defaults with env vars:
# export TF_VAR_xe_username=(your username)
# export TF_VAR_xe_password=(your password)
# etc ...
variable "xe_username" {
  type = string
  description = "Login username for Cat8000v"
  default = "ec2-user"
}

variable "xe_password" {
  type = string
  description = "Login password for Cat8000v"
  default = "password123!"
}

variable "xe_version" {
  type = string
  description = "Software version of XE device to deploy"
  default = "17.12.01a"  # newest at time of recording
}

variable "xe_hostname" {
  type = string
  description = "Device hostname and AWS Name tag"
  default = "C8K"
}

variable "ec2_keypair" {
  type = string
  description = "EC2 keypair name for SSH access"
  default = "EC2-key-pair"
}
