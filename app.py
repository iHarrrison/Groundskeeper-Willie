from flask import Flask, render_template
import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

app = Flask(__name__)

@app.route('/')
def index():
    # Authenticate with Azure
    resource_client = authenticate_azure()

    # Retrieve resource names
    resource_names = get_resource_names(resource_client)

    # Render template with resource names
    return render_template('index.html', resource_names=resource_names)

def authenticate_azure():
    credential = DefaultAzureCredential()
    subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    resource_client = ResourceManagementClient(credential, subscription_id)
    return resource_client

def get_resource_names(resource_client):
    resource_names = []
    resources = resource_client.resources.list()
    for resource in resources:
        resource_names.append(resource.name)
    return resource_names

if __name__ == '__main__':
    app.run(debug=True)
