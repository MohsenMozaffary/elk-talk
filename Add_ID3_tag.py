from mutagen.id3 import ID3, TIT2, TLAN, TPE1, TALB, TYER, TCON, COMM, TXXX, TCOP

def add_id3_metadata(mp3_file, title=None, language=None, artist=None, album=None, year=None, genre=None, comment=None, copyright=None, additional_tags=None):
    audiofile = ID3(mp3_file)

    if title:
        audiofile["TIT2"] = TIT2(encoding=3, text=title)
    if language:
        audiofile["TLAN"] = TLAN(encoding=3, text=language)
    if artist:
        audiofile["TPE1"] = TPE1(encoding=3, text=artist)
    if album:
        audiofile["TALB"] = TALB(encoding=3, text=album)
    if year:
        audiofile["TYER"] = TYER(encoding=3, text=str(year))
    if genre:
        audiofile["TCON"] = TCON(encoding=3, text=genre)
    if comment:
        audiofile["COMM"] = COMM(encoding=3, lang='eng', desc='', text=comment)
    if copyright:
        audiofile["TCOP"] = TCOP(encoding=3, text=copyright)
    if additional_tags:
        for tag in additional_tags:
            audiofile["TXXX:{}".format(tag)] = TXXX(encoding=3, desc=str(tag), text=str(additional_tags[tag]))

    audiofile.save()

