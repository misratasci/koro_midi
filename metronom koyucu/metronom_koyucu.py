import mido
import os


midi_file_list = []

for file in os.listdir():
    if file.endswith(".mid"):
        midi_file_list.append(file)
if len(midi_file_list) <= 0:
    input("Klasörde .mid dosyası yok. Çıkmak için enter'a basın.")
    raise Exception("Klasörde .mid dosyası yok")
for file_name in midi_file_list:
    if " " in file_name:
        file_name = file_name.replace(" ", "_")

for midi_file in midi_file_list:
    mid = mido.MidiFile(midi_file, clip=True, type=1)
    #yeni track ekle
    track = mido.MidiTrack()
    mid.tracks.append(track)
    #uzun uğraşlar sonucu buldum ki: program 116, note 76 wood blocksun a sesi, 77de b sesi.
    #programdan emin değilim 120de falan da geçerli olabilir.
    track.append(mido.Message('program_change', program=116, time=0))
    #480 bir dörtlük'ün time ı.

    timesum = 0
    sigler_num = []
    sigler_denom = []
    sig_times = []
    for a in mid.tracks[0]:
        timesum += a.time
        if a.type == "time_signature":
            sigler_num.append(a.numerator)
            sigler_denom.append(a.denominator)
            sig_times.append(timesum)
            timesum = 0

    sig_times = sig_times[1:]
    sig_times.append(timesum)
    sig_ind = 0
    for sig in sigler_num:
        num = sigler_num[sig_ind]
        denom = sigler_denom[sig_ind]
        sig_time = sig_times[sig_ind]
        
        olcu_sayisi = int(sig_time/num/(480*4/denom))
        #print(num,denom,olcu_sayisi, end="\t")
        if denom == 4:
            for olcu in range(olcu_sayisi):
                #bir ölçü için metronom gir
                track.append(mido.Message('note_on', note=76, velocity=80, time=0))
                track.append(mido.Message('note_on', note=76, velocity=0, time=480))
                for i in range(num-1):
                    track.append(mido.Message('note_on', note=77, velocity=80, time=0))
                    track.append(mido.Message('note_on', note=77, velocity=0, time=480))
        #ileride 5 8lik falan için de bişey düşünebilirsin
        elif denom == 8 and num % 3 == 0:
            for olcu in range(olcu_sayisi):
                #bir ölçü için metronom gir
                track.append(mido.Message('note_on', note=76, velocity=80, time=0))
                track.append(mido.Message('note_on', note=76, velocity=0, time=720))
                for i in range(int(num/3)-1):
                    track.append(mido.Message('note_on', note=77, velocity=80, time=0))
                    track.append(mido.Message('note_on', note=77, velocity=0, time=720))
        elif denom == 8 and num % 2 == 0 and num % 3 != 0:
            for olcu in range(olcu_sayisi):
                #bir ölçü için metronom gir
                track.append(mido.Message('note_on', note=76, velocity=80, time=0))
                track.append(mido.Message('note_on', note=76, velocity=0, time=480))
                for i in range(int(num/2)-1):
                    track.append(mido.Message('note_on', note=77, velocity=80, time=0))
                    track.append(mido.Message('note_on', note=77, velocity=0, time=480))
        elif denom == 2:
            for olcu in range(olcu_sayisi):
                #bir ölçü için metronom gir
                track.append(mido.Message('note_on', note=76, velocity=80, time=0))
                track.append(mido.Message('note_on', note=76, velocity=0, time=960))
                for i in range(num-1):
                    track.append(mido.Message('note_on', note=77, velocity=80, time=0))
                    track.append(mido.Message('note_on', note=77, velocity=0, time=960))
        else:
            track.append(mido.Message('note_on', note=76, velocity=80, time=0))
            track.append(mido.Message('note_on', note=76, velocity=0, time=sig_time))

        sig_ind += 1

    #for m in mid.tracks[0]:
    #    print(m)
    #print(f"{midi_file[:-4]}_metronomlu.mid")
    mid.save(f"{midi_file[:-4]}_metronomlu.mid")
