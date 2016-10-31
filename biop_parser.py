from Bio import SeqIO
import argparse
from sequence_classes import *

def parse_repeats_file(file):
    handle = open(file, "rU")
    mapping_dictionary = {}

    for sequence in SeqIO.parse(handle, "fasta"):
        seq_description = sequence.description.replace(sequence.name + " read_length_100 ", "")
        seq_description = seq_description[1:-1].split(";")
        seq_location = seq_description[0]
        seq_number_spacers = seq_description[1].replace(" number of spacers: ", "")
        seq_scaffold = sequence.id.split("|")[0]
        array_num = sequence.id.split("|")[2]
        seq = Repeat(sequence.seq, seq_scaffold, seq_location, int(array_num), int(seq_number_spacers))
        mapping_dictionary[str(sequence.seq + "_" + array_num)] = seq
    handle.close()
    return mapping_dictionary


def parse_spacers_file(file):
    handle = open(file, "rU")
    mapping_dictionary = {}

    for sequence in SeqIO.parse(handle, "fasta"):
        seq_description = sequence.description.replace(sequence.name + " read_length_100 ", "")
        seq_description = seq_description[1:-1].split(";")
        seq_location = seq_description[0]
        seq_repeat = seq_description[1].replace(" DR: ", "")
        seq_scaffold = sequence.id.split("|")[0]
        array_num = sequence.id.split("|")[2]
        order_num = sequence.id.split("|")[4].split("of")[0]
        seq = Spacer(sequence.seq, seq_scaffold, seq_location, int(array_num), int(order_num), seq_repeat)
        mapping_dictionary[str(sequence.seq)] = seq
    handle.close()
    return mapping_dictionary


def direct_files(repeat_file, spacer_file, questionable_repeats_file=None, questionable_spacers_file=None, question=False):
    print(repeat_file)
    repeat_dict = parse_repeats_file(repeat_file)
    spacer_dict = parse_spacers_file(spacer_file)


    name = repeat_file.split("_")[0]

    if question:
        q_repeat_dict = parse_repeats_file(questionable_repeats_file)
        q_spacer_dict = parse_spacers_file(questionable_spacers_file)
        #merge the repeat and the spacer dictionaries
        pass

    x = Sample(repeat_dict, spacer_dict, name)
    print(x.mapping_dictionary)
    new_spacer_list = []
    dictionary = x.mapping_dictionary
    for repeat in dictionary:
        array = dictionary[repeat]
        list_of_spacers = array.get_spacer_list()
        for spacer in range(len(list_of_spacers)):
            new_spacer_list.append(list_of_spacers[spacer].get_sequence())
            #x = list_of_spacers[spacer]
            #print(list_of_spacers[spacer].get_sequence())
            #print(x.get_location())

    for i in range(len(new_spacer_list)):
        seq1 = new_spacer_list[i]
        for j in range(i + 1, len(new_spacer_list)):
            seq2 = new_spacer_list[j]
            print("Sequences: " + seq1 + " " + seq2)
            print("Result: " +  str(levenshtein(seq1, seq2)))

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def main():
    # Parser takes in repeat.fna, spacer.fna, and questionables if marked
    parser = argparse.ArgumentParser(description='Process document type.')
    parser.add_argument('-q', '--questionable', action='store_true', help='will include questionable results')
    parser.add_argument('-s', '--spacer', nargs='+', help='fna files with spacer information')
    parser.add_argument('-r', '--repeat', nargs='+', help='fna files with repeat information')
    args = parser.parse_args()


    repeat_file = args.repeat[0]
    spacer_file = args.spacer[0]

    if (args.questionable):
        q_spacer_file = args.spacer[1]
        q_repeat_file = args.repeat[1]

    direct_files(str(repeat_file), str(spacer_file))

if __name__ == '__main__':
    main()