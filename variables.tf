variable "aws_region" {
  description = "The AWS region to use"
  type        = string
  default     = "eu-west-1"  # You can set a default value or specify it during runtime
}

variable "s3_bucket_name" {
  description = "The name of the S3 bucket to list objects from"
  type        = string
}

