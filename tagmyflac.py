import argparse, string, sys, glob, mutagen
from mutagen.mp3 import MP3, MutagenError
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError


r"""       ______                  __   
_________/     \\     ____       / /   _______    ____    ___
|__   __|  ____  |   /  \_\     /_/    |  ___|  //   \\_//  \\
   | |  |  |__|  |  |   _____          |  |_   | |     V    | |
   | |  |        |  |      ||          |   _|  | |     |    | |
   | |  |   __   |   \\___//           |  |____| |          | |
   |_|  |__|  |__|                     |_______|_|          |_|

"""


""" prints verboooose text """
def print_verbose(v, verbose_str=""):
    if v:
        print(verbose_str)


""" creates file list recursively from input dir """
def list_files_recursive(input_dir):
    return glob.iglob(input_dir + "**/*", recursive=True)


""" enumerate all possible id3 keys """
def valid_keys():
    return EasyID3.valid_keys.keys()


""" parses filenames """
def parse_filename(filename):
    return {
        "filename": filename.rsplit("/", 1)[1],
        "path": filename,
        "metadata": {
            "artist": filename.rsplit("/", 1)[1].rsplit("-", 1)[0].rstrip(),
            "title": filename.rsplit("[", 1)[0].rsplit("-", 1)[1].lstrip().rstrip() if "[" in filename
                else filename.rsplit("/", 1)[1].rsplit("-", 1)[1].rsplit(".", 1)[0].lstrip(),
            "album": filename.rsplit("[")[1].rsplit("]")[0].lstrip() if "[" in filename else ""
        }
    }


""" handles eye d three """
def walk_directory(input_dir):
    for filename in list_files_recursive(input_dir):
        file = parse_filename(filename)
        try:
            audio = EasyID3(filename)
            if (args.scrape):
                delete_tags(file, audio)
            if (args.retag):
                tag_title_artist(file, audio)
            if (args.print):
                print_tags(file, audio)
        except ID3NoHeaderError:
            print("No ID3 tags found for " + file["filename"])
            print("Adding empty tags")
            meta = mutagen.File(file["path"], easy=True)
            meta.add_tags()
            meta.save(file["path"], v1=2)
        except MutagenError:
            print("Loading " + filename + " failed :(")


""" delete tags from file """
def delete_tags(file, audio):
    audio.delete()
    """ adding empty tags back in """
    meta = mutagen.File(file["path"], easy=True)
    meta.add_tags()
    meta.save(file["path"], v1=2)
    print_verbose(args.verbose, "Deleted tags from " + file["filename"])


""" writes title artist tag """
def tag_title_artist(file, audio):
    for key in file["metadata"]:
        audio[key] = file["metadata"][key]
    print_verbose(args.verbose, verbose_str="Renamed " + file["filename"])
    audio.save()


""" print metadata """
def print_tags(file, audio):
    print(file["path"])
    for line in iter(audio.pprint().splitlines()):
        print("   " + line)
    else:
        print("   no tags")


""" main """
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tag My FLAC')
    parser.add_argument("-s", "--source", type=str, help="source path of directory of your files")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-r", "--retag", help="tags title and artist", action="store_true")
    parser.add_argument("-p", "--print", help="print metadata tags", action="store_true")
    parser.add_argument("--scrape", help="scrape ID3 tags from files", action="store_true")
    parser.add_argument("--print_valid_keys", help="print taggable keys list", action="store_true")

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    if (args.print_valid_keys):
        print(valid_keys())
    elif (args.source):
        walk_directory(args.source)
    else:
        print("Please provide an input directory")
        parser.print_usage()
        sys.exit(1)

    print("Exited")