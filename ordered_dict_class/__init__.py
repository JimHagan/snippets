import random
from collections import OrderedDict, namedtuple
from siphon.utils import csv_unicode


def get_num_lines(filename):
    num_lines = 0
    with open(filename, 'rb') as f:
        for line in f:
            num_lines += 1
    return num_lines


def write_dicts_to_csv(dict_list, output_file, fields=None, delimiter=',', verbose=True,
                       append_to_file=False):
    """ Write list of dicts to CSV output file. """
    if not dict_list:
        return
    with open(output_file, 'a' if append_to_file else 'w') as f:
        if not fields:
            fields = []
            for d in dict_list:
                fields.extend([key for key in d.keys() if key not in fields])
            writer = csv_unicode.UnicodeDictWriter(f, fields, delimiter=delimiter)
            if not append_to_file:
                writer.writeheader()
            writer.writerows(dict_list)
        else:
            writer = csv_unicode.UnicodeDictWriter(f, fields, delimiter=delimiter)
            if not append_to_file:
                writer.writeheader()
            for row in dict_list:
                d = OrderedDict([(key_field, value) for key_field, value in row.items() \
                                 if key_field in fields])
                writer.writerow(d)
        if verbose:
            print 'File %s written.' % output_file


def ordered_dicts_from_csv(read_file, delimiter=','):
    with open(read_file, 'rb') as f:
        reader = csv_unicode.UnicodeDictReader(f, delimiter=delimiter)
        header = reader.fieldnames
        data = []
        for row in reader:
            data.append(OrderedDict([(field, row.get(field)) for field in header]))
        return data


def named_tuples_from_csv(read_file, delimiter=','):
    """ Read a CSV file and return a list of named tuples. """
    with open(read_file, 'rb') as f:
        reader = csv_unicode.UnicodeDictReader(f, delimiter=delimiter)
        DataTuple = namedtuple('DataTuple', ','.join(reader.fieldnames))
        return [DataTuple(**row) for row in reader]


def shuffle_with_seed(lst, seed=None):
    """
    Shuffles a list. By providing (and holding onto) a seed, one
    can unshuffle the list later, returning the list to its
    original, unshuffled state.
    """
    # Create our own Random object so we can mess with its state without
    # affecting global random state
    r = random.Random()
    r.seed(seed)
    # .shuffle shuffles in place, this is the best way to shuffle not in place
    shuffled = sorted(lst, key=lambda item: r.random())
    return shuffled
