from Add_ID3_tag import add_id3_metadata
from Body import wav_creation
from Create_audio import *
from Read_ID3 import print_id3_metadata
import os
import streamlit as st


def process_main(eaf_dir, saving_dir, sound_dir, vol=0.5, n_repeats = 1, silence_duration = 2, title = "translation"):

    res = eaf_process(eaf_dir)
    ex = wav_creation()
    progress_bar = st.progress(0)
    total_iterations = len(res)
    for i, ann in enumerate(res):
        ann_url = ann['url']
        sound_name = ann_url[2:]
        start = ann['start']
        start = float(start)/1000.0
        end = ann['end']
        end = float(end)/1000.0
        eng_trans = ann['eng_translation']
        ir_trans = ann['ir_translation']
        order = ann['order']
        speaker = ann['speaker']
        language = ann['language']
        year = ann['year']
        ID = ann['item_number']
        sound_path = os.path.join(sound_dir, sound_name)
        out_name = str(order) + "_" + str(year) + "_" + str(speaker) + "_" + str(language) + "_" + str(ir_trans) + "_" + str(eng_trans) + str(ID[-1]) + ".mp3"
        out_path = os.path.join(saving_dir, out_name)
        ex.create_repeat_silence(sound_path, out_path, float(start), float(end), n_repeats, silence_duration, vol)
        add_id3_metadata(out_path, title=title, artist=speaker, year=year, album = ann_url)
        progress_bar.progress((i + 1) / total_iterations)