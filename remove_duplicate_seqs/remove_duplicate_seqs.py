#!/usr/bin/python3

"""
Description:
Remove duplicate sequences from one or several multifasta files.
According to the id in the header or the sequence itself.

Usage:
Filter according to the sequence id:
$python3 remove_duplicate_seqs.py --id input.fa [input2.fa ...] > output.fa

or filter according to the sequence itself:
$python3 remove_duplicate_seqs.py --seq input.fa [input2.fa ...] > output.fa
"""
import sys
import textwrap
from Bio import SeqIO

__author__ = "Heyu Lin"
__contact__ = "heyu.lin@student.unimelb.edu.au"

def arg_parser(arr):
    if arr[1] != '--id' and arr[1] != '--seq':
        raise Exception('Please indicate the filter method by --id or --seq')
    if not arr[2]:
        raise Exception('Please indicate the input fasta file(s)')
    ref = arr[1]
    inputs = arr[2:]
    return ref, inputs


def seqs_parser(filter, files):
    rec_dic = {}
    for fasfile in files:
        for seq_record in SeqIO.parse(fasfile, "fasta"):
            if filter == '--id':
                rec_dic[str(seq_record.description)] = str(seq_record.seq)
            elif filter == '--seq':
                rec_dic[str(seq_record.seq)] = str(seq_record.description)
    return rec_dic


def main():
    ref, inputs = arg_parser(sys.argv)
    rec_dic = seqs_parser(ref, inputs)
    if ref == '--id':
        for key, value in rec_dic.items():
            print('>' + key)
            print(textwrap.fill(value))
    elif ref == '--seq':
        for key, value in rec_dic.items():
            print('>' + value)
            print(textwrap.fill(key))


if __name__ == '__main__':
    main()

