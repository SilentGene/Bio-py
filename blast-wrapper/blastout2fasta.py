#!/usr/bin/python3

"""
Used to convert the output from blast_wrapper.py to fasta format

Usage:
$ python3 blastout2fasta.py blast.out > blast_out.fa
"""

import sys
import textwrap

__author__ = "Heyu Lin"
__contact__ = "heyu.lin(AT)student.unimelb.edu.au"

in_file = sys.argv[1]
with open(in_file, 'r') as fi:
    for line in fi.readlines():
        fields = line.strip().split('\t')
        if fields[0] != 'qid':
            print('>{header}'.format(header=fields[0]))
            print(textwrap.fill(fields[15], 80))
