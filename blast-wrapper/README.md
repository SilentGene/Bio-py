# blast-wrapper
Pipeline for conducting **makeblastdb** and **blastp/blastn/blastx/tblastn** using one simple command.

Show blast results in a **more elegant way**. Not only table headers, but also **query coverages** and the **original query sequences** were calculated and showed in the results.

This script can also parse and filter the blast result by setting threshold of identity and coverage!

## Require
- BLAST+ installed in `$PATH`
- Using **Python3**
- Works both on Windows and unix-like systems
## Usage
```
$ python3 blast_wrapper.py -h
usage: blast_wrapper.py [-h] -q query_fasta [-o output] [-df database_fasta]
                        [-db database] [-e max_e-value] [-ms num_sequences]
                        [-n num_cpu] [-b blast+ program]
                        [-id identity_threshold] [-qc coverage_threshold]
                        [--no_qseq [hide qseq column]] [-f output_format*]

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
  -id identity_threshold, --identity identity_threshold
                        specify the threshold of identity (default=0)
  -qc coverage_threshold, --qcov coverage_threshold
                        specify the threshold of query coverage (default=0)
  --no_qseq [hide qseq column]
                        no query sequences will be showed if this argument is
                        added
  -f output_format*, --outfmt output_format*
                        outfmt defined by blast+, it is dangerous to change
                        the default value
```
## Sample Output
qid | sid | ident% | aln_len | miss | gap | qstart | qend | sstart | send | qlen | slen | evalue | bitscore | qcov% | qseq
--- | --- | ------ | ------- | ---- | --- | ------ | ---- | ------ | ---- | ---- | ---- | ------ | -------- | ----- | ----
HC_02247 | HgcA_ND132 | 34.483 | 58 | 37 | 1 | 550 | 607 | 9 | 65 | 608 | 95 | 1.42e-08 | 43.1 | 9.4 | MEAVE...
HC_00217 | HgcB_ND132 | 28.049 | 82 | 42 | 3 | 104 | 176 | 18 | 91 | 220 | 95 | 8.56e-06 | 33.5 | 32.7 | METVE...
HC_01133 | MerA_RS | 31.567 | 453 | 286 | 12 | 6 | 445 | 9 | 450 | 466 | 480 | 2.88e-55 | 182 | 94.2 | MSKVH...
HC_01413 | MerA_WE | 30.660 | 424 | 283 | 4 | 26 | 443 | 114 | 532 | 455 | 554 | 7.74e-63 | 204 | 91.6 | MDFFD...
## Simplest
```bash
$ python blast_wrapper.py -q query.faa -df database.faa
```
or if you already have an established database:
```bash
$ python blast_warpper.py -q query.faa -db database
```
## Moderate
```bash
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna -e 1e-10 -n 5
```

## Control freak
```bash
$ python blast_wrapper.py -b blastx -q query.fna -o output -df database.faa -e 1e-10 -id 30 -qc 50 -n 5 -ms 3 --no_qseq
```
*Any change to output format by -f option may lead to errors when parsing output results, although it's up to you to make any change*

## Note
- blastp would be used if no algorithm is specified by option `-b blastn`.
- The option `-q` is required to specify the query fasta file. The option `-df` or `-db` is required to specify the target database in fasta famat or an database that has already made by makeblastdb command in blast+ software.
- If no output is specified by `-o`, the result would be created in the current direcoty according to the regular `QueryFileName_blast.out`.
- If `-df` is specified, the database would be created in the same directory as the argument specified using the name `DatabaseFasta.db`. And if such a database already exsits, the script would skip the makeblastdb step.
- Using `-id` and `-qc` to set the threshold of **identity** and **query coverage**, respectively.
- `--no_seqs` could used when you don't want the orignal query sequences appear in the final result. This may speed up the program in some extend.
- 3 threads would be used by default, which could be modified by the `-n` option.
- A custom function has been developed to take the place of the original `-max_target_seqs` option, since the latter one has been found to only generate the first hit, not the best hit.

## Tips
If you happen to have a bunch of fasta files waiting for blast against a single database, try out the following bash command to make your life simpler: (eg. you are in the fasta files directory, and all the query files have a suffix `.faa`)
```bash
$ for f in *.faa; do python3 blast_wrapper.py -q $f -df data.faa; done
```

You can use the script `blastout2fasta.py` provided along with this blast wrapper to convert the output to `fasta` format.

```bash
$ python3 blastout2fasta.py blast.out > blast_out.fa
```



# Chinese Usage 中文使用说明

blast-wrapper.py脚本能够通过简单的一行命令实现**建库**和**blast搜索**两个本地blast步骤。

使用该脚本还可以帮助我们以更优雅的方式阅读blast的结果。得到的表格不仅具有清晰的表头信息，且经过计算的**覆盖度**和**原查询序列**均可以显示在结果中，便于进一步分析解读。

## 要求
- Blast+已安装并存在环境变量`$PATH`中
- 使用**Python3**
- 在Windows和类unix系统中均可运行
## 初级

大多数情况下，你只需要用如下的命令进行blastp：

```bash
$ python blast_wrapper.py -q query.faa -df database.faa
```
如果你已经有一个通过blast+的makeblastdb建立的数据库，则:
```bash
$ python blast_warpper.py -q query.faa -db database
```
## 中级
```bash
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna -e 1e-10 -n 5
```

## 高级
```bash
$ python blast_wrapper.py -b blastn -q query.fna -o output -df database.fna -e 1e-10 -id 30 -qc 50 -n 5 -ms 3 --no_qseq
```
*虽然脚本支持通过选项-f来更改输出样式，但任何样式的更改都可能会导致后续分析结果呈现的错误*

## 注意
- 默认使用blastp运行程序，可通过`-b blastn`来指定使用blastn。
- 选项 `-q`是必选项，用来指定查询序列的文件位置。选项`-df`或者 `-db` 必须指定其一，分别可以指定用来建库的fasta文件或者已经建立的数据库位置。
- 如果`-o`选项为缺省状态，则程序会在当前路径下新建文件名为 `QueryFileName_blast.out`格式的文件存放结果。
- 如果指定了`-df`选项，则程序会在指定的fasta库相同路径下新建`DatabaseFasta.db`名称格式的数据库文件，如果该数据库被程序发现已经存在，则程序会自动跳过建库步骤，直接使用存在的数据库进行搜索。
- 通过`-id`和`-qc`分别指定**一致性**和**覆盖度**的最小值以实现对结果的过滤
- 可以使用`--no_seqs`选项来取消在结果中显示查询序列的原序列，这可能会在一定程度上加快程序运行的速度。 
- 程序默认的线程数是3个，可以使用`-n`选项来更改。
- 编写了自定义的函数来代替原生`-max_target_seqs` 参数来筛选出最优的结果。因为原生参数实际只产出数据库中第一个匹配序列，而不是最优的序列。


## 输出示例

qid | sid | ident% | aln_len | miss | gap | qstart | qend | sstart | send | qlen | slen | evalue | bitscore | qcov% | qseq
--- | --- | ------ | ------- | ---- | --- | ------ | ---- | ------ | ---- | ---- | ---- | ------ | -------- | ----- | ----
HC_02247 | HgcA_ND132 | 34.483 | 58 | 37 | 1 | 550 | 607 | 9 | 65 | 608 | 95 | 1.42e-08 | 43.1 | 9.4 | MEAVE...
HC_00217 | HgcB_ND132 | 28.049 | 82 | 42 | 3 | 104 | 176 | 18 | 91 | 220 | 95 | 8.56e-06 | 33.5 | 32.7 | METVE...
HC_01133 | MerA_RS | 31.567 | 453 | 286 | 12 | 6 | 445 | 9 | 450 | 466 | 480 | 2.88e-55 | 182 | 94.2 | MSKVH...
HC_01413 | MerA_WE | 30.660 | 424 | 283 | 4 | 26 | 443 | 114 | 532 | 455 | 554 | 7.74e-63 | 204 | 91.6 | MDFFD...

## 小技巧

如果你有很多fasta文件想要对一个数据库进行比对，不妨试试下面的命令调用bash来帮助你循环调用脚本（假设当前路径在存放fasta文件的路径中，且所有的fasta文件有统一的后缀`.faa`：
```bash
$ for f in *.faa; do python3 blast_wrapper.py -q $f -df data.faa; done
```
你可以使用脚本`blastout2fasta.py`来将`blast_wrapper.py`的结果转换成对应的`fasta`格式：
```bash
$ python3 blastout2fasta.py blast.out > blast_out.fa
```