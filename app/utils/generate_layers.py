import os

def generate_mixed_case_alphabet_array_with_format(max_size, start_char, layer_name):
    # Create a combined list of uppercase and lowercase letters
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + [chr(i) for i in range(ord('a'), ord('z') + 1)]
    alphabet_size = len(alphabet)

    # Calculate the starting index in the alphabet array
    start_index = alphabet.index(start_char)

    # Create the formatted output
    result = f"\t{layer_name} = [\n"
    for i in range(max_size):
        row = []
        for j in range(max_size):
            # Calculate the character with the shift applied
            char_index = (start_index + i + j) % alphabet_size  # Wrap around the entire alphabet list
            row.append(alphabet[char_index])
        result += f"\t    {row},\n"
    result += "\t]"
    return result


def generate_empty_grid_with_format(max_size, layer_name):
    result = f"\t{layer_name} = [\n"
    for i in range(max_size):
        row = [0 for _ in range(max_size)]
        result += f"\t    {row},\n"
    result += "\t]"
    return result


def output_to_map(text):
    # Get the base directory (assumes 'generate.py' is in 'app/utils')
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Construct the path to 'map.py'
    map_path = os.path.join(base_dir, 'states', 'game', 'map.py')

    with open(map_path, 'w') as map_file:  # Use 'a' to append, or 'w' to overwrite
        map_file.write(text)

if __name__ == "__main__":
    # Example usage
    max_number = 18  # Specify the size
    start_char = 'D'  # Start from 'D'

    result = "class Map:"
    result += "\n"
    result += generate_empty_grid_with_format(max_number, "FLOOR_LAYER")
    result += "\n"
    result += generate_empty_grid_with_format(max_number, "COLLISION_LAYER")
    result += "\n"
    result += generate_empty_grid_with_format(max_number, "PLACED_LAYER")
    result += "\n"
    result += generate_mixed_case_alphabet_array_with_format(max_number, start_char, "DEPTH_LAYER")

    output_to_map(result)

