#Import necessary libraries
import pandas as pd
import os
import io
from azure.storage.blob import BlobServiceClient, BlobClient
from dotenv import load_dotenv

ziko_df = pd.read_csv("ziko_logistics_data.csv")

# Data cleaning and Transformation

ziko_df.fillna({
    'Unit_Price' : ziko_df['Unit_Price'].mean(),
    'Total_Cost' : ziko_df['Total_Cost'].mean(),
    'Discount_Rate' : 0.0,
    'Return_Reason' : 'Unknown'
}, inplace=True)


ziko_df['Date'] = pd.to_datetime(ziko_df['Date'])

# Customer table
customer = ziko_df[['Customer_ID', 'Customer_Name', 'Customer_Phone', 'Customer_Email', 'Customer_Address']].copy().drop_duplicates().reset_index(drop=True)
customer.head()

#product table
product = ziko_df[['Product_ID', 'Product_List_Title', 'Quantity', 'Unit_Price', 'Discount_Rate']].copy().drop_duplicates().reset_index(drop=True)

product.head()

#Transaction fact table
transaction_fact = ziko_df.merge(customer, on=['Customer_ID', 'Customer_Name', 'Customer_Phone', 'Customer_Email', 'Customer_Address'], how='left')\
                  .merge(product, on=['Product_ID', 'Product_List_Title', 'Quantity', 'Unit_Price', 'Discount_Rate'], how='left')\
                    [['Transaction_ID', 'Date', 'Customer_ID', 'Product_ID', 'Total_Cost',\
                      'Sales_Channel','Order_Priority', 'Warehouse_Code', 'Ship_Mode', 'Delivery_Status',\
                      'Customer_Satisfaction', 'Item_Returned', 'Return_Reason',\
                      'Payment_Type', 'Taxable', 'Region', 'Country'
                      ]]


customer.to_csv(r'dataset/customer.csv', index=False)
product.to_csv(r'dataset/product.csv', index=False)
transaction_fact.to_csv(r'dataset/transaction_fact.csv', index=False)


#Data loading
#Azure blob connection
# load_dotenv()
# connection_str = os.getenv('CONNECT_STR')
# blob_service_client = BlobServiceClient.from_connection_string(connection_str)

# container_name = os.getenv('CONTAINER_NAME')
# container_client = blob_service_client.get_container_client(container_name)


# #create a function that would load data into Azure blob storage as a oarquet file

# def upload_df_to_blob_as_parquet(df, container_client, blob_name):
#     buffer = io.BytesIO()
#     df.to_parquet(buffer, index=False)
#     buffer.seek(0)
#     blob_client = container_client.get_blob_client(blob_name)
#     blob_client.upload_blob(buffer, blob_type = "BlockBlob", overwrite = True)
#     print(f'{blob_name} uploaded to Blob storage successfully')


# upload_df_to_blob_as_parquet(customer, container_client, 'rawdata/customer.parquet')
# upload_df_to_blob_as_parquet(product, container_client, 'rawdata/product.parquet')
# upload_df_to_blob_as_parquet(transaction_fact, container_client, 'rawdata/transaction_fact.parquet')