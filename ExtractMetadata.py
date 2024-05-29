from PIL import Image
from PIL.TiffTags import TAGS
import exifread
import os


def save_tiff_metadata(tiff_path, output_path):
    try:
        # Open the TIFF image
        with Image.open(tiff_path) as img:
            # Extract metadata
            # tags = exifread.process_file(img)
            # print(tags)
            metadata = img.tag_v2
            # print(metadata.items())
            # Open the output file for writing
            with open(output_path, 'w') as f:
                # Write metadata to the file
                for tag, value in metadata.items():
                    tag_name = TAGS.get(tag, tag)
                    f.write(f"{tag}: {value}")

        print(f"Metadata successfully saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Define the paths
tiff_path = "IMG_0003_1.tif"
output_path = "TIF/metadata.txt"

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the metadata
save_tiff_metadata(tiff_path, output_path)
