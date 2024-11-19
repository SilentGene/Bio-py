# BLAST Matrix

This script calculates pair-wise sequence identities for all sequences in a multifasta format file.
A matrix table will be generated after the calculation, and a clustered heatmap will be drawn if required.

## Require

- BLAST+ installed in $PATH
- Biopython (with pandas > 0.21)
- seaborn & scipy (for drawing clustered heatmap) 

## Usage

```bash
  $ python blast_identity_matrix.py -i input_seqs.fasta [-o output_matrix.tsv] [--thread 4] [--program blastp] [--heatmap output_heatmap.pdf] [--clean]
```

## Options

- `-i`: Input file in multi-sequence FASTA format
- `-o`: Output matrix table in tab-delimited format [default: (input file name) + '_ident.tsv']
- `-t`: Threads that would be used for makeblastdb and blast [default: 2]
- `-p`: blast program that would be used (blastp or blastn) [default: blastp]
- `--heatmap`: Draw clustered heatmap.
- `--clean`: Clean temporary files. [default: False]



# Chinese Usage 中文使用说明

此脚本会进行两两blast比较并计算一致性（identity）。输入一个含有多条fasta序列的文件，生成一个一致性数值矩阵。

## 要求

- BLAST+ 安装在 `$PATH`
- Python3.x
- Biopython (包含pandas > 0.21)
- seaborn & scipy (如果绘制聚类热图需要安装) 

## 使用命令

```bash
  $ python blast_identity_matrix.py -i input_seqs.fasta [-o output_matrix.tsv] [--thread 4] [--program blastp] [--heatmap] [--clean]] 
```

## 可选项

- `-i`: 输入文件。含有多条fasta序列的文件。
- `-o`: 输出文件。tab分割的数值矩阵。[默认文件名: (输入文件名) + '_ident.tsv']
- `-t`: makeblastdb和blast过程会调用的线程数。 [默认: 2]
- `-p`: blast程序 (可选blastp或blastn) [默认: blastp]
- `--heatmap`: 绘制聚簇热图.
- `--clean`: 清除中间文件 [默认: False]
