# Groundskeeper-Willie
An open-source automated tool that cleans up a given cloud subscription/resources when given expiration criteria.

## Further Information
Groundskeeper-Willie is a project for my Production Project Module at Leeds Beckett University. It is part of my final year
of my Computer Science Degree. <br>

It aims to test whether the management of an Azure Cloud resource, handled by this tool alone, is feasible.
This is done with the help of Azure tags and CRON jobs - the idea being Groundskeeper is run daily.

## Who Is Groundskeeper For?
Groundskeeper is being designed for everyone. This included large businesses that contain multiple Azure subscriptions
that each contain lots of resources, and for the smaller businesses/passion developers who may only have a smaller
footprint in the cloud.<br>

As this is my project for university, I will be able to post my accompanying documents
and reports on my findings after I graduate.

## How to Set Up Groundskeeper
Please ensure the Azure CLI is installed on the machine. <br>

In order to set up Groundskeeper, please pull the repository. 
From here, you need to enter your Azure Subscription ID in the ".env.template" file. 
Please rename this file to just ".env".<br>

## How Groundskeeper Works
Groundskeeper Willie is designed to check for an ExpirationDate tag. If it finds it and the date matches the date of the job, it will delete the resource.

## Groundskeeper Log
A log will be created upon Groundskeeper running, and it will be stored in the root directory of the project. Here, you can see a full audit log of what it has done upon running.