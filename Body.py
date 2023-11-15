import os
import uuid
import subprocess
from pathlib import Path



class wav_creation():
    def __init__(self, sample_rate=44100, channels=1, size = 16):
        self.sample_rate = str(sample_rate)
        self.channels = str(channels)
        self.size = int(size)

    def audio_extraction(self, in_file_name, out_file_name, start, end, vol):

        cmd = ['ffmpeg', '-i', in_file_name,
               '-ac', self.channels,
                '-ar', self.sample_rate,
                '-sample_fmt', 's{}'.format(self.size),
                '-ss', str(start),
                '-to', str(end),
                '-af', 'volume={}'.format(vol),
                out_file_name]
        exec1 = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, startupinfo = subprocess.STARTUPINFO())
        
        exec1.wait()

    def create_repeat_silence(self, in_file_dir, out_file_dir, start, end, repeats, silence_duration, vol, metadata = {}):

        random_name1 = str(uuid.uuid4())
        silence_file_name = str(random_name1 + ".wav")
        random_name2 = str(uuid.uuid4())
        main_file_name = str(random_name2 + ".wav")
        random_name3 = str(uuid.uuid4())
        text_file_name = str(random_name3 + ".txt")

        random_name4 = str(uuid.uuid4())
        final_file_name = str(random_name4 + ".wav")

        
        silence_file_dir = os.path.join(os.path.dirname(out_file_dir), silence_file_name)

        
        main_file_dir = os.path.join(os.path.dirname(out_file_dir), main_file_name)


        text_file_dir = os.path.join(os.path.dirname(out_file_dir), text_file_name)


        silence_file_cmd = ['sox', '-n', '-r', str(self.sample_rate),
                            '-c', str(self.channels),
                            '-b', str(self.size),
                            silence_file_dir,
                            'trim', '0.0', str(silence_duration)
                            ]

        
        exec2 = subprocess.Popen(silence_file_cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo = subprocess.STARTUPINFO())
        exec2.wait()
    
        self.audio_extraction(in_file_dir, main_file_dir, start, end, vol)

        text = ""
        for repeat in range(repeats):
            text += "file '{}'\n".format(silence_file_name)
            text += "file '{}'\n".format(main_file_name)
        with open(text_file_dir, "w", encoding="utf-8") as f:
            f.write(text)

        silence_repeat_cmd = ['ffmpeg', '-f', 'concat', '-i', text_file_dir,
                              '-sample_fmt', 's{}'.format(self.size),
                              '-ac', self.channels,
                              '-ar', self.sample_rate]
        
        for key in metadata:
            new_meta = metadata[key]
            silence_repeat_cmd += ['-metadata', "{}={}".format(key, new_meta)]
        silence_repeat_cmd += [out_file_dir]
        #print(silence_repeat_cmd)
        silence_repeat = subprocess.Popen(silence_repeat_cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo = subprocess.STARTUPINFO())
        silence_repeat.wait()


        os.remove(silence_file_dir)
        os.remove(text_file_dir)
        os.remove(main_file_dir)


        

        


        

#metadata = {}
#metadata["Album"] = "1"
#metadata["Year"] = 222222323
#metadata[""]
#path = 'D:\\PHD\\UI\\ELAN\\data\\051384_Laki_Q_Lex_20210326.WAV'       
#out_path = 'D:\\PHD\\UI\\ELAN\\Results\\0_2021_unknown_Hr_rishi_root4f7ff9ec.mp3' 
#ex = wav_creation()
#ex.create_repeat_silence(path, out_path, 0.001, 2, 3, 2.0, 0.5)




        
               

