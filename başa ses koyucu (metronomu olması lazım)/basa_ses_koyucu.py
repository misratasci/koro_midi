import mido
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
    mid = mido.MidiFile(midi_file, clip=True, type=1)
    for msgs in mid.tracks:
        is_percussion = False
        for a in msgs:
            if a.type == "program_change":
                if a.program != 0:
                    is_percussion = True
                    break
            if a.type == "time_signature":
                dortluks_in_bar = a.numerator * (4/a.denominator)
            if a.type == "note_on":
                ind = msgs.index(a)
                note = a.note
                channel = a.channel
                break
        bir_olculuk_time = int(480*dortluks_in_bar)
        if not is_percussion:
            m = mido.Message("note_on", note=note, time=0, velocity=80, channel=channel)
            n = mido.Message("note_on", note=note, time=bir_olculuk_time, velocity=0, channel=channel)
            p = mido.Message("note_on", note=note, time=bir_olculuk_time, velocity=0, channel=channel)
            r = mido.Message("note_on", note=note, time=0, velocity=0, channel=channel)
            #time=480 bir dörtlük oluyor. 
            msgs.insert(ind,m)
            msgs.insert(ind+1,n)
            msgs.insert(ind+2,p)
            msgs.insert(ind+3,r)
        else:
            time_sum = 0
            for m in msgs[:20]:
                if m.type == 'note_on' or m.type == 'note_off':
                    time_sum += m.time
                if time_sum > 2*bir_olculuk_time:
                    ind = msgs.index(m)
            eklenecek = msgs[:ind]
            msgs = eklenecek + msgs
    mid.save(f"Output/{midi_file}")