#!/bin/bash

CONFIG_DIR="/workspace/config"

TEMPLATE_DIR="/workspace/config_template"

if [ ! -d "$CONFIG_DIR" ] || [ -z "$(ls -A $CONFIG_DIR)" ]; then
    echo "Importing configs from template..."
    mkdir -p "$CONFIG_DIR"
    cp -r "$TEMPLATE_DIR"/* "$CONFIG_DIR/" || exit 1
fi

echo "Running label studio..."
./run.sh
