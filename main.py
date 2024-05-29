
################### Scan All file Of tif in directory
# import os
# from PIL import Image
#
# yourpath = os.getcwd()
# for root, dirs, files in os.walk(yourpath, topdown=False):
#     for name in files:
#         print(os.path.join(root, name))
#         if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
#             if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
#                 print("A jpeg file already exists for %s" % name)
#             # If a jpeg is *NOT* present, create one from the tiff.
#             else:
#                 outfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
#                 try:
#                     im = Image.open(os.path.join(root, name))
#                     print("Generating jpeg for %s" % name)
#                     im.thumbnail(im.size)
#                     im.save(outfile, "JPEG", quality=100)
#                 except Exception as e:
#                     print (e)



# from PIL import Image
#
# def convert_tif_to_jpg(tif_path, jpg_path):
#     try:
#         # Open the TIFF file
#         with Image.open(tif_path) as img:
#             # Convert and save as JPEG
#             img.convert("RGB").save(jpg_path, "JPEG")
#         print(f"Conversion successful: {tif_path} -> {jpg_path}")
#     except FileNotFoundError:
#         print(f"Error: File not found: {tif_path}")
#     except IsADirectoryError:
#         print(f"Error: {tif_path} is a directory, not a file.")
#     except PermissionError:
#         print(f"Error: Permission denied to access {tif_path}")
#     except Exception as e:
#         print(f"Error converting file: {e}")
#
# # Example usage
# tif_file = "flight1.tif"
# jpg_file = "testImage.jpg"
# convert_tif_to_jpg(tif_file, jpg_file)



from PIL import Image, TiffTags

# Open the TIFF file
tiff_image_path = 'TIF/output_image_with_metadata.tif'
tiff_image = Image.open(tiff_image_path)

# Print TIFF metadata
print("TIFF Metadata:")

for tag, value in tiff_image.tag_v2.items():
    tag_name = TiffTags.TAGS_V2.get(tag, tag)
    print(f"{tag_name}: {value}")
    # print(f"Tag: {tag}")
# print(f"Original image mode: {tiff_image.mode}")
# if tiff_image.mode == 'I;16':
#     # Scale the pixel values down to 8-bit range
#     tiff_image = tiff_image.point(lambda i: i * (1. / 256)).convert('L')
#
# # Convert the 8-bit grayscale image to RGB
# rgb_image = tiff_image.convert('RGB')
# jpeg_image_path = 'new.jpg'
# quality = tiff_image.info.get('quality', 95)
# rgb_image.save(jpeg_image_path, 'JPEG', quality=quality)

# print(f"\nImage successfully converted and saved to {jpeg_image_path}")
