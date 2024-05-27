from PIL import Image
import os


def convert_jpg_to_tif(input_path, output_path):
    try:
        # Open the JPEG image
        with Image.open(input_path) as img:
            # Save the image as a TIFF
            img.save(output_path, format="TIFF")
        print(f"Image successfully converted to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Define the paths
input_path = "new.jpg"
output_path = "TIF/image.tif"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Convert the image
convert_jpg_to_tif(input_path, output_path)
