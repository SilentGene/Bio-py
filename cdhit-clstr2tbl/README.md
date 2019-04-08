# CD-HIT clstr2tbl
Given a `clstr` file from `CD-HIT` program, this program will generate a table (tab separated) that contains the header of every sequence in the 1st column and the corresponding representative in the 2nd column.

The output file is more friendly for further analysis.

## Usage
```bash
$ python3 cdhit_clstr2tbl.py input.clstr > out.tab
```
## Input Sample

```
>Cluster 0
0   14739aa, >gene1... *
1   656aa, >gene2... at 99.85%
>Cluster 1
0   66aa, >gene3... at 100.00%
1   13708aa, >gene4... *
2   13708aa, >gene5... at 100.00%
```

Output Sample

| gene1 | gene1 |
| ----- | ----- |
| gene2 | gene1 |
| gene3 | gene4 |
| gene4 | gene4 |
| gene5 | gene4 |

# Chinese Usage 中文使用说明
输入一个`CD-HIT`文件产出的`clstr`文件，此脚本可以将其转换为一个tab分隔的表格文件，第一列是每个序列的名称，第二列是每个序列对应的代表序列的名称。

经转换过的文件对下游分析更友好。

## 使用
```bash
$ python3 cdhit_clstr2tbl.py input.clstr > out.tab
```
## 输入文件示例

```
>Cluster 0
0   14739aa, >gene1... *
1   656aa, >gene2... at 99.85%
>Cluster 1
0   66aa, >gene3... at 100.00%
1   13708aa, >gene4... *
2   13708aa, >gene5... at 100.00%
```

## 输出文件示例

| gene1 | gene1 |
| ----- | ----- |
| gene2 | gene1 |
| gene3 | gene4 |
| gene4 | gene4 |
| gene5 | gene4 |
