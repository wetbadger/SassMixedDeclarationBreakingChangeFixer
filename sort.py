import parse
import pprint

def get_sass(filename):
    with open(filename, 'r') as f:
        sass = f.read()
        return '{' + sass + '}'

def sort_sass(sass_list):
    def is_function_call(s):
        """Check if string is part of a function call"""
        if not isinstance(s, str):
            return False
        s = s.strip()
        return ('(' in s and 
                not s.endswith(';') and 
                (s.startswith('@') or ':' in s))

    def get_function_call_parts(lst, start_idx):
        """Get all parts of a multi-line function call"""
        parts = [lst[start_idx]]
        balance = lst[start_idx].count('(') - lst[start_idx].count(')')
        
        i = start_idx + 1
        while i < len(lst) and balance != 0:
            if i >= len(lst):
                break
            curr = lst[i]
            if not isinstance(curr, str):
                break
            balance += curr.count('(') - curr.count(')')
            parts.append(curr)
            i += 1
        return parts

    def is_property(s):
        if not isinstance(s, str):
            return False
        s = s.strip()
        # Check if it's a property declaration (contains colon)
        if ':' in s:
            return s.endswith(';')
        # Check if it's a continuation line of a property
        prev_non_empty = get_previous_non_empty_line(s)
        return (s.endswith(';') and 
                prev_non_empty and 
                not prev_non_empty.endswith(';') and 
                not ':' in s)

    def get_previous_non_empty_line(current_line):
        """Helper function to look at previous non-empty line in the list"""
        if not hasattr(get_previous_non_empty_line, "full_list"):
            return None
        try:
            idx = get_previous_non_empty_line.full_list.index(current_line)
            for i in range(idx - 1, -1, -1):
                prev = get_previous_non_empty_line.full_list[i]
                if isinstance(prev, str) and prev.strip():
                    return prev.strip()
        except ValueError:
            return None
        return None

    def flatten_list(lst):
        """Helper function to flatten list for line context"""
        result = []
        for item in lst:
            if isinstance(item, list):
                result.extend(flatten_list(item))
            else:
                result.append(item)
        return result

    def is_selector_block(item):
        return (isinstance(item, list) and 
                len(item) >= 2 and 
                isinstance(item[0], str) and 
                isinstance(item[1], list))

    def process_block(lst):
        if not isinstance(lst, list):
            return lst
        
        if is_selector_block(lst):
            header = lst[0]
            contents = lst[1:]
            return [header] + [process_block(content) for content in contents]
        
        # Store the full flattened list for context
        get_previous_non_empty_line.full_list = flatten_list(lst)
        
        # Group properties and non-properties while preserving order
        properties = []
        non_properties = []
        i = 0
        while i < len(lst):
            item = lst[i]
            
            # Handle function calls first
            if is_function_call(item):
                function_parts = get_function_call_parts(lst, i)
                non_properties.extend(function_parts)
                i += len(function_parts)
                continue
                
            # Handle properties
            if is_property(item):
                # Check if this is the start of a multi-line property
                if ':' in item and not item.strip().endswith(';'):
                    property_parts = [item]
                    j = i + 1
                    while j < len(lst):
                        next_item = lst[j]
                        if isinstance(next_item, str) and not ':' in next_item:
                            property_parts.append(next_item)
                            if next_item.strip().endswith(';'):
                                break
                        else:
                            break
                        j += 1
                    properties.extend(property_parts)
                    i = j + 1
                    continue
                properties.append(item)
            else:
                non_properties.append(process_block(item))
            i += 1
        
        return properties + non_properties

    return process_block(sass_list)

def generate_sorted_list(filename):
    input_str = get_sass(filename)
    nested_list = parse.parse(input_str)
    nested_list = parse.format_nested_list(nested_list)
    sorted_list = []
    
    for rule in nested_list:
        sorted_list.append(sort_sass(rule))

    while len(sorted_list) == 1:
        sorted_list = sorted_list[0]

    return sorted_list

if __name__ == "__main__":
    sorted_list = generate_sorted_list("test.sass")
