#!/usr/bin/env python3

# Add Reed-Solomon ECC to the input data.
# The program reads the whole input data into memory. If the data is big, it can pose a problem.
# The percentage is calculated quite roughly for edge cases
# (bigger than 12700%, which corresponds about 127 times of the input data. Why do you even need that much?)

import argparse
import logging
import sys
from reedsolo import RSCodec

PACKET_SIZE = 256

def calculate_ecc_length(args):
    percentage = args.redundancy
    if percentage < 0:
        raise ValueError(f"Percentage is too small: {percentage}")
    total_percentage = 100.0 + percentage
    ecc_length = int(PACKET_SIZE / total_percentage * percentage)
    ecc_max_len = PACKET_SIZE - 2
    if ecc_length > ecc_max_len:
        raise ValueError(f"Percentage is too big: {percentage}")
    return ecc_length


def build_encoded_data(args, input_data):
    ecc_len = calculate_ecc_length(args)
    codec = RSCodec(ecc_len)
    encoded_data = codec.encode(input_data)
    return encoded_data


def iterate_over_lines(args, fdi, fdo):
    input_data = fdi.read()
    encoded_data = build_encoded_data(args, input_data)
    fdo.write(encoded_data)


def process_input_file(args):
    if args.infile is not None:
        infile = args.infile
    else:
        infile = sys.stdin.fileno()
    if args.outfile is not None:
        outfile = args.outfile
    else:
        outfile = sys.stdout.fileno()
    with open(infile, 'rb') as fdi:
        with open(outfile, 'wb') as fdo:
            iterate_over_lines(args, fdi, fdo)


def main(args):
    process_input_file(args)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile')
    parser.add_argument('-o', '--outfile')
    parser.add_argument('-r', '--redundancy', type=int, default=10, help="Level of redundancy (percentage)")
    parser.add_argument('-d', '--debug', default='info')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = get_args()
    debug_level = arguments.debug.upper()
    logging.basicConfig(format='%(asctime)s %(message)s', level=debug_level)
    main(arguments)
