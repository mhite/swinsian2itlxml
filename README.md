# swinsian2itlxml

A tool for generating iTunes library XML from a Swinsian music library
database.

## Background

Currently, DJ software applications such as [Serato](https://serato.com/) and
[Traktor](http://www.native-instruments.com/en/products/traktor/) are able
to access a read-only version of the iTunes library through a special XML
file. Apple briefly describes this XML mechanism in a
[support note](https://support.apple.com/en-us/HT201610):

> The iTunes Library.xml file contains some, but not all, of the same
> information that's stored in the iTunes Library.itl file. The purpose of the
> iTunes Library.xml file is to make your music and playlists available to
> other applications on your computer, such as iPhoto, Garageband, iMovie, and
> third-party software, in OS X Mountain Lion and earlier. These applications
> use this file to make it easier for you to add music from your iTunes library
> to your projects.

iTunes, however, is a bloated monster that starts to fall over with large
libraries typical of a DJ. Enter [Swinsian](http://swinsian.com/).

Swinsian is an excellent Mac OS X music management alternative to iTunes. It
is especially well-suited for large music collections and does not suffer from
the same feature bloat as iTunes.

The swinsian2itlxml script is an attempt to bridge the gap between Swinsian
and DJ software such as Serato by generating an iTunes XML file. Specifically,
the important bits of the iTunes XML is generated using data stored in
Swinsian's sqlite database.

Please note that this script has been tested with Serato DJ only. It may or
may not work with other products like Traktor.

## Warning

This script overwrites the iTunes XML file. It does not back anything up --
use at your own peril!

To force iTunes versions prior to 12.2 to regenerate the XML file, simply
delete it and relaunch iTunes. Do not delete the .itl file.

## Requires

This tool was developed and test with the following:

- macOS Sierra 10.12.4
- Python 2.7.10
- Swinsian 1.13.1 (332)
- Serato DJ 1.9.6 (1964129)

## Limitations

- No Swinsian smart playlist support
- No backup of existing iTunes library XML currently performed

## Installation

No special installation steps required other than cloning the git
repo to the machine hosting the Swinsian library.

```
$ git clone https://github.com/mhite/swinsian2itlxml
```

## Usage

Information about the tool's usage can be viewed with the ```-h``` option.

```
$ cd swinsian2itlxml
$ ./swinsian2itlxml.py -h
usage: swinsian2itlxml.py [-h] [--version]
                          [--log-level {critical,error,warning,info,debug}]
                          [--log-filename LOGFILE] [--db DB] [--xml XML]
                          [--itunes-music ITUNES_MUSIC_FOLDER]

Swinsian to iTunes XML tool

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         Display version
  --db DB, -d DB        Swinsian sqlite database file
                        [/Users/mhite/Library/Application
                        Support/Swinsian/Library.sqlite]
  --xml XML, -x XML     iTunes library XML [/Users/mhite/Music/iTunes/iTunes
                        Library.xml]
  --itunes-music ITUNES_MUSIC_FOLDER, -i ITUNES_MUSIC_FOLDER
                        iTunes music folder [/Users/mhite/Music/iTunes/iTunes
                        Music/]

logging:
  --log-level {critical,error,warning,info,debug}, -l {critical,error,warning,info,debug}
                        Logging level [info]
  --log-filename LOGFILE, -o LOGFILE
                        Logging output filename
```
## Examples

The most basic use case is to just launch the script. Default locations for
the Swinsian database file and the iTunes XML are assumed. Warning messages
about play dates vs. date added may appear -- these are harmless and do
not prevent generation of the iTunes library XML.

```
$ ./swinsian2itlxml.py
2015-09-12 09:10:42 INFO: Opening Swinsian database '/Users/mhite/Library/Application Support/Swinsian/Library.sqlite'...
2015-09-12 09:10:42 INFO: Generating track information...
2015-09-12 09:10:42 WARNING: Destiny's Child / Say My Name has a play date earlier than date added, 2007-10-02 17:37:36 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:10:42 WARNING: Placebo / Pure Morning has a play date earlier than date added, 2007-10-18 15:39:19 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:10:42 WARNING: Massive Attack / Protection (Album Version) has a play date earlier than date added, 2007-11-02 15:44:52 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:10:42 WARNING: Fort Minor F.styles of Beyond / Remember the Name has a play date earlier than date added, 2007-10-19 00:17:59 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:10:42 WARNING: Rihanna Ft. Lil Mama / Umbrella (Remix) has a play date earlier than date added, 2007-10-26 17:02:48 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:10:42 WARNING: Club Nouveau / Lean On Me has a play date earlier than date added, 2007-10-01 15:30:39 [play date] < 2008-05-09 12:41:09 [date added]
2015-09-12 09:10:42 WARNING: Destiny's Child / Jumpin' Jumpin' has a play date earlier than date added, 2007-10-09 13:28:36 [play date] < 2008-05-09 12:41:09 [date added]
...
2015-09-12 09:10:43 WARNING: Smokey Robinson & the Miracles / Mickey's Monkey (Instrumental) has a play date earlier than date added, 2011-08-06 16:43:42 [play date] < 2013-11-28 10:22:20 [date added]
2015-09-12 09:10:43 INFO: Generating 'master' library hidden playlist...
2015-09-12 09:10:43 INFO: Generating folder playlist information...
2015-09-12 09:10:43 INFO: Generating playlist information...
2015-09-12 09:10:43 INFO: Outputting iTunes XML to '/Users/mhite/Music/iTunes/iTunes Library.xml'...
2015-09-12 09:10:50 INFO: Done.
```

This next example uses the ```-d``` option to explicitly specify the location of the
Swinsian sqlite database file.

```
$ ./swinsian2itlxml.py -d ~/Dropbox/Library.sqlite
2015-09-12 09:20:53 INFO: Opening Swinsian database '/Users/mhite/Dropbox/Library.sqlite'...
2015-09-12 09:20:53 INFO: Generating track information...
2015-09-12 09:20:54 WARNING: Destiny's Child / Say My Name has a play date earlier than date added, 2007-10-02 17:37:36 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:20:54 WARNING: Placebo / Pure Morning has a play date earlier than date added, 2007-10-18 15:39:19 [play date] < 2008-05-09 12:41:08 [date added]
...
2015-09-12 09:20:55 WARNING: Smokey Robinson & the Miracles / Mickey's Monkey (Instrumental) has a play date earlier than date added, 2011-08-06 16:43:42 [play date] < 2013-11-28 10:22:20 [date added]
2015-09-12 09:20:55 INFO: Generating 'master' library hidden playlist...
2015-09-12 09:20:55 INFO: Generating folder playlist information...
2015-09-12 09:20:55 INFO: Generating playlist information...
2015-09-12 09:20:55 INFO: Outputting iTunes XML to '/Users/mhite/Music/iTunes/iTunes Library.xml'...
2015-09-12 09:21:01 INFO: Done.
```

To output the iTunes XML into a non-standard location, use the the ```-x```
option.

```
$ ./swinsian2itlxml.py -d ~/Dropbox/Library.sqlite -x test.xml
2015-09-12 09:33:33 INFO: Opening Swinsian database '/Users/mhite/Dropbox/Library.sqlite'...
2015-09-12 09:33:33 INFO: Generating track information...
2015-09-12 09:33:34 WARNING: Destiny's Child / Say My Name has a play date earlier than date added, 2007-10-02 17:37:36 [play date] < 2008-05-09 12:41:08 [date added]
2015-09-12 09:33:34 WARNING: Placebo / Pure Morning has a play date earlier than date added, 2007-10-18 15:39:19 [play date] < 2008-05-09 12:41:08 [date added]
...
2015-09-12 09:33:35 WARNING: Limelight / Ready Or Not - Mondo Dub Mix (Clean) has a play date earlier than date added, 2010-04-08 18:48:51 [play date] < 2013-11-28 10:21:34 [date added]
2015-09-12 09:33:35 WARNING: Kylie / All The Lovers (Dada Life Dub) has a play date earlier than date added, 2010-06-19 19:02:54 [play date] < 2013-11-28 10:21:35 [date added]
2015-09-12 09:33:35 WARNING: Smokey Robinson & the Miracles / Mickey's Monkey (Instrumental) has a play date earlier than date added, 2011-08-06 16:43:42 [play date] < 2013-11-28 10:22:20 [date added]
2015-09-12 09:33:35 INFO: Generating 'master' library hidden playlist...
2015-09-12 09:33:35 INFO: Generating folder playlist information...
2015-09-12 09:33:35 INFO: Generating playlist information...
2015-09-12 09:33:35 INFO: Outputting iTunes XML to 'test.xml'...
2015-09-12 09:33:41 INFO: Done.
```

## Author

[Matt Hite](mailto:mhite@hotmail.com) created swinsian2itlxml.

## Contribute

Your code contributions are welcome. Please fork and open a pull request.

## Change Log

### 1.0.3

- Fix for file classification. This should allow more supported file types to play in Serato DJ.
- Default path to XML updated to reflect iTunes' most current default file path. The old file path was `~/Music/iTunes/iTunes Library.xml`. The new path is `~/Music/iTunes/iTunes Music Library.xml`. If the old behavior was working for you, you may need to explicitly pass the file path via the `--xml` option now.

### 1.0.2

- Fix for `ValueError: strings can't contains control characters; use plistlib.Data instead` crash when XML-unsafe UTF-8 characters were encountered. Thanks to Seth Millstein for sending me a sample Swinsian database exhibiting this issue. Also thanks to [Lendar](https://github.com/Lendar) for submitting a [pull request](https://github.com/mhite/swinsian2itlxml/pull/4) which was the basis for this fix.

### 1.0.1

- Fix for case when folder playlist information SQL query returns empty

### 1.0

- Initial release

## License

Please see [LICENSE](./LICENSE).

