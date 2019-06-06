import os
import fnmatch
# import id3reader  #need to download p3 version pytthon 3 vers

def find_music(start, extension):
    for path, directories, files in os.walk(start):
        for file in fnmatch.filter(files, '*{}'.format(extension)):
            absolute_path = os.path.abspath(path)       # Creating absolute path
            yield os.path.join(absolute_path, file)              # use it in yielded values


root = "D:\Muzica"
my_music_files = find_music(root, 'mp3')

error_list = []
for f in my_music_files:

    # try:
        # # id3r = id3reader.Reader(f)
        # print("Artist: {}, Album: {}, Track: {}, Song: {}".format(id3r.get_value('performer'),
        #                                                           id3r.get_value('album'),
        #                                                           id3r.get_value('track'),
        #                                                           id3r.get_value('title')
        #                                                           ))
        print(f)
