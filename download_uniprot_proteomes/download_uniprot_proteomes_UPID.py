#! /usr/bin/env python3

"""
This script is used for batch retrieval proteomes in faa.gz format according 
to a list of Proteome identifiers (UPIDs)

# Usage:
$ python3 download_uniprot_proteomes_UPID.py input_list.txt output_dir

input_list.txt sample:
UP000000272
UP000000391
UP000000442
"""

import sys
import os
import requests

__author__ = "Heyu Lin"
__contact__ = "heyu.lin@student.unimelb.edu.au"

list_file = sys.argv[1]
output_dir = sys.argv[2]


def request_proteome(upid, output_dir, num):
    base_url = 'https://www.uniprot.org/uniprot/?include=false&format=fasta&compress=yes&force=true&query=proteome:'
    request_url = base_url + upid
    try:
        r = requests.get(request_url, allow_redirects=True)
        r.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        raise SystemExit(f'HTTP error occurred: {http_err}')
    except Exception as err:
        raise SystemExit(f'Other error occurred: {err}')
    else:
        print(f'[{num}] {upid} - OK')

    # save the content with name
    open(os.path.join(output_dir, upid + '.faa.gz'), 'wb').write(r.content)


if __name__ == "__main__":
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # read input list
    with open(list_file) as f:
        upids = f.read().splitlines()
    print(str(len(upids)) + ' lines have been read. Request started...')

    # retreival
    num = 1
    for upid in upids:
        request_proteome(upid, output_dir, num)
        num += 1
