resource "aws_s3_bucket" "unprocessed_bucket" {
  bucket = "unprocessed-bucket-tvw"
  #acl    = "private"

  tags = {
    Name        = "Unproccesed HTML"
  }
}

resource "aws_s3_bucket" "processed_bucket" {
  bucket = "processed-bucket-tvw"
  #acl    = "private"

  tags = {
    Name        = "Proccesed HTML"
  }
}

resource "aws_s3_bucket" "processed_bucket" {
  bucket = "processed-bucket-tvw"
  #acl    = "private"

  tags = {
    Name        = "Proccesed HTML"
  }
}

resource "aws_iam_role" "job_process_role" {
  name = "job_process_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "s3_attach" {
  role = aws_iam_role.job_process_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "proccess_new_job_page" {
  filename = "lambda2.zip"
  function_name = "proccess_new_job_page"
  role = aws_iam_role.job_process_role.arn
  handler = "lambda_function.lambda_handler"

  source_code_hash = filebase64sha256("lambda2.zip")

  runtime = "python3.8"
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.proccess_new_job_page.arn
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.unprocessed_bucket.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.unprocessed_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.proccess_new_job_page.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "job_page/"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}

resource "aws_instance" "collection_server" {
  ami           = "ami-08d70e59c07c61a3a"
  instance_type = "t2.micro"

  user_data = 

  tags = {
    Name = "collection-server"
  }
}

