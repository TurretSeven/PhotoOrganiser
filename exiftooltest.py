import exiftool

files = ["/Users/steve/Temp/PhotoTest/New Layout/2022/01/22/Watloo Sunset 1.tif"]
with exiftool.ExifToolHelper() as et:
    metadata = et.get_metadata(files)

for d in metadata:
    print("{:20.20} {:20.20}".format(d["SourceFile"], d["EXIF:DateTimeOriginal"]))