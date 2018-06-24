# Graph Algorithms for MIR

## Objectives
The purpose of this project is to explore a novel, graph-based approach to music
information retrieval (MIR). 
Songs are represented using a graph, and features are extracted from the graph
using various graph algorithms. 
These features can be used in machine learning applications, such as 
classification of song by genre or composer.

## Findings
In my experiments, I was able to achieve .98 accuracy in a classical vs. jazz
genre classification problem. I was also able to achieve .92 accuracy in a Bach
vs. Chopin composer classification problem. A report summarizing my findings is
included in the repository (report.pdf).

## Source MIDI data:
[Classical Music for Genre Classification](http://www.piano-midi.de/)  
[Jazz Music for Genre Classification](http://bushgrafts.com/)  
[Classical Music for Artist Classification](http://www.kunstderfuge.com/)  
No MIDI data are included in this repository due to copyright policies.  

## Parsing MIDI files
MIDI data was parsed using [Mido](http://mido.readthedocs.io/en/latest/). In the
utilities folder, miditograph.py will take midi data and output the 
corresponding digraph as an adjacency list. 

## Feature Extraction
In the classification folder, feature\_extraction.py can be used to extract
features from graph data as described above.
