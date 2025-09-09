#!/usr/bin/env bash

# This script sets various environment variables for the Label Studio application.
# These variables control paths, features, data handling, and authentication.

# === Auxiliary path variables ===
# Set directory where this script is located.
script_dir="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"

# Set Ppth to the directory where Label Studio stores project data
data_path="$(realpath "$script_dir/../data")"

# Path to the SQLite database file used by Label Studio.
db_path="$script_dir/db.sqlite3"

# Base directory for Label Studio's configuration and internal data.
config_path="$script_dir/label_studio"

# === Local files setup ===
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT="$data_path"
export LABEL_STUDIO_PORT=8000

# === Label Studio feature flags ===
# These flags enable or disable specific experimental or development features.
# Set to 'true' to enable, 'false' to disable.
export ff_front_dev_1682_model_version_dropdown_070622_short=false
export fflag_feat_front_lsdv_e_297_increase_oss_to_enterprise_adoption_short=false

# === Data upload settings ===
export DATA_UPLOAD_MAX_MEMORY_SIZE=262144000 # 250 * 1024 * 1024 (bytes)
export DATA_UPLOAD_MAX_NUMBER_FILES=50000

# === Configuration and annotation storage ===
export LABEL_STUDIO_DATABASE="$db_path"
export LABEL_STUDIO_BASE_DATA_DIR="$config_path"
export EDITOR_KEYMAP='{"annotation:submit":{"key": "enter","description": "My Custom Submit Hotkey!"}}'

# === Authentication settings ===
export LABEL_STUDIO_USERNAME="user@email.com"
export LABEL_STUDIO_PASSWORD="mypassword123456"
export LABEL_STUDIO_USER_TOKEN="my_token" 
# If true, users cannot sign up without an invitation link.
export LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK=false

