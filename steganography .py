from PIL import Image

# Banner
print("""
============================================================
       Steganography Tool - Hide Text in Images
       Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan
============================================================
""")

def text_to_binary(text):
    """Convert text to binary string."""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Convert binary string to text."""
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text

def encode_image(image_path, message, output_path):
    """Encode a message into an image."""
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        pixels = img.load()
        binary_message = text_to_binary(message) + '1111111111111110'  # Delimiter
        binary_index = 0
        
        for i in range(img.width):
            for j in range(img.height):
                if binary_index < len(binary_message):
                    r, g, b = pixels[i, j]
                    # Modify LSB of red channel
                    r = (r & ~1) | int(binary_message[binary_index])
                    pixels[i, j] = (r, g, b)
                    binary_index += 1
                else:
                    img.save(output_path)
                    print(f"Message encoded successfully! Saved as {output_path}")
                    return
        print("Image too small for message!")
    except Exception as e:
        print(f"Error during encoding: {e}")

def decode_image(image_path):
    """Decode a message from an image."""
    try:
        img = Image.open(image_path)
        pixels = img.load()
        binary_message = ''
        
        for i in range(img.width):
            for j in range(img.height):
                r, _, _ = pixels[i, j]
                binary_message += str(r & 1)
                # Check for delimiter
                if len(binary_message) >= 16 and binary_message[-16:] == '1111111111111110':
                    return binary_to_text(binary_message[:-16])
        print("No message found!")
        return None
    except Exception as e:
        print(f"Error during decoding: {e}")
        return None

def main():
    while True:
        print("\n1. Encode message\n2. Decode message\n3. Exit")
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            image_path = input("Enter input image path (e.g., input.png): ")
            message = input("Enter message to hide: ")
            output_path = input("Enter output image path (e.g., output.png): ")
            encode_image(image_path, message, output_path)
        elif choice == '2':
            image_path = input("Enter image path to decode (e.g., output.png): ")
            message = decode_image(image_path)
            if message:
                print(f"Decoded message: {message}")
        elif choice == '3':
            print("Exiting... Thank you for using the tool!")
            break
        else:
            print("Invalid choice! Please try again.")  # Properly indented

if __name__ == "__main__":
    main()