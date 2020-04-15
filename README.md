# TagMyFlac
ID3 tagger for music files

**Installation**

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
usage: tagmyflac.py [-h] [-s SOURCE] [-v] [-r] [-p]

Tag My FLAC

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source path of directory of your files
  -v, --verbose         increase output verbosity
  -r, --retag           tags title and artist
  -p, --print           print metadata tags
```

You can always access this help page via the `-h` or `--help` flags.

**Basic usage scenarios**

1.) 
Supppose you have some online rips of songs.
Name them the following way: 
`ARTIST NAME - SONG TITLE [CAT_ID].mp3`

You can then use TagMyFlac to automatically add the given ID3 metadata for the files in the source directory *recursively*:

```
python3 tagmyflac.py -vrs <source directory>
```

Do not forget to add a trailing slash `/` after the directory name.