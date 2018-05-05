import mido as M
from mido import MidiFile
from mido import Parser

from sys import argv
import os.path
import numpy as np

#quantize note lengths appropriately
def quantize_note_length(note_length):
    pass    

#parse note data from track to list of notes
def parse_note_data(track, ticks_per_beat):
    note_data  = []
    being_played = {}
    tempo = 1
    beats_per_measure = 4
    unit_length = 4
    current_time = 0
    current_chord = 0
    note_counter = 0
    for msg in track:
        current_time += msg.time
        if msg.type   == 'note_on': 
            if msg.velocity != 0: #note pressed
                note_counter += 1
                if len(being_played) == 0:
                    note_data.append([])
                    current_chord += 1
                if msg.time != 0: #rest since previous note
                    pass #being_played[msg.note] = msg.time/ticks_per_beat  
                being_played[msg.note] = current_time 
            elif msg.velocity == 0 and msg.note in being_played: #note released
                duration = current_time - being_played[msg.note]
                note_data[current_chord - 1].append((msg.note, duration/ticks_per_beat))
                del being_played[msg.note]
                    
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
            pass
            #print(msg)
    return note_data 

def generate_graph(note_data):
    notes = set()
    for chord in note_data:
        for note in chord:
            print(note)
            notes.add(note)
    
    adjMatrix = np.zeros((len(notes), len(notes)))
    return adjMatrix

def write_graph(adjMatrix, directory, filename):
    fullname = os.path.join(directory, filename[:len(filename) - 3] + "grph")
    fullname = directory + "/" + filename
    outfile = open(fullname, 'w')
    for row in adjMatrix:
        for col in row:
            outfile.write(str(adjMatrix[row][col]) + " ")
        outfile.write("\n")
    outfile.close()

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
    adjMatrix = generate_graph(note_data)
    write_graph(adjMatrix, output_directory, str(i))

