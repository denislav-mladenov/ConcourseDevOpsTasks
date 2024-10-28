# Provider configuration with secure credentials handling
provider "aws" {
  region = var.aws_region
}

# Updated data source to list all objects in a specific S3 bucket
data "aws_s3_objects" "bucket_objects" {
  bucket = var.s3_bucket_name
}

# Output the list of S3 object keys
output "s3_objects" {
  value = data.aws_s3_objects.bucket_objects.keys
}

