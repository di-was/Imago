from ast import arg
from PIL import Image
import os, sys
from PIL.ExifTags import TAGS

#IMAGE_EXTENSIONS = ['.jpg', '.png', '.webp', '.gif']
#VIDEO_EXTENSIONS = ['.mp4']
# Previous Variables initialized in case the project steers toward file catorization. 

# Get and validate image path
def verify_path():
    file_path = input("Enter the path : ")
    while not os.path.exists(file_path):
        file_path = input("File doesn't exist. Try again : ")
    return file_path

def get_metadata(image=None):
    exifdata = image.getexif()    
    if len(exifdata) == 0:
        return "The image has no metadata"
    else:
        metadata = []
        for tagid in exifdata:
            tagname = TAGS.get(tagid, tagid)
            value = exifdata.get(tagid)
            metadata.append(f"{tagname:25}: {value}")
        return metadata


def image_detail():
    image = Image.open(verify_path())
    metadata = get_metadata(image=image)    
    print(metadata)
    sys.exit()

def get_argumnets():
    try:
        sys.argv[1]
    except IndexError:
        return None
    return sys.argv
        

def optimize():
    path = verify_path()
    folder = [ y for y in os.listdir(path) if y.__contains__('.')]
    ordering = 0
    for x in folder:
        os.rename(path + '/' +  x, path + '/' + f'image{ordering}')
        ordering += 1
    
    


def main():
    arguments = get_argumnets()
    if arguments  != None:   
        image_detail()
    else:
        optimize()

if __name__ == "__main__":
    main()