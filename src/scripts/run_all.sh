#!/bin/bash

# Run the Python scripts in order using the current virtual environment
echo "Running count_words.py..."
python count_words.py

echo "Running download_titles.py..."
python download_titles.py

echo "Running download_versions.py..."
python download_versions.py

echo "All scripts completed!"