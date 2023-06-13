from mido import MidiFile
from funcs import set_track_volume
import os

midi_file_list = []
for file in os.listdir():
    if file.endswith(".mid"):
        midi_file_list.append(file)
print(len(midi_file_list))
if len(midi_file_list) <= 0:
    input("Klasörde .mid dosyası yok. Çıkmak için enter'a basın.")
    raise Exception("Klasörde .mid dosyası yok")
for file_name in midi_file_list:
    if " " in file_name:
        file_name = file_name.replace(" ", "_")

for midi_file in midi_file_list:
    mid = MidiFile(midi_file, clip=True, type=1)
    for tr in mid.tracks:
        set_track_volume(tr, 80)
    mid.save(midi_file)