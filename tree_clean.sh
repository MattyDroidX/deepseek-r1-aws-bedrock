#!/bin/bash

# Define the root directory (current directory by default)
ROOT_DIR=${1:-.}

# Exclude directories and files
EXCLUDE_DIRS=(
    "node_modules"
    "__pycache__"
    ".git"
    ".venv"
    ".DS_Store"
    "venv"
    "dist"
    "build"
    "coverage"
    ".pytest_cache"
    "env"
    "bedrock_env"
)

# Convert exclude array into `--exclude` arguments for `tree`
EXCLUDE_ARGS=()
for DIR in "${EXCLUDE_DIRS[@]}"; do
    EXCLUDE_ARGS+=("-I" "$DIR")
done

# Run tree command with exclusions
tree "$ROOT_DIR" "${EXCLUDE_ARGS[@]}"

