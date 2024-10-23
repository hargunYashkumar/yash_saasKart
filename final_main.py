import json
from collections import defaultdict

# Function to recursively traverse and merge nested dictionaries with unique values, data types, and nullable information
def merge_nested_dicts(d, parent_path='', merged_dict=None):
    if merged_dict is None:
        merged_dict = defaultdict(lambda: {'types': set(), 'nullable': False, 'examples': set()})
    
    if isinstance(d, dict):
        for key, value in d.items():
            current_path = f"{parent_path}.{key}" if parent_path else key
            if isinstance(value, dict):
                # Recursively merge dictionaries within dictionaries
                merge_nested_dicts(value, current_path, merged_dict)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        merge_nested_dicts(item, current_path, merged_dict)
                    else:
                        # Add non-dict list items and check their types
                        update_merged_dict(current_path, item, merged_dict)
            else:
                # Add non-dict values and check their types
                update_merged_dict(current_path, value, merged_dict)
    return merged_dict

# Helper function to update merged_dict with value, data types, nullable info, and examples
def update_merged_dict(path, value, merged_dict):
    if value is None:
        merged_dict[path]['nullable'] = True
    else:
        merged_dict[path]['types'].add(type(value).__name__)  # Add the type of the value
    
    merged_dict[path]['examples'].add(value)  # Add value as an example

# Function to handle list lengths, data types, and nullable information
def process_merged_data(merged_data):
    result = {}
    for key, value_info in merged_data.items():
        # Convert sets to lists, handle nullable and list sizes
        types = list(value_info['types'])
        nullable = value_info['nullable']
        examples = list(value_info['examples'])
        
        # Handle more than 4 unique example values
        if len(examples) > 4:
            examples = examples[:4] + ["Too many values"]
        
        # Store the final result in the dictionary
        result[key] = {
            'types': types,
            'nullable': nullable,
            'examples': examples
        }
    return result

# Main function to read input JSON, process, and save result as JSON
def process_json_file(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Process the JSON data
    merged_data = merge_nested_dicts(data)
    
    # Process the merged data for output
    processed_result = process_merged_data(merged_data)
    
    # Save the merged result as a new JSON file
    with open(output_file, 'w') as outfile:
        json.dump(processed_result, outfile, indent=4)
    print(f"Processed data saved to {output_file}")



input_file = 'D:\work_place\Main\KEY_23.json'  # Path to your input JSON file
output_file = 'D:\work_place\Main\key5.json'  # Path to the output file to store the result# Example usage
process_json_file(input_file, output_file)
