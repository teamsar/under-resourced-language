import nltk
import pickle
from nltk import bigrams
from nltk.probability import *
from NewsHandler import NewsHandler
from EDBNormiliser import EDBNormaliser
from TokenHandler import TokenHandler
from KBBIOfflineHandler import KBBIOfflineHandler

if __name__ == '__main__':
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

    cfd_pickled = pickle.dumps(nltk.ConditionalFreqDist(lm))
    lidstone_estimator = lambda fd: LidstoneProbDist(fd, 0.01, fd.B() + 1)
    cpd = ConditionalProbDist(pickle.loads(cfd_pickled), lidstone_estimator)


    kms = KBBIOfflineHandler(configs['dbkbbi_cleaned_offline']) \
        .get_all_datakata()

    tokens = ('dan', 'javatan')
    normalised_token = EDBNormaliser(tokens, kms, cpd).normalise_token()
    print(normalised_token)
