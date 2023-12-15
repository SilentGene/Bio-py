#! /usr/bin/env python3

"""
This script calculates pair-wise sequence identities for all sequences in a multifasta format file.
A matrix table will be generated after the calculation, and a clustered heatmap will be drawn if required.

# Required:
- BLAST+ installed in $PATH
- Biopython (with pandas > 0.21)
- seaborn & scipy (for drawing clustered heatmap)

# Usage:
$ python blast_identity_matrix.py -i input_seqs.fasta [-o output_matrix.tsv] [--thread 4] [--program blastp] [--heatmap] [--clean]

# Options:
-i: Input file in multi-sequence FASTA format
-o: Output matrix table in tab-delimited format [default: (input file name) + '_ident.tsv']
-t: Threads that would be used for makeblastdb and blast [default: 2]
-p: blast program that would be used (blastp or blastn) [default: blastp]
--heatmap: Draw clustered heatmap. [default: False]
--clean: Clean temporary files. [default: False]
"""

import os
from Bio import SeqIO
import argparse
import random
import shutil
from itertools import permutations
import pandas as pd
import subprocess
from multiprocessing import Pool

__author__ = "Heyu Lin"
__contact__ = "heyu.lin@student.unimelb.edu.au"

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', metavar='input_fasta_file', dest='i',
                    type=str, required=True,
                    help='Input file in multi-sequence FASTA format')
parser.add_argument('-o', '--output', metavar='output_table', dest='o',
                    type=str, required=False,
                    help='Output matrix table in tab-delimited format')
parser.add_argument('-t', '--threads', metavar='threads', dest='t',
                    type=int, required=False, default=2,
                    help='Threads that would be used for makeblastdb and blast')
parser.add_argument('-p', '--program', metavar='blast_program', dest='p',
                    type=str, required=False, default='blastp',
                    help='blast program that would be used (blastp or blastn)')
parser.add_argument('--heatmap', metavar='heatmap', dest='m',
                    action='store_true', required=False,
                    help='Draw clustered heatmap. Default: False')
parser.add_argument('--clean', metavar='clean', dest='c',
                    action='store_true', required=False,
                    help='Clean temporary files. Default: False')
args = parser.parse_args()

input_faa = args.i
output_table = input_faa + '_ident.tsv' if args.o == None else args.o
tmp_folder = 'blast_matrix_tmp_' + str(random.randint(0,999999)).zfill(6)
if args.p == 'blastp':
    blast_program = 'blastp'
    data_type = 'prot'
elif args.p == 'blastn':
    blast_program = 'blastn'
    data_type = 'nucl'
else:
    raise AttributeError('Only blastp or blastn is supported!')

if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)
else:
    raise IOError(f"Sorry, the temporary folder could not be created. Please remove the {tmp_folder} folder.")


def run_mkblastdb(fi, tp):
    fo = fi + '.db'
    '''
    fi: input fasta file
    fo: output database name
    tp: prot or nucl
    '''
    cmd_para = [
                'makeblastdb',
                '-in', fi,
                "-dbtype", tp,
                "-parse_seqids",
                "-out", fo
                ]
    try:
        # print("\n", 'Make Blast Database'.center(50, '*'))
        # print(cmd, "\n")
        subprocess.check_call(cmd_para,
                              stdout=open(os.devnull, 'wb'),
                              stderr=subprocess.STDOUT,
                              )
    except subprocess.CalledProcessError as exc:
        print('cmd:', exc.cmd)
        print("Status : FAIL", exc.returncode, exc.output)


def run_blast(q, o, db, e, b):
    '''
    q: query
    o: output
    db: database
    e: evalue
    f: outfmt
    n: num_threads
    b: blast program
    '''
    cmd_para = [
                b,
                '-query', q,
                '-out', o,
                '-db', db,
                '-evalue', str(e),
                '-outfmt', '6',
                '-num_threads', '1'
                ]
    try:
        # print("\n", 'BLAST Searching'.center(50, '*'))
        # print(cmd, "\n")
        res = subprocess.check_call(cmd_para,
                                  stdout=open(os.devnull, 'wb'),
                                  stderr=subprocess.STDOUT,
                                  )
    except subprocess.CalledProcessError as exc:
        print('cmd:', exc.cmd)
        print('output:', exc.output)


def blast_Parser(fi):
    '''
    fi: blast output (format 6)
    '''
    if not os.path.getsize(fi):
        return 0

    with open(fi) as input:
        for line in input.readlines():
            items = line.strip().split("\t")
            return float(items[2])


def include_outputdir(s):
    return os.path.join(tmp_folder, s)

def draw_heatmap(df):
    import seaborn as sns
    import scipy

    # Draw clustered heatmap
    cmap = sns.clustermap(df)

    # Save plot to a PDF file
    cmap.savefig("heatmap.pdf")


if __name__ == "__main__":
    pool = Pool(args.t)

    seq_ids = []
    for seq_record in SeqIO.parse(input_faa, "fasta"):
        single_seq = include_outputdir(seq_record.id) + ".faa"
        SeqIO.write(seq_record, single_seq, "fasta")
        seq_ids.append(seq_record.id)

    # build parameters for mkblastdb
    mkblastdb_para = [(include_outputdir(i + '.faa'), data_type) for i in seq_ids]
    # run mkblastdb in parallel
    pool.starmap(run_mkblastdb, mkblastdb_para)

    blast_para = []  # build parameters for blast
    for query, targ in permutations(seq_ids, 2):
        blast_out = include_outputdir(query + '+' + targ + '_blast')
        blast_query = include_outputdir(query + '.faa')
        blast_targ = include_outputdir(targ + '.faa.db')
        blast_para.append((blast_query, blast_out, blast_targ, '1e-5', blast_program))

    data = {}
    pool.starmap(run_blast, blast_para)
    
    for query, targ in permutations(seq_ids, 2):
        blast_out = include_outputdir(query + '+' + targ + '_blast')
        ident = blast_Parser(blast_out)
        if data.get(query):
            data[query][targ] = ident
        else:
            data[query] = {}
            data[query][targ] = ident

    df = pd.DataFrame(data).sort_index().sort_index(axis=1)


    mean_ident = df.mean(skipna = True).mean()

    max_qur_tar = df.stack().idxmax()
    max_ident = df.loc[max_qur_tar]
    min_qur_tar = df.stack().idxmin()
    min_ident = df.loc[min_qur_tar]


    print('\n***** Statistics *****')
    print(f'Maximum Identity:\n{max_ident}%: {max_qur_tar[0]} -> {max_qur_tar[1]}')
    print(f'Mimimum Identity:\n{min_ident}%: {min_qur_tar[0]} -> {min_qur_tar[1]}')
    print(f'Average Identity: {mean_ident}%')

    df = df.fillna(100)  # Fill NaN values with 100
    df.to_csv(output_table, sep='\t')

    if args.c:
        shutil.rmtree(tmp_folder)

    ######## ~ draw clustered heatmap ~ ########
    if args.m:
        draw_heatmap(df)
    


