variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "tags" {
  description = "List of tags"
  type        = list(string)
  default     = ["env:prod"]
}
