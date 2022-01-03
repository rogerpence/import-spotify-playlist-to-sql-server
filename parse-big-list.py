def readfile():
    with open('rp-big-list.txt', encoding='utf-8') as f:
        lines = f.readlines()
    return lines

def get_artist(lines):
    artists = []
    for line in lines:
        line = line.strip()
        first_dash_location = line.find(' - ')
        artist = line[0:first_dash_location]
        if not artist in artists: 
            artists.append(artist)
    return artists            

def create_sql_populate_artist(artists):
    sql_lines = []

    prefixWithThe = 0
    for artist in artists:
        if artist.startswith('The '):
            artist = artist.replace('The ', '')
            prefixWithThe = 1
        else:
            prefixWithThe = 0             

        artist = artist.replace("'", "''").strip()
        values = F"('{artist}', CURRENT_TIMESTAMP, {prefixWithThe});"
        sql_lines.append('INSERT INTO [dbo].[Artist] ([Name], [Added], [PrefixWithThe]) VALUES')
        sql_lines.append(values) 

    sql = '\n'.join(sql_lines)[:-1]        
    with open('populate_artist.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    print(F"populate_artist.sql file written." )        

def create_sql_populate_song(lines):
    unique_songs = []
    duplicate_songs = []
    sql_lines = []

    sql_lines.append('Drop Table If Exists [dbo].[Song]')

    sql_lines.append('-- One to one relationship with Artist.')
    sql_lines.append('CREATE TABLE [dbo].[Song]')
    sql_lines.append('(')
    sql_lines.append('[Id] INT NOT NULL PRIMARY KEY IDENTITY,')
    sql_lines.append('    [ArtistId] INT FOREIGN KEY REFERENCES [dbo].[Artist](Id),')
    sql_lines.append('    [Title] NVARCHAR(200) NOT NULL,')
    sql_lines.append('    [Added] datetime,')
    sql_lines.append('    [Updated] datetime')
    sql_lines.append(')')
    sql_lines.append('')    
    sql_lines.append('declare @artistId int') 
    sql_lines.append('')    

    lines.sort()
    
    for line in lines:
        line = line.strip()
        if not line in unique_songs:
            unique_songs.append(line)
            first_dash_location = line.find(' - ')
            artist = line[0:first_dash_location].replace("'", "''")            
            if artist.startswith('The '):
                artist = artist.replace('The ', '')     
            song = line[first_dash_location + 2:].strip().replace("'", "''")            
            sql_lines.append(F"set @artistId = (Select Id from Artist where Name = '{artist}')")
            sql_lines.append(F"INSERT INTO [dbo].[Song] (ArtistId, Title, Added)   VALUES(@artistId,'{song}', CURRENT_TIMESTAMP)") 
        else:
            duplicate_songs.append(line)

    sql = '\n'.join(sql_lines)
    with open('populate_song.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    print(F"populate_song.sql file written." )        

    duplicate_songs.sort()
    dupes = '\n'.join(duplicate_songs)
    with open('duplicate_songs.txt', 'w', encoding='utf-8') as f:
        f.write(dupes) 
    print(F"duplicate_songs.txt file written." )        





if __name__ == '__main__':
    lines = readfile()
    artists = get_artist(lines)
    artists.sort()

    create_sql_populate_artist(artists)        

    create_sql_populate_song(lines)    


    
