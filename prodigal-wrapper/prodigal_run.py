from multiprocessing import Pool
import os

def prodigal(fasta, basename, outdir):
    cmd_para = [
                'prodigal', '-q',
                '-i', fasta,
                '-p', 'meta',
                '-a', os.path.join(outdir, basename + '.faa'),
                '-d', os.path.join(outdir, basename + '.ffn'),
                '-o', os.path.join(outdir, basename + '.gbk')
                ]
    cmd = ' '.join(cmd_para)
    try:
        print("\n" + 'ORFs prediction'.center(50, '*'))
        print(cmd + '\n')
        os.system(cmd)
    except:
        print("\nSomething wrong with prodigal annotation!")


