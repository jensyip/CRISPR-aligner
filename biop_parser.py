from Bio import SeqIO
import argparse
from sequence_classes import *
from utils import *
from key_creator import *

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
        mapping_dictionary[str(sequence.seq)+ "_" + array_num + "_" + order_num] = seq
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

    #for space in spacer_dict:
    #    spacer = spacer_dict[space]
    #    if (spacer.get_corresponding_repeat() == "GTTTTCCCCGCGCGAGCGGGGATGTTCC" and spacer.get_order_number() == 8):
    #        print (spacer)
    #        print ( spacer.get_array_number())

    x = Sample(repeat_dict, spacer_dict, name)
    print(x.mapping_dictionary)
    sorted_array = sort_sample_arrays_by_repeat(x)
    key_map = assign_key(sorted_array)
    #is_sorted(sorted_array)
    string_map = reconstruction(key_map, sorted_array)

    #attach key to each spacer

def comparison_of_spacers(x):
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

def sort_sample_arrays_by_repeat(x):
    #sorted arrays will hold all of the arrays in key=repeat value=[array, array]
    sorted_arrays = {}

    dictionary = x.mapping_dictionary
    for repeat in dictionary:
        array = dictionary[repeat]
        repeat_seq = array.get_repeat_sequence()
        added = False
        for rep in sorted_arrays:
            difference = levenshtein(repeat_seq, rep)
            if (difference < 3):
                sorted_arrays[rep].append(array)
                added = True
        if not added:
            sorted_arrays[repeat_seq] = [array]

    print(sorted_arrays)
    return sorted_arrays



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