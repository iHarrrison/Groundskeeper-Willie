# Groundskeeper-Willie
An open-source automated tool that cleans up a given cloud subscription/resources when given expiration criteria. It also comes with a helper UI created with the Flask framework.

## Who Is Groundskeeper For?
Groundskeeper is being designed for everyone. This included large businesses that contain multiple Azure subscriptions
that each contain lots of resources, and for the smaller businesses/passion developers who may only have a smaller
footprint in the cloud.<br>

## How to Set Up Groundskeeper
Please ensure the Azure CLI is installed on the machine. <br>

In order to set up Groundskeeper, please pull the repository. 
From here, you need to enter your Azure Subscription ID in the ".env.template" file. 
Please rename this file to just ".env".<br>

## How Groundskeeper Works
Groundskeeper Willie is designed to check for an ExpirationDate tag. If it finds it and the date matches the date of the job being ran, it will delete the resource. It skips any resources that have an Azure lock on it, so it is advised that any resources that are important are given a resource lock. Reading on azure resource locks can be found here - https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources?tabs=json

It also comes with a Dry Run flag - set this to false to actually perform deletion (it is recommended this happens once you are ready for it to begin groundskeeping your subscription) and set it to True to test/ensure set-up has worked. The True flag will not perform any deletions, but it will inform you what it would have deleted.

## Groundskeeper Log
A log will be created upon Groundskeeper running, and it will be stored in the root directory of the project. Here, you can see a full audit log of what it has done upon running.

## Groundskeeper Dashboard
As part of this project, a UI has been created via the flask framework. This ui will search the given Azure Subscription Id in the .env file, and return two lists of resources. One list will contain resources scheduled for deletion in the next 7 days, and another will conatain a list of resources that do not have an ExpirationDate tag. From here, you can untag a resource for expiration, or bring one forward for deletion by applying an ExpirationDate tag all through the UI. You are also able to go directly to the resource should you choose to put a resource lock on it, or to gain further information about the resource.

## Further Information
Groundskeeper-Willie is a project for my Production Project Module at Leeds Beckett University. It is part of my final year
of my Computer Science Degree. <br>

It aims to test whether the management of an Azure Cloud resource, handled by this tool alone, is feasible.
This is done with the help of Azure tags and in the real working world, CRON jobs - the idea being Groundskeeper is run daily.

As this is my project for university, I will be able to post my accompanying documents
and reports on my findings after I graduate.
