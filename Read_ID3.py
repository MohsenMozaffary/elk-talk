from mutagen.id3 import ID3

def print_id3_metadata(mp3_file):
    audiofile = ID3(mp3_file)
    
    for key in audiofile.keys():
        print(key, ":", audiofile[key])

# Usage example
#mp3_file_path = mp3_file_path

#print_id3_metadata(mp3_file_path)