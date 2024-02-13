import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv

# Load environment variables from the .env file (where the subscription id is located)
load_dotenv()

def connect_to_azure():
    # Use DefaultAzureCredential which automatically selects appropriate credentials in order to connect to Azure
    credentials = DefaultAzureCredential()

    # Create the Azure Resource Management client and retrieve the subscription id
    resource_client = ResourceManagementClient(credentials, subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"))

    return resource_client

def list_resources(resource_client):
    # List resources in the Azure subscription
    resources = resource_client.resources.list()

    # Print resource information
    for resource in resources:
        print(f"Resource ID: {resource.id}, Type: {resource.type}")

if __name__ == "__main__":
    azure_client = connect_to_azure()
    list_resources(azure_client)
