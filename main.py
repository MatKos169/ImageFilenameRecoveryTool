import exifread
import datetime
import os
from sys import exit as quit

if not os.path.exists('./data'):
    os.mkdir('./data')
    print('Copy Images to data folder and restart the programm')
    quit()

liste = os.listdir('./data')




for bild in liste:
    if not os.path.isdir(bild):
        with open('./data/'+bild, 'rb') as fh:
            try:
                tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                dateTaken = tags["EXIF DateTimeOriginal"]
                try:
                    print(datetime.datetime.strptime(str(dateTaken), '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d'))
                    dateTaken = datetime.datetime.strptime(str(dateTaken), '%Y:%m:%d %H:%M:%S').strftime('%Y%m%d')
                except:
                    print('Unknown timeformat found in file')
            except:
                print('capture timestamp not found. Using modification timestamp')
                try:
                    t = os.path.getmtime('./data/'+bild)
                    dateTaken = "mod_" + datetime.datetime.fromtimestamp(t).strftime('%Y%m%d')
                    print(dateTaken)
                except:
                    if not os.path.exists('./error'):
                        os.mkdir('./error')
                    os.rename('./data/'+bild, './error/'+bild)
            print(bild)

            print()
            fh.close()

            os.rename('./data/'+bild, f"./data/{bild.split('.')[0]}_" + dateTaken + '.' + str(bild.split('.')[1]))
    else:
        print(f'Wound touch "{bild}". Cause it is not a file')