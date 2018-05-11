import mido as M
from mido import MidiFile
from mido import Parser

from sys import argv
import os.path
import numpy as np



#quantize note lengths appropriately
def quantize(note_length):
    lengths = [.03125, .0416, .0625, .0833, .125, .1667, .25, .3333, .5, .75,\
                1, 1.25, 1.5, 1.75, 2, 2.5, 2.5, 2.75, 3, 3.5, 4, 4.5, 5, 6, 7,\
                8, 9, 10, 12, 16,24]

    diffs = np.zeros((len(lengths)))
    for i, l in enumerate(lengths):
        diffs[i] = abs(l - note_length)
    closest = min(diffs)
    return list(diffs).index(closest)

#parse note data from track to list of notes
def parse_note_data(track, ticks_per_beat):
    note_data  = []
    being_played = {}
    tempo = 1
    beats_per_measure = 4
    unit_length = 4
    current_time = 0
    note_counter = 0
    for msg in track:
        current_time += msg.time
        if msg.type   == 'note_on': 
            if msg.velocity != 0: #note pressed
                note_counter += 1
                note_data.append([])
                if msg.time != 0: #rest since previous note
                    pass #being_played[msg.note] = msg.time/ticks_per_beat  
                being_played[msg.note] = current_time 
            elif msg.velocity == 0 and msg.note in being_played: #note released
                duration = current_time - being_played[msg.note]
                note_data[note_counter - 1].append((msg.note, quantize(duration/ticks_per_beat)))
                del being_played[msg.note]
        elif msg.type == 'note_off':
            pass
        elif msg.type == 'set_tempo':
            tempo = msg.tempo
        elif msg.type == 'time_signature':
            beats_per_measure = msg.numerator
            unit_length = msg.denominator
        else:
            pass
    return list(filter(([]).__ne__,note_data))

def generate_graph(note_data):
    if len(note_data) == 0:
        return []

    notes = {} 
    note_index = 0
    for chord in note_data:
        for note in chord:
            if note not in notes:
                notes[note] = note_index
                note_index += 1
    adjMatrix = np.zeros((len(notes), len(notes)))
    
    prev_notes = []
    for chord in note_data:
        for note in chord:
            for prev in prev_notes:
                adjMatrix[notes[prev]][notes[note]] += 1
            for other in chord:
                if note != other:
                    adjMatrix[notes[note]][notes[other]] += 1

        prev_notes = chord
    return adjMatrix

def write_graph(adjMatrix, directory, filename):
    if adjMatrix == []:
        return
    fullname = os.path.join(directory, filename + ".grph")
    fullname = directory + "/" + filename
    outfile = open(fullname, 'w')
    for row in range(len(adjMatrix)):
        for col in range(len(adjMatrix)):
            if adjMatrix[row][col] != 0:
                outfile.write(str(col) + ',' + str(adjMatrix[row][col]) + " ")
        outfile.write("\n")
    outfile.close()

###############################MAIN PROCESS#####################################
output_directory = ""
midi_files = []
for arg in argv[1:]:
    if ".mid" in arg or ".MID" in arg:
        try:
            midi_files.append((MidiFile(arg), arg))
        except:
            print("Unable to open midi file " + arg)
    elif "--dir=" in arg:
        output_directory = arg.replace("--dir=", "")
    else:
        print("Unexpected argument: " + arg)
        print("Expecting midi file (.mid, .MID) or outputfile path")

if output_directory == "":
    print('Not output directory specified')
    quit()

note_data = []
for i, midi_file in enumerate(midi_files):
    mid, name = midi_file
    merged = M.merge_tracks(mid.tracks)
    note_data.append(parse_note_data(merged, mid.ticks_per_beat))
    adjMatrix = generate_graph(note_data[i])
    write_graph(adjMatrix, output_directory, str(i))
    print('Wrote ' + name) 

