This file contains notes about data types and structures present in the iTunes XML plist file.

## plist XML sections

### Tracks

|Key|Type|Description|Table|Column|y/n|
|---|----|-----------|-----|------|-----------|
|Track ID|integer|Track identifier|track|track_id|yes|
|Name|string|Title|track|name|yes|
|Artist|string|Artist|track|artist|yes|
|Album Artist|string|Album artist|track|albumartist|yes|
|Composer|string|Composer|track|composer|no|
|Album|string|Album|track|album|yes|
|Grouping|string|Grouping|track|grouping|yes|
|Genre|string|Genre|track|genre|yes|
|Kind|string|See 'Kind' section|||no|
|Size|integer|File size in bytes|track|filesize|yes|
|Total Time|integer|Track length|track|length|yes|
|Disc Number|integer|Disc number|track|discnumber|no|
|Disc Count|integer|Disc total|track|totaldiscnumber|no|
|Track Number|integer|Track number|track|tracknumber|yes|
|Track Count|integer|Track total|track|totaltracknumber|no|
|Year|integer|Year|track|year|yes|
|BPM|integer|Beats per minute|track|bpm|yes|
|Date Modified|date|Last modification date, ie. 2014-06-12T05:34:51Z|||no|
|Data Added|date|Date added to library, ie. 2008-05-09T19:41:13Z|track|dateadded|yes|
|Bit Rate|integer|Audio bit rate, ie. 192|track|bitrate|yes|
|Sample Rate|integer|Audio sample rate, ie. 44100|track|samplerate|yes|
|Volume Adjustment|integer|unknown|||no|
|Comments|string|Track comments|track|comments|yes|
|Album Rating|integer|unknown|||no|
|Album Rating Computed|boolean|unknown|||no|
|Compilation|boolean|Part of compilation album|track|compilation|yes|
|Sort Album|string|unknown|||no|
|Sort Album Artist|string|unknown|||no|
|Sort Artist|string|unknown|||no|
|Play Count|integer|Play count|track|playcount|yes|
|Play Date|integer|Play date encoded as number of seconds elapsed since 1/1/1904, ie. 3269511323|track|lastplayed|yes|
|Play Date UTC|date|Play date, ie. 2007-08-09T20:35:23Z|track|lastplayed|yes|
|Skip Count|integer|unknown|||no|
|Skip Date|date|unknown|||no|
|Artwork Count|integer|unknown|||no|
|Persistent ID|string|16-digit unique hex track identifier, ie. 3B84165CAAA56C98|||yes|
|Track Type|string|unknown||||no|
|Location|string|Percent-encoded file path URL|track|filename|yes|
|File Folder Count|integer|unknown|||no|
|Library Folder Count|integer|unknown|||no|

#### 'Kind'

The following table of supported audio file types ("Kind" in the track plist dict) was determined using the output from the following command:

```
strings /Applications/iTunes.app/Contents/Resources/English.lproj/Localizable.strings matches | grep -i "audio file"
```

The table also shows the file extension mappings the conversion tool uses to populate the Kind key/value pair.

|Kind|Extension|
|---------|----|
|AAC audio file|
|AIFF audio file|
|Apple Lossless audio file|m4a|
|Apple Music AAC audio file|
|Internet audio file|
|MPEG audio file|mp3|
|MPEG-4 audio file|
|Matched AAC audio file|
|Protected AAC audio file|
|Protected MPEG-4 audio file|
|Purchased AAC audio file|
|Purchased MPEG-4 audio file|
|Sound Designer II audio file|
|WAV audio file|

Serato depends on an accurate "Kind" specification in the XML or else the file will fail to play.

#### Supported types

Swinsian

MP3, AAC, ALAC, WAV, FLAC, Ogg Vorbis, AIFF, Opus, AC3, APE WavPack, MusePack, and WMA

Serato

.MP3
.OGG
.AAC
.ALAC/.FLAC
.AIF
.WAV
.WL.MP3

iTunes

