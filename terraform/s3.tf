resource "aws_s3_bucket" "bucket" {
  bucket_prefix = "${local.name}-bucket"
  acl           = "private"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "history"
    enabled = true
    transition {
      days          = 30
      storage_class = "INTELLIGENT_TIERING"
    }
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "AES256"
      }
    }
  }

  tags = merge(
    {
        Name = "${local.name}-bucket"
    },
    local.tags
  )
}

resource "aws_s3_bucket_object" "raw_data" {
  bucket  = "${aws_s3_bucket.bucket.id}"
  acl     = "private"
  key     = "raw_data"
  content = ""
}

resource "aws_s3_bucket_object" "processed_data" {
  bucket  = "${aws_s3_bucket.bucket.id}"
  acl     = "private"
  key     = "processed_data"
  content = ""
}