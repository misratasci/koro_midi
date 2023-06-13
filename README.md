# midi-editors-for-choir

These scripts were made to automate various tasks involving midi files that contain choir songs.

---

mid_mp3_exporter.py creates one midi and mp3 file for each track in the input file, where that track has an increased volume while the others have decreased volumes. This enables each party in the choir (Soprano, Alto, Tenor, Bas ...etc) to have a file for themselves where they hear their part more than others' parts.

To use it, add one or more midi files into the same folder as mid_mp3_exporter.py. Then run it.
The instructions are in Turkish but first the user will be asked whether they want to also save the separated files as mp3.
Secondly, the user will be asked if they want to rename the parts or use the original part names in the midi file. (Press Enter to use the originals, and enter the names without spaces and separated by commas (,) to name the parts. Give the exact same number of tracks as parts. Also there shouldn't be any spaces inside the part names.)
Then the program asks the user to enter the part names that are not going to be saved in the output folder. These parts might be the rythym parts which would have no use to the singers if they have a high volume. 
Finally the program creates a folder that has one midi and (if wanted) one mp3 file for each track with increased volume of that specific track and decreased volume for other tracts. The folder also contains a "choir" file which is the same as the input file with equally high volume parts. 

To use mid_mp3_exporter with a bulk of files, or to avoid writing out the part names each time; one can use eser_partileri.txt as a sort of database. The program reads it to find any midi files with matching names in each line of the text file and if it finds one, just gives the part names inside the text file.
Each line in eser_partileri.txt should have the midi file name, the part names, and the part names that are not going to be outputted all separated with tabs. The part names and the part names that are not going to be outputted should have commas in between them, and no spaces. 

---

make_all_notes_mf.py sets the velocity of each message in the midi file to 80, which can be thought as mezzoforte for every note.
To use it, again add the midi file(s) to the same folder and run the script. The output will be written on the input and have the same name. 

---

metronom_koyucu.py in the "metronom koyucu" folder adds a "metronome" (another tract that has "wood blocks" sound) to the midi file according to the song's time signature with a harder beat at the start of each bar and softer beats.
To use it, add the midi file(s) in the same folder. The outputs will be written in the Output folder.

---

basa_ses_koyucu.py in the "başa ses koyucu (metronomu olması lazım)" adds 2 bars at the start of the song. The first added bar contains the starting note of each track, so that the singers can prepare themselves while practicing and singing on the file.
To use it, add the midi file(s) in the same folder. The outputs will be written in the Output folder. The midi file to be used as input should have a final track which is a rythym track, so it would be better to use it on the output of metronom_koyucu.py if it doesn't have one.

