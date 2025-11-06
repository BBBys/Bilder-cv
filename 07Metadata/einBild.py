import exifread
import logging, os
import pprint


def metasuche(einpfad, name, ext):
    EXCLUDETAGS = (
        "Image Software" "JPEGThumbnail",
        "TIFFThumbnail",
        "Filename",
        "EXIF MakerNote",
        "EXIF ExifVersion",
        "Image Software",
        "Image ExifOffset",
        "GPS GPSVersionID",
        "GPS GPSLatitudeRef",
        "GPS GPSLatitude",
        "GPS GPSLongitudeRef",
        "GPS GPSLongitude",
        "GPS GPSAltitudeRef",
        "Image GPSInfo",
        "Image Padding",
        "EXIF DateTimeDigitized",
        "EXIF SubSecTimeOriginal",
        "EXIF SubSecTimeDigitized",
        "EXIF ImageUniqueID",
        "EXIF Padding",
        "Image XResolution",
        "Image YResolution",
        "Image ResolutionUnit",
        "Image DateTime",
    )
    KEYS = ("kamera", "fotograf")
    ergebnis = dict.fromkeys(KEYS, None)
    eindatei = os.path.join(einpfad, name + ext)
    logging.debug(f"Analysiere Bild: {eindatei}")
    with open(eindatei, "rb") as img:
        tags = exifread.process_file(
            img,
            details=False,
            debug=False,
            builtin_types=False,
            strict=False,
            extract_thumbnail=False,
        )
        for tag, value in tags.items():
            match tag:
                case "Image Model":
                    ergebnis["kamera"] = value
                case "Image Artist":
                    logging.warning(f"Key: {tag}")
                    logging.warning(f"Fotograf: {value}")
                    ergebnis["fotograf"] = value
                case "EXIF ExifVersion":
                    logging.info(f"EXIF Version: {value}")
                case "Image Make":
                    logging.info(f"  Kamerahersteller: {value}")
                case "EXIF FNumber":
                    logging.info(f"  Blende: {value}")
                case "EXIF ExposureTime":
                    logging.info(f"  Belichtungszeit: {value}")
                case "EXIF ISOSpeedRatings":
                    logging.info(f"  ISO-Wert: {value}")
                case "EXIF FocalLength":
                    logging.info(f"  Brennweite: {value}")
                case _:
                    if tag not in EXCLUDETAGS:
                        print(f"Key: {tag}, value {value}")

    return ergebnis
