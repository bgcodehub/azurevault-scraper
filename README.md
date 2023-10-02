# Azure Secrets Exporter

A Python script to export secrets from an Azure Key Vault to a CSV file.

## Prerequisites

- Azure CLI must be installed on your machine.
- Python must be installed and available from your command line or terminal.

## Setup and Usage

### 1. Clone the Repository

First, clone the repository to your local machine. Navigate to the directory where you want to keep the project and run:

`git clone https://github.com/bgcodehub/vault_scraper`

### 2. Generate the List of Secrets

Before running the Python script, you must generate a list of all the secrets in your Key Vault. To do this, use the following command:

`az keyvault secret list --vault-name WUS2-PC-OPS-TF-PRD-kvt --query "[].name" -o tsv > secrets_list.txt`

This will generate a `secrets_list.txt` file with the names of all secrets in the specified vault.

### 3. Update Script Configuration

In the `app.py` script, replace `YOUR_SUBSCRIPTION_ID` with your Azure subscription ID and `YOUR_KEYVAULT_NAME` with the name of your Azure Key Vault.

### 4. Run the Script

Execute the Python script to fetch the secret values and write them to a CSV file:

`python app.py`

Once the script completes successfully, you should see a `secrets.csv` file in the project directory containing the names and values of all the secrets.

## Note

Ensure you treat the `secrets.csv` file with care as it contains sensitive information. Avoid committing this file to public repositories or sharing it without encryption.
