import re

# Read the format file for the SAS dataset
def parse_sas_formats(file_path):
    # Read the entire file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dictionary to store all formats
    formats_dict = {}

    # Compile the regex
    value_block_pattern = re.compile(r"VALUE\s+(\$?\w+)\s*(.*?)\s*;\s*\n", re.DOTALL | re.IGNORECASE)
    
    # Regex to capture mappings
    mapping_pattern = re.compile(r"(['\"]([^'\"]+)['\"]|-*.*(\d*))\s*=\s*(?:('([^']+)')|(\"([^\"]+)\"))", re.IGNORECASE)

    # For each value block, parse the mapping and update the formats dictionary
    for value_match in value_block_pattern.finditer(content):
        format_name = value_match.group(1).strip()
        mappings_text = value_match.group(2)
        mapping_dict = {}

        for m in mapping_pattern.finditer(mappings_text):
            for group in m.groups():
                if group is not None:
                    key = group.strip()
                    if is_integer(key):
                        key_conv = int(key)
                    elif "'" in key:
                        key_conv = f"'{key.split("'")[1].strip()}'"
                    elif "\"" in key:
                        key_conv = f"'{key.split("\"")[1].strip()}'"
                    else:
                        key_conv = key
                    break
            
            for i in range(len(m.groups()), 0, -1):
                if m.group(i) is not None and m.group(i) != '':
                    value = m.group(i)
                    break

            mapping_dict[key_conv] = value
            
        formats_dict[format_name] = mapping_dict
    return formats_dict

# Check if a given value is an integer (positive or negative)
def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False