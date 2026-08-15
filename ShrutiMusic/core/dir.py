import os

from ..logging import LOGGER

def dirr():
    for file in os.listdir():
        if file == "elina_banner.png":
            continue
        if file.endswith(".jpg"):
            os.remove(file)
        elif file.endswith(".jpeg"):
            os.remove(file)
        elif file.endswith(".png"):
            os.remove(file)

    if "downloads" not in os.listdir():
        os.mkdir("downloads")
    else:
        for file in os.listdir("downloads"):
            try:
                os.remove(os.path.join("downloads", file))
            except:
                pass
    if "cache" not in os.listdir():
        os.mkdir("cache")

    LOGGER(__name__).info("Directories Updated.")
