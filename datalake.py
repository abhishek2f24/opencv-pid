from flask import Flask, request, jsonify
import datetime
import sql_client
import fetch_raw_data
import json
import sys
import concurrent
from itertools import repeat
import azure.functions as func
from typing import List
import multiprocessing as mp
app = Flask(__name__)


@app.route('/raw_datalake', methods=['GET','POST'])
def processrawdatalake():
    if request.method =="GET":
        return "Webapp is up and running"
    
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8'))
        to_time = datetime.datetime.strptime(data["from_time"],'%Y-%m-%d %H:%M:%S')
        from_time = datetime.datetime.strptime(data["to_time"],'%Y-%m-%d %H:%M:%S')
        if (to_time - from_time).total_seconds() / 60 >= 60:
            return "Max difference between from_time and to_time should be 1 hour"
        
        if from_time and to_time:
            #Get Cleansing database comnection string from keyvalut
            clconnectionstring = sql_client.getCleansingDbConnString()

            print("call getConnection for acdclconnection")
            engine = sql_client.getConnection(clconnectionstring)
            sql_query = "select tagId from PiTagMaster"
            print("SQL client starting connection")
            print(engine, flush=True)

            # Get database connection string and all other data configuration info from database table column
            tag_dataframe = sql_client.read_data_from_sql(engine, sql_query)
            print("Fetch tag master completed")
            
            # Getting list of tags from tag master database 
            tag_list = tag_dataframe["tagId"].values.tolist()

            # Get raw data from datalake between custom time range
            cpu_count: mp.cpu_count()
            chunk_size: int = len(tag_list) // cpu_count + 1
            tag_chunks: List[List[str]] = [tag_list[x:x + chunk_size] for x in
                                            range(0, len(tag_list), chunk_size)]
            print(len(tag_chunks))
            with concurrent.futures.ThreadPoolExecutor(cpu_count) as executor:
                for prime in zip(tag_chunks, executor.map(fetch_raw_data.fetch_raw,tag_chunks)):
                    print(f'{prime} has been completed')
            output = fetch_raw_data.fetch_raw(tag_list, from_time, to_time)
            print("Fetch raw data from datalake is completed")
            json_output = fetch_raw_data.transformation(output, from_time, to_time) 

            # Send json data to bulk insert in cosmos DB
            bulk_response = fetch_raw_data.bulkinsert(json_output)
            
            #json_payload = json_output.to_dict(orient='records')
            # with open('data.json', 'w', encoding='utf-8') as f:
            #     json.dump(json_payload, f, ensure_ascii=False, indent=4)
         
            if bulk_response.status_code == 200:
                print("Bulk Insert run successfully")
                return "Bulk insert to Azure Cosmos DB executed successfully"
            else:
                print("Bulk insert to Azure Cosmos DB finished with status code: {}".format(bulk_response.status_code))
                return "Bulk insert failed"


def fetch_raw(tag_list, from_time, to_time):
    account_url = "https://stpdlk2srciasp.blob.core.windows.net"
    default_credential = ManagedIdentityCredential()
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)    
    container_client = blob_service_client.get_container_client(container='pi-da-rc-fr-nor')
    filtered_df = None
    for tag in tag_list:
        container_tag_folder = f'RAW/ARCHIVE/{tag}/IN'
        print("Start of", tag)
        print(datetime.now())
        blobs = container_client.list_blobs(name_starts_with=container_tag_folder)
        print("end of", tag)
        print(datetime.now())
        
        for blob in blobs:
            blob_name = blob.name
            if date_to_retrieve in blob_name:
                print("Start file load",datetime.now() )
                blob_client = blob_service_client.get_blob_client(container="pi-da-rc-fr-nor" ,blob=blob_name)
                stream_data = blob_client.download_blob().readall()
                data = pd.read_csv(BytesIO(stream_data),on_bad_lines='skip', sep=";", low_memory=True,encoding="utf-8",names=['Tag','Timestamp','Value'])
                filtered_df = pd.concat([filtered_df, data], ignore_index=True)
                print("End file load",datetime.now() )
                
            break
        print("end of blob read ", datetime.now())

def transformation(filtered_df,from_time,to_time):   
    filtered_df['Timestamp'] = pd.to_datetime(filtered_df['Timestamp'])
    mask = (filtered_df["Timestamp"].dt.to_pydatetime() < to_time) & (filtered_df["Timestamp"].dt.to_pydatetime() > from_time)
    filteredf = filtered_df.loc[mask]
    filteredf['Timestamp'] = pd.to_datetime(filteredf['Timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    filteredf['Timestamp'] = filteredf['Timestamp'].astype(str)
    filteredf.rename(columns = {'Timestamp':'TimestampUtcTime'}, inplace = True)
    filteredf['id'] = uuid.uuid4()
    filteredf['id'] = filteredf['id'].astype(str)
    return filtered_df

def bulkinsert(df_json):
    url = "https://BulkInsertCleanData.azurewebsites.net/api/Tag/BulkUploadRawTagData"
    json_payload = json.dumps(df_json.to_dict(orient='records'))
    response_bulkinsert = requests.post(url=url, data=json_payload)
    return response_bulkinsert
    
        
 
# main driver function
if __name__ == '__main__':
    app.run(debug=True)
