# Circular genomes from GFA

This script is used for extracting circular DNA sequences (including genomes, plasmids, viruses, etc) from a GFA file

## Usage

```bash
$ python circular_genomes_from_gfa.py <input.gfa> [output_dir]
```

## Example

Using the "assembly_graph.gfa" file generated by flye

```bash
# Assembly
$ flye --pacbio-hifi pacbio-css.fq.gz --out-dir flye_out --threads 16 --meta --scaffold
# Get circular DNA
$ cd flye_out
$ python circular_genomes_from_gfa.py assembly_graph.gfa
```

### Result

- Output folder: assembly_graph_circular
    - assembly_graph_circular_all.fna: A fasta file containing all circular sequences
    - assembly_graph_circular_all_info.tsv: A tab-separated file containing information about the circular sequences (ID, length)
    - edge_17343.fasta: Each *.fasta file contains an individule circular sequence
    - edge_129.fasta
    - edge_*.fasta

## Chinese Usage 中文使用说明

这个脚本用于从 GFA 文件中提取环形的DNA序列（包括基因组、质粒、病毒等）

## 使用

```bash
$ python circular_genomes_from_gfa.py <input.gfa> [output_dir]
```

## 示例

使用 flye 生成的 "assembly_graph.gfa" 文件

```bash
# Assembly
$ flye --pacbio-hifi pacbio-css.fq.gz --out-dir flye_out --threads 16 --meta --scaffold
# Get circular DNA
$ cd flye_out
$ python circular_genomes_from_gfa.py assembly_graph.gfa
```

### 结果

- 输入文件夹: assembly_graph_circular
    - assembly_graph_circular_all.fna: 包含所有环形序列的fasta文件
    - assembly_graph_circular_all_info.tsv: 包含环形序列信息的tab分隔文件（ID, 长度）
    - edge_17343.fasta: 每个 *.fasta 文件包含一个环形序列
    - edge_129.fasta
    - edge_*.fasta
