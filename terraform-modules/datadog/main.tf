terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "datadog_monitor" "example" {
  name    = "Example Monitor"
  type    = "metric alert"
  query   = "avg(last_5m):avg:aws.ec2.cpu{environment:prod} > 80"
  message = "High CPU Utilization detected"
  tags    = var.tags
}

variable "region" {
  type        = string
  description = "AWS region"
}

variable "tags" {
  type        = list(string)
  default     = ["env:prod"]
  description = "Tags to apply to resources"
}
