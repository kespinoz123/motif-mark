#!/usr/bin/env python

#########
# Imports
#########

import argparse
import re
import cairo
import bioinfo 

##################
# Global Constants
##################

LEFT_MARGIN_X = 100
GENE_HEADER_Y_MARGIN = 60

# ALL CAPS = global variable, have access to it everywhere
MOTIF_COLOR_LIST = [(0.7, 0.1, 1), (1, 0.2, 0.2), (1, 0.5, 1), (1, 1, 0)]
MOTIF_COLOR_DICT = {} # keys = motif_string (eg. YCGA) and my values = colors for each individual motif (eg. (0.7, 0.1, 1))

MOTIF_LEGEND_POSITION = {MOTIF_COLOR_LIST[0]: 800, MOTIF_COLOR_LIST[1]:805, MOTIF_COLOR_LIST[2]: 810,MOTIF_COLOR_LIST[3]: 815}
#######
# Args
#######

def get_args():
    parser = argparse.ArgumentParser(description="A program to visualize different motifs on DNA sequences using pycairo")
    parser.add_argument("-f", "--fasta", help="designates absolute file path to fasta file")
    parser.add_argument("-m", "--motif", help="designates absolute file path to motif file")
    return parser.parse_args()

args=get_args()

# Re-writing the Args commands
fasta_file = args.fasta
motif_file = args.motif

############
# Functions
############

def setup_pycairo():
    '''Setting Up Surface and Context using Pycairo'''

    # Size of Canvas
    WIDTH = 1100
    HEIGHT = 900

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)

    # Create context 
    context = cairo.Context(surface)

    # Saving background/canvas in white filled color 
    context.set_source_rgb(255,255,255)
    context.paint()

    return surface, context


############
# Classes
############

class Gene():
    def __init__(self, context, gene_item, gene_name, gene_start, gene_end, y_offset) -> None:
        self.context = context
        self.gene_name = gene_name
        self.gene_item =gene_item
        self.gene_start = gene_start
        self.gene_end = gene_end
        self.y_offset = y_offset
    
    # do def draw and change thickness for gene to smaller
    def draw_my_gene(self):

        # Width of 2 for a fine line and grey colored
        self.context.set_line_width(2)
        self.context.set_source_rgba(0, 0, 0)
        self.context.stroke()

        #start position
        self.context.move_to(self.gene_start+LEFT_MARGIN_X , self.y_offset)        #(x,y)
        
        # end position of line from start position
        self.context.line_to(self.gene_end+LEFT_MARGIN_X, self.y_offset)
        self.context.stroke()
        
        self.context.set_font_size(15)
        self.context.select_font_face("Arial",
                        cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_NORMAL)
        
        self.context.move_to(LEFT_MARGIN_X, self.y_offset-GENE_HEADER_Y_MARGIN)

        self.context.show_text(self.gene_name)

class Exon:
    def __init__(self, context, exon_start, exon_end, ex_offset) -> None:
        self.context = context
        self.exon_start = exon_start
        self.exon_end = exon_end
        self.ex_offset = ex_offset

    
    def draw_my_exon(self):

        # Thicker width for line to differentiate between gene line and exon
        self.context.set_line_width(20)
        # Black colored exons
        self.context.set_source_rgba(0, 0, 0)
        self.context.fill()

        #start position
        self.context.move_to(self.exon_start+LEFT_MARGIN_X, self.ex_offset)        #(x,y)

        # end position of line from start position
        self.context.line_to(self.exon_end+LEFT_MARGIN_X, self.ex_offset)
        self.context.stroke()

class Motif:
    def __init__(self, motif_start, motif_end, y_offset, motif_string) -> None:
        self.y_offset = y_offset
        self.motif_string = motif_string
        self.motif_start = motif_start
        self.motif_end = motif_end
        self.color = MOTIF_COLOR_DICT[motif_string]

    def __repr__(self) -> str:
        '''This functions prints a representive of a motif: Motif(89, 93, 150, YGCY)'''
        return f"Motif({self.motif_start}, {self.motif_end}, {self.y_offset}, {self.motif_string})"
    

    def draw_my_motif(self, context):
        # Thicker width for line to differentiate between gene line and exon
        context.set_line_width(5)
        context.set_source_rgb(*self.color)
        
        #start position
        context.move_to(self.motif_start+LEFT_MARGIN_X, self.y_offset)        #(x,y)

        # end position of line from start position
        context.line_to(self.motif_end+LEFT_MARGIN_X, self.y_offset)
        context.stroke()

#######
# Main 
#######

# Defining my context and surface 
surface, context = setup_pycairo()
  

iupac_dict = {"C":"[C]", "T":"[T]","A":"[A]", "G":"[G]",
              "Y":"[CT]", "R":"[AG]", "W":"[AT]","S":"[CG]",
              "M":"[AC]", "K":"[GT]", "B":"[CGT]", "D":"[AGT]",
              "H":"[ACT]", "V":"[ACG]", "N":"[ACGT]"}

##########################
# Lists of Motif Sequences
##########################

known_motif_dict = {} # This list has the known motif sequences in the input file to look for
# keys = motif string ( eg. YGCY) , values = regex expression for motif (eg. [CT]GC[CT])

with open(motif_file, 'r') as motif_fh:
    base_count = 0
    for i, motif_string in enumerate(motif_fh): # here, I am still printing motifs lowercase and upper in motif input file
        motif_regex = ""
        # BUT it is better to make all motifs upper case to avoid dealing with lowecase motifs
        motif_string = motif_string.strip('\n').upper()
        for base in motif_string:
            if base.upper() in iupac_dict:
                
                # Translating or replacing the iupac key for the actual base of motif sequence
                motif_regex += iupac_dict[base.upper()]
    
       
        known_motif_dict[motif_string] = motif_regex
        MOTIF_COLOR_DICT[motif_string] = MOTIF_COLOR_LIST[i]


# >>>>>>>>>> Converting the input FASTA file to a one line FASTA file <<<<<<<<<<<<<<<<
# This will make the different sequences for each gene into 1 continious sequence/gene
oneline_file = bioinfo.oneline_fasta(fasta_file)

oneline_file = open('oneline_fasta.fa', 'r')
gene_item = 0
y_offset = 0

while True:
    # each iteration = one fasta record
    header = oneline_file.readline()
    sequence = oneline_file.readline()

    
    # Checking the end of file: EOF
    if header == "":
        break
    
    ############################ Building a Gene ################################
    gene_name = header
    gene_item +=1 
    gene_start = 1
    gene_end = len(sequence)
    
    # How far do I want each gene to be apart from the other gene
    y_offset += 150 
    
    gene = Gene(context, gene_item, gene_name, gene_start, gene_end, y_offset)
    gene.draw_my_gene()

############################ EXONS ################################
    exon_positions = []

    # Searching for exon pattern of all upper case letters within my sequence line
    for character in re.finditer(r'[A-Z]', sequence):
        # Storing those upper case characters inside exon_position list
        exon_positions.append(character.start())
        exon_start = exon_positions[0] 
        exon_end = exon_positions[-1] 
        # generate Exon objects and draw them

        exon = Exon(context, exon_start, exon_end, y_offset)
        exon.draw_my_exon()

############################ Building Motifs ################################

    for motif_string, motif_regex in known_motif_dict.items(): 
        for match in re.finditer(motif_regex, sequence, re.IGNORECASE):
            motif_start = match.start()
            motif_end = match.end()
            motif = Motif(motif_start, motif_end, y_offset, motif_string)
            draw = motif.draw_my_motif(context)


#--------------- This is the END ---------------
context.save()

# Saving the pycairo drawing
surface.write_to_png("Figure_1.png")
surface.finish()

# Closing the files used in this script
oneline_file.close()

