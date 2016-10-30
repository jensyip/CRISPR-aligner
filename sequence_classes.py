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
        mapping_dictionary = {}
        for repeat in self.repeat_dictionary:
            mapping_dictionary[repeat] = []
        for spacer in self.spacer_dictionary:
            value = self.spacer_dictionary[spacer]
            repeat = value.get_corresponding_repeat() + "_" + str(value.get_array_number())
            if (repeat in mapping_dictionary):
                mapping_dictionary[repeat].append(value)

        for map in mapping_dictionary:
            value_1 = mapping_dictionary[map]
            value_2 = self.repeat_dictionary[map]
            number_spacers = value_2.get_number_of_spacers()
            number_found_spacers = len(value_1)
            if (number_spacers != number_found_spacers):
                print("For repeat %s, all of spacers not found." %(map))

        return mapping_dictionary

    def get_mapping(self):
        return self.mapping_dictionary

    def get_repeat_dict(self):
        return self.repeat_dictionary

    def get_spacer_dict(self):
        return self.spacer_dictionary


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

class Repeat(Sequence):
    def __init__(self, sequence, scaffold, location, array_number, number_of_spacers, sequence_type="repeat", questionable=False):
        super(Repeat, self).__init__(sequence_type, sequence, scaffold, location, questionable)
        self.number_of_spacers = number_of_spacers

    def get_number_of_spacers(self):
        return self.number_of_spacers


class Spacer(Sequence):
    def __init__(self, sequence, scaffold, location, array_number, order_number, corresponding_repeat, sequence_type="spacer", questionable=False):
        super(Spacer, self).__init__(sequence_type, sequence, scaffold, location, questionable)
        self.corresponding_repeat = corresponding_repeat
        self.order_number = order_number
        self.array_number = array_number

    def get_corresponding_repeat(self):
        return self.corresponding_repeat

    def get_array_number(self):
        return self.array_number



