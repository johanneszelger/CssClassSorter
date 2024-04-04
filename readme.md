# HTML Class Sorter Script

This script organizes and sorts the class names within HTML files according to predefined rules and weights. It scans a user-specified directory for HTML files, then reorders the class names in each file's class attributes based on the weights for different class patterns. The aim is to ensure consistency and improve readability in HTML class usage.

## Features

- **Pattern-based Class Weighting:** Assigns weights to different class patterns to define their sort order.
- **Responsive Prefix Support:** Manages responsive utility classes with prefixes (e.g., sm, md, lg, xl, 2xl) for different screen sizes.
- **Directory Scanning:** Finds and processes all HTML files in a specified directory.
- **In-place File Modification:** Modifies HTML files directly to sort class names within class attributes.

## Requirements

- Python 3.x
- No external Python packages are required.

## Usage

1. **Set Directory Path:**
   Provide the directory path as a command-line argument when running the script. Ensure this directory contains the HTML files you wish to sort.

```bash
python html_class_sorter.py <path_to_directory>