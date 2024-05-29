# from PIL import Image
# from PIL.TiffTags import TAGS
# import os
# # Define the paths
metadata_file_path = "TIF/metadata.txt"
tiff_path = "TIF/image.tif"
output_tiff_path = "TIF/output_image_with_metadata.tif"
#
#
#
# def read_metadata_from_file(file_path):
#     metadata = {}
#     if not os.path.exists(file_path):
#         print(f"Error: Metadata file '{file_path}' not found.")
#         return metadata
#
#     try:
#         with open(file_path, 'r') as f:
#
#             for line in f:
#                 # Assuming each line is in the format: tag_name: value
#                 tag_name, value = line.strip().split(': ', 1)
#                 # Find the tag id from the TAGS dictionary
#
#                 tag_id = {v: k for k, v in TAGS.items()}.get(tag_name, None)
#                 print(line)
#                 if tag_id:
#                     metadata[tag_id] = value
#     except Exception as e:
#         print(f"An error occurred while reading the metadata file: {e}")
#     return metadata
#
#
# def attach_metadata_to_tiff(tiff_path, metadata, output_path):
#     if not os.path.exists(tiff_path):
#         print(f"Error: TIFF file '{tiff_path}' not found.")
#         return
#
#     try:
#         # Open the original TIFF image
#
#         with Image.open(tiff_path) as img:
#             if img.format != 'TIFF':
#                 print(f"Error: The file '{tiff_path}' is not a valid TIFF image.")
#                 return
#
#             # Attach metadata to the image
#             for tag_id, value in metadata.items():
#                 img.tag_v2[tag_id] = value
#
#             # Save the image with metadata
#             img.save(output_path)
#
#         print(f"Metadata successfully attached and saved to {output_path}")
#     except IOError as e:
#         print(f"An error occurred while opening the TIFF file: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# # Read metadata from file
# metadata = read_metadata_from_file(metadata_file_path)
# if metadata:
#     # Ensure the output directory exists
#     os.makedirs(os.path.dirname(output_tiff_path), exist_ok=True)
#
#     # Attach metadata and save the TIFF image
#     attach_metadata_to_tiff(tiff_path, metadata, output_tiff_path)


from PIL import Image, TiffTags, TiffImagePlugin
import os


# TAG_NAME_TO_ID = {
#     'ImageWidth': 256,
#     'ImageLength': 257,
#     'BitsPerSample': 258,
#     'Compression': 259,
#     'PhotometricInterpretation': 262,
#     'Make': 271,
#     'Model': 272,
#     'Orientation': 274,
#     'SamplesPerPixel': 277,
#     'RowsPerStrip': 278,
#     'StripOffsets': 273,
#     'StripByteCounts': 279,
#     'PlanarConfiguration': 284,
#     'DateTime': 306,
#     'Software': 305,
#     'GPSInfoIFD': 34853,
#     'ExifIFD': 34665,
#     'XMP': 700,
#     '51022': 51022,
#     '48020': 48020,
#     '48021': 48021,
#     '48022': 48022,
#     'BlackLevelRepeatDim': 50713,  # example custom tag
#     'BlackLevel': 50714,  # example custom tag
#     'NewSubfileType': 254,
#     # Add other mappings as necessary
# }


def read_metadata_from_file(file_path):
    metadata = {}
    if not os.path.exists(file_path):
        print(f"Error: Metadata file '{file_path}' not found.")
        return metadata

    try:
        with open(file_path, 'r') as f:
            for line in f:
                tag_name, value = line.strip().split(': ', 1)
                tag_id = TiffTags.TAGS_V2.get(tag_name)
                if tag_id is not None:
                    metadata[tag_id] = value
                else:
                    print(f"Warning: Tag name '{tag_name}' not found in TiffTags.TAGS_V2.")
    except Exception as e:
        print(f"An error occurred while reading the metadata file: {e}")
    return metadata


def parse_value(value):
    try:
        if value.startswith("b'") or value.startswith('b"'):
            return eval(value)  # Convert string representation of bytes to bytes
        elif value.startswith('(') and value.endswith(')'):
            # Handle tuples, considering elements could be int, float, or str
            return tuple(map(parse_single_value, value[1:-1].split(',')))  # Convert tuple strings to tuples
        elif value.isdigit():
            return int(value)  # Convert string numbers to integers
        elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            return float(value)  # Convert string numbers with a decimal point to floats
        else:
            return value  # Return the value as-is for any other types (e.g., string)
    except Exception as e:
        print(f"Error parsing value: {value}, error: {e}")
        return value


def parse_single_value(value):
    value = value.strip()
    if value.isdigit():
        return int(value)
    elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
        return float(value)
    else:
        return value


def convert_metadata_value(tag_id, value):
    if tag_id == 700:
        return bytes(value, 'utf-8')  # Handle XMP metadata
    return parse_value(value)


def attach_metadata_to_tiff(tiff_path, metadata, output_path):
    if not os.path.exists(tiff_path):
        print(f"Error: TIFF file '{tiff_path}' not found.")
        return

    try:
        with Image.open(tiff_path) as img:
            if img.format != 'TIFF':
                print(f"Error: The file '{tiff_path}' is not a valid TIFF image.")
                return

            for tag_id, value in metadata.items():
                converted_value = convert_metadata_value(tag_id, value)
                img.tag_v2[tag_id] = converted_value

            img.save(output_path)

        print(f"Metadata successfully attached and saved to {output_path}")
    except IOError as e:
        print(f"An error occurred while opening the TIFF file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")



# Read metadata from file
metadata = read_metadata_from_file(metadata_file_path)

if metadata:
    os.makedirs(os.path.dirname(output_tiff_path), exist_ok=True)
    attach_metadata_to_tiff(tiff_path, metadata, output_tiff_path)








# from PIL import Image, TiffImagePlugin, TiffTags
# import numpy as np
# import os
#
#
# # Add custom tags to TAGS_V2 if they are not already present
# for tag_name, tag_id in TAG_NAME_TO_ID.items():
#     if tag_id not in TiffTags.TAGS_V2:
#         TiffTags.TAGS_V2[tag_id] = tag_name
#
# def parse_value(value):
#     """Parse a string value to its appropriate type."""
#     try:
#         if value.startswith("b'") or value.startswith('b"'):
#             return eval(value)  # Convert string representation of bytes to bytes
#         elif value.startswith('(') and value.endswith(')'):
#             return tuple(map(parse_single_value, value[1:-1].split(',')))  # Convert tuple strings to tuples
#         elif value.isdigit():
#             return int(value)  # Convert string numbers to integers
#         elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
#             return float(value)  # Convert string numbers with a decimal point to floats
#         else:
#             return value  # Return the value as-is for any other types (e.g., string)
#     except Exception as e:
#         print(f"Error parsing value: {value}, error: {e}")
#         return value
#
# def parse_single_value(value):
#     """Parse individual values within a tuple."""
#     value = value.strip()
#     if value.isdigit():
#         return int(value)
#     elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
#         return float(value)
#     else:
#         return value
#
# def read_metadata_from_file(file_path):
#     metadata = {}
#     if not os.path.exists(file_path):
#         print(f"Error: Metadata file '{file_path}' not found.")
#         return metadata
#
#     try:
#         with open(file_path, 'r') as f:
#             for line in f:
#                 tag_name, value = line.strip().split(': ', 1)
#                 tag_id = TiffTags.TAGS_V2.get(tag_name, TAG_NAME_TO_ID.get(tag_name))
#                 if tag_id is not None:
#                     metadata[tag_id] = parse_value(value)
#                 else:
#                     print(f"Warning: Tag name '{tag_name}' not found in TiffTags.TAGS_V2.")
#     except Exception as e:
#         print(f"An error occurred while reading the metadata file: {e}")
#     return metadata
#
# def create_blank_tiff_with_metadata(output_path, metadata, image_size=(1280, 960)):
#     try:
#         # Create a blank image
#         blank_image = Image.new('I;16', image_size)  # 16-bit grayscale image
#
#         # Set the metadata
#         for tag_id, value in metadata.items():
#             blank_image.tag_v2[tag_id] = value
#
#         # Save the image
#         blank_image.save(output_path, tiffinfo=blank_image.tag_v2)
#
#         print(f"Metadata successfully attached and saved to {output_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# # Read metadata from file
# metadata = read_metadata_from_file(metadata_file_path)
#
# # Create a new blank TIFF image and attach metadata
# create_blank_tiff_with_metadata(output_tiff_path, metadata)








#
# from PIL import Image, TiffImagePlugin
# import tifffile as tiff
#
# def parse_metadata(data):
#     metadata = {}
#     items = data.split('\n')
#     for item in items:
#         if not item.strip():
#             continue
#         tag, value = item.split(': ', 1)
#         tag = int(tag)
#         if value.startswith("b'") or value.startswith('b"'):
#             value = eval(value)
#         elif value.startswith('(') and value.endswith(')'):
#             value = eval(value)
#         elif value.isdigit():
#             value = int(value)
#         elif value.replace('.', '', 1).isdigit():
#             value = float(value)
#         metadata[tag] = value
#     return metadata
#
# def create_blank_tiff(image_size=(1280, 960)):
#     return Image.new('I;16', image_size)  # 16-bit grayscale image
#
# def attach_metadata(image, metadata):
#     tiffinfo = TiffImagePlugin.ImageFileDirectory_v2()
#     for tag, value in metadata.items():
#         tiffinfo[tag] = value
#         # print(f"TiffInfo {tiffinfo}")
#     return tiffinfo
#
# def save_tiff(image, output_path, tiffinfo):
#     tiff.imwrite(output_path, tiffinfo)
#     # image.save(output_path,  tiffinfo=tiffinfo)
#
# # Example metadata string
# metadata_str = """256: 1280
# 257: 960
# 258: (16,)
# 259: 1
# 262: 1
# 51022: b"\\x00\\x00\\x00\\x02\\x00\\x00\\xbec\\x01\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00T\\x00\\x00\\x00\\x01@\\x96\\xb4\\xd7\\x9c\\xd8)C@\\x96\\xb7\\x82\\x9cF\\x12r\\xbf\\xba\\xae5\\x18\\xdb\\xabQ?\\xca \\x7f\\x14\\xed\\x1cK\\xbf\\xc4\\x05\\x9c\\xe2\\x8cR\\xc1?#i\\xe1+\\x00g\\xa2?5h\\x1b\\xed\\x9eP\\xce?\\xe0y\\x1e\\x131\\xfc\\x01?\\xe0\\x02\\xa6\\x03\\xdc\\x94\\xb7\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\xa1o\\x01\\x03\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00@\\xbf\\x1c\\xc0\\x1f\\xaf\\x85\\x14\\x85>\\xb6\\x12U\\xa6\\xb6\\x9bx\\xbeG\\xe2]\\xf1.\\xef\\xba=\\xc11G7\\xff\\xe7\\xb5\\xbd%\\x96!\\xb3\\xff\\xa9'<s|\\x82o\\xcd*\\xf7?\\xe1,\\xd8\\xe5\\x8aZr?\\xdf\\xccK\\x9a\\x10\\xb8\\r"
# 271: MicaSense
# 272: RedEdge
# 273: (8, 256008, 512008, 768008, 1024008, 1280008, 1536008, 1792008, 2048008, 2304008)
# 274: 1
# 48020: (1, 1, 1, 7, 0, 0, 1, 4, 1, 48022, 21, 0, 2, 48022, 21, 21, 3, 48021, 1, 0, 4, 48022, 16, 42, 5, 48021, 8, 1, 6, 48021, 2, 9)
# 277: 1
# 278: 100
# 279: (256000, 256000, 256000, 256000, 256000, 256000, 256000, 256000, 256000, 153600)
# 48021: (154.74623107910156, 0.24311977624893188, 467271.0, 475.0, 20.0, 0.10100000351667404, 220.0, 16.0, 860.0, 466.0, 0.0)
# 48022: DFj0YDYQsRJd6hDUj7qZ|20Ntb9oCOg7Cm7HUbb1i|DL06-1808359-SC|5
# 0713: (2, 2)
# 50714: (4800, 4800, 4800, 4800)
# 284: 1
# 34853: 2457942
# 34665: 2457704
# 3305: v3.4.3
# 306: 2024:01:03 07:31:35
# 700: (b'<?xpacket begin="\\xef\\xbb\\xbf" id="W5M0MpCehiHzreSzNTczkc9d"?>\\n<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0">\\n   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\\n      <rdf:Description rdf:about="Pix4D Camera Information"\\n            xmlns:MicaSense="http://micasense.com/MicaSense/1.0/">\\n         <MicaSense:BootTimestamp>466</MicaSense:BootTimestamp>\\n         <MicaSense:RadiometricCalibration>\\n            <rdf:Seq>\\n               <rdf:li>0.000145914</rdf:li>\\n               <rdf:li>1.39479e-07</rdf:li>\\n               <rdf:li>1.1714499999999999e-05</rdf:li>\\n            </rdf:Seq>\\n         </MicaSense:RadiometricCalibration>\\n         <MicaSense:FlightId>20Ntb9oCOg7Cm7HUbb1i</MicaSense:FlightId>\\n         <MicaSense:CaptureId>DFj0YDYQsRJd6hDUj7qZ</MicaSense:CaptureId>\\n         <MicaSense:TriggerMethod>4</MicaSense:TriggerMethod>\\n         <MicaSense:PressureAlt>154.74623107910156</MicaSense:PressureAlt>\\n         <MicaSense:DarkRowValue>\\n            <rdf:Seq>\\n               <rdf:li>5206</rdf:li>\\n               <rdf:li>5206</rdf:li>\\n               <rdf:li>5023</rdf:li>\\n               <rdf:li>5032</rdf:li>\\n            </rdf:Seq>\\n         </MicaSense:DarkRowValue>\\n      </rdf:Description>\\n      <rdf:Description rdf:about="Pix4D Camera Information"\\n            xmlns:Camera="http://pix4d.com/camera/1.0">\\n         <Camera:BandName>Blue</Camera:BandName>\\n         <Camera:CentralWavelength>475</Camera:CentralWavelength>\\n         <Camera:WavelengthFWHM>20</Camera:WavelengthFWHM>\\n         <Camera:VignettingCenter>\\n            <rdf:Seq>\\n               <rdf:li>687.00738320456162</rdf:li>\\n               <rdf:li>476.97042888281499</rdf:li>\\n            </rdf:Seq>\\n         </Camera:VignettingCenter>\\n         <Camera:VignettingPolynomial>\\n            <rdf:Seq>\\n               <rdf:li>-0.00010967439073279919</rdf:li>\\n               <rdf:li>1.3155710359786701e-06</rdf:li>\\n               <rdf:li>-1.1121968712206205e-08</rdf:li>\\n               <rdf:li>3.1272962518162695e-11</rdf:li>\\n               <rdf:li>-3.8345241237884648e-14</rdf:li>\\n               <rdf:li>1.6901727679290724e-17</rdf:li>\\n            </rdf:Seq>\\n         </Camera:VignettingPolynomial>\\n         <Camera:ModelType>perspective</Camera:ModelType>\\n         <Camera:PrincipalPoint>2.47097,1.80116</Camera:PrincipalPoint>\\n         <Camera:PerspectiveFocalLength>5.4507902034623514</Camera:PerspectiveFocalLength>\\n         <Camera:PerspectiveFocalLengthUnits>mm</Camera:PerspectiveFocalLengthUnits>\\n         <Camera:PerspectiveDistortion>\\n            <rdf:Seq>\\n               <rdf:li>-0.10422069413077152</rdf:li>\\n               <rdf:li>0.20411671182430022</rdf:li>\\n               <rdf:li>-0.15642129003449237</rdf:li>\\n               <rdf:li>0.00014811395294672425</rdf:li>\\n               <rdf:li>0.00032663995590921375</rdf:li>\\n            </rdf:Seq>\\n         </Camera:PerspectiveDistortion>\\n         <Camera:BandSensitivity>0.26096922524726113</Camera:BandSensitivity>\\n         <Camera:RigCameraIndex>0</Camera:RigCameraIndex>\\n         <Camera:IrradianceExposureTime>0.10100000351667404</Camera:IrradianceExposureTime>\\n         <Camera:IrradianceGain>16</Camera:IrradianceGain>\\n         <Camera:Irradiance>0.24311977624893188</Camera:Irradiance>\\n         <Camera:IrradianceYaw>42.003950838721998</Camera:IrradianceYaw>\\n         <Camera:IrradiancePitch>2.3695857031864969</Camera:IrradiancePitch>\\n         <Camera:IrradianceRoll>8.8167169211321763</Camera:IrradianceRoll>\\n      </rdf:Description>\\n      <rdf:Description rdf:about="Pix4D Camera Information"\\n            xmlns:DLS="http://micasense.com/DLS/1.0/">\\n         <DLS:Serial>DL06-1808359-SC</DLS:Serial>\\n         <DLS:SwVersion>v1.0.1</DLS:SwVersion>\\n         <DLS:SensorId>0</DLS:SensorId>\\n         <DLS:CenterWavelength>475</DLS:CenterWavelength>\\n         <DLS:Bandwidth>20</DLS:Bandwidth>\\n         <DLS:TimeStamp>467271</DLS:TimeStamp>\\n         <DLS:Exposure>0.10100000351667404</DLS:Exposure>\\n         <DLS:Gain>16</DLS:Gain>\\n         <DLS:SpectralIrradiance>0.24311977624893188</DLS:SpectralIrradiance>\\n         <DLS:RawMeasurement>220</DLS:RawMeasurement>\\n         <DLS:OffMeasurement>860</DLS:OffMeasurement>\\n         <DLS:Yaw>0.73310724098153246</DLS:Yaw>\\n         <DLS:Pitch>0.041357072428789457</DLS:Pitch>\\n         <DLS:Roll>0.15388073949005368</DLS:Roll>\\n      </rdf:Description>\\n   </rdf:RDF>\\n</x:xmpmeta>\\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                                                                                                    \\n                           \\n<?xpacket end="w"?>',)
# 254: 0
# """
#
# # Parse the metadata
# metadata = parse_metadata(metadata_str)
# print(metadata)
# # Create a blank TIFF image
# image = create_blank_tiff()
#
# # Attach metadata to the blank image
# # attach_metadata(image, metadata)
#
# tiffinfo = attach_metadata(image, metadata)
# # Save the TIFF image
# output_path = 'output_with_metadata.tif'
# save_tiff(image, output_path, tiffinfo)
# print(f"Image saved with metadata to {output_path}")
