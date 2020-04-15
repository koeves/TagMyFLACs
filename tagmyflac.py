import argparse, string, sys, glob
from mutagen.mp3 import MP3, MutagenError
from mutagen.easyid3 import EasyID3

""" 
prints verboooose text 
"""
def print_verbose(v, verbose_str=""):
    if v:
        print(verbose_str)


""" 
creates file list recursively from input dir 
"""
def list_files_recursive(input_dir):
    return glob.iglob(input_dir + "**/*", recursive=True)

""" 
parses filenames
RETURN: dictionary{filename, path, artist, title, cat-id} 
"""
def parse_filename(filename):
    return {
        "filename": filename.rsplit("/", 1)[1],
        "path": filename,
        "artist": ((filename.rsplit("/", 1)[1]).rsplit("-", 1)[0]).rstrip(),
        "title": (((filename.rsplit("/", 1)[1]).rsplit("-", 1)[1]).rsplit(".", 1)[0]).lstrip(),
        "cat-id": " " 
    }


""" 
handles eye d three 
"""
def walk_directory(input_dir):
    for filename in list_files_recursive(input_dir):
        file = parse_filename(filename)
        try:
            if (args.print):
                print_tags(file)
            if (args.retag):
                tag_title_artist(file)
        except MutagenError:
            print("Loading " + filename + " failed :(")

""" 
writes title artist tags
"""
def tag_title_artist(file):
    audio = EasyID3(file["path"])
    audio["title"] = file["title"]
    audio["artist"] = file["artist"]
    print_verbose(args.verbose, verbose_str="Renamed " + file["filename"])
    audio.save()


""" 
print metadata 
"""
def print_tags(file):
    audio = EasyID3(file["path"])
    print(file["path"])
    for line in iter(audio.pprint().splitlines()):
        print("   " + line)


""" 
main 
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tag My FLAC')
    parser.add_argument("-s", "--source", type=str, help="source path of directory of your files")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-r", "--retag", help="tags title and artist", action="store_true")
    parser.add_argument("-p", "--print", help="print metadata tags", action="store_true")

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    if (args.source): 
        """ print_verbose(args.verbose, args.source, "You provided the following source directory: " + args.source) """
        walk_directory(args.source)
    else:
        print("Please provide an input directory")
        parser.print_usage()
        sys.exit(1)