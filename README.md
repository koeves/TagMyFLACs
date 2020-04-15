# TagMyFlac
ID3 tagger for music files

## Installation

Clone or download the repo, `cd` into the directory

Use `pip3` to install requirements:

```
sudo -H pip3 install -r requirements.txt
```

Run `tagmyflac.py`:

```
python3 tagmyflac.py -h
```

The output should now be the following:

```
usage: tagmyflac.py [-h] [-s SOURCE] [-v] [-r] [-p] [--scrape]
                    [--print_valid_keys]

Tag My FLAC

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source path of directory of your files
  -v, --verbose         increase output verbosity
  -r, --retag           tags title and artist
  -p, --print           print metadata tags
  --scrape              scrape ID3 tags from files
  --print_valid_keys    print taggable keys list
```

You can always access this help page via the `-h` or `--help` flags.

## Basic usage scenarios

### I. Basic metadata from filename
Supppose you have some online rips of songs.
Name them the following way: 
`ARTIST NAME - SONG TITLE [CAT_ID/ALBUM NAME -- optional].mp3`

You can then use TagMyFlac to automatically add the given ID3 metadata for the files in the source directory *recursively*:

```
python3 tagmyflac.py -vrs <source directory>
```
 
#### A note on source directory paths
By default, when you provide a directory's path you would exclude the trailing slash `/`. This however will result in file changes only *one level* down the tree. Would you prefer to walk all subdirectories, put an ending slash `/` after the source directory path.

### II. Scraping tags from files

You can reset the tags from your files by running

```
python3 tagmyflac.py --scrape -vs <source directory>
```

The `--scrape` flag reinitialises the files again, so you can run the `--retag` option easily.  
  
Scenarios I. and II. can also be combined naturally:
```
python3 tagmyflac.py --scrape -vrs <source directory>
```

### III. Printing all tags of a file

Just use the `-p` or `--print` flags:

```
python3 tagmyflac.py --print -s <source directory>
```