from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

# Bit janky, likely to change
import configparser

def connect_to_azure():
    # Read your configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    subscription_id = config['Azure']['subscription_id']

    # Obtain Azure credentials using the default credential provider
    credentials = DefaultAzureCredential()

    # Create the Azure Resource Management client
    resource_client = ResourceManagementClient(credentials, subscription_id)

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
