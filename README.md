## Import artists and songs from Spotify 

This script uses a playlist text file export created with [](https://www.tunemymusic.com) to populate Artist and Song tables with SQL. 

The script is hardcoded to read an export file named `rp-bit-list.txt`. 

Three output files are created:

* populate_artist.sql
* populate_song.sql
* duplicate_songs.txt -- this shows the number of song duplicates.
