from PIL import Image
from PIL.TiffTags import TAGS
import os
# Define the paths
metadata_file_path = "TIF/metadata.txt"
tiff_path = "TIF/image.tif"
output_tiff_path = "TIF/output_image_with_metadata.tif"



def read_metadata_from_file(file_path):
    metadata = {}
    if not os.path.exists(file_path):
        print(f"Error: Metadata file '{file_path}' not found.")
        return metadata

    try:
        with open(file_path, 'r') as f:

            for line in f:
                # Assuming each line is in the format: tag_name: value
                tag_name, value = line.strip().split(': ', 1)
                # Find the tag id from the TAGS dictionary

                tag_id = {v: k for k, v in TAGS.items()}.get(tag_name, None)
                print(line)
                if tag_id:
                    metadata[tag_id] = value
    except Exception as e:
        print(f"An error occurred while reading the metadata file: {e}")
    return metadata


def attach_metadata_to_tiff(tiff_path, metadata, output_path):
    if not os.path.exists(tiff_path):
        print(f"Error: TIFF file '{tiff_path}' not found.")
        return

    try:
        # Open the original TIFF image

        with Image.open(tiff_path) as img:
            if img.format != 'TIFF':
                print(f"Error: The file '{tiff_path}' is not a valid TIFF image.")
                return

            # Attach metadata to the image
            for tag_id, value in metadata.items():
                img.tag_v2[tag_id] = value

            # Save the image with metadata
            img.save(output_path)

        print(f"Metadata successfully attached and saved to {output_path}")
    except IOError as e:
        print(f"An error occurred while opening the TIFF file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Read metadata from file
metadata = read_metadata_from_file(metadata_file_path)
if metadata:
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_tiff_path), exist_ok=True)

    # Attach metadata and save the TIFF image
    attach_metadata_to_tiff(tiff_path, metadata, output_tiff_path)
