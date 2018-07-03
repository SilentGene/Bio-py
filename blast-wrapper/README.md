# blast-wrapper
Pipleline for conducting makeblastdb and blastp/blastn using one simple command.
## Usage
```
$ python3 blast_wrapper.py -h
usage: blast_wrapper.py [-h] -q query_fasta [-o output][-df database_fasta]
                        [-db database][-e max_e-value] [-ms num_sequences]
                        [-n num_cpu][-b blast+ program]
                        [--no_qseq [hide qseq column]][-f output_format*]

optional arguments:
  -h, --help            show this help message and exit
  -q query_fasta, --query query_fasta
  -o output, --output output
  -df database_fasta, --database_fasta database_fasta
                        fasta file to be used as database
  -db database, --database database
                        blast database which has already been made
  -e max_e-value, --evalue max_e-value
                        threshod e-value for blast (default=1e-5)
  -ms num_sequences, --max_target_seqs num_sequences
                        specify the max_number of target seqs for hits per
                        query (default=1)
  -n num_cpu, --num_threads num_cpu
                        specify the number of threads used by blast
                        (default=3)
  -b blast+ program, --blast_program blast+ program
                        specify the blast program (default=blastp)
  --no_qseq [hide qseq column]
                        no query sequences will be showed if this argument is
                        added
  -f output_format, --outfmt output_format
                        outfmt defined by blast+, it is dangerous to change
                        the default value
```
## Simplest
```
$ python blast_wrapper.py -q query.faa -df database.faa
```
or if you already have an established database:
```
$ python blast_warpper.py -q query.faa -db blast+_database
```
## Moderate
```
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna -e 1e-10 -n 5
```

## Control freak
```
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna -e 1e-10 -n 5 -ms 3 --no_qseq
```
*Any change to output format by -f option may lead to errors when parsing output results, although it's up to you to make any change*

## Note
- blastp would be used if no algorithm is specified by option `-b`.
- The option `-q` is required to specify the query fasta file. The option `-df` or `-db` is required to specify the target database in fasta famat or an database that has already made by makeblastdb command in blast+ software.
- If no output is specified, the result would be created in the current direcoty according to the regular `QueryFileName_blast.out`.
- if `-df` is specified, the database would be created in the same directory as the argument specified using the name `DatabaseFasta.db`. And if such a database already exsits, the script would skip the makeblastdb step.
- `--no_seqs` could used when you don't want the orignal query sequences appear in the final result. This may speed up the program in some extend.

  

