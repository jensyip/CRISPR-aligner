from string import ascii_uppercase as au
import random
from utils import *

key_components = list(au)

def grab_key():
    primary_key = random.choice(key_components)
    secondary_key = random.choice(key_components)
    key = primary_key + secondary_key
    return key

def assign_key(sorted_arrays):
    key_map = {}
    keys_check = []

    for array_list in sorted_arrays:
        arr_list = sorted_arrays[array_list]
        for crispr_array in arr_list:
            #CRISPR Array Object
            for i in range(len(crispr_array.get_spacer_list())):
                spacer_sequence_object = crispr_array.get_spacer_list()[i].get_sequence()
                spacer_sequence = spacer_sequence_object.tostring()
                added = False
                # if spacer is already in key_map then go to next spacer
                if (spacer_sequence in key_map):
                    continue;
                # check all keys in key_map for mutations
                for key in key_map:
                    difference = levenshtein(spacer_sequence, key)
                    if (difference < 3):
                        key_map[spacer_sequence] = key_map[key].lower()
                        added = True
                        break;
                if not added:
                    key = grab_key()
                    while key in keys_check:
                        key = grab_key()
                key_map[spacer_sequence] = key
    print(key_map)
    return key_map

def reconstruction (key_map, sorted_array):
    string_map = {}
    for array_list in sorted_array:
        arr_list = sorted_array[array_list]
        for crispr_array in arr_list:
            string = ""
            for i in range(len(crispr_array.get_spacer_list())):
                spacer_sequence = crispr_array.get_spacer_list()[i].get_sequence().tostring()
                string += key_map[spacer_sequence]
            string_map[crispr_array] = string

    print(string_map)
    return string_map

#Test if the spacers are sorted
def is_sorted(sorted_array):
    for array_list in sorted_array:
        arr_list = sorted_array[array_list]
        for crispr_array in arr_list:
            for i in range(len(crispr_array.get_spacer_list())):
                spacer_sequence_object = crispr_array.get_spacer_list()[i]
                print(spacer_sequence_object.get_order_number())