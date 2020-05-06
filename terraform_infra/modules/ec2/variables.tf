variable "region" {
}

// variable "vpc" {
// }

variable "instance_type" {
  description = "What size of instance to spin up."
  default     = "t2.micro"
}

variable "ebs_device_name" {
  description = "Mount point for EBS volume on host server."
  default     = "/dev/xdh"
}
