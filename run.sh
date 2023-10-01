#!/bin/bash

# Function to generate .env from arguments and .env.sample
generate_env() {
    # Iterate through the provided arguments
    while [[ "$#" -gt 0 ]]; do
        # Extract the argument name and convert it to uppercase and replace "-" with "_"
        var_name=$(echo $1 | cut -d'=' -f1 | tr '[:lower:]-' '[:upper:]_')
        # Extract the value of the argument
        value=$(echo $1 | cut -d'=' -f2)
        
        # If the variable name exists in .env.sample, update the value in .env
        if grep -q "^$var_name=" .env.sample; then
            sed -i "s/^$var_name=.*/$var_name=$value/" .env
        fi

        shift
    done
}

# If .env doesn't exist, copy from .env.sample
if [ ! -f .env ]; then
    cp .env.sample .env
fi

# If arguments are provided, update .env
if [ "$#" -gt 0 ]; then
    generate_env "$@"
fi

# Read DEV value from .env
source .env

if [ "$DEV" = "true" ]; then
    echo "Running in DEV mode"
    docker compose -f docker-compose.yml -f docker-compose.override.yml up --build
else
    docker compose -f docker-compose.yml up --build
fi
