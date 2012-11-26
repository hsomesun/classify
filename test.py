import os
import sys

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
    accurate_dict = {}
    filelist = os.listdir(test_dir)
    error = 0
    test_size = len(filelist)
    for subject in subject_dict['subject'].keys(): 
	accurate_dict[subject] = {'classify' : 0, 'fact' : 0}
    for filename in filelist:
        real_subject = filename.split('_')[0]
        prob_subject = test_by_file('test/' + filename)
	accurate_dict[prob_subject]['classify'] += 1
	if prob_subject != real_subject:
	    error += 1	
            print filename, ' ', real_subject, ' ', prob_subject
	else:
	    accurate_dict[real_subject]['fact'] += 1
    classify = 0
    fact = 0
    for subject in accurate_dict.keys():
	classify += accurate_dict[subject]['classify'] 
	fact += accurate_dict[subject]['fact']
	print 'subject(%s) classify: %s fact: %s accurate: %s%%' \
		% (subject, accurate_dict[subject]['classify'], \
		   accurate_dict[subject]['fact'], \
		   100.0 * accurate_dict[subject]['fact'] / accurate_dict[subject]['classify'])
	
    print 'All: %s correct: %s error: %s recall: %s%%\n' \
	  'fact: %s classify: %s accurate: %s%%' \
		% (test_size, test_size - error, error, \
		100.0 * (test_size - error) / test_size, \
		fact, classify, fact * 100.0 / classify)

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

def bayes_classify(test_set):
    (max_prob, prob_subject) = (0, None)
    for subject in subject_dict['subject'].keys():
	prob = 1.0 * subject_dict['subject'][subject]['doc_cnt'] / subject_dict['doc_cnt']
	for word in test_set:
	    prob = prob * subject_dict['subject'][subject]['words'][word] * 1000
	if prob >= max_prob:
	    (max_prob, prob_subject) = (prob, subject)
    return prob_subject


if __name__ == '__main__':
    read_train('./', 'data.dat')
    if len(sys.argv) < 2:
        test_by_dir('test/')
    else:
	print 'The file classify to "%s"' % test_by_file(sys.argv[1])
    
    
    
