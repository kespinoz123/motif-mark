# OOP Motif Mark 👩🏻‍💻 🧬

Author:  Itzel Espinoza  

Date: February 20th, 2023           
                                 

## Purpose of Assignment

The goal of this assignment is to write a python script using object-oriented code to visualize motifs on sequences using pycairo. I'll be using a FASTA file containing reverse complemented DNA sequences, where exons are indicated by upper case letters and introns with lowercase letters following traditional 5’ to 3’ direction.


## Requirements Summary Data Table 

|  Input Files |    Argparse  |             File Size + Description              |     Output File
|--------------|--------------|--------------------------------------------------|-------------------|
|  FASTA File  |     (-f)     |                 Seqs ≤ 1000 base                 |   file_name.png   |
|  Motif File  |     (-m)     |   ≤ 10 bases each, One motif/line in a text file |  To scale         |


### Important Notes
  1. Implement argparse functions
  2. Well commented python script
  > Example: Python script must be named "motif-mark-oop.py"

### List of OOP Classes to implement in Motif Mark Project

1. Find_Motif 

```
It might be useful to create a dictionary where the key(s) are the motifs and values be the counts of how many were found in the given input FASTA         file. 
```

```
Similar to the deduping assignment, I can then store the motifs found in my dictionary and save them in some found_motif list and only keep unique IDs to avoid over counting.  By using dictionaries, I believe I should be able to handle multiple motifs in multiple genes!
```

2. Parse_FASTA 

```
Here, I would keep track of each motif found in FASTA File (Format: 1 record = 4 lines).
```

```
The keys of my dictionary would still be the motifs found, but the value in this case would be the start and stop position of where these motifs 
are found to be able to draw them later using pycairo.
```

3. Draw_Pycairo

```
This should create an illustration (to scale) of introns, cassette exons, and the specific location and length of motifs found encoded within that sequence. Short exon = small exon in picture, thin motif = short motif length.
```

```
I can then determine where these motifs are located: upstream, downstream, inside exon etc.
```

```
Another function to color code within motifs and be able to differentiate between 1-4.
Then I can see where motif 1 clusters vs motif 2 etc + legend key.
```

```
A final function to save figure as (f"{file_name}.png") format.
```

4. Other Functions 

```
Another function to identify and classify exons (upstream) given upper cases and introns (downstream) given lowercase bases.
```

```
To identify motifs with flexibility such as having the degenerate bases of Y, I can create a function implementing import re (regex).
Maybe this could also help with translating any ambiguous motifs found in Fasta file. 
```
 
### To make class types interact with each other, I can do the following.

```
I can use the objects created by X class type and make them interact with other objects from another class. 
```

```
For example, I can use the location infomation that make up each of these objects: exon, intron, motif) and include it to the class Pycairo to create a summary illustration up to scale. 
```
