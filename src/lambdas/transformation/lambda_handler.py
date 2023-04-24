import os
import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # Get the source bucket and object key from the S3 event
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    source_key = event["Records"][0]["s3"]["object"]["key"]

    # Get the destination bucket from the Lambda environment variables
    destination_bucket = os.environ["DESTINATION_BUCKET"]

    # Read the CSV file from the source S3 bucket
    s3 = boto3.client("s3")
    csv_obj = s3.get_object(Bucket=source_bucket, Key=source_key)
    csv_data = csv_obj["Body"].read().decode("utf-8")

    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(StringIO(csv_data), sep=";")

    # Perform the required transformation
    transformed_df = (
        df.groupby(["start_city", "end_city"])["journey_time"]
        .mean()
        .reset_index()
        .rename(columns={"journey_time": "average_journey_time"})
    )

    # Write the transformed DataFrame to a CSV string
    transformed_csv = transformed_df.to_csv(sep=";", index=False)

    # Save the transformed CSV to the destination S3 bucket
    s3.put_object(
        Bucket=destination_bucket,
        Key=source_key.replace(".csv", "_transformed.csv"),
        Body=transformed_csv
    )
