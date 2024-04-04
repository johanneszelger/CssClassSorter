import os
import re
import sys

media = "(sm|md|lg|xl|2xl):"

# Define regex patterns and associated weights
class_weights = {}

curr_weight = 1
class_weights[re.compile(r'^(hidden)$')] = curr_weight  # Visibility classes
class_weights[re.compile('^' + media + r'(hidden|visible)$')] = curr_weight + 0.1

curr_weight += 1
class_weights[re.compile(r'^(flex|block|inline|inline-block)$')] = curr_weight  # Display classes
class_weights[re.compile('^' + media + r'(flex|block|inline|inline-block)$')] = curr_weight + 0.1

# Default weight for classes that don't match any pattern
default_weight = 99999


def get_class_weight(class_name):
    """Get the weight for a class name based on defined patterns."""
    for pattern, weight in class_weights.items():
        if pattern.match(class_name):
            return weight
    return default_weight


def find_files_with_ext(directory, ext):
    scss_files = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(ext):
                # Append the file path if it ends with .scss
                scss_files.append(os.path.join(root, file))
    return scss_files

# Check if a directory argument is provided
if len(sys.argv) < 2:
    print("Usage: python html_class_sorter.py <directory>")
    sys.exit(1)

directory_to_search = sys.argv[1]

# Find SCSS files
html_files_found = find_files_with_ext(directory_to_search, ".html")

# Print the list of found SCSS files
print(f"Found HTML files:\n{html_files_found}")


def sort_class_names(html_content):
    """Sort class names in class attributes while preserving case of attribute names."""

    def sort_classes(match):
        full_match = match.group(0)
        class_names = match.group(1).split()
        sorted_class_names = sorted(class_names, key=lambda x: (get_class_weight(x)))
        return full_match.replace(match.group(1), " ".join(sorted_class_names))

    # This regex finds class attributes and captures their values for sorting
    # It's designed to match the class attribute and its values, ignoring case and spaces
    return re.sub(r'class="([^"]*)"', sort_classes, html_content, flags=re.IGNORECASE)


def process_html_file(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        html_content = file.read()
        sorted_html_content = sort_class_names(html_content)

        # Overwrite the file with sorted class names
        file.seek(0)
        file.write(sorted_html_content)
        file.truncate()

        print(f'Processed {file_path}')


for f in html_files_found:
    process_html_file(f)
