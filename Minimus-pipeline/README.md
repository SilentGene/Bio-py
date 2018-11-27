# Minimus2 Pipeline
Using Minimus2 (a component of `Amos`) to merge two sets of genome contigs.

This pipeline is described in the Amos official website:
http://amos.sourceforge.net/wiki/index.php/Minimus2
All the parameters are as default.

## Usage
```bash
$ python Minimus2_pipleline.py -s1 S1.fas -s2 S2.fas -o output_prefix
```
##Sample

```bash
$ python Minimus2_pipeline.py -s1 seq1.fas -s2 seq2.fas -o Minimus2_out/seq1-2
```

## Options

- `-s1`: genome set 1 (fasta format; used as reference)
- `-s2`: genome set 2 (fasta format)
- `-o`: prefix of output (directory is allowed to involve and will be create if not exists)

## Require
- Using **Python3**
- Amos was installed, including which `toAmos` and `minimus2` was already in the $PATH
- No 3rd party python modules required

## Output

The following two files are the most important output:

 - prefix.fasta : merged contig sequences
 - prefix.singletons.seq : singleton sequences

 Consider to use `cat` command to combine these two files, in order to do downstream analysis.

# Chinese Usage 中文使用说明
Minimus2是Amos套件中的一个程序，主要用于进行两个基因组文件的合并与再拼接。

## 使用
```bash
$ python Minimus2_pipleline.py -s1 S1.fas -s2 S2.fas -o output_prefix
```
##示例

```bash
$ python Minimus2_pipeline.py -s1 seq1.fas -s2 seq2.fas -o Minimus2_out/seq1-2
```

## 选项

- `-s1`: 基因组1（fasta格式，将会用做参考序列）
- `-s2`: 基因组2（fasta格式）
- `-o`: 输出文件的前缀（可以包含前置路径名，路径若不存在则会被新建）
## 要求
- 使用**Python3**
- 无需第三方python模块
- Amos已安装，并至少将`toAmos` 和 `minimus2` 两个组件放进$PATH中以便调用

## 输出

下面两个文件是所有输出文件中最重要的：

- prefix.fasta : 合并的contigs文件
- prefix.singletons.seq : 未合并的contigs

可以考虑使用 `cat` 命令将这两个文件合并进行下游分析。