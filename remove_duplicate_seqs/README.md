# Remove duplicate sequences
Remove duplicate sequences from one or several multifasta files.
According to the **id** in the header or the **sequence** itself.

## Require
- Biopython module
- Using **Python3**
- Works both on Windows and unix-like systems
## Usage

Filter according to the sequence id:

```
$python3 remove_duplicate_seqs.py --id input.fa [input2.fa ...] > output.fa
```
or filter according to the sequence itself:
```
$python3 remove_duplicate_seqs.py --seq input.fa [input2.fa ...] > output.fa
```

## Note
- `--id` or `--seq` are necessary and should be right put following the name of the script

# Chinese Usage 中文使用说明
本脚本能够在一个或多个fasta格式的文本文件中清除重复的序列
可以根据序列的id或者根据序列本身来去除这种冗余

## 要求
- 使用**Python3**
- 需要调用Biopython
- 在Windows和类unix系统中均可运行
##使用
通过序列的id号来过滤:

```
$python3 remove_duplicate_seqs.py --id input.fa [input2.fa ...] > output.fa
```
通过序列本身来过滤:
```
$python3 remove_duplicate_seqs.py --seq input.fa [input2.fa ...] > output.fa
```

## 注意
- 参数'--id' 或者 '--seq`必须指定其一，并且它只能被置于第一个参数的位置（脚本名之后）