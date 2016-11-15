line_count = 1
N_count = 0
start = 0
end = 0
chromosome = []
region = []
with open('../data/processed/ARID3A_seq.fa') as f:
    for line in f:
        if line_count % 2 == 0:
            if 'N'*200 in line:
                N_count += 1
                temp = temp [1:-1]
                temp = temp.split(':')
                if chromosome == [] or chromosome[-1] != temp[0]:
                    chromosome.append(temp[0])
                    start, end = [int(x) for x in temp[1].split('-')]
                    region.append([])
                    region[-1].append([start,end])
                else:
                    temp_start, temp_end = [ int(x) for x in temp[1].split('-') ]
                    if temp_start < end:
                        end = temp_end
                        region[-1][-1][1]= end
                    else:
                        start = temp_start
                        end = temp_end
                        region[-1].append([temp_start, temp_end])
        else:
            temp = line
        line_count += 1
    f.close()
print(str(N_count/((line_count-1)/2)*100)+'% of sequences (with overlap) are Ns')
for i in range(len(chromosome)):
    print(chromosome[i])
    print(region[i])
with open('../data/processed/ARID3A_headless.bed') as f:
    for line in f:
        temp = line[0:-1].split('\t')
        for start, end in region[chromosome.index(temp[0])]:
            if start <= int(temp[1]) and end >= int(temp[2]):
                if temp[3] != 'U':
                    print(temp[3])
                break
    f.close()
            

