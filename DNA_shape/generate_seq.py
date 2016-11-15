import subprocess
subprocess.run(['bedtools','getfasta',
                '-fi','../../data/annotations/hg19.genome.fa',
                '-bed','../../data/annotations/train_regions.blacklistfiltered.bed',
                '-fo','../../data/processed/train_regions.blacklistfiltered.fa'])

subprocess.run(['bedtools','getfasta',
                '-fi','../../data/annotations/hg19.genome.fa',
                '-bed','../../data/annotations/test_regions.blacklistfiltered.bed',
                '-fo','../../data/processed/test_regions.blacklistfiltered.fa'])
