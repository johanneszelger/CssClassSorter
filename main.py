import os
import re
import sys

media = "(sm|md|lg|xl|2xl):"
colors = "(primary|light|dark|white|surface|color-secondary|[0-9]+|[a-z]+(-[a-z]+)*-[0-9]+)"
sizes = "(none|xs|sm|md|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl|10xl|full)"
weights = "(thin|extralight|light|normal|medium|semibold|bold|extrabold|black)"
state = ("(hover|active|visited|focus|disabled|first|last|odd|even|group-hover|group-focus|focus-within|checked):")
numeric_modifiers = "([0-9/]+|auto|[\[[0-9]+(px|rem|%)\]])"

# Define regex patterns and associated weights
class_weights = {}

##################################
##### POSITIONING AND SIZING #####
##################################
# Visibility classes
curr_weight = 1
class_weights[re.compile(r'^(hidden)$')] = curr_weight

# Display classes
curr_weight += 1
class_weights[re.compile(r'^(flex|block|inline|inline-block)$')] = curr_weight

# overflow
curr_weight += 1
class_weights[re.compile(
    r'^(overflow-auto|overflow-hidden|overflow-visible|overflow-scroll|overflow-x-auto|overflow-x-hidden|overflow-x-visible|overflow-x-scroll|overflow-y-auto|overflow-y-hidden|overflow-y-visible|overflow-y-scroll)$')] = curr_weight

# position
curr_weight += 1
class_weights[re.compile(r'^(static|fixed|absolute|relative|sticky)$')] = curr_weight

# placement
curr_weight += 1
class_weights[re.compile(
    rf'^(top-{numeric_modifiers}|right-{numeric_modifiers}|bottom-{numeric_modifiers}|left-{numeric_modifiers})$')] = curr_weight

# flex directions
curr_weight += 1
class_weights[re.compile(r'^(flex-row|flex-row-reverse|flex-col|flex-col-reverse)$')] = curr_weight

# flex wrap
curr_weight += 1
class_weights[re.compile(r'^(flex-nowrap|flex-wrap|flex-wrap-reverse)$')] = curr_weight

# flex grow
curr_weight += 1
class_weights[re.compile(r'^(flex-(1|auto|initial|none))$')] = curr_weight
curr_weight += 1
class_weights[re.compile(r'^(flex-grow(-0|-1)|flex-shrink(-0|-1))$')] = curr_weight

# flex gap
curr_weight += 1
class_weights[re.compile(r'^(gap-[0-9]+|row-gap-[0-9]+|column-gap-[0-9]+)$')] = curr_weight

# flex order
curr_weight += 1
class_weights[re.compile(r'^(order-[0-9]+)$')] = curr_weight

# justify content
curr_weight += 1
# tailwind
class_weights[re.compile(
    r'^(justify-start|justify-end|justify-center|justify-between|justify-around|justify-evenly)$')] = curr_weight
# primeflex
class_weights[re.compile(
    r'^(justify-content-start|justify-content-end|justify-content-center|justify-content-between|justify-content-around|justify-content-evenly)$')] = curr_weight

# align content
curr_weight += 1
# tailwind
class_weights[re.compile(
    r'^(content-start|content-end|content-center|content-between|content-around|content-evenly)$')] = curr_weight
# primeflex
class_weights[re.compile(
    r'^(align-content-start|align-content-end|align-content-center|align-content-between|align-content-around|align-content-evenly)$')] = curr_weight

# align items
curr_weight += 1
# tailwind
class_weights[re.compile(r'^(items-start|items-end|items-center|items-baseline|items-stretch)$')] = curr_weight
# primeflex
class_weights[re.compile(
    r'^(align-items-start|align-items-end|align-items-center|align-items-baseline|align-items-stretch)$')] = curr_weight

# align self
curr_weight += 1
# tailwind
class_weights[re.compile(r'^(self-start|self-end|self-center|self-baseline|self-stretch)$')] = curr_weight
# primeflex
class_weights[re.compile(
    r'^(align-self-start|align-self-end|align-self-center|align-self-baseline|align-self-stretch)$')] = curr_weight

# widths
curr_weight += 1
class_weights[
    re.compile(rf'^(w-{numeric_modifiers}|min-w-{numeric_modifiers}|max-w-{numeric_modifiers})$')] = curr_weight

# heights
curr_weight += 1
class_weights[
    re.compile(rf'^(h-{numeric_modifiers}|min-h-{numeric_modifiers}|max-h-{numeric_modifiers})$')] = curr_weight

# margins
curr_weight += 1
class_weights[re.compile(rf'^m-{numeric_modifiers}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(rf'^mx-{numeric_modifiers}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(rf'^my-{numeric_modifiers}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(rf'^m[tblr]-{numeric_modifiers}$')] = curr_weight

# paddings
curr_weight += 1
class_weights[re.compile(rf'^p-{numeric_modifiers}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(rf'^px-{numeric_modifiers}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(rf'^py-{numeric_modifiers}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(rf'^p[tblr]-{numeric_modifiers}$')] = curr_weight

##################################
########### DECORATION ###########
##################################
# shadow
curr_weight += 1
class_weights[re.compile(r'^shadow-([0-9]|none)$')] = curr_weight

# background
curr_weight += 1
class_weights[re.compile(rf'^bg-{colors}$')] = curr_weight
curr_weight += 1
class_weights[re.compile(r'^bg-(repeat|no-repeat|repeat-x|repeat-y|round|space)$')] = curr_weight
curr_weight += 1
class_weights[re.compile(r'^bg-(auto|cover|contain)$')] = curr_weight
curr_weight += 1
class_weights[
    re.compile(r'^bg-(bottom|center|left|left-bottom|left-top|right|right-bottom|right-top|top)$')] = curr_weight

# Border
# width
curr_weight += 1
class_weights[re.compile(r'^border-([0-9]|none)$')] = curr_weight
curr_weight += 1
class_weights[re.compile(r'^border-x-([0-9]|none)$')] = curr_weight
curr_weight += 1
class_weights[re.compile(r'^border-y-([0-9]|none)$')] = curr_weight
curr_weight += 1
class_weights[re.compile(r'^border-[tlrb]-([0-9]|none)$')] = curr_weight
# style
curr_weight += 1
class_weights[re.compile(r'^border-(solid|dashed|dotted|double)$')] = curr_weight
# color
curr_weight += 1
class_weights[re.compile(rf'^border-{colors}$')] = curr_weight
# radius
curr_weight += 1
# tailwind
class_weights[re.compile(rf'^rounded(-{sizes})*$')] = curr_weight
class_weights[re.compile(rf'^rounded-[tlrbse]{1, 2}(-{sizes})*$')] = curr_weight
# primeflex
class_weights[re.compile(rf'^border-noround(-(left|right|top|bottom))*$')] = curr_weight
class_weights[re.compile(rf'^border-circle(-(left|right|top|bottom))*$')] = curr_weight
class_weights[re.compile(rf'^border-round$')] = curr_weight
class_weights[re.compile(rf'^border-round(-(left|right|top|bottom))*-{sizes}$')] = curr_weight

##################################
########### TYPOGRAPHY ###########
##################################
# color
curr_weight += 1
class_weights[re.compile(rf'^text-{colors}$')] = curr_weight
# font size
curr_weight += 1
class_weights[re.compile(rf'^text-{sizes}$')] = curr_weight
# font weight
curr_weight += 1
class_weights[re.compile(rf'^font-{weights}$')] = curr_weight
# align
curr_weight += 1
class_weights[re.compile(r'^text-(left|right|center|justify|start|end)$')] = curr_weight
# overflow
curr_weight += 1
class_weights[re.compile(r'^(truncate|text-overflow-(ellipsis|clip))$')] = curr_weight
# decoration
curr_weight += 1
class_weights[re.compile(r'^line-through|underline|no-underline|overline$')] = curr_weight
# tranform
curr_weight += 1
class_weights[re.compile(r'^uppercase|lowercase|capitalize|normal-case$')] = curr_weight
# line height
curr_weight += 1
# tailwind
class_weights[re.compile(r'^leading-([3-9]+|none|tight|snug|normal|relaxed|loose)$')] = curr_weight
# primeflex
class_weights[re.compile(r'^line-height-[1-4]$')] = curr_weight
# vertical align
curr_weight += 1
# tailwind
class_weights[re.compile(r'^align-(baseline|top|middle|bottom|text-top|text-bottom|sub|super)$')] = curr_weight
# primeflex
class_weights[re.compile(r'^vertical-align-(baseline|top|middle|bottom|text-top|text-bottom|sub|super)$')] = curr_weight
# list type
curr_weight += 1
class_weights[re.compile(r'^list-(none|disc|decimal)$')] = curr_weight

##################################
########### ANIMATION ###########
##################################
# TODO

# Default weight for classes that don't match any pattern
default_weight = 99999

##################################
##### States and responsive ######
##################################
enriched_class_weights = {}
for pattern, weight in class_weights.items():
    enriched_class_weights[re.compile(f'{pattern.pattern}')] = weight
    enriched_class_weights[re.compile(f'{state}{pattern.pattern}')] = weight + 0.1
    enriched_class_weights[re.compile(f'{media}{pattern.pattern}')] = weight + 0.2
    enriched_class_weights[re.compile(f'{media}{state}{pattern.pattern}')] = weight + 0.3

    # dark mode
    enriched_class_weights[re.compile(f'dark:{state}{pattern.pattern}')] = weight + 0.4
    enriched_class_weights[re.compile(f'dark:{media}{pattern.pattern}')] = weight + 0.5
    enriched_class_weights[re.compile(f'dark:{media}{state}{pattern.pattern}')] = weight + 0.6


def get_class_weight(class_name):
    """Get the weight for a class name based on defined patterns."""
    for pattern, weight in enriched_class_weights.items():
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
        sorted_class_names = sorted(class_names, key=lambda x: (get_class_weight(x), x))
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
