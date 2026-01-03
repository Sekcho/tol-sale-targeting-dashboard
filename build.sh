#!/usr/bin/env bash
# Don't exit on error for database init
set -o errexit

echo "===== Starting build process ====="

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "===== Build process completed ====="
echo "Note: Database will be initialized at runtime by app_sales_v2.py"
