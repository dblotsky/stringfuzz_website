import sys
import os
import yaml
import random

from stringfuzz.constants import SMT_20_STRING, SMT_25_STRING
from stringfuzz.generators import concats, overlaps, lengths, regex, equality
from stringfuzz.generator import generate_file
from stringfuzz.smt import smt_string_logic, smt_get_model

GENERATORS = {
    'concats':  concats,
    'overlaps': overlaps,
    'lengths':  lengths,
    'regex':    regex,
    'equality': equality,
}

RANDOM_SEED = 0

def parse_config(config_path):
    config = []

    # read in config file
    with open(config_path, 'r') as config_file:
        return yaml.load(config_file.read())

    return config

def str2value(v):
    try:
        return int(v)
    except ValueError as e:
        pass
    try:
        return float(v)
    except ValueError as e:
        pass
    return v

def format_value(value, x):
    if isinstance(value, str):
        return str2value(value.format(x=x))
    return value

def format_args(args, x):
    return {key: format_value(value, x) for key, value in args.items()}

def main():

    # seed RNG
    random.seed(RANDOM_SEED)

    # get args
    root = sys.argv[1]
    config_file_path = sys.argv[2]

    if len(sys.argv) == 4:
        recursion_depth = int(sys.argv[3])
        sys.setrecursionlimit(recursion_depth)

    # parse config
    config = parse_config(config_file_path)
    if config is None:
        print('ERROR: failed to parse config from {!r}'.format(config_file_path), file=sys.stderr)
        exit(1)

    # generate each suite
    for suite in config:
        suite_dir_path = os.path.join(root, suite['name'])
        print(suite_dir_path)

        # make a directory for the suite
        try:
            os.makedirs(suite_dir_path)
        except OSError as e:
            pass

        # generate all the problems
        x = suite['start']
        num_levels = int(suite['count'])
        for i in range(num_levels):

            # format args
            args = format_args(suite['args'], x)

            # get generator
            generator_name = suite['generator']
            generator = GENERATORS[generator_name]

            # get number of times to repeat each level
            num_problems_at_level = int(suite['count_each'])

            # generate as many problems at each level as necessary
            for y in range(num_problems_at_level):

                # get file paths
                file_name = '{name}-{x:0>5}-{y}'.format(name=suite['name'], x=x, y=y)

                smt25_file_path = os.path.join(suite_dir_path, file_name) + '.smt25'
                smt20_file_path = os.path.join(suite_dir_path, file_name) + '.smt20'

                # generate problem
                ast = generator(**args)
                ast = [smt_string_logic()] + ast

                # write out the files
                generate_file(ast, SMT_25_STRING, smt25_file_path)
                generate_file(ast, SMT_20_STRING, smt20_file_path)

            # increment arg
            x += int(suite['increment'])

if __name__ == '__main__':
    main()
