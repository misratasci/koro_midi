from mido import MidiFile
from funcs import midi2mp3, set_track_volume, create_folder, get_file_name_str, Eser
import os

kısık_volume_value = 25
açık_volume_value = 100

#dosyaları mp3e çevirelim mi diye sor
mp3_input = input("Bu program içinde bulunduğu dosyadaki bütün .mid dosyaları için birer klasör açar, ve bu klasörlere dosyayı partilerine ayrılmış şekilde .mid ve (istersen) .mp3 formatlarında kaydeder.\n\nDosyalar mp3'e de çevrilsin mi? (y/n)\n")
while not (mp3_input == "y" or mp3_input == "n"):
    mp3_input = input("Evet için 'y', hayır için 'n' yazın.\n")
if mp3_input == "y":
    mp3_convert = True
elif mp3_input == "n":
    mp3_convert = False

#scriptin bulunduğu dosyadaki bütün .mid dosyalarını bir listeye koy:
midi_file_list = []
for file in os.listdir():
    if file.endswith(".mid"):
        midi_file_list.append(file)

#eğer klasörde midi dosyası yoksa raise exception.
if len(midi_file_list) <= 0:
    input("Klasörde .mid dosyası yok. Çıkmak için enter'a basın.")
    raise Exception("Klasörde .mid dosyası yok")

eserler = []
for file_name in midi_file_list:
    #if " " in file_name:
    #    file_name = file_name.replace(" ", "_")
    eserler.append(Eser(file_name))
try:
    for eser in eserler:

        #midi dosyası için klasör oluştur:
        create_folder(eser.file_name)
        folder_name = get_file_name_str(eser.file_name) + "_Midi"
        file_name = get_file_name_str(eser.file_name)

        #ilk koro midisi ve mp3ünü kaydet:
        eser.midi_file.save(f"{folder_name}\Koro_{file_name}.mid")
        print(f"{folder_name}\Koro_{file_name}.mid yüklendi.")
        if mp3_convert:
            midi2mp3(f"{folder_name}\Koro_{file_name}.mid")
            print(f"{folder_name}\Koro_{file_name}.mp3 yüklendi.")

        #önce bütün trackleri bir kıs
        for track in eser.track_list:
            set_track_volume(track, kısık_volume_value)

        #sonra hepsini teker teker aç, kaydet ve geri kıs
        for track in eser.track_list:
            set_track_volume(track, açık_volume_value)
            
            track_name = eser.track_names[eser.track_list.index(track)]
            #if " " in track_name:
            #    track_name = track_name.replace(" ", "_")
            file_name_to_be_saved = f"{folder_name}\{track_name}_{file_name}.mid"
            file_name_to_be_saved_wo_extension = f"{folder_name}\{track_name}_{file_name}"

            if eser.save_dict[track_name]: 
                eser.midi_file.save(file_name_to_be_saved)
                print(f"{file_name_to_be_saved} yüklendi.")
                if mp3_convert:
                    midi2mp3(file_name_to_be_saved)
                    print(f"{file_name_to_be_saved_wo_extension}.mp3 yüklendi.")

            set_track_volume(track, kısık_volume_value)
        print()
    input("Kazasız belasız kaydettik. Çıkmak için enter.")

except Exception as e:
    print()
    print(e, "Bir sıkıntı çıktı. Çıkmak için enter", sep="\n")
    input()
