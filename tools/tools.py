from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def remove_redundant_strings(cluster):
    '''
    Takes a list of strings and removes those which are entirely contained within other strings
    '''
    not_duplicated = []
    
    for i in range(len(cluster)):
        duplicate = False
        for j in range(len(cluster)):
            if i == j:
                pass
            elif cluster[i]+'s' == cluster[j]:
                # Check for failures of lemmatisation
                # for instance, dataset, datasets
                pass
            elif cluster[i] == cluster[j]+'s':
                # Check for failures of lemmatisation
                duplicate = True
            elif cluster[i] in cluster[j]:
                duplicate = True
        if not duplicate:
            not_duplicated.append(cluster[i])
    
    return not_duplicated
    
    
def get_top_n_bursts(burstiness, n):
    return list(burstiness.nlargest(n, "max").index)

def s_curve(x, a, b, c, d):
    return a / (1. + np.exp(-c * (x - d))) + b
	
def all_subterms(term):
    subterms = term.split(' ')
    vectorizer = CountVectorizer(strip_accents='ascii', ngram_range=(1,len(subterms)-1))
    vectorizer.fit_transform([term])
    return list(vectorizer.vocabulary_)


	
	
def normalise_time_series(time_series):
    # Normalise prevalance such that it is capped at 1 and has a minimum at 0.
    return (time_series-time_series.min())/(time_series.max()-(time_series.min()))