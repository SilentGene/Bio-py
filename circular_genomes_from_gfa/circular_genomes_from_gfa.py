import sys
import os

"""
Extract circular genomes from a GFA file
Usage: python circular_genomes_from_gfa.py <input.gfa> [output_dir]
"""

def usage():
    print("Extract circular genomes from a GFA file")
    print("Usage: python circular_genomes_from_gfa.py <input.gfa> [output_dir]")
    print("\tOptional: output_dir - directory to write output files to (default: <input>_circular)")
    sys.exit(1)

def get_args():
    if len(sys.argv) < 2:
        usage()
    
    input_file = sys.argv[1]
    if not input_file.endswith('.gfa'):
        print("Error: Input file must be a .gfa file")
        usage()
    
    base = os.path.splitext(input_file)[0]

    output_dir = sys.argv[2] if len(sys.argv) > 2 else f"{base}_circular"
    fasta_file = os.path.join(output_dir, f'{base}_circular_all.fna')
    tsv_file = os.path.join(output_dir, f'{base}_circular_all_info.tsv')
    return input_file, output_dir, fasta_file, tsv_file

def get_seqs(gfa_file):
    segments = {}  # id -> sequence
    
    with open(gfa_file) as f:
        for line in f:
            if line.startswith('S'):  # Segment line
                parts = line.strip().split('\t')
                seg_id, sequence = parts[1], parts[2]
                segments[seg_id] = sequence  
    return segments

def find_circular_paths(gfa_file):
    circular_paths = set()
    with open(gfa_file) as f:
        for line in f:
            if line.startswith('L'):  # Link line
                parts = line.strip().split('\t')
                from_id, from_orient = parts[1], parts[2]
                to_id, to_orient = parts[3], parts[4]
                overlap = parts[5]
                if from_id == to_id and from_orient == to_orient and overlap == '0M':
                    circular_paths.add(from_id)
    # if no circular paths found, exit with warning
    if not circular_paths:
        print("Warning: No circular paths found in the GFA file")
        sys.exit(1)
    return circular_paths

def write_output(seq_dict, ids, output_dir, output_fasta, output_tsv):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    count = 1
    seq_len = {}
    for id in ids:
        sequence = seq_dict[id]
        seq_len[id] = len(sequence)
    # order by length
    sorted_ids = sorted(ids, key=lambda x: seq_len[x], reverse=True)
    with open(output_fasta, 'w') as ff, open(output_tsv, 'w') as tf:
        tf.write('#id\tSeqID\tLength(bp)\n')
        for id in sorted_ids:
            sequence = seq_dict[id]
            ff.write(f'>{id}\n{sequence}\n')
            tf.write(f'{count}\t{id}\t{seq_len[id]}\n')
            count += 1
    # write sequences to individual files
    for id in sorted_ids:
        with open(os.path.join(output_dir, f'{id}.fasta'), 'w') as f:
            f.write(f'>{id}\n{seq_dict[id]}\n')


            

def main():
    input_file, output_dir, fasta_file, tsv_file = get_args()
    
    # Parse GFA file
    segments_dict = get_seqs(input_file)
    
    # Find circular paths
    circular_edges = find_circular_paths(input_file)
    
    # Write output files
    write_output(segments_dict, circular_edges, output_dir, fasta_file, tsv_file)

if __name__ == '__main__':
    main()