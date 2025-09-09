#!/usr/bin/env bash
# Run the Label Studio app

# Set script directory
script_dir="$(dirname "$0")"

# Run app
source "$script_dir/config/env.sh"

label-studio -db "$LABEL_STUDIO_DATABASE"
