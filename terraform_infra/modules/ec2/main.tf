data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "ec2_deployment" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  // key_name                    = aws_key_pair.ec2_deployment.key_name
  // associate_public_ip_address = false
  // vpc_security_group_ids      = [aws_security_group.lockdown]
  #ebs_optimized               = true

  tags = {
    Terraform = true
    BuiltBy   = "Terraform"
    Name      = "test-instance"
  }
}

resource "aws_ebs_volume" "data" {
  size              = 40
  availability_zone = aws_instance.ec2_deployment.availability_zone
}

resource "aws_volume_attachment" "data_attach" {
  device_name = "/dev/sdh"
  instance_id = aws_instance.ec2_deployment.id
  volume_id   = aws_ebs_volume.data.id
}

// resource "aws_key_pair" "ec2_deployment" {
//   key_name   = "imcuster_key"
//   public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDzCoT/n0DF2lUmTwjhwGVc8E/useQemvWMVwcRsL67hTDUMsk7C2oeiA3M5UmcYV8Qb8cyBeth/EInPsAEBOklXP08jjQ7UhVgKNc5HnDBgzp5eADoUkJKkMgZKyp3el8SwiRf9HbIS01qcX9cfc8zNTGTiv9mNRO+ENXRch4QVd9HSjg27EqXL3L+TaiTaDUzxkuTJJidqe8W4BMdyX2zBlPLPxxU65SZHtm79Y1bSGqe7btX+Nv1M5/FwzaH0AOK8glAW9Z7qoknbKT5hdzO2tmmc73zQXqnNSrRb2eYvNMXUMATsUS+YQ3s4OjyPut9+hX0EIL2jZGplMN/9sZF Ian@RAIN-KING.local"
// }

// resource "aws_security_group" "lockdown" {
//   name        = "lockdown"
//   description = "Allow only connections from self."
//   vpc_id      = data.aws_vpc.selected.id
//
//   tags = {
//     Terraform = true
//     BuiltBy   = "Terraform"
//   }
//
//   ingress {
//     description = "ssh"
//     from_port   = 22
//     to_port     = 22
//     protocol    = "tcp"
//     self        = true
//   }
//
//   egress {
//     description = "Enable outbound traffic"
//     from_port   = 0
//     to_port     = 0
//     protocol    = "-1"
//     cidr_blocks = ["0.0.0.0/0"]
//   }
// }
