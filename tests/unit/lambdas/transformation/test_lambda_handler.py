# for unit tests
import pytest
from moto import mock_s3, mock_lambda
import json
from io import StringIO
import pandas as pd
import boto3
# code to test
from src.lambdas.transformation import lambda_handler

# Helper function to read a file from a bucket
def read_file_from_bucket(bucket_name, key):
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response["Body"].read().decode("utf-8")
    return content

# Fixture that sets up the necessary resources for testing
@pytest.fixture
def setup_resources():
    with mock_s3():  # Ensures that the resources are created and cleaned up within this context

        # Create AWS resources
        #   1. S3 buckets
        #   2. Event created when uploading file
        #   3. Lambda Function 
        # Test Lambda Function

        # Create source bucket and content
        # "source_bucket_name" has to be the same as in test_event.json
        s3 = boto3.client("s3")
        source_bucket_name = "source-bucket"
        s3.create_bucket(Bucket=source_bucket_name)
        
        sample_data_file_name="sample_data.csv"
        sample_data_csv = open(f"tests/unit/lambdas/transformation/{sample_data_file_name}", "r").read()
        s3.put_object(Bucket=source_bucket_name, Key=sample_data_file_name, Body=sample_data_csv)
        
        # create destination bucket
        destination_bucket_name = "destination-bucket"
        s3.create_bucket(Bucket=destination_bucket_name)

        # Load the test event
        # with open("tests/unit/lambdas/transformation/test_event.json", "r") as f:
        #    event = json.load(f)
        
        # Create the Lambda event
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": source_bucket_name
                        },
                        "object": {
                            "key": sample_data_file_name
                        }
                    }
                }
            ]
        }

        # Set the environment variable for the Lambda function
        import os
        os.environ["DESTINATION_BUCKET"] = destination_bucket_name

        # Run the Lambda function
        lambda_handler.lambda_handler(event, None)

        # Read the transformed file from the destination bucket
        transformed_key = "sample_data_transformed.csv"
        transformed_content = read_file_from_bucket(destination_bucket_name, transformed_key)

        # Parse the transformed content into a DataFrame
        transformed_df = pd.read_csv(StringIO(transformed_content), sep=";")
        
        # Yield the transformed DataFrame to the test functions
        yield transformed_df

 
# Test the row count of the transformed DataFrame
def test_row_count(setup_resources):
    transformed_df = setup_resources
    assert len(transformed_df) == 5


# Test the columns in the transformed DataFrame
def test_columns(setup_resources):
    transformed_df = setup_resources
    assert "start_city" in transformed_df.columns
    assert "end_city" in transformed_df.columns
    assert "average_journey_time" in transformed_df.columns


# Test the calculated average journey times for each pair of cities
@pytest.mark.parametrize(
    "start_city, end_city, expected_average",
    [
        ("Erfurt", "Fulda", 5.75),
        ("Fulda", "Erfurt", 6.25),
        ("Leipzig", "Potsdam", 2.25),
        ("Potsdam", "Leipzig", 2.75),
        ("Stuttgart", "Frankfurt am Main", 1.25),
    ],
)
def test_average_journey_time(setup_resources, start_city, end_city, expected_average):
    transformed_df = setup_resources
    avg_journey_time = transformed_df.loc[
        (transformed_df["start_city"] == start_city) & (transformed_df["end_city"] == end_city),
        "average_journey_time",
    ].values[0]

    assert pytest.approx(avg_journey_time, 0.01) == expected_average