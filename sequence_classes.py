import datetime

class Sample:
    def __init__(self, repeat_dictionary, spacer_dictionary, sample_id):
        self.repeat_dictionary = repeat_dictionary
        self.spacer_dictionary = spacer_dictionary
        self.sample_id = sample_id
        self.log = self.log('create')
        self.mapping_dictionary = self.mapping_dictionary()

    def log(self, command):
        now = datetime.datetime.now()
        if command == 'create':
            return ["Created sample %s at %s" %(self.sample_id, now)]
        else:
            self.log.append("v")

    def mapping_dictionary(self):
        # Dictionary of Crispr Arrays key=repeatSequence_ArrayNum value=CRISPR Array Object
        #Create empty mapping for each repeat stylized sequence_arrayNum
        mapping_dictionary = dict.fromkeys(self.repeat_dictionary.keys())
        #print(mapping_dictionary)
        #If the repeat values of the spacer are the same with
        for spacer in self.spacer_dictionary:
            #Value is the spacer object
            value = self.spacer_dictionary[spacer]

            #Testing to check why the number spacers found and required differ
            #if (value.get_corresponding_repeat() == "GTTTTCCCCGCGCGAGCGGGGATGTTCC" and value.get_order_number() == 8):
            #    print("Printing corresponding information: %d and arraynum: %d" %(value.get_order_number(), value.get_array_number()))
            corr_repeat = value.get_corresponding_repeat()
            array_number = str(value.get_array_number())
            repeat =  corr_repeat + "_" + array_number
            #print("Official repeat")
            #print(repeat)

            if (repeat in mapping_dictionary):
                #print(repeat)
                if (mapping_dictionary[repeat] == None):
                    initialize_list = [value]
                    arr = CRISPR_Array(self.sample_id, corr_repeat, array_number, initialize_list)
                    mapping_dictionary[repeat] = arr
                else:
                    mapping_dictionary[repeat].add_spacer(value)

        #print(mapping_dictionary)
        #y = mapping_dictionary["GTTTTCCCCGCGCGAGCGGGGATGTTCC_2"].get_spacer_list()
        #print(y)
        #for spacer in y:
        #    if (spacer.get_corresponding_repeat() == "GTTTTCCCCGCGCGAGCGGGGATGTTCC"):
        #        print(spacer.get_order_number())
        #print(mapping_dictionary["GTTTTCCCCGCGCGAGCGGGGATGTTCC_2"].num_spacers())

        for map in mapping_dictionary:
            value_1 = mapping_dictionary[map]
            value_2 = self.repeat_dictionary[map]
            number_spacers = value_2.get_number_of_spacers()
            number_found_spacers = value_1.num_spacers()
            if (number_spacers != number_found_spacers):
                #print(number_spacers)
                #print(number_found_spacers)
                print("For repeat %s, all of spacers not found.\n" %(map))
        return mapping_dictionary

    def get_mapping(self):
        return self.mapping_dictionary

    def get_repeat_dict(self):
        return self.repeat_dictionary

    def get_spacer_dict(self):
        return self.spacer_dictionary


class CRISPR_Array:
    def __init__(self, sample, repeat_sequence, array_num, spacer_list):
        self.sample = sample
        self.repeat_sequence = repeat_sequence
        self.array_num = array_num
        self.spacer_list = spacer_list

    def get_sample(self):
        return self.sample
    def get_repeat_sequence(self):
        return self.repeat_sequence
    def get_array_num(self):
        return self.array_num
    def get_spacer_list(self):
        self.spacer_list = sort_spacers(self.spacer_list)
        return self.spacer_list
    def add_spacer(self, spacer):
        self.spacer_list.append(spacer)
    def num_spacers(self):
        return len(self.spacer_list)

def sort_spacers(spacer_list):
    sorted_spacers_list = [0] * len(spacer_list)
    for spacer in spacer_list:
        order_number = spacer.get_order_number()
        sorted_spacers_list[order_number - 1] = spacer
    return sorted_spacers_list

class Sequence:
    def __init__(self, sequence, scaffold, location, sequence_type, array_number, questionable=False):
        self.sequence_type = sequence_type
        self.sequence = sequence
        self.location = location
        self.questionable = questionable
        self.scaffold = scaffold
        self.array_number = array_number
    def get_sequence_type(self):
        return self.sequence_type
    def get_sequence(self):
        return self.sequence
    def get_location(self):
        return self.location
    def get_array_number(self):
        return self.array_number

class Repeat(Sequence):
    def __init__(self, sequence, scaffold, location, array_number, number_of_spacers, sequence_type="repeat", questionable=False):
        super(Repeat, self).__init__(sequence, scaffold, location, sequence_type, array_number, questionable)
        self.number_of_spacers = number_of_spacers

    def get_number_of_spacers(self):
        return self.number_of_spacers


class Spacer(Sequence):
    def __init__(self, sequence, scaffold, location, array_number, order_number, corresponding_repeat, sequence_type="spacer", questionable=False):
        super(Spacer, self).__init__(sequence, scaffold, location, sequence_type, array_number, questionable)
        self.corresponding_repeat = corresponding_repeat
        self.order_number = order_number
        self.array_number = array_number

        #Test to check if correct number of spacers are going through
        #if (corresponding_repeat == "GTTTTCCCCGCGCGAGCGGGGATGTTCC"):
        #    print("Printing corresponding information: %d and arraynum: %d" %(order_number, array_number))

    def get_corresponding_repeat(self):
        return self.corresponding_repeat

    def get_order_number(self):
        return self.order_number




