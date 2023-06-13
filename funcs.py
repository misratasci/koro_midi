import subprocess, os
import mido

kısık_volume_value = 25
açık_volume_value = 100
metronom_volume_value = 35

# Some midi files use a message with type note_on and 0 velocity instead of a message type note_off:
def signal_is_note_off(msg):
    return msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0)
def signal_is_note_on(msg):
    return msg.type == "note_on" and msg.velocity != 0

# The value should be between 1 and 127. 
def set_track_volume(track, value):
    for message in track:
        if signal_is_note_on(message):
            message.velocity = value

def get_file_name_str(file_name):
    file_name_str = file_name.split(".", 1)[0]
    return file_name_str

def create_folder(file_name):
    folder_name = get_file_name_str(file_name)
    folder_name += "_Midi"
    if os.path.exists(folder_name) == False:
        os.makedirs(folder_name)

def midi2mp3(midi_file):
    file_name = midi_file.split(".", 1)[0]
    subprocess.call(['fluidsynth/bin/fluidsynth.exe', '-ni', '-g', '4', 'sf1.sf3', midi_file, '-F', f'{file_name}.mp3', '-r', '44100'])

eser_partileri_file = open("eser_partileri.txt", "r")
eser_partileri_lines = eser_partileri_file.read().split("\n")
eser_partileri_file.close()

class Eser():
    def __init__(self, file_name):
        self.file_name = file_name
        print(self.file_name)
        self.midi_file = mido.MidiFile(self.file_name, clip=True, type=1)
        self.track_list = self.midi_file.tracks
        self.set_track_names()
        self.set_to_be_saveds()
    def set_track_names(self):
        self.track_names = []
        self.track_name_available = False
        for line in eser_partileri_lines:
            if line.split("\t")[0] == self.file_name:
                self.track_name_available = True
                self.track_names = line.split("\t")[1].split(",")
                if len(self.track_list) != len(self.track_names):
                    self.track_name_available = False
                    print("eser_partileri.txt dosyasında yazan parti ismi sayısı midi dosyasındaki parti sayısı ile uyuşmuyor.\n")
                    print(f"eser_partileri.txt'deki parti sayısı: {len(self.track_names)}")
                    print(f"midi dosyasındaki parti sayısı: {len(self.track_list)}")
                else:
                    print("Partiler, eser_partileri.txt dosyasına göre isimlendirilecek.\nParti isimleri:")
                    for name in self.track_names[:-1]:
                        print(name, end=", ")
                    print(self.track_names[-1])
                    print("Aşağıdaki partiler kaydedilmeyecek:")
                    self.tracks_to_be_not_saved = line.split("\t")[2].split(",")
                    for name in line.split("\t")[2].split(",")[:-1]:
                        print(name, end=", ")
                    print(line.split("\t")[2].split(",")[-1])

        if self.track_name_available == False:

            #sen isimlendirmek ister misin diye sor
            midi_isim_input = input("\nİsimleri ben koyacağım diyorsan araya virgül koyarak parti isimlerini sırasıyla yaz. Koro hariç.\n(Virgülden sonra boşluk bırakma.)\nÖrnek: \"S1,S2,A1,A2,T1,T2,B1,B2,Metronom\"\nMidi dosyasındaki isimler kalsın diyorsan 'enter'a bas.\n")
            print(f"{len(midi_isim_input.split(','))} tane parti ismi girdin.")
            while midi_isim_input and len(midi_isim_input.split(",")) != len(self.track_list):
                midi_isim_input = input("Verdiğin isimlerin sayısı midideki parti sayısıyla uyuşmuyor.\nTekrar yaz veya midinin kendi verdiği isimler olsun diyorsan enter'a bas.\n")
            if len(self.track_list) == len(midi_isim_input.split(",")):
                self.track_names = midi_isim_input.split(",")
            elif midi_isim_input == "":
                print("Parti ismi girmedin, dosyadaki şu isimler kullanılacak:")
                self.track_names = []
                #track isimlerini bir listeye yaz.
                for track in self.track_list:
                    self.track_names.append(track.name)
                
                #eğer orijinal track isimlerinde aynı isimliler varsa track isimlerini numaralandır.
                same_elements = False
                for name in self.track_names:
                    if self.track_names.count(name) > 1:
                        same_elements = True
                if same_elements == True:
                    i = 1
                    temp_list = []
                    for name in self.track_names:
                        if name != "":
                            name = name+f"_{i}"
                        else:
                            name = f"{i}"
                        temp_list.append(name)
                        i += 1
                    self.track_names = temp_list
                for name in self.track_names[:-1]:
                    print(name, end=",n")
                print(self.track_names[-1])
            
            
        #for name in self.track_names:
            #if " " in name:
            #    name = name.replace(" ", "_")
    def set_to_be_saveds(self):
        self.save_dict = {}
        for track in self.track_names:
            self.save_dict[track] = True
        if self.track_name_available == True:
            for inp in self.tracks_to_be_not_saved:
                self.save_dict[inp] = False 
        elif self.track_name_available == False:
            #hangilerini kaydetmek istiyorsun diye sor. kaydedilecekler için True veren bir dict yap. onu aşağıdaki loopta kullan.
            which_tracks_to_save_input = input("Kaydedilmesini **istemediğin** partilerin isimlerini aynı şekilde arada virgül olacak şekilde gir.\nHepsi kaydedilsin diyorsan enter'a bas.\n")
            if which_tracks_to_save_input:
                for inp in which_tracks_to_save_input.split(","):
                    while inp not in self.track_names:
                        which_tracks_to_save_input = input("Girdiğin parti isimlerinden en az biri midideki isimler ile (veya senin az önce koyduğun isimler ile) uyuşmuyor.\nTekrar gir, veya bütün partiler kaydedilsin diyorsan enter'a bas.\n")
            for inp in which_tracks_to_save_input.split(","):
                self.save_dict[inp] = False   
#a = Eser("Pseudo_Yoik.mid")