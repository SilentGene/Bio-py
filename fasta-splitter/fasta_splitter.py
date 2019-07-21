#!/usr/bin/python3

"""
A Python script for splitting a fasta format file into pieces by
specifying the number of divided files or the number of sequences in divided files

Inspired by Biopython wiki - https://biopython.org/wiki/Split_large_file

==Required: Biopython

==Options:
-i, --input: input fasta file
-o, --output: output directory
-partn, --partnumber: number of files will be divided into
-parts, --partseq: number of sequences will be put into every divided file

==Examples:
1. Divide a fasta file into <10> files, storing in <output_dir>
python fasta_splitter.py -i input.fasta -o output_dir -partn 10

2. Divide a fasta file into files containing <1000> sequences in <current path>
python fasta_splitter.py -i input.fasta -parts 1000
"""

import sys
import os
from math import ceil
from Bio import SeqIO
import argparse

#
__author__ = "Heyu Lin"
__contact__ = "heyu.lin(AT)student.unimelb.edu.au"


"""
Arguments
"""
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='input_file', dest='i',
                    type=str, required=True)
parser.add_argument('-o', '--output', metavar='output_dir', dest='o',
                    type=str, default='.')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-partn', '--partnumber', metavar='number_of_parts', dest='p',
                    type=int)
group.add_argument('-parts', '--partseq', metavar='number_of_seqences_in_every_part', dest='s',
                    type=int)

args = parser.parse_args()

def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = next(iterator)
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch


def total_num_calc(fasta):
    """
    Calculate total number of the given fasta file
    """
    total_num = len([1 for line in open(fasta) if line.startswith(">")])
    return total_num


def splitter(input, num, outdir):
    """
    split fasta sequences into pieces
    """
    fname = os.path.basename(input)
    fbname, fename = os.path.splitext(fname)
    record_iter = SeqIO.parse(open(input),"fasta")
    for i, batch in enumerate(batch_iterator(record_iter, num)):
        filename = "{0}.p-{1}{2}".format(fbname, i + 1, fename)
        output = os.path.join(outdir, filename)
        with open(output, "w") as handle:
            count = SeqIO.write(batch, handle, "fasta")
        print("Wrote %i records to %s" % (count, output))


def main():
    n_seq = 0 # Number of sequences in every divided files

    if args.p:
        total_num = total_num_calc(args.i)
        n_seq = ceil(total_num / args.p)
    elif args.s:
        n_seq = args.s

    splitter(args.i, n_seq, args.o)


if __name__ == '__main__':
    main()