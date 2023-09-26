from pyspark.sql import SparkSession
import pandas as pd
from io import BytesIO
from datetime import datetime

# Initialize a Spark session
spark = SparkSession.builder.appName("AzureBlobProcessor").getOrCreate()

# Set your Azure Blob Storage configurations
azure_blob_connection_string = "your_connection_string_here"
container_name = "your_container_name_here"
tag_list = ["tag1", "tag2"]  # Replace with your list of tags

# Initialize the Azure Blob Storage client
container_tag_folder = "RAW/ARCHIVE/{}/IN"

for tag in tag_list:
    print("Start of", tag)
    print(datetime.now())
    
    # List blobs in the container with a specific tag folder
    blobs = spark._jvm.azure.storage.blob.BlobServiceClientBuilder() \
        .connectionString(azure_blob_connection_string) \
        .containerClient(container_name) \
        .getContainerClient(container_tag_folder.format(tag)) \
        .listBlobs().iterator()

    print("End of", tag)
    print(datetime.now())

    date_to_retrieve = "20230924"

    for blob in blobs:
        blob_name = blob.getName()
        if date_to_retrieve in blob_name:
            print("Start file load", datetime.now())

            # Initialize the blob client
            blob_client = spark._jvm.azure.storage.blob.BlobServiceClientBuilder() \
                .connectionString(azure_blob_connection_string) \
                .containerClient(container_name) \
                .getBlobClient(blob_name)

            # Download blob data
            blob_data = blob_client.downloadBlob().readAll()
            blob_data_bytes = bytearray(blob_data)

            # Process the data using Pandas (you can use Spark DataFrame for large-scale data)
            data = pd.read_csv(BytesIO(blob_data_bytes), on_bad_lines='skip', sep=";", low_memory=True, encoding="utf-8", na_values=[""])

            # Here, you can further process the data or save it as needed
            # For large-scale data, consider using Spark DataFrame operations

            print("End file load", datetime.now())

# Stop the Spark session when done
spark.stop()
