import mido as M
from mido import MidiFile
from mido import Parser

from sys import argv

#quantize note lengths appropriately
def quantize_note_length(note_length):
    pass    

#parse note data from track to list of notes
def parse_note_data(track, ticks_per_beat):
    print(ticks_per_beat)
    note_data  = []
    being_played = set()
    tempo = 1
    beats_per_measure = 4
    unit_length = 4
    for msg in track:
        if msg.type   == 'note_on': 
            if msg.time != 0 and msg.velocity != 0:
                being_played.add((msg.note, msg.time/ticks_per_beat))
                note_data.append((msg.note, msg.time/ticks_per_beat))
            #if msg.velocity == 0:
            #    notes = []
            #    for note in being_played:
            #        notes.append(note)
            #    being_played = set()
            #    if notes != []:
            #        note_data.append(notes)
        elif msg.type == 'note_off':
            pass
        elif msg.type == 'set_tempo':
            tempo = msg.tempo
        elif msg.type == 'time_signature':
            beats_per_measure = msg.numerator
            unit_length = msg.denominator
        else:
            print(msg)
    return note_data 



###############################MAIN PROCESS#####################################
output_directory = ""
midi_files = []
for arg in argv[1:]:
    if ".mid" in arg or ".MID" in arg:
        if len(midi_files) == 1:
            continue #only consider 1 song for now
        midi_files.append((MidiFile(arg), arg))
    elif "--dir=" in arg:
        output_directory = arg.replace("--dir=", "")
    else:
        print("Unexpected argument: " + arg)
        print("Expecting midi file (.mid, .MID) or outputfile path")

note_data = []
for i, midi_file in enumerate(midi_files):
    mid, name = midi_file
    merged = M.merge_tracks(mid.tracks)
    note_data.append(parse_note_data(mid.tracks[0], mid.ticks_per_beat))
    print(name)
    print(note_data)

