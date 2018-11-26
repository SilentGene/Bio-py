#!/usr/bin/python3

"""
This pipline is described in the Amos official website:
http://amos.sourceforge.net/wiki/index.php/Minimus2
All the parameters are as default

Usage:
$ python3 Minimus2_pipleline.py -s1 S1.fas -s2 S2.fas -o output_prefix

Sample:
$ python Minimus2_pipeline.py -s1 seq1.fas -s2 seq2.fas -o Minimus2_out/seq1-2

"""
import os
import argparse

__author__ = "Heyu Lin"
__contact__ = "heyu.lin(AT)student.unimelb.edu.au"

parser = argparse.ArgumentParser()
parser.add_argument('-s1', metavar='seq_1', dest='s1',
                    type=str, required=True)
parser.add_argument('-s2', metavar='seq_2', dest='s2',
                    type=str, required=True)
parser.add_argument('-o', metavar='output', dest='o',
                    type=str, required=True)
args = parser.parse_args()


def create_dir(directory):
    dirnm = os.path.dirname(directory)
    if not os.path.exists(dirnm):
        os.makedirs(dirnm)


def seq_num(fasta_file):
    num = len([1 for line in open(fasta_file) if line.startswith(">")])
    return num


def cat_files(file_list, outfile):
    with open(outfile, 'w') as fo:
        for fname in file_list:
            with open(fname) as infile:
                for line in infile:
                    fo.write(line)


def run_toAmos(in_fas, out_afg):
    cmd_para = [
                'toAmos',
                '-s', in_fas,
                "-o", out_afg
                ]
    cmd = ' '.join(cmd_para)
    try:
        print("\n", 'RUN toAmos'.center(50, '*'))
        print(cmd, "\n")
        os.system(cmd)
    except Exception as e:
        raise e


def run_minimus2(in_afg, refcount):
    cmd_para = [
                'minimus2',
                in_afg,
                '-D', 'REFCOUNT=' + str(refcount)
                ]
    cmd = ' '.join(cmd_para)
    try:
        print("\n", 'RUN Minimus2'.center(50, '*'))
        print(cmd, "\n")
        os.system(cmd)
    except Exception as e:
        raise e


def main():
    create_dir(args.o)
    seq_1_num = seq_num(args.s1)
    cat_fas = args.o + '.cat.seq'
    cat_files([args.s1, args.s2], cat_fas)
    run_toAmos(cat_fas, args.o + '.cat.afg')
    run_minimus2(args.o + '.cat', seq_1_num)


if __name__ == '__main__':
    main()
