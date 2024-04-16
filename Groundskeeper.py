import os
from datetime import datetime, timedelta

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.locks import ManagementLockClient
from dotenv import load_dotenv

# Load environment variables from the .env file (where the subscription id is located)
load_dotenv()


def connect_to_azure():
    try:
        # Use DefaultAzureCredential to authenticate
        credentials = DefaultAzureCredential()

        # Create the Azure Resource Management client and retrieve the subscription id
        resource_client = ResourceManagementClient(credentials, subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"))

        return resource_client

    except ClientAuthenticationError as e:
        print("Authentication has failed. Please double check your Azure credentials are correct.")
        print(e)


def check_expiration_tags(resource_client):
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
                    print(f"Resource {resource_name} would be deleted.")


def delete_resource(resource_id, credentials):
    if not is_resource_locked(resource_id, credentials):
        # Perform deletion operation
        # Implement your deletion logic here
        print(f"Resource {resource_id} would be deleted.")
    else:
        print(f"Resource {resource_id} is locked and cannot be deleted.")


def is_resource_locked(resource_id, credentials):
    lock_client = ManagementLockClient(credentials)
    locks = lock_client.management_locks.list_at_resource_level(resource_id)
    return any(lock.name for lock in locks)


if __name__ == "__main__":
    azure_client = connect_to_azure()
    # ||IMPORTANT||
    # Please set the dry_run flag to false for actual deletion
    dry_run = True
    check_expiration_tags(azure_client)
