import os
import math

global stop_set
global word_dict
global sort_word_list
global TF_IDF_dict
global subject_dict
global dictionary

def init():
    global stop_set
    global word_dict
    global sort_word_list
    global TF_IDF_dict
    global subject_dict
    global dictionary

    stop_set = set()
    #{ word1 : (filelist1), .. wordn : (filelistn) }
    word_dict = {}
    sort_word_list = []
    TF_IDF_dict = {}
    subject_dict = {}
    dictionary = set()

def listdir(rootpath):
    return os.listdir(rootpath) 

def get_stop_words(stop_words_file):
    stop_file = open(stop_words_file)
    global stop_dict
    for line in stop_file:
	word = line.replace('\r', '').replace('\n', '')
	stop_set.add(word)

def count(frompath, filenum, filelist):
    print 'counting...'
    i = 0
    for filename in filelist:
	i += 1
	if i % (filenum / 100) == (filenum / 100 - 1):
	    print 'processing: %s%%' % ((i + 0.0) * 100 / filenum)
	count_file(frompath, filename)
    print 'counted!'

def count_file(frompath, filename):
    f = open(frompath + filename)
    subject = filename.split('_')[0]
    if not subject_dict.has_key(subject):
	# 'words' record every word's document count, 'count' record the subject document count
	subject_dict[subject] = {'words' : {}, 'doc_cnt' : 0}
    subject_dict[subject]['doc_cnt'] += 1

    #split every line in file into words list
    for line in f:
	words = line.split(' ')
	#for every word get word name and word property
	for wd in words:
	    w = wd.split('/')
	    if len(w) == 2:
	        (word, prop) = w
		#only record noun word and not stop word
		if word not in stop_set and prop.startswith('n'):
		    if not word_dict.has_key(word):
			word_dict[word] = set()
		    word_dict[word].add(filename)
		    #count every word for every subject
    		    if not subject_dict[subject]['words'].has_key(word):
			subject_dict[subject]['words'][word] = set()
		    subject_dict[subject]['words'][word].add(filename)
    f.close()

def create_train(topath, filenum, filelist, result_file):
    print 'creating...'
    f = open(topath + result_file, "w")
    
    title = str(len(dictionary))
    for word in dictionary:
	title += (" %s" % word)
    title += '\n'
    f.write(title)
    vocabulary = len(dictionary)

    for subject in subject_dict.keys():
        TF_IDF_sum = 0
        TF_IDF_list = []
	record = subject + " " + str(subject_dict[subject]['doc_cnt'])
	for word in dictionary:
	    nk = 0
	    if subject_dict[subject]['words'].has_key(word):
		nk += len(subject_dict[subject]['words'][word])
	    n = subject_dict[subject]['doc_cnt']
	    TF = (1.0 + nk) / (n + vocabulary)
	    IDF = math.log10((0.0 + filenum) / len(word_dict[word]))
	    TF_IDF = TF * IDF
	    TF_IDF_list.append(TF_IDF)
            TF_IDF_sum += TF_IDF

	for TF_IDF in TF_IDF_list:
	    TF_IDF_V = TF_IDF / TF_IDF_sum
	    record += ' %s' % str(TF_IDF_V)
	record += '\n'
	f.write(record)
    f.close()
    print 'created!'

def CHI(N):
    print 'CHI ing...'
    for subject in subject_dict.keys():
	#count every word for every subject CHI
	AC = subject_dict[subject]['doc_cnt']
	BD = N - AC
	chi = {}
	print 'CHI subject: %s' % subject
        for word in word_dict.keys():
	    AB = 0
	    A, B, C, D = 0, 0, 0, 0
	    if subject_dict[subject]['words'].has_key(word):
	        A = len(subject_dict[subject]['words'][word])
	    C = AC - A
	    for sub in subject_dict.keys():
		if subject_dict[sub]['words'].has_key(word):
		    AB += len(subject_dict[sub]['words'][word])
	    B = AB - A
	    D = BD - B 
	    X2 = (1.0 * N * ((A * D - B * C) ** 2)) / ((A + C) * (A + B) * (B + D) * (C + D))
	    chi[word] = X2

	subject_key = sorted(chi.iterkeys(), key=lambda (k): (chi[k],k), reverse=True)
	for key in subject_key[0: 500]:
	    dictionary.add(key)
    print 'CHI end!'

if __name__ == '__main__':
    init()
    get_stop_words('stop_words_ch.txt')
    frompath = 'train/'
    topath = './'
    result_file = 'data.dat'
    filelist = listdir(frompath)
    filenum = len(filelist)
    count(frompath, filenum, filelist)
    CHI(filenum)
    create_train(topath, filenum, filelist, result_file)
    
