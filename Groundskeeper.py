import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from dotenv import load_dotenv

# Load environment variables from the .env file (where the subscription id is located)
load_dotenv()

def connect_to_azure():
    # Use DefaultAzureCredential to authenticate
    credentials = DefaultAzureCredential()

    # Create the Azure Resource Management client and retrieve the subscription id
    resource_client = ResourceManagementClient(credentials, subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"))

    return resource_client

def check_expiration_tags(resource_client):
    # Define the tag key indicating expiration
    expiration_tag_key = 'ExpirationDate'
    # Define a threshold date (e.g., today) to identify expired resources
    threshold_date = datetime.utcnow().date()  # Get the current date without the time

    # List resources and check expiration tags
    resources = resource_client.resources.list()
    for resource in resources:
        # Check if resource has tags
        if resource.tags:
            if expiration_tag_key in resource.tags:
                expiration_date = datetime.strptime(resource.tags[expiration_tag_key], '%Y-%m-%d').date()
                if expiration_date <= threshold_date:
                    # Resource has expired, take appropriate action (e.g., delete)
                    delete_resource(resource.id)
        #else:
            # Resource has no tags
            #print(f"Resource {resource.id} has no tags.")

def delete_resource(resource_id):
    # Print the resource ID instead of deleting it
    print(f"Resource {resource_id} would be deleted.")

if __name__ == "__main__":
    azure_client = connect_to_azure()
    check_expiration_tags(azure_client)
