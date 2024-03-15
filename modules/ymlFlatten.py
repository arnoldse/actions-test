import os
import sys
import yaml
import jsonref


def flatten_reference(file_path):
    with open(file_path, 'r') as file1:
        data = yaml.safe_load(file1)
        # data = jsonref.load(file1, yaml.Loader)
    # print(f"Original Data: {data}\n\n")

    flattened_data = flatten(data)
    # print(f"Flattened Data: {flattened_data}\n\n")

    output_filename = os.path.splitext(file_path)[0] + "_flat.yaml"

    with open(output_filename, 'w') as file_out:
        yaml.dump(flattened_data, file_out)

    return output_filename

def flatten(data):
    if isinstance(data, dict):
        if '$ref' in data:
            try:
                ref_path = data['$ref']
                print(f"Reference Found: {ref_path}")
                recursive_path = os.path.join(os.path.dirname(input_filename),(ref_path))
                if os.path.exists(recursive_path):
                    with open(recursive_path, 'r') as file2:
                        file2_data = yaml.safe_load(file2)
                    return flatten(file2_data)  # Recursively flatten the referenced data
                else:
                    # raise FileNotFoundError(f"File {ref_path} referenced in {data} does not exist.")
                    print(f"File {ref_path} referenced in {data} does not exist.")
                    return {key: flatten(value) for key, value in data.items()}  # Copy reference
            except:
                print(f"{ref_path} in {data} is missing.")
        else:
            return {key: flatten(value) for key, value in data.items()}  # Flatten the other keys recursively
    elif isinstance(data, list):
        return [flatten(item) for item in data]  # Flatten the list items recursively

    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ymlFlatten.py <filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    print(sys.argv[1])

    try:
        flattened_filename = flatten_reference(input_filename)
        print(f"Flattening successful! Flattened data saved in {flattened_filename}")
    except Exception as e:
        print(f"Error occurred while flattening: {str(e)}")
