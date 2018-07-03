#!/usr/bin/python3

"""
Required: BLAST+ installed in $PATH

Usage:

## Simplest:
$ python blast_wrapper.py -q query.faa -df database.faa
or if you already have an established database:
$ python blast_warpper.py -q query.faa -db blast+_database

## Moderate:
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna \
                          -e 1e-10 -n 5

## Control freak:
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna \
                          -e 1e-10 -n 5 -ms 3 --no_qseq

*Any change to output format by -f option may lead to errors when parsing output results.
"""

import os, sys
import argparse
from collections import defaultdict

__author__ = "Heyu Lin"
__contact__ = "heyu.lin@student.unimelb.edu.au"

parser = argparse.ArgumentParser()
parser.add_argument('-q', '--query', metavar='query_fasta', dest='q',
    type=str, required=True)
parser.add_argument('-o', '--output', metavar='output', dest='o',
    type=str)
parser.add_argument('-df', '--database_fasta', metavar='database_fasta',
    dest='df', type=str, help='fasta file to be used as database')
parser.add_argument('-db', '--database', metavar='database',
    dest='db', type=str, help='blast database which has already been made')
parser.add_argument('-e', '--evalue', metavar='max_e-value', dest='e',
    type=float, default=1e-5, help='threshod e-value for blast (default=1e-5)')
parser.add_argument('-ms', '--max_target_seqs', metavar='num_sequences',
    dest='ms', type=float, default=1,
    help='specify the max_number of target seqs for hits per query (default=1)')
parser.add_argument('-n', '--num_threads', metavar='num_cpu',
    dest='n', type=float, default=3,
    help='specify the number of threads used by blast (default=3)')
parser.add_argument('-b', '--blast_program', metavar='blast+ program',
    dest='b', type=str, default='blastp',
    help='specify the blast program (default=blastp)')
parser.add_argument('--no_qseq', metavar='hide qseq column',
    dest='nq', nargs="?", const=True, default=False,
    help='no query sequences will be showed if this argument is added')
# You're not going to like to change this default output format.
# Any change to this outfmt argument may lead to exceptions for query coverage calculation
parser.add_argument('-f', '--outfmt', metavar='output_format*', dest='f', type=str,
    default='"6 qseqid sseqid pident length mismatch gapopen qstart qend ' \
    + 'sstart send qlen slen evalue bitscore"',
    help='outfmt defined by blast+, it is dangerous to change the default value')
args=parser.parse_args()

def input_type(b):
    '''
    return blast database type (prot or nucl)
    '''
    if  b== 'blastp':
        tp = 'prot'
        return tp
    elif b == 'blastn':
        tp = 'nucl'
        return tp
    else:
        sys.exit("Error: -b argument should only be 'blastp' or 'blastn'!")

def database_exist(db):
    prot_databases = db + '.phr'
    nucl_databases = db + '.nhr'
    if os.path.exists(prot_databases) or os.path.exists(nucl_databases):
        return True

def run_mkblastdb(fi, fo, tp):
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
    cmd = ' '.join(cmd_para)
    try:
        print("\n", 'Make Blast Database'.center(50,'*'))
        print(cmd, "\n")
        os.system(cmd)
    except Exception as e:
        raise e

def run_blast(q, o,db, e, f, ms, n, b):
    '''
    q: query
    o: output
    db: database
    e: evalue
    f: outfmt
    ms: max_target_seqs
    n: num_threads
    b: blast program
    '''
    cmd_para = [
                b,
                '-query', q,
                '-out', o,
                '-db', db,
                '-evalue', str(e),
                '-outfmt', f,
                '-max_target_seqs', str(ms),
                '-num_threads', str(n)
                ]
    cmd = ' '.join(cmd_para)
    try:
        print("\n", 'BLAST Searching'.center(50,'*'))
        print(cmd, "\n")
        os.system(cmd)
    except Exception as e:
        raise e

def creat_dict(fa):
    f = open(fa, 'r')
    dict = defaultdict(str)
    name = ''
    for line in f:
        if line.startswith('>'):
            name = line[1:-1].split()[0]
            continue
        dict[name] += line.strip()
    return dict

def blast_Parser(fi, fo, header, *dict):
    '''
    fi: blast output (format as defined in this script)
    fo: final output
    dict: dict that created from query fasta file (used to extract hit sequences)
    '''
    seq_dict = {} # initialize a dict to index query sequences
    if dict:
        seq_dict = dict[0]

    with open(fi) as input, open(fo, 'w') as output:
        output.write( "\t".join(header) + "\n" )
        for line in input.readlines():
            items = line.strip().split("\t")
            qstart, qend, qlen = map(float, (items[6], items[7], items[10]))
            qcov = 100 * (qend - qstart) / qlen
            qcov = str(round(qcov, 1))
            items.append(qcov)
            if seq_dict:
                qid = items[0]
                items.append(seq_dict[qid])
            output.write( "\t".join(items) + "\n" )

def main():
    tp = input_type(args.b)

    if not args.o:
        args.o = args.q + '_blast.out'

    # Make blast database
    if args.df:
        database_file = os.path.join(os.getcwd(), args.df) + '.db'
        if not database_exist(database_file):
            print("Starting to make blast database...")
            run_mkblastdb(args.df, database_file, tp)
        args.db = database_file
        print('DB: ', args.db)

    # Run blast program
    tempt_output = 'blast_output.tmp'
    run_blast(args.q, tempt_output, args.db, args.e, args.f, args.ms, args.n, args.b)

    # creat dict from query fasta, in order to extract sequencs later
    dict = creat_dict(args.q)

    # Parse blast output
    header = [
                'qid', 'sid', 'ident%', 'aln_len', 'miss',
                'gap', 'qstart', 'qend', 'sstart','send',
                'qlen', 'slen', 'evalue', 'bitscore', 'qcov%', 'qseq'
            ]
    # if the --no_qseq option was specified, there would be no qseq column.
    if args.nq == True:
        header.remove('qseq')
        blast_Parser(tempt_output, args.o ,header)
    else:
        blast_Parser(tempt_output, args.o ,header, dict)
    # Remove temp file
    os.remove('blast_output.tmp')

if __name__ == '__main__':
    main()
