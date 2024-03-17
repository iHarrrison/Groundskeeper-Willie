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

def check_expiration_tags(resource_client, dry_run = True):
    expiration_tag_key = 'ExpirationDate'
    threshold_date = datetime.utcnow().date()

    # List resources and check expiration tags
    resources = resource_client.resources.list()
    for resource in resources:
        if resource.tags:
            if expiration_tag_key in resource.tags:
                expiration_date = datetime.strptime(resource.tags[expiration_tag_key], '%Y-%m-%d').date()
                if expiration_date <= threshold_date:
                    # Extract resource name from the resource ID
                    resource_name = resource.id.split('/')[-1]
                    # Print resource name
                    if dry_run:
                        print(f"Resource {resource_name} would be deleted.")
                    else:
                        delete_resource(resource.id)

def delete_resource(resource_id):
    pass

if __name__ == "__main__":
    azure_client = connect_to_azure()
    # Set dry_run to False to perform actual deletion
    check_expiration_tags(azure_client, dry_run=True)
