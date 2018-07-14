#!/usr/bin/python3

"""
Calculate the percentage of conserved proteins (POCP) between two or
more genomes to estimate their evolutionary and phenotypic distance.
An elegant matrix table will be created after the calculation.

The program was written based on (Qin et al. 2014; doi: 10.1128/JB.01688-14)

# Required:
BLAST+ installed in $PATH

# Usage:
$ python POCP-matrix.py -i input_dir -o output_matrix.tab [-n 8] [--clean]

# Options:
-i: input directory contained more than 2 translated genome files (suffix: .faa)
-o: output POCP matrix file
-n: number of threads (optional, default: 3)
--clean: blast output and databases created by this program will be removed (optional)

"""

import sys, os, re
import glob
import itertools
from math import factorial # used to compute the progress
import subprocess
import argparse

__author__ = "Heyu Lin"
__contact__ = "heyu.lin@student.unimelb.edu.au"

"""
Deal with some options
"""
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='input_directory', dest='i',
    type=str, required=True)
parser.add_argument('-o', '--output', metavar='output_filename', dest='o',
    type=str, required=True)
parser.add_argument('-n', '--num_threads', metavar='num_cpu',
    dest='n', type=int, default=3,
    help='specify the number of threads used by blast (default=3)')
parser.add_argument('--clean', metavar='clean_blast_db_output',
    dest='c', nargs="?", const=True, default=False,
    help='redundant files created by this program will be removed if this argument is added')
args=parser.parse_args()

"""
Define functions
"""

def run_mkblastdb(fi, fo):
    '''
    fi: input fasta file
    fo: output database name
    '''
    cmd_para = [
                'makeblastdb',
                '-in', fi,
                '-dbtype', 'prot',
                '-parse_seqids',
                '-out', fo
                ]
    try:
        run = subprocess.call(cmd_para, stdout=subprocess.PIPE)
    except Exception as e:
        raise e

def run_blastp(q, db, o, n):
    """
    q: query
    db: database
    o: output
    n: num_cpu
    """
    cmd_para = [
                'blastp',
                '-query', q,
                '-out', o,
                '-db', db,
                '-evalue', '1e-5',
                '-outfmt', "6 std qlen",
                '-max_target_seqs', '1',
                '-num_threads', str(n)
                ]
    try:
        run = subprocess.call(cmd_para, stdout=subprocess.PIPE)
    except Exception as e:
        raise e

def num_sequnces(fasta):
	pattern = r"^>"
	with open(fasta, "r") as f:
		data = f.read()
		iterator = re.finditer(pattern, data, re.MULTILINE)
		count = 0
		for match in iterator:
			count += 1
		return count

def comb(n, r):
	return factorial(n) // factorial(r) // factorial(n-r)

def POCP_calculator(pair, num_cpu):
	T1 = num_sequnces(pair[0])
	T2 = num_sequnces(pair[1])
	blastout_name1 = pair[0] + '--' + os.path.basename(pair[1]) + '.POCPout'
	if not os.path.exists(blastout_name1):
		run_blastp(pair[0], pair[1]+'_POCP', blastout_name1, num_cpu)
	blastout_name2 = pair[1] + '--' + os.path.basename(pair[0]) + '.POCPout'
	if not os.path.exists(blastout_name2):
		run_blastp(pair[1], pair[0]+'_POCP', blastout_name2, num_cpu)
	hit_sum = 0 # Initialize the number of hit sequences
	for outfile in [blastout_name1, blastout_name2]:
		with open(outfile, 'r') as f:
			"""
			qury_temp: used to test whether a query has only one hit region
			recd: In the case that a query has more than on alignabe region,
				only one hit that eligible should be count
			"""
			qury_temp = 'temp'
			recd = False
			for line in f.readlines():
				items = line.split()
				qury = items[0]
				iden = float(items[2])
				qcov = float(items[3]) / float(items[12])
				if qury != qury_temp and iden >= 40 and qcov >= 0.5:
					hit_sum += 1
					recd = True # This query has been counted, and should not be
								# counted again if it has another eligible regions
				elif qury == qury_temp and iden >= 40 and qcov >= 0.5:
					if recd == False: # Although the sequence has two hit region,
									# the previous regions were not eligible
						hit_sum += 1
						recd = True
				qury_temp = qury
	return hit_sum/(T1 + T2) * 100

def output_table(dict, items, out):
	with open(out, 'w') as fo:
		fo.write('POCP' + "\t" + "\t".join(items) + "\n")
		num = len(items)
		for i in range(len(items)):
			lst = []
			lst.append(os.path.basename(items[i]))
			for j in range(len(items)):
				if items[i] == items[j]:
					lst.append('100')
				else:
					lst.append(str(dict.get((items[j],items[i]), '~')))
			fo.write("\t".join(lst) + "\n")

def clean(pth):
	for file in glob.iglob(os.path.join(pth,'*_POCP.p??')):
		os.remove(file) # Clean blast databases
	for file in glob.iglob(os.path.join(pth,'*.POCPout')):
		os.remove(file) # Clean blast output files

"""
Main Program
"""
def main():
	genomes = glob.glob(os.path.join(args.i,'*.faa'))
	genomes_bn = list(map(os.path.basename, genomes))
	num_genomes = len(genomes)
	print(num_genomes, 'genomes have been read.')
	num_blastp = comb(num_genomes,2) * 2 # The number of blastp should be called
	# Make blast database for all the genomes
	for genome in genomes:
		run_mkblastdb(genome, genome+'_POCP')
	# Run blastp between every two genomes
	dict = {}
	processed = 0
	for genome_pair in itertools.combinations(genomes,2):
		genome_pair_bn = tuple(map(os.path.basename, genome_pair))
		POCP_value = POCP_calculator(genome_pair, args.n)
		dict[genome_pair_bn] = POCP_value
		processed += 2
		processed_perc = round(processed/num_blastp * 30)
		print("\r"+"["+">"*processed_perc+"]",
			"{}/{}".format(processed, num_blastp),end='') # print progress bar
		sys.stdout.flush()
	output_table(dict, genomes_bn, args.o)
	if args.c == True:
		clean(args.i)
	print("\ndone.")

if __name__ == '__main__':
    main()