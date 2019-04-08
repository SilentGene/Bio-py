#!/usr/bin/python3

"""
Given a clstr file from cd-hit program, this program will generate a table that
contains the header of every sequence in the 1st column and the corresponding
representative in the 2nd column.
The output file is more friendly for further analysis.

Usage: $ python3 cdhit_clstr2tbl.py input.clstr > out.tab


The input .clstr file looks like:
>Cluster 0
0   14739aa, >gene1... *
1   656aa, >gene2... at 99.85%
>Cluster 1
0   66aa, >gene3... at 100.00%
1   13708aa, >gene4... *
2   13708aa, >gene5... at 100.00%

The output table file looks like:
gene1 gene1
gene2 gene1
gene3 gene4
gene4 gene4
gene5 gene4
"""
import re
import sys

__author__ = "Heyu Lin"
__contact__ = "heyu.lin(AT)student.unimelb.edu.au"

in_file = sys.argv[1]

match_header = re.compile(r'>(.*?)\.')

header_list = []
repre = ''

with open(in_file) as input:
    for line in input.readlines():
        if line.startswith('>'):
            for name in header_list:
                print(name + '\t' + repre)
            header_list = []
        else:
            if line.strip().endswith('*'):
                repre = match_header.findall(line)[0]
                header_list.append(repre)
            else:
                header_list.append(match_header.findall(line)[0])

# patch for the last cluster
for name in header_list:
    print(name + '\t' + repre)
