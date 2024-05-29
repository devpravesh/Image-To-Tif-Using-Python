import exifread
import json

# output_path = "TIF/metadata1.txt"
def get_gps_data(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        # with open(output_path, 'w') as m:
        #     m.write(json.dumps(tags))
        print(tags)
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
        gps_altitude = tags.get('GPS GPSAltitude')
        # print(gps_latitude)
        # for tag in tags.keys():
        #     print(f"{tag}: {tags[tag]}")

        if gps_latitude and gps_longitude and gps_latitude_ref and gps_longitude_ref:
            lat = [float(x.num) / float(x.den) for x in gps_latitude.values]
            lon = [float(x.num) / float(x.den) for x in gps_longitude.values]

            latref = gps_latitude_ref.values[0]
            lonref = gps_longitude_ref.values[0]

            latitude = lat[0] + lat[1] / 60 + lat[2] / 3600
            longitude = lon[0] + lon[1] / 60 + lon[2] / 3600

            if latref != 'N':
                latitude = -latitude
            if lonref != 'E':
                longitude = -longitude

            print(f"Latitude: {latitude}°")
            print(f"Longitude: {longitude}°")
        else:
            print("No GPS Latitude and Longitude data found")

        if gps_altitude:
            altitude = float(gps_altitude.values[0].num) / float(gps_altitude.values[0].den)
            print(f"Altitude: {altitude} meters")
        else:
            print("No GPS Altitude data found")


# Path to the uploaded file
# file_path = "TIF/output_image_with_metadata.tif"
file_path = "TIF/output_image_with_metadata.tif"
# file_path = "new.jpg"

# Call the function
get_gps_data(file_path)