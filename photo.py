
import os
import time
import shutil
from PIL import Image
from PIL.ExifTags import TAGS

localPath = "/Users/carolynwhelpley/Documents/PhotosToSort"
destinationPath = "/Users/carolynwhelpley/Documents/SortedPhotos"
_TAGS_r = dict((v, k) for k, v in TAGS.items())
totalFiles = 0
processedPhotos = 0
notPhotos = 0

def processPhoto(photoPath):
    print("got here")
    global processedPhotos, notPhotos
    try:

        
        with Image.open(photoPath) as im:
            exif_data_PIL = im._getexif()
            if exif_data_PIL is not None:
                if exif_data_PIL[_TAGS_r["DataTimeOriginal"]] is not None:
                    fileDate = exif_data_PIL[_TAGS_r["DateTimeOriginal"]]
                    if fileDate != " " and len(fileDate) > 10:
                        fileDate = fileDate.replace(":", " ")
                        destinationFolder = fileDate[:6]
                        if not os.path.isdir(os.path.abspath(os.path.join(destinationPath, destinationFolder))):
                            os.mkdir(os.path.abspath(os.path.join(
                                destinationPath, destinationFolder)))

                        newPhotoName = os.path.abspath(os.path.join(
                            destinationPath, destinationFolder, fileDate + '.' + im.format))
                        im.close()
                        shutil.move(photoPath, newPhotoName)
                        processedPhotos += 1
                        print("/r%d photo processed. %d not processed" %
                              (processedPhotos, notPhotos), end="")
            else:
                notPhotos += 1
                print("\r%d photos processed, %d not processed" %
                      (processedPhotos, notPhotos), end='')
    except IOError as err:
        notPhotos += 1
        print(err)
        pass
    except KeyError:
        notPhotos += 1
        pass

    def processFolder(folderPath, countOnly):
        global totalFiles
        for file in os.listdir(folderPath):
            fileNameIn = os.path.abspath(os.path.join(folderPath, file))
            if os.path.isdir(fileNameIn):
                processFolder(fileNameIn, countOnly)
            else:
                if countOnly:
                    totalFiles += 1
                else:
                    processPhoto(fileNameIn)

    def main(argv=None):
        tic = time.perf_counter()
        processFolder(localPath, True)
        processFolder(localPath, False)
        toc = time.perf_counter()
        print(f"Time used: {toc - tic:0.4f} seconds")

    if __name__ == "_main_":
        main()
