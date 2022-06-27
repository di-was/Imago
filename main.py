from ast import arg
from inspect import classify_class_attrs
from PIL import Image
import os, sys
from PIL.ExifTags import TAGS
import shutil

IMAGE_EXTENSIONS = ['.apng', '.avif', '.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.webp']
VIDEO_EXTENSIONS = ['.WEBM', '.MPG', '.MP2', '.MPEG', '.MPE', '.MPV', '.OGG' , '.MP4', '.M4P',  '.M4V', '.AVI', '.WMV', '.MOV', '.QT' '.FLV', '.SWF', '.AVCHD']
IMAGE_DIRECTORY = 'images'
VIDEO_DIRECTORY = 'videos'

# Get and validate image path
def verify_path():
    file_path = input("Enter the path : ")
    while not os.path.exists(file_path):
        file_path = input("File/Directory doesn't exist. Try again : ")
    return file_path

# retrieves the metadata of any image
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


# Takes an image and returns it's metadata
def image_detail():
    image = Image.open(verify_path())
    metadata = get_metadata(image=image)    
    print(metadata)
    sys.exit()

# returns all the arguments supplied through command line
def get_argumnets():
    try:
        sys.argv[1]
    except IndexError:
        return None
    return sys.argv
        

def orderImage(variable='image', verified_path=None):
    if verified_path != None:
        path = verified_path
    else:
        path = verify_path()
    folder = [ y for y in os.listdir(path) if y.__contains__('.')]
    ordering = 0
    
    for x in folder:
        extension = os.path.splitext(x)[1]
        os.rename(path + '/' +  x, path + '/' + f'{variable}{ordering}{extension}')
        ordering += 1
    
    data = {
        'path': path,
        'Total Files': len(folder)
    }

    return data
    
    
def classify_and_arrange():
    # create directories
    path = verify_path()
    image_path = path + '/' + IMAGE_DIRECTORY
    video_path = path + '/' + VIDEO_DIRECTORY
    if not os.path.exists(image_path) and not os.path.exists(video_path):
        os.mkdir(path + '/' + IMAGE_DIRECTORY)
        os.mkdir(path + '/' + VIDEO_DIRECTORY)

    folder = [ y for y in os.listdir(path) if y.__contains__('.')]
    for x in folder:
        extension = os.path.splitext(x)[1]
        if extension in IMAGE_EXTENSIONS:
            original_path = path + '/' + x
            dst_path = path + '/' + IMAGE_DIRECTORY + '/'  + x
            shutil.move(original_path, dst_path)
        if extension.upper() in VIDEO_EXTENSIONS:
            original_path = path + '/' + x
            dst_path = path + '/' + VIDEO_DIRECTORY + '/' +  x
            shutil.move(original_path, dst_path)

    # order Image and Video
    orderImage(verified_path=image_path)
    orderImage(variable='video', verified_path=video_path)

    data  = {
        'path': path,
        'Total Files': len(folder),
        'Images' : len([y for y in os.listdir(path + '/' + IMAGE_DIRECTORY)]),
        'videos': len([y for y in os.listdir(path + '/' + VIDEO_DIRECTORY)]),
    }

    return data

    


def main():
    arguments = get_argumnets()[1:]
    if 'og' in arguments: # og -> Order Image
        print(orderImage())
    if 'i' in arguments: # i -> single image
        image_detail()
    if 'og-cl' in arguments: # Classify and order them accordingly
        print(classify_and_arrange())

if __name__ == "__main__":
    main()