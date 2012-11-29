import os
import sys

global subject_dict
global dictionary

def init():
    global subject_dict
    global dictionary

    subject_dict = {'subject' : {}, 'doc_cnt' : 0}
    dictionary = set()


def read_train(frompath, filename):
    f = open(frompath + filename)
    flag = True
    for train_record in f:  
	if flag:
	    flag = False
	    title = train_record.split(' ')[1:]
	    for word in title:
		dictionary.add(word)
	else:
	    record = train_record.split(' ')
	    subject = record[0]
	    sub_doc_cnt = int(record[1])
	    ix = 0
	    subject_dict['doc_cnt'] += sub_doc_cnt
	    subject_dict['subject'][subject] = {'doc_cnt' : sub_doc_cnt, 'words' : {}}
	    for TF_IDF in record[2:]: 
		word = title[ix]
		subject_dict['subject'][subject]['words'][word] = float(TF_IDF)
		ix += 1
    f.close()
		
def test_by_dir(test_dir):
    filelist = os.listdir(test_dir)
    test_by_filelist('test/', filelist)

def test_by_filelist(frompath, filelist):
    rate_dict = {}
    error = 0
    test_size = len(filelist)
    for subject in subject_dict['subject'].keys(): 
	rate_dict[subject] = {'classify' : 0, 'fact' : 0, 'error' : 0, 'total' : 0}
    for filename in filelist:
        real_subject = filename.split('_')[0]
        prob_subject = test_by_file(frompath + filename)
	rate_dict[prob_subject]['classify'] += 1
	rate_dict[real_subject]['total'] += 1
	if prob_subject != real_subject:
	    rate_dict[real_subject]['error'] += 1
	    error += 1	
            print filename, ' ', real_subject, ' ', prob_subject
	else:
	    rate_dict[real_subject]['fact'] += 1
    classify = 0
    fact = 0
    for subject in rate_dict.keys():
	classify += rate_dict[subject]['classify'] 
	fact += rate_dict[subject]['fact']
	print 'subject(%s) fact: %s classify: %s recall: %s%% correct: %s total: %s accurate: %s%%' \
		% (subject, \
		   rate_dict[subject]['fact'], \
		   rate_dict[subject]['classify'], \
		   100.0 * rate_dict[subject]['fact'] / rate_dict[subject]['classify'], \
		   rate_dict[subject]['fact'], \
		   rate_dict[subject]['total'], \
		   100.0 * (rate_dict[subject]['fact']) / rate_dict[subject]['total'])
	
    print 'All: %s correct: %s error: %s rate: %s%%\n' \
		% (test_size, test_size - error, error, \
		100.0 * (test_size - error) / test_size)
    return rate_dict

def test_by_file(filename):
    f = open(filename)
    test_record = []
    for line in f:
        words = line.split(' ')
        for wd in words:
    	    w = wd.split('/')
    	    if len(w) == 2:
    	        (word, prop) = w
    	        if prop.startswith('n') and word in dictionary:
    	    	    test_record.append(word)
    f.close()
    prob_subject = bayes_classify(test_record)
    return prob_subject

def science_record(prob):
    power = 0
    while prob >= 10:
	prob = prob / 10;
	power += 1
    while prob < 1:
	prob = prob * 10 
	power -= 1
    return (prob, power)
	
    
def bayes_classify(test_set):
    (max_prob, max_power, prob_subject) = (0, None, None)
    for subject in subject_dict['subject'].keys():
	(prob, power) = science_record(1.0 * subject_dict['subject'][subject]['doc_cnt'] / subject_dict['doc_cnt'])
	for word in test_set:
	    (sprob, spower) = science_record(prob * subject_dict['subject'][subject]['words'][word])
	    (prob, power) = (sprob, power + spower)
	#print subject, prob, power
	if max_power == None or power > max_power or (prob >= max_prob and power == max_power):
	    (max_prob, max_power, prob_subject) = (prob, power, subject)
    return prob_subject


if __name__ == '__main__':
    init()
    read_train('./', 'data.dat')
    if len(sys.argv) < 2:
        test_by_dir('test/')
    else:
	print 'The file classify to "%s"' % test_by_file(sys.argv[1])
    
    
    
