import argparse, string, sys, glob, mutagen, json, datetime
from mutagen.mp3 import MP3, MutagenError
from mutagen.easyid3 import EasyID3, EasyID3KeyError
from mutagen.id3 import ID3NoHeaderError

hello = r"""
      ___           ___           ___                    ___           ___     
     /\  \         /\  \         /\  \                  /\__\         |\__\    
     \:\  \       /::\  \       /::\  \                /::|  |        |:|  |   
      \:\  \     /:/\:\  \     /:/\:\  \              /:|:|  |        |:|  |   
      /::\  \   /::\~\:\  \   /:/  \:\  \            /:/|:|__|__      |:|__|__ 
     /:/\:\__\ /:/\:\ \:\__\ /:/__/_\:\__\          /:/ |::::\__\     /::::\__\
    /:/  \/__/ \/__\:\/:/  / \:\  /\ \/__/          \/__/~~/:/  /    /:/~~/~   
   /:/  /           \::/  /   \:\ \:\__\                  /:/  /    /:/  /     
   \/__/            /:/  /     \:\/:/  /                 /:/  /     \/__/      
                   /:/  /       \::/  /                 /:/  /                 
                   \/__/         \/__/                  \/__/                  
             ___           ___       ___           ___           ___     
            /\  \         /\__\     /\  \         /\  \         /\  \    
           /::\  \       /:/  /    /::\  \       /::\  \       /::\  \   
          /:/\:\  \     /:/  /    /:/\:\  \     /:/\:\  \     /:/\ \  \  
         /::\~\:\  \   /:/  /    /::\~\:\  \   /:/  \:\  \   _\:\~\ \  \ 
        /:/\:\ \:\__\ /:/__/    /:/\:\ \:\__\ /:/__/ \:\__\ /\ \:\ \ \__\
        \/__\:\ \/__/ \:\  \    \/__\:\/:/  / \:\  \  \/__/ \:\ \:\ \/__/
             \:\__\    \:\  \        \::/  /   \:\  \        \:\ \:\__\  
              \/__/     \:\  \       /:/  /     \:\  \        \:\/:/  /  
                         \:\__\     /:/  /       \:\__\        \::/  /   
                          \/__/     \/__/         \/__/         \/__/    
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


""" calls the apporiate functions based on flags """
def argument_check(filename, songs=None):
    file = parse_filename(filename)
    try:
        audio = EasyID3(filename)
        if (args.scrape):
            delete_tags(file, audio)
        if (args.retag):
            retag_from_filename(file, audio)
        if (args.tags):
            write_tags(args.tags, file, audio)
        if (args.print):
            print_tags(file, audio)
        if (args.export):
            songs[file["filename"]] = get_tags(audio)
            return songs
    except ID3NoHeaderError:
        print("No ID3 tags found for " + file["filename"])
        print("Adding empty tags")
        meta = mutagen.File(file["path"], easy=True)
        meta.add_tags()
        meta.save(file["path"], v1=2)
    except MutagenError:
        print("Loading " + filename + " failed :(")


""" handles eye d three """
def walk_directory(input_dir):
    songs = {}
    is_directory = False
    for filename in list_files_recursive(input_dir):
        is_directory = True
        songs = argument_check(filename, songs)

    # a file was provided for source, check
    if not is_directory:
        argument_check(input_dir)

    if (args.export):
        export_tags(songs, input_dir)

""" writes tags provided in JSON format """
def write_tags(tags, file, audio):
    if "{" and "}" in tags:
        try:
            tags_json = json.loads(tags)
        except ValueError:
            print("Wrongly formatted JSON!")
            print("Sample format: '{\"genre\": \"minimal\"}'")
            sys.exit(1)
            
        for key in tags_json:
            try:
                audio[key] = tags_json[key]
            except EasyID3KeyError:
                print("Provided key " + key + " is invalid.")
                print("Run with --print_valid_keys flag to check available keys")
                sys.exit(1)

    print("Added tags to " + file["filename"])
    audio.save()


""" delete tags from file """
def delete_tags(file, audio):
    audio.delete()
    # adding empty tags back in
    meta = mutagen.File(file["path"], easy=True)
    meta.add_tags()
    meta.save(file["path"], v1=2)
    print_verbose(args.verbose, "Deleted tags from " + file["filename"])


""" retags song from filename """
def retag_from_filename(file, audio):
    for key in file["metadata"]:
        audio[key] = file["metadata"][key]
    print_verbose(args.verbose, verbose_str="Renamed " + file["filename"])
    audio.save()


""" returns a dictionary of song tags """
def get_tags(audio):
    tags = {}
    for key in sorted(audio.keys()):
        values = audio[key]
        for value in values:
            tags.update({key: value})
    return tags


""" print metadata """
def print_tags(file, audio):
    print(file["filename"])
    tags = get_tags(audio)
    if tags:
        print(json.dumps(tags, sort_keys=True, indent=4))
    else:
        print("   no tags")


""" export tags """
def export_tags(songs, input_dir):
    filename = "dumps-" + datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S") + ".json"
    with open(filename, "w") as fp:
        json.dump(songs, fp, indent=4)
    print("Dumped metadata of folder " + input_dir + " in file " + filename)


""" main """
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tag My FLAC')
    parser.add_argument("-s", "--source", type=str, help="source path of directory of your files")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-r", "--retag", help="tags title and artist", action="store_true")
    parser.add_argument("-p", "--print", help="print metadata tags", action="store_true")
    parser.add_argument("--scrape", help="scrape ID3 tags from files", action="store_true")
    parser.add_argument("--print_valid_keys", help="print taggable keys list", action="store_true")
    parser.add_argument("-t", "--tags", type=str, help="write the provided key-value pairs as tags")
    parser.add_argument("-e", "--export", help="export song metadata in JSON", action="store_true")

    print(hello)

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