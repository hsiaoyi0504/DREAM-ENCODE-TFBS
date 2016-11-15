import os
def merge_feature(TF_name,cell_line_name,data_type):
    output_file_name = '../../data/features/merge_feature_' + data_type + '_' + TF_name + '_' + cell_line_name + '.csv'
    order_file_name = '../../data/annotations/'  + data_type  + '_regions.blacklistfiltered.bed'
    input_files_dir = '../../data/features/'
    input_files_list = [
        cell_line_name + '.dnase.' + data_type + '.feature', # dnase features
        data_type + '_shape_feature_HelT.bed', # shape features
        data_type + '_shape_feature_MGW.bed',
        data_type + '_shape_feature_ProT.bed',
        data_type + '_shape_feature_Roll.bed',
        data_type + '_kmer_frequency.bed', # kmer features
        'gccontent.' + data_type + '.feature', #gccontnet features
        cell_line_name + '.gene.' + data_type + '.feature' #expression features
    ]
    input_files_list = [input_files_dir + i for i in input_files_list]
    if data_type == 'train':
        input_files_list.append('../../data/ChIPseq/label/' + TF_name + '.train.labels.tsv')
    elif data_type == 'test':
        pass
    else:
        raise ValueError('Error data_type, data_type should be "train" or "test"')
    order = {}
    with open(order_file_name) as f:
        for line in f:
            temp = line.rstrip(os.linesep)
            temp = temp.split('\t')
            temp = ','.join(temp)
            order[temp] = []
        f.close()
    for file in input_files_list: 
        with open(file) as f:
            if file.split('.')[-1] == 'tsv':
                line = f.readline()
                temp = line.rstrip(os.linesep)
                temp = temp.split('\t')
                pos = temp.index(cell_line_name)
                for line in f:
                    temp = line.rstrip(os.linesep)
                    temp = temp.split('\t')
                    order[','.join(temp[0:3])].extend(temp[pos])
            else:
                for line in f:
                    temp = line.rstrip(os.linesep)
                    temp = temp.split('\t')
                    order[','.join(temp[0:3])].extend(temp[3:])
            f.close()
    items = order.items()
    with open(output_file_name,'w') as f:
        for key, value in items:
            temp = []
            temp.append(key)
            temp.extend(value)
            f.write(','.join(temp))
            f.write(os.linesep)
        f.close()
merge_feature('ATF2','H1-hESC','train')
merge_feature('ATF2','MCF-7','train')
merge_feature('ATF2','GM12878','train')
merge_feature('ATF2','K562','test')
merge_feature('ATF2','HepG2','test')
