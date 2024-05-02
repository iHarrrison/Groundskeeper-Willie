import os
import time
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

app = Flask(__name__)

@app.route('/')
def index():
    # Authenticate with Azure
    resource_client = authenticate_azure()

    # Retrieve resources
    resources = get_resources(resource_client)

    # Separate resources into two lists: scheduled for expiration and not scheduled for expiration
    resources_scheduled_for_expiration = []
    resources_not_scheduled_for_expiration = []

    for resource in resources:
        # Check if tags are None or if 'ExpirationDate' tag is missing
        if resource.tags is None or 'ExpirationDate' not in resource.tags:
            resources_not_scheduled_for_expiration.append({
                'name': resource.name,
                'url': get_resource_url(resource)
            })
            continue

        expiration_date_str = resource.tags.get('ExpirationDate')

        # Try parsing expiration date as a datetime
        try:
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            # If parsing fails, try parsing as a date
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')

        # Check if expiration date is within the next 7 days
        if expiration_date <= datetime.utcnow() + timedelta(days=7):
            resources_scheduled_for_expiration.append({
                'name': resource.name,
                'expiration_date': expiration_date.strftime('%Y-%m-%d %H:%M:%S'),
                'url': get_resource_url(resource)
            })
        else:
            resources_not_scheduled_for_expiration.append({
                'name': resource.name,
                'url': get_resource_url(resource)
            })

    # Render template with resource lists
    return render_template('index.html',
                           resources_scheduled_for_expiration=resources_scheduled_for_expiration,
                           resources_not_scheduled_for_expiration=resources_not_scheduled_for_expiration)

@app.route('/update-tag', methods=['POST'])
def update_tag():
    # Authenticate with Azure
    resource_client = authenticate_azure()

    action = request.form.get('action')
    selected_resources = request.form.getlist('resource')

    for resource_name in selected_resources:
        resource = get_resource_by_name(resource_client, resource_name)
        if resource:
            if action == 'remove':
                remove_expiration_date_tag(resource_client, resource.id)  # Pass resource ID
            elif action == 'tag':
                tag_expiration_date(resource_client, resource.id)  # Pass resource ID

    # Introduce a delay of 1 second before redirecting
    time.sleep(1)

    return redirect(url_for('index'))


def authenticate_azure():
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_client = ResourceManagementClient(credential, subscription_id)
    return resource_client

def get_resources(resource_client):
    return list(resource_client.resources.list())

def get_resource_by_name(resource_client, resource_name):
    for resource in get_resources(resource_client):
        if resource.name == resource_name:
            return resource
    return None

def get_resource_url(resource):
    return f"https://portal.azure.com/#resource{resource.id}"

def remove_expiration_date_tag(resource_client: ResourceManagementClient, resource_id: str):
    # Retrieve the resource
    resource = resource_client.resources.get_by_id(resource_id, api_version='2023-05-01')

    # Remove the ExpirationDate tag
    if resource.tags and 'ExpirationDate' in resource.tags:
        resource.tags.pop('ExpirationDate')

        # Update the resource to remove the tag
        resource_client.resources.begin_create_or_update_by_id(resource_id, parameters=resource, api_version='2023-05-01')
    else:
        print(f"Resource {resource_id} does not have the 'ExpirationDate' tag.")

def tag_expiration_date(resource_client: ResourceManagementClient, resource_id: str):
    # Retrieve the resource
    resource = resource_client.resources.get_by_id(resource_id, api_version='2023-05-01')

    # Calculate expiration date (7 days from now)
    expiration_date = datetime.utcnow() + timedelta(days=7)

    # Format expiration date as string
    expiration_date_str = expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Update resource tags
    resource.tags['ExpirationDate'] = expiration_date_str

    # Update the resource to add the tag
    resource_client.resources.begin_create_or_update_by_id(resource_id, parameters=resource, api_version='2023-05-01')

if __name__ == '__main__':
    app.run(debug=True)
