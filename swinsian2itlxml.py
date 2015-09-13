#!/usr/bin/env python
# mhite@hotmail.com
# 7/6/2015

# this terrible script is my own weapon of mass destruction, sorry in advance

import argparse
import collections
import datetime
import logging
import math
import os
import plistlib
import sqlite3
import time
import urllib


__VERSION__ = '1.0'
DEFAULT_SQLITE = os.path.expanduser('~/Library/Application Support/Swinsian/Library.sqlite')
DEFAULT_XML = os.path.expanduser('~/Music/iTunes/iTunes Library.xml')
DEFAULT_ITUNES_MUSIC_FOLDER = os.path.expanduser('~/Music/iTunes/iTunes Music/')
NSTimeIntervalSince1970 = 978307200.0

# monkey patch to avoid sorting the dict in the PlistWriter
# class' writeDict() method. Since we monkey patch, this is
# likely to break compatability with anything but Python 2.7.
# I haven't investigated monkey patching other Python versions
# of the plistlib library.

def writeDict(self, d):
    self.beginElement("dict")
    items = d.items()
    #items.sort()
    for key, value in items:
        if not isinstance(key, (str, unicode)):
            raise TypeError("keys must be strings")
        self.simpleElement("key", key)
        self.writeValue(value)
    self.endElement("dict")

plistlib.PlistWriter.writeDict = writeDict


def configure_logging(level, filename):
    """Sets up global logging module.

    Args:
        level: Log level of critical, error, warning, info, or debug.
        filename: Fully qualified filename for log output.
    """
    LOGGING_LEVELS = {'critical': logging.CRITICAL,
                      'error': logging.ERROR,
                      'warning': logging.WARNING,
                      'info': logging.INFO,
                      'debug': logging.DEBUG}
    loglevel = LOGGING_LEVELS.get(level, logging.NOTSET)
    # logging.basicConfig(level=loglevel, filename=filename,
    #                     format='%(asctime)s %(levelname)s: [%(thread)d ' +
    #                     '%(module)s:%(funcName)s %(lineno)d] %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    logging.basicConfig(level=loglevel, filename=filename,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def extant_file(filename):
    """Checks that a file exists for argparse.

    'Type' for argparse - checks that file exists but does not open.

    Args:
        filename: File to test.
    Returns:
        Filename passed to it.
    """
    if not os.path.exists(filename):
        raise argparse.ArgumentTypeError('%s does not exist' % filename)
    return filename


def get_parser():
    """Generates an argparse parser.

    Returns:
        An instantiated argparse parser object.
    """
    parser = argparse.ArgumentParser(description="Swinsian to iTunes XML tool",
                                     fromfile_prefix_chars='@')
    parser.add_argument('--version', '-v', help="Display version",
                        action='version', version=__VERSION__)
    log_group = parser.add_argument_group('logging')
    log_group.add_argument('--log-level', '-l',
                           help='Logging level [%(default)s]',
                           choices=('critical', 'error', 'warning', 'info',
                                    'debug'),
                           dest='loglevel',
                           default='info')
    log_group.add_argument('--log-filename', '-o',
                           help='Logging output filename',
                           action='store', dest='logfile')
    parser.add_argument('--db', '-d',
                        help='Swinsian sqlite database file [%(default)s]',
                        dest='db',
                        type=extant_file,
                        default=DEFAULT_SQLITE)
    parser.add_argument('--xml', '-x',
                        help='iTunes library XML [%(default)s]',
                        dest='xml',
                        default=DEFAULT_XML)
    parser.add_argument('--itunes-music', '-i',
                        help='iTunes music folder [%(default)s]',
                        dest='itunes_music_folder',
                        default=DEFAULT_ITUNES_MUSIC_FOLDER)
    return parser


def generate_xml(swinsian_db, itunes_xml, itunes_music_folder):
    # plist header meta data -- mostly hard-coded for now
    plist_dict = collections.OrderedDict([('Major Version', 1),
                                          ('Minor Version', 1),
                                          ('Date', datetime.datetime.fromtimestamp(time.mktime(time.localtime()))),
                                          ('Features', 5),
                                          ('Show Content Ratings', True),
                                          ('Application Version', '12.1.2.27'),
                                          ('Music Folder', 'file://' + urllib.quote(itunes_music_folder)),
                                          ('Library Persistent ID', '0000000000000001')])
    # database connection
    logging.info('Opening Swinsian database \'%s\'...' % swinsian_db)
    con = sqlite3.connect(swinsian_db)
    with con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # tracks
        logging.info("Generating track information...")
        cur.execute("SELECT title, artist, albumartist, album, grouping, genre, filesize, length, tracknumber, year, bpm, dateadded, bitrate, samplerate, comment, playcount, lastplayed, compilation, track_id, path FROM track")
        rows = cur.fetchall()
        iTunesTrackDict = collections.OrderedDict()
        for row in rows:
            track_id = row['track_id']
            # convert strings to UTF-8
            name = row["title"]
            artist = row["artist"]
            album_artist = row["albumartist"]
            album = row["album"]
            grouping = row["grouping"]
            genre = row["genre"]
            kind = ""
            size = row["filesize"]
            # total_time = int(round(row["length"] * 1000, 10))
            total_time = int(math.ceil(row["length"] * 1000))
            track_number = row["tracknumber"]
            year = row["year"]  # for some reason Serato isn't picking this up
            bpm = row["bpm"]
            date_modified = ""
            date_added = datetime.datetime.fromtimestamp(row["dateadded"] + NSTimeIntervalSince1970)  # convert to date
            bit_rate = row["bitrate"]
            sample_rate = row["samplerate"]
            comments = row["comment"]
            play_count = row["playcount"]
            compilation = bool(row["compilation"])
            persistent_id = "%0.16x".upper() % row["track_id"]
            track_type = ""
            location = "file://" + urllib.quote(row["path"].encode('utf-8'))
            file_folder_count = ""  # no idea what this is for
            library_folder_count = ""  # no idea what this is for

            track_dict = {'Track ID': track_id,
                          'Name': name,
                          'Artist': artist,
                          'Album Artist': album_artist,
                          'Album': album,
                          'Grouping': grouping,
                          'Genre': genre,
                          'Size': size,
                          'Total Time': total_time,
                          'Track Number': track_number,
                          'Year': year,
                          'BPM': bpm,
                          'Bit Rate': bit_rate,
                          'Sample Rate': sample_rate,
                          'Comments': comments,
                          'Play Count': play_count,
                          'Compilation': compilation,
                          'Persistent ID': persistent_id,
                          'Location': location,
                          'Kind': 'MPEG audio file',
                          'Date Added': date_added}

            if row["lastplayed"]:
                # Swinsian stores 'lastplayed' attribute as number of seconds since 1/1/2001
                play_date_utc = datetime.datetime.fromtimestamp(row["lastplayed"] + NSTimeIntervalSince1970)
                # iTunes XML needs 'Play Date' attribute to be number of seconds elapsed since 1/1/1904
                play_date = int((play_date_utc - datetime.datetime(1904, 1, 1, 0, 0)).total_seconds())
                track_dict['Play Date UTC'] = play_date_utc
                track_dict['Play Date'] = play_date
                if play_date_utc < date_added:
                    logging.warn('%s / %s has a play date earlier than date added, %s [play date] < %s [date added]' % (artist, name, play_date_utc, date_added))

            # Remove k/v pairs whose value is None

            track_dict = dict((k, v) for k, v in track_dict.iteritems() if v != None)

            iTunesTrackDict[str(track_id)] = track_dict

        plist_dict['Tracks'] = iTunesTrackDict

        # playlists

        # master hidden playlist, contains every track

        playlist_array = []
        logging.info("Generating 'master' library hidden playlist...")
        playlist_id = 1
        playlist_persistent_id = "%0.16x".upper() % playlist_id
        playlist_items = []
        for x in plist_dict['Tracks']:
            playlist_track_dict = {'Track ID': int(x)}
            playlist_items.append(playlist_track_dict)
        playlist = {'Name': 'Library',
                    'Master': True,
                    'Playlist ID': playlist_id,
                    'Playlist Persistent ID': playlist_persistent_id,
                    'Visible': False,
                    'All Items': True,
                    'Playlist Items': playlist_items}
        playlist_array.append(playlist)

        # folder playlists
        logging.info("Generating folder playlist information...")
        cur.execute("SELECT * FROM playlist WHERE folder IS NOT NULL")
        rows = cur.fetchall()
        for x, row in enumerate(rows, 2):
            name = row['name']
            playlist_id = x
            playlist_persistent_id = "%0.16x".upper() % row["playlist_id"]
            playlist = {'Name': name,
                        'Playlist ID': playlist_id,
                        'Playlist Persistent ID': playlist_persistent_id,
                        'All Items': True,
                        'Folder': True,
                        'Playlist Items': []}
            # determine if we are inside a folder
            cur.execute('SELECT * FROM playlistfolderplaylist WHERE playlist_id = %s' % row["playlist_id"])
            playlist_parent = cur.fetchall()
            if len(playlist_parent) > 1:
                print "something weird happened, folder can't have more than 1 parent"
                sys.exit()
            elif len(playlist_parent) == 1 and playlist_parent[0]['playlistfolder_id']:
                parent_persistent_id = "%0.16x".upper() % playlist_parent[0]['playlistfolder_id']
                playlist['Parent Persistent ID'] = parent_persistent_id
            playlist_array.append(playlist)

        # normal playlists
        logging.info("Generating playlist information...")
        # query DB for playlists that aren't folder or smart playlists
        cur.execute("SELECT * FROM playlist WHERE folder IS NULL AND smart IS NULL")
        rows = cur.fetchall()
        # iterate through playlists
        for x, row in enumerate(rows, x+1):  # start numbering playlists from where we left off
            name = row['name']
            playlist_id = x
            playlist_persistent_id = "%0.16x".upper() % row["playlist_id"]
            # retrieve list of playlist tracks that match our current playlist_id
            cur.execute("SELECT * FROM playlisttrack WHERE playlist_id = %s" % row['playlist_id'])
            playlist_tracks = cur.fetchall()
            # if the playlist isn't empty, construct the playlist data structure
            if playlist_tracks:
                playlist_items = []
                for playlist_track in playlist_tracks:
                    playlist_track_dict = {'Track ID': playlist_track['track_id']}
                    playlist_items.append(playlist_track_dict)
                playlist = {'Name': name,
                            'Playlist ID': playlist_id,
                            'Playlist Persistent ID': playlist_persistent_id,
                            'All Items': True,
                            'Playlist Items': playlist_items}
                # determine if we are inside a folder in order to set playlist's parent persistent ID attribute
                cur.execute('SELECT * FROM playlistfolderplaylist WHERE playlist_id = %s' % row["playlist_id"])
                playlist_parent = cur.fetchall()
                if len(playlist_parent) > 1:
                    # there shouldn't be more than 1 parent returned in the DB query
                    logging.critical("Unexpected situation: more than one parent associated with playlist ... aborting!")
                    sys.exit()
                elif len(playlist_parent) == 1 and playlist_parent[0]['playlistfolder_id']:
                    # playlist does have a parent folder
                    # set the playlist's parent k/v
                    parent_persistent_id = "%0.16x".upper() % playlist_parent[0]['playlistfolder_id']
                    playlist['Parent Persistent ID'] = parent_persistent_id
                    # populate the playlist_items to each parent -- all the way up the playlist hierarchy tree
                    while parent_persistent_id:
                        # now we need to add the 'track ids' of this playlist to its parent folder 'playlist items'
                        for i, item in enumerate(playlist_array):  # search for parent playlist/folder through simple iteration
                            if item['Playlist Persistent ID'] == parent_persistent_id:  # found playlist/folder matching parent
                                playlist_array[i]['Playlist Items'].extend(playlist_items)  # add playlist's items to parent folder playlist
                                # if the parent also has a parent, reset our parent_persistent_id cursor to it
                                # we do this because we have to attach current playlist to all playlists in the hierarchy,
                                # not just the direct parent
                                if 'Parent Persistent ID' in playlist_array[i]:
                                    parent_persistent_id = playlist_array[i]['Parent Persistent ID']
                                else:
                                    # no parent, we are at top of hierarchy
                                    parent_persistent_id = None  # leave while loop during next eval
                                break  # we found the parent, no need to continue searching -- break out of for loop
                        else:
                            parent_persistent_id = None  # technically we should never hit this, but handle it just in case

                playlist_array.append(playlist)

        plist_dict['Playlists'] = playlist_array
        # Write out plist file
        logging.info('Outputting iTunes XML to \'%s\'...' % itunes_xml)
        plistlib.writePlist(plist_dict, itunes_xml)
        return


def main(arg_list=None):
    parser = get_parser()
    args = parser.parse_args(args=arg_list)
    # configure appropriate logging
    configure_logging(level=args.loglevel, filename=args.logfile)
    logging.debug("args = %s" % args)

    # check to make sure we can write new XML
    # check that DEFAULT_ITUNES_MUSIC_FOLDER exists
    # Need logic to determine 'Kind' key

    generate_xml(swinsian_db=args.db, itunes_xml=args.xml,
                 itunes_music_folder=args.itunes_music_folder)
    logging.info("Done.")


if __name__ == "__main__":
    main()

