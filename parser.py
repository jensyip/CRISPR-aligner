import argparse
from Bio import SeqIO

#Parser takes in repeat.fna, spacer.fna, and questionables if marked
parser = argparse.ArgumentParser(description='Process document type.')
parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')

parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')
parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')
parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')
parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')
parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')

args = parser.parse_args()


#Open file
#Split file with delimiter "|"

reliable_repeats = parse_fna(reliable_repeats_file)
reliable_spacers = parse_fna(reliable_spacers_file)


def parse_fna(file):
    handle = open(file, "rU")
    for record in SeqIO.parse(handle, "fasta"):
        print(record.id)
    handle.close()



# Data structure with <key=repeat, value=[spacers]> 
sequence_mapping = match_repeat_and_spacers(list_of_repeats, list_of_spacers)

def match_repeat_and_spacers(list_of_repeats, list_of_spacers):
    sequence_mapping = {}
    repeat_sequence_list = []

    for repeat in list_of_repeats:
        sequence_mapping[repeat] = []
        repeat_sequence_list.append(repeat.sequence())
    
    for spacer in list_of_spacers:
        spacer_repeat = spacer.get_corresponding_repeat()
        if spacer_repeat in repeat_sequence_list:
            for repeat_object in sequence_mapping:
                if repeat_object.sequence() == spacer.repeat:
                    sequence_mapping[repeat_object] += spacer
    
    for matching in sequence_mapping:
        if sequence[matching].length() != matching.get_number_of_spacers():
            print("Number of matched spacers to repeat does not match expected.")
            
    return sequence mapping
    
#Store in corresponding class structure
class sequence:
    def __init__(self, sequence_type, sequence, location, questionable=false):
        self.sequence_type = sequence_type
        self.sequence = sequence
        self.location = location
    def get_sequence_type(self):
        return self.sequence_type
    def get_sequence(self):
        return self.sequence
    def get_location(self):
        return self.location

class repeat(sequence):
    
    def __init__(self, sequence_type, sequence, location, number_of_spacers, questionable=false):
        super(repeat, self).__init__(sequence_type, sequence, location, questionable)
        self.number_of_spacers = number_of_spacers
    def get_number_of_spacers(self):
        return self.number_of_spacers

class spacer(sequence):
    def __init__(self, sequence_type, sequence, location, corresponding_repeat, questionable=false):
        super(spacer, self).__init__(sequence_type, sequence, location, questionable)
        self.corresponding_repeat = corresponding_repeat
        self.key = generate_key()
    def get_corresponding_repeat(self):
        return self.get_corresponding_repeat
    
    def generate_key():
        return

