import re
import pprint

def format_sass(sorted_list, indent_level=-1):
    if isinstance(sorted_list, str):
        return sorted_list
    
    # Calculate indentation strings
    base_indent = "  " * indent_level
    inner_indent = "  " * (indent_level + 1)
    
    # Process nested elements
    elements = []
    for x in sorted_list:
        formatted = format_sass(x, indent_level + 1)
        # Skip elements that are just braces and whitespace
        #if formatted.strip():
        elements.append(formatted)
    
    # Join elements with proper indentation
    if elements:
        # Special case: if the first element doesn't contain newlines
        # or is not just braces, it's a selector
        first_elem = elements[0]
        if "\n" not in first_elem:
            # Preserve original whitespace around the selector
            result = first_elem.rstrip() + " {\n"
            # Add middle elements
            result += "".join(inner_indent + e + "\n" for e in elements[1:-1])
            # Add closing brace with proper indentation
            if len(elements) > 1:
                result += base_indent + "}"
            return result
        else:
            middle_content = "".join(elements)
            #return "\n" + base_indent + "{" + middle_content + "\n" + base_indent + "}"
            return "{" + middle_content + "\n" + base_indent + "}"
    else:
        # Handle empty lists by returning braces
        if indent_level >= 0:
            return " {}"

    return ""


def clean_extra_braces(sass_string):
   return re.sub(r'^(?:\s*){([\s\S]*)}$', r'\1', sass_string)

def format(sorted_list):
    sass = format_sass(sorted_list)

    while re.search('^\s*{', sass):
        sass = clean_extra_braces(sass)

    return sass
