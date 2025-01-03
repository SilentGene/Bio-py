# POCP Calculator

Calculate the percentage of conserved proteins **(POCP)** between two or
more genomes to estimate their evolutionary and phenotypic distance.

POCP value could be used as a robust genomic index for establishing the **genus boundary** for prokaryotic groups. Generally, a POCP value of 50% could be used as a genus boundary for prokaryotic lineages according to [Qin et al (2014)](https://journals.asm.org/doi/10.1128/JB.01688-14)

An elegant matrix table will be created after the calculation.

The program was written based on the paper (*Qin et al. 2014; doi: [10.1128/JB.01688-14](https://journals.asm.org/doi/10.1128/JB.01688-14)*)

## Usage

```bash
$ python POCP-matrix.py -i input_dir -o output_matrix.tab [-n 8] [--clean]
```

## Options

- `-i`: input directory contained more than 2 translated genome files (suffix: .faa)
- `-o`: output POCP matrix file
- `-n`: number of threads (optional, default: 3)
- `--clean`: blast output and databases created by this program will be removed (optional)

## Require

- BLAST+ installed in `$PATH`
- Using **Python3**
- Works both on Windows and unix-like systems
- No 3rd party python modules required

## Sample Output：

| POCP        | Genome1.faa | Genome2.faa | Genome3.faa | Genome4.faa |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| Genome1.faa | 100         | ~           | ~           | ~           |
| Genome2.faa | 77.25376031 | 100         | ~           | ~           |
| Genome3.faa | 92.18714253 | 59.14082    | 100         | ~           |
| Genome4.faa | 41.25224685 | 57.19096    | 66.48514    | 100         |

> Please ensure that the length of every sequence header is less than 50 characters. Otherwise, Blast will be unable to create the database and will produce an error.

# Chinese Usage 中文使用说明

POCP_matrix.py脚本能够计算多个基因组之间的**POCP值**（保守蛋白百分比），用来判断原核生物在**属水平**上的遗传距离。POCP值在50%以上可以被认为是一个属的边界[Qin et al (2014)](https://journals.asm.org/doi/10.1128/JB.01688-14)。

该程序基于文献：(*Qin et al. 2014; doi: [10.1128/JB.01688-14](https://journals.asm.org/doi/10.1128/JB.01688-14)*)

## 使用

```bash
$ python POCP-matrix.py -i input_dir -o output_matrix.tab [-n 8] [--clean]
```

## 选项

- `-i`: 输入文件夹，至少含有两个基因组的蛋白质文件（后缀为.faa）
- `-o`: 输出POCP表格的文件名
- `-n`: 使用cpu核心数 (可选, 默认: 3)
- `--clean`: 该程序计算过程中产生的blast数据库与结果将会被清除 (可选)
  
  ## 要求
- Blast+已安装并存在环境变量`$PATH`中
- 使用**Python3**
- 在Windows和类unix系统中均可运行
- 无需第三方python模块

## 输出示例：

| POCP        | Genome1.faa | Genome2.faa | Genome3.faa | Genome4.faa |
| ----------- | ----------- | ----------- | ----------- | ----------- |
| Genome1.faa | 100         | ~           | ~           | ~           |
| Genome2.faa | 77.25376031 | 100         | ~           | ~           |
| Genome3.faa | 92.18714253 | 59.14082    | 100         | ~           |
| Genome4.faa | 41.25224685 | 57.19096    | 66.48514    | 100         |

> 注意：faa文件中的header必须都小于50个字符，否则blast无法建库，会报错
