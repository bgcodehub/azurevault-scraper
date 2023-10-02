import subprocess
import csv
import sys
import json

def set_subscription(subscription_id):
    """
    Set a specific subscription using Azure CLI.
    """
    print(f"Setting subscription {subscription_id}...")
    try:
        subprocess.check_call(["C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd", "account", "set", "--subscription", subscription_id])
        print(f"Subscription {subscription_id} set successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting subscription {subscription_id}: {e}")
        sys.exit(1)

def get_secret_names_from_file(filename):
    """
    Read the list of secret names from a file.
    """
    print(f"Fetching secret names from {filename}...")
    with open(filename, 'r') as file:
        secrets = [line.strip() for line in file if line.strip()]
    print(f"Found {len(secrets)} secret names.")
    return secrets

def get_secret_value(secret_name, vault_name):
    """
    Use Azure CLI to get the value of a specific secret.
    """
    print(f"Fetching value for secret {secret_name} from vault {vault_name}...")
    try:
        result = subprocess.check_output(["C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd", "keyvault", "secret", "show", "--name", secret_name, "--vault-name", vault_name])
        data = json.loads(result)
        return data["name"], data["value"]
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        return None, None

def parse_secret(secret_value):
    """
    Parse the secret value into a dictionary.
    """
    elements = secret_value.split()
    parsed = {}
    for element in elements:
        key, value = element.split('=')
        parsed[key] = value
    return parsed

def write_to_csv(secrets, csv_filename):
    """
    Write secret names and values to a CSV file.
    """
    print(f"Writing secrets to {csv_filename}...")
    try:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['name'] + [f"key{i}" for i in range(1, len(secrets) + 1)]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for secret in secrets:
                secret_name, secret_value = secret
                parsed_secret = parse_secret(secret_value)
                row_data = {'name': secret_name, **parsed_secret}
                writer.writerow(row_data)
        print(f"Successfully wrote secrets to {csv_filename}.")
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

