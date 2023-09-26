from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from datetime import datetime

# Initialize a Spark session
spark = SparkSession.builder.appName("AzureBlobProcessor").getOrCreate()

# Set your Azure Blob Storage configurations
container_name = "your_container_name_here"
tag_list = ["tag1", "tag2"]  # Replace with your list of tags
date_to_retrieve = "20230924"

# Define a UDF to read and process data from Azure Blob Storage
def process_blob_data(tag):
    print("Start of", tag)
    print(datetime.now())

    container_tag_folder = f"RAW/ARCHIVE/{tag}/IN"
    
    # Read data from Azure Blob Storage into a Spark DataFrame
    df = spark.read.option("header", "true").option("sep", ";").csv(f"abfss://{container_name}@your_account.dfs.core.windows.net/{container_tag_folder}/*.csv")
    
    # Filter data for the specific date
    filtered_df = df.filter(col("date_column") == date_to_retrieve)

    # Process the data as needed
    # For example, you can perform transformations or aggregations here

    print("End of", tag)
    print(datetime.now())

    return filtered_df

# Create a list of DataFrames, one for each tag
tag_dataframes = [process_blob_data(tag) for tag in tag_list]

# Union the DataFrames into a single DataFrame
result_df = tag_dataframes[0]
for df in tag_dataframes[1:]:
    result_df = result_df.union(df)

# Show or save the result DataFrame as needed
result_df.show()

# Stop the Spark session when done
spark.stop()
