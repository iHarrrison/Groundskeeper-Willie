import os
from datetime import datetime
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
    expiration_tag_key = 'ExpirationDate'
    threshold_date = datetime.utcnow().date()

    # List to store resources for deletion
    resources_for_deletion = []

    # Fetch resources by page
    resources_pages = resource_client.resources.list().by_page()

    # Iterate over pages of resources
    for resources_page in resources_pages:
        # Iterate over resources on the current page
        for resource in resources_page:
            if resource.tags and expiration_tag_key in resource.tags:
                expiration_date = datetime.strptime(resource.tags[expiration_tag_key], '%Y-%m-%d').date()
                if expiration_date <= threshold_date:
                    resource_name = resource.id.split('/')[-1]
                    # Check if it's dry-run mode and add resource to the list
                    if dry_run:
                        resources_for_deletion.append(resource_name)
                    else:
                        delete_resource(resource_client, resource.id, resource_name)

    # Print resources picked up for deletion in dry-run mode
    if dry_run:
        print("Resources that would be deleted:")
        for resource_name in resources_for_deletion:
            print(f"- {resource_name}")

def delete_resource(resource_client, resource_id, resource_name):
    if dry_run:
        print(f"Resource {resource_name} would be deleted.")
    else:
        try:
            # Delete the resource
            resource_client.resources.begin_delete_by_id(resource_id, api_version='2023-05-01')
            print(f"Resource {resource_name} has been deleted.")
        except Exception as e:
            print(f"Failed to delete resource {resource_name}: {e}")

if __name__ == "__main__":
    # |||IMPORTANT|||
    # Please set the dry_run to False in order to perform actual deletion
    dry_run = True
    azure_client = connect_to_azure()
    check_expiration_tags(azure_client)
