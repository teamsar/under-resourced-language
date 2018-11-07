import nltk
import pickle
from nltk import bigrams
from nltk.probability import *
from NewsHandler import NewsHandler
from PolarityAnnotator import PolarityAnnotator
from TokenHandler import TokenHandler

if __name__ == '__main__':
    isNormalised = input('Normalised? (True/False): ')
    isNormalised = True if 'true' in isNormalised.lower() else False

    resulting_file = input('File name as an output: ')

    # Read configuration
    configs = {}
    f = open('System.conf', 'r')
    for line in f.readlines():
        cfg = line.strip().split('=')
        configs[cfg[0].strip()] = cfg[1].strip()

    # Get political news comments
    comments = NewsHandler(configs['dbnews']).get_political_news_comment()

    # Handle bigram model first to ease next computation
    f = open('political_comment_corpus.txt', 'r')
    corpus = TokenHandler().word_tokenizer(f.readline())
    lm = bigrams(corpus)

    # MLE only -> change to Lidstone smoothing
    # cfd_pickled = pickle.dumps(nltk.ConditionalFreqDist(lm))
    # cpd = ConditionalProbDist(pickle.loads(cfd_pickled), MLEProbDist)
    # cpd_pickled = pickle.dumps(cpd)

    # Lidstone smoothing
    cfd_pickled = pickle.dumps(nltk.ConditionalFreqDist(lm))
    lidstone_estimator = lambda fd: LidstoneProbDist(fd, 0.01, fd.B() + 1)
    cpd = ConditionalProbDist(pickle.loads(cfd_pickled), lidstone_estimator)

    # Annotate each comment
    before_annotated, after_annotated = PolarityAnnotator(comments, configs['dbkbbi_cleaned_offline'], cpd, normalised=isNormalised)\
        .get_annotated_comments()

    f = open(resulting_file, 'w')
    f.write(str(after_annotated))
    f.flush()
    f.close()
