import exifread
import datetime
from time import sleep
import os
from sys import exit as quit
import configparser

if not (os.path.exists('config.ini') or os.path.isfile('config.ini')):
    print('"config.ini" could not be found. Creating new (empty) config File')
    config = configparser.ConfigParser()
    config['config'] = {'workdir': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
        configfile.close()
    sleep(5)
    quit()


config = configparser.ConfigParser()
config.read('config.ini')

print(config['config']['workdir'])

if not os.path.exists(config['config']['workdir']):

    os.mkdir(config['config']['workdir'])
    print('Copy Images to data folder and restart the programm')
    quit()


def getAllImages():
    allImages = []
    dirList = os.listdir(config['config']['workdir'])
    print(dirList)
    for item in dirList:
        print(item)
        if os.path.isFile(item):
            print(item)
    return allImages


liste=getAllImages()

for bild in liste:
    if not os.path.isdir(bild):
        with open(config['config']['workdir']+'/'+bild, 'rb') as fh:
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
                    t = os.path.getmtime(config['config']['workdir']+'/'+bild)
                    dateTaken = "mod_" + datetime.datetime.fromtimestamp(t).strftime('%Y%m%d')
                    print(dateTaken)
                except:
                    if not os.path.exists('./error'):
                        os.mkdir('./error')
                    os.rename(config['config']['workdir']+'/'+bild, './error/'+bild)
            print(bild)

            print()
            fh.close()

            os.rename(config['config']['workdir']+'/'+bild, f"{config['config']['workdir']}/{bild.split('.')[0]}_" + dateTaken + '.' + str(bild.split('.')[1]))
    else:
        print(f'Wound touch "{bild}". Cause it is not a file')