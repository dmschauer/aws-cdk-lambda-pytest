from aws_cdk import core
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_apigateway import LambdaRestApi

class MyCdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the source and destination S3 buckets
        source_bucket = Bucket(self, "SourceBucket")
        destination_bucket = Bucket(self, "DestinationBucket")

        # Create the Lambda function
        lambda_function = Function(
            self,
            "CSVTransformFunction",
            runtime=Runtime.PYTHON_3_9,
            code=Code.from_asset("src/lambdas/transformation"),
            handler="lambda_handler.lambda_handler",
            environment={
                "DESTINATION_BUCKET": destination_bucket.bucket_name
            }
        )

        # Grant the Lambda function read access to the source bucket
        source_bucket.grant_read(lambda_function)

        # Grant the Lambda function write access to the destination bucket
        destination_bucket.grant_write(lambda_function)
