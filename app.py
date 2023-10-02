import subprocess
import csv
import sys
import json

def set_subscription(subscription_id):
    """
    Set a specific subscription using Azure CLI.
    """
    try:
        subprocess.check_call(["az", "account", "set", "--subscription", subscription_id])
    except subprocess.CalledProcessError as e:
        print(f"Error setting subscription {subscription_id}: {e}")
        sys.exit(1)

def get_secret_names_from_file(filename):
    """
    Read the list of secret names from a file.
    """
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_secret_value(secret_name, vault_name):
    """
    Use Azure CLI to get the value of a specific secret.
    """
    try:
        result = subprocess.check_output(["az", "keyvault", "secret", "show", "--name", secret_name, "--vault-name", vault_name])
        data = json.loads(result)
        return data["name"], data["value"]
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None, None

def write_to_csv(secrets, csv_filename):
    """
    Write secret names and values to a CSV file.
    """
    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['name', 'value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for secret in secrets:
                writer.writerow({'name': secret[0], 'value': secret[1]})
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def main():
    # Subscription ID and Key Vault name
    SUBSCRIPTION_ID = "YOUR_SUBSCRIPTION_ID"
    VAULT_NAME = "YOUR_KEYVAULT_NAME"
    set_subscription(SUBSCRIPTION_ID)

    # Retrieve secret names from file
    secret_names = get_secret_names_from_file("secrets_list.txt")
    
    secrets_to_export = []
    
    for secret_name in secret_names:
        name, value = get_secret_value(secret_name, VAULT_NAME)
        if name and value:
            secrets_to_export.append((name, value))
    
    write_to_csv(secrets_to_export, "secrets.csv")

if __name__ == "__main__":
    main()
