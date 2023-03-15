#!/usr/bin/env python3.10


def oneline_fasta(fasta):
    '''Tranforms the sequences in a FAST file to 1 continous sequence line and writes it out to a new file
        called "one_line.fa." In this new temporary file, it will also return the # of records to double check this #
        with the # header lines in the output file = confirm accurate output'''
    
# make dict with headers as keys and sequences as values
    seq_dict = {}
    with open(fasta, 'r') as fa:
        line_count = 0

        for l in fa:
            line_count +=1
            line = l.strip('\n')

        # only get header lines
            if line[0] == '>':
                header = line

                if header not in seq_dict:
                    seq_dict[header] = ""
                else:
                    seq_dict[header] += sequence
                    
            else:
                sequence = line
                seq_dict[header] += sequence
    
    # write out to file
    onelinefasta= open('oneline_fasta.fa', 'w')
    for keys,vals in seq_dict.items():
        onelinefasta.write(str(keys) + '\n' + str(vals) + '\n')
    onelinefasta.close()
    return onelinefasta



