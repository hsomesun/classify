import os

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
    error = 0
    test_size = len(filelist)
    for filename in filelist:
	f = open('test/' + filename)
	real_subject = filename.split('_')[0]
	test_record = []
	for line in f:
	    words = line.split(' ')
	    for wd in words:
		w = wd.split('/')
		if len(w) == 2:
		    (word, prop) = w
		    if prop.startswith('n') and word in dictionary:
			test_record.append(word)
	prob_subject = classify(test_record)
	if real_subject != prob_subject:
	    error += 1	
	    print filename, ' ', real_subject, ' ', prob_subject
    print 'All: %s correct: %s error: %s percision: %s%%' % (test_size, test_size - error, error, 100.0 * (test_size -error) / test_size)

def classify(test_set):
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
    test_by_dir('test/')
    
    
    
