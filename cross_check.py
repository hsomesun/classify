import train  
import test
import os

if __name__ == '__main__':
    frompath = 'train/'
    savepath = 'tmp'
    topath = 'tmp/'
    os.system('if [ ! -d %s ]; then mkdir %s; fi' % (savepath, savepath))
    filelist = os.listdir(frompath)
    group_ix = 0
    group_num = 10
    fp = open('tmp/stat.dat', 'w')
    total_rate = {}
    for group_ix in xrange(group_num):
	print 'Group %s:', group_ix
	train.init()
    	train.get_stop_words('stop_words_ch.txt')
	test_filelist = []
        train_filelist = []
	train_filenum = 0
	test_filenum = 0

	for file_ix in xrange(len(filelist)):
	    if file_ix % group_num == group_ix: 
		test_filelist.append(filelist[file_ix])
		test_filenum += 1
	    else:
		train_filelist.append(filelist[file_ix])
		train_filenum += 1
	
	train.count(frompath, train_filenum, train_filelist)
	train.CHI(train_filenum)
	result_file = 'tmp%s.dat' % group_ix
	
	train.create_train(topath, train_filenum, train_filelist, result_file)

	test.init()
	test.read_train('tmp/', result_file)

	rate_dict = test.test_by_filelist('train/', test_filelist)

	fp.write('Group %s:\n' % group_ix)
	
	group_classify = 0
	group_fact = 0
	group_error = 0
	group_total = 0
	for subject in rate_dict.keys():
	    if not total_rate.has_key(subject):
		total_rate[subject] = {'classify' : 0, 'fact' : 0, 'error' : 0, 'total' : 0}
	    
	    group_classify += rate_dict[subject]['classify'] 
	    group_fact += rate_dict[subject]['fact']
	    group_error += rate_dict[subject]['error']
	    group_total += rate_dict[subject]['total']

	    total_rate[subject]['classify'] += rate_dict[subject]['classify'] 
	    total_rate[subject]['fact'] += rate_dict[subject]['fact']
	    total_rate[subject]['error'] += rate_dict[subject]['error']
	    total_rate[subject]['total'] += rate_dict[subject]['total']

	    fp.write('subject(%s) fact: %s classify: %s recall: %s%% correct: %s total: %s accurate: %s%%\n' \
	    	    % (subject, \
	    	       rate_dict[subject]['fact'], \
	    	       rate_dict[subject]['classify'], \
	    	       100.0 * rate_dict[subject]['fact'] / rate_dict[subject]['classify'], \
	    	       rate_dict[subject]['fact'], \
	    	       rate_dict[subject]['total'], \
	    	       100.0 * (rate_dict[subject]['fact']) / rate_dict[subject]['total']))
	    fp.write('group all: %s correct: %s error: %s rate: %s%%\n' \
			% (group_total, group_fact, group_error, \
			100.0 * (group_total - group_error) / group_total))

	fp.write('\n')

    fp.write('All: \n')

    all_fact = 0
    all_error = 0
    all_total = 0
    for subject in total_rate.keys():
	all_fact += total_rate[subject]['fact']
	all_error += total_rate[subject]['error']
	all_total += total_rate[subject]['total']
	fp.write('subject(%s) fact: %s classify: %s recall: %s%% correct: %s total: %s accurate: %s%%\n' \
	    	    % (subject, \
	    	       total_rate[subject]['fact'], \
	    	       total_rate[subject]['classify'], \
	    	       100.0 * total_rate[subject]['fact'] / total_rate[subject]['classify'], \
	    	       total_rate[subject]['fact'], \
	    	       total_rate[subject]['total'], \
	    	       100.0 * (total_rate[subject]['fact']) / total_rate[subject]['total']))
    fp.write('all: %s correct: %s error: %s rate: %s%%\n' \
		% (all_total, all_fact, all_error, \
		100.0 * (all_total - all_error) / all_total))
    fp.write('\n')

    fp.close()

        
	

    
    
   

    
    



