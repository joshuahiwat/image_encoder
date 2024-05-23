from PIL import Image
import numpy as np

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def build_frequency_table(data):
    frequency_table = {}
    for char in data:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1
    return frequency_table

def build_binary_tree(frequency_table):
    nodes = [Node(char, freq) for char, freq in frequency_table.items()]
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged_node = Node(freq=left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right
        nodes.append(merged_node)
    return nodes[0]

def build_custom_tree():
    # Construct a custom binary tree with the specified characters
    root = Node()
    root.left = Node()
    root.left.left = Node(char='E', freq=1)
    root.left.right = Node(char='A', freq=1)
    root.right = Node()
    root.right.left = Node(char='C', freq=1)
    root.right.right = Node()
    root.right.right.left = Node(char='F', freq=1)
    root.right.right.right = Node(char='H', freq=1)
    root.right.right.right.left = Node(char='I', freq=1)
    root.right.right.right.right = Node(char='L', freq=1)
    root.right.right.right.right.left = Node(char='M', freq=1)
    root.right.right.right.right.right = Node(char='N', freq=1)
    root.right.right.right.right.right.left = Node(char='O', freq=1)
    root.right.right.right.right.right.right = Node(char='0', freq=1)
    root.right.right.right.right.right.right.left = Node(char='1', freq=1)
    return root

def build_custom_codes(root):
    codes = {}
    def traverse(node, code=""):
        if node is not None:
            if node.char is not None:
                codes[node.char] = code
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    traverse(root)
    
    # Ensure all characters are included in the custom codes dictionary
    for char in "EACFHI LMNO01":
        if char not in codes:
            codes[char] = ''
    return codes

def encode_data(data, custom_codes):
    encoded_data = ""
    for char in data:
        encoded_data += custom_codes.get(char, '')
    return encoded_data

def decode_data(encoded_data, root):
    decoded_data = ""
    current_node = root
    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        elif bit == '1':
            current_node = current_node.right
        else:
            # Skip characters that are not '0' or '1'
            continue
        if current_node.char is not None:
            decoded_data += current_node.char
            current_node = root
    return decoded_data

# Example usage:
input_image_path = "input_image.jpeg"
output_encoded_text_file = "encoded_image.txt"
output_decoded_image_path = "decoded_image.jpeg"

# Read binary data from a file
with open(input_image_path, "rb") as file:
    original_binary_data = file.read()

# Convert binary data to a string of characters
original_characters = "".join([chr(byte) for byte in original_binary_data])

# Build frequency table from the data
frequency_table = build_frequency_table(original_characters)

# Build custom binary tree
custom_tree_root = build_custom_tree()

# Build custom codes from the binary tree
custom_codes = build_custom_codes(custom_tree_root)

# Encode the data using custom coding
encoded_data = encode_data(original_characters, custom_codes)

# Ensure encoded data fits into 2KB (2048 bytes)
encoded_data = encoded_data[:2048]

# Write encoded data to a text file
with open(output_encoded_text_file, 'w') as file:
    file.write(encoded_data)

print("Encoded data size:", len(encoded_data), "bytes")

# Decode the encoded data from the text file
with open(output_encoded_text_file, 'r') as file:
    encoded_data = file.read()

# Decode the data using custom coding
decoded_characters = decode_data(encoded_data, custom_tree_root)

# Calculate the dimensions of the original image
original_image = Image.open(input_image_path)
original_width, original_height = original_image.size

# Calculate the total number of pixels in the original image
total_pixels = original_width * original_height

# Pad or truncate the decoded data to match the size of the original image
decoded_data_padded = decoded_characters.ljust(total_pixels, ' ')

# Reshape the characters to form an image array
decoded_image_array = np.array(list(decoded_data_padded)).reshape((original_height, original_width))

# Convert the image array to an image and save it
decoded_image = Image.fromarray(decoded_image_array.astype(np.uint8) * 255)  # Scale to 0-255 range
# Save the decoded image using the same format as the original image
decoded_image.save(output_decoded_image_path, format='JPEG')

print("Decoded image saved to:", output_decoded_image_path)
