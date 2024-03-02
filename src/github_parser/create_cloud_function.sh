#!/bin/bash

# Check for Yandex Cloud CLI
if ! command -v yc &>/dev/null; then
  echo "Yandex Cloud CLI not found. Install and authenticate."
  exit
fi

# Prompt for FOLDER_ID
echo "Enter FOLDER_ID:"
read FOLDER_ID

if [ -z "$FOLDER_ID" ]; then
  echo "FOLDER_ID is required. Exiting."
  exit 1
fi

# Function name
FUNCTION_NAME="parse-github-data"

# Check if the function exists
EXISTING_FUNCTION=$(yc serverless function list --folder-id "$FOLDER_ID" --format json | grep -oP '(?<="name": ")[^"]*' | grep -w "$FUNCTION_NAME")

if [ -n "$EXISTING_FUNCTION" ]; then
  echo "Function with the name '$FUNCTION_NAME' already exists."
else
  echo "Creating function..."
  yc serverless function create --name="$FUNCTION_NAME" --folder-id "$FOLDER_ID"
fi

# Creating a zip archive from the directory
ZIP_PATH="./parse_github_data.py.zip"
zip -r "$ZIP_PATH" .

# Creating a version of cloud function...
echo "Creating a version of cloud function..."

# Prompt for environment variables
echo "Enter POSTGRES_DB:"
read POSTGRES_DB
echo "Enter POSTGRES_USER:"
read POSTGRES_USER
echo "Enter POSTGRES_PASSWORD:"
read POSTGRES_PASSWORD
echo "Enter POSTGRES_HOST:"
read POSTGRES_HOST

yc serverless function version create --function-name="$FUNCTION_NAME" --folder-id "$FOLDER_ID" --runtime python311 \
  --entrypoint parse_github_data.parse_github_data --memory 128m --execution-timeout 600s --source-path "$ZIP_PATH" \
  --environment POSTGRES_DB="$POSTGRES_DB",POSTGRES_USER="$POSTGRES_USER",POSTGRES_PASSWORD="$POSTGRES_PASSWORD",POSTGRES_HOST="$POSTGRES_HOST"
rm "$ZIP_PATH"

# Check if the service account exists
EXISTING_SERVICE_ACCOUNT=$(yc iam service-account list --folder-id "$FOLDER_ID" --format json | grep -oP '(?<="name": ")[^"]*' | grep -w "my-robot")

if [ -n "$EXISTING_SERVICE_ACCOUNT" ]; then
  echo "Service account with the name 'my-robot' already exists."
else
  echo "Creating service account..."
  yc iam service-account create --name my-robot --folder-id "$FOLDER_ID"
fi

SERVICE_ACCOUNT_ID=$(yc iam service-account get --name my-robot --folder-id "$FOLDER_ID" --format json | grep -oP '(?<="id": ")[^"]*')
echo "$SERVICE_ACCOUNT_ID"

# Check if the service account already has access to the folder
EXISTING_ACCESS_BINDING=$(yc resource-manager folder list-access-bindings "$FOLDER_ID" --format json | grep -oP '(?<="id": ")[^"]*' | grep -w "$SERVICE_ACCOUNT_ID")

if [ -n "$EXISTING_ACCESS_BINDING" ]; then
  echo "Service account with the ID '$SERVICE_ACCOUNT_ID' already has access to the folder. Skipping access binding."
else
  echo 'Assigning roles...'
  yc resource-manager folder add-access-binding "$FOLDER_ID" --role editor --subject serviceAccount:"$SERVICE_ACCOUNT_ID"
fi

# Check if the trigger already exists
TRIGGER_NAME="cron-trigger"
EXISTING_TRIGGER=$(yc serverless trigger list --folder-id "$FOLDER_ID" --format json | grep -oP '(?<="name": ")[^"]*' | grep -w "$TRIGGER_NAME")

if [ -n "$EXISTING_TRIGGER" ]; then
  echo "Trigger with the name '$TRIGGER_NAME' already exists. Skipping trigger creation."
else
  echo "Creating a trigger..."
  yc serverless trigger create timer --name "$TRIGGER_NAME" --cron-expression '*/30 * * * ? *' --invoke-function-name "$FUNCTION_NAME" --folder-id "$FOLDER_ID" --invoke-function-service-account-id "$SERVICE_ACCOUNT_ID"
fi

echo "Invoke the function now? ([y]es/n])"

read launch
launch=$(echo "$launch" | tr '[:upper:]' '[:lower:]')

if [[ "$launch" == "y" ]] || [[ "$launch" == "yes" ]]; then
  nohup yc serverless function invoke --name "$FUNCTION_NAME" --folder-id "$FOLDER_ID" > /dev/null 2>&1 &
  echo "Function invoked in the background."
else
  echo "Function not invoked."
fi
