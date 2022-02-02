# data cleaning
import re

# lemmatisation
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer

class Clean:
    def __init__(self, ngram_length):
        self.ngram_length = ngram_length
        
        self.alphabets ="([A-Za-z])"
        self.prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        self.suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        self.starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        self.acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        self.websites = "[.](com|net|org|io|gov)"
        self.htmltags = '<[^>]+>'
        self.htmlspecial = '&#?[xX]?[a-zA-Z0-9]{2,8};'
        self.start_delimiter = 'documentstart' 
        self.sent_delimiter = 'sentenceboundary'
        self.end_delimiter = 'documentend'

        # Download the lemmatisesr
        self.wnl = WordNetLemmatizer()

        # Create a tokeniser
        count = CountVectorizer(strip_accents='ascii', min_df=1)
        self.tokeniser = count.build_analyzer()

    def normalise_acronymns(self, text):
        '''
        Remove the periods in acronyms. 
        Adapted from the method found at https://stackoverflow.com/a/40197005 
        '''

        # deal with single letters before sentence boundaries
        text = re.sub(r'\s([A-Z, a-z])\.\s', r' \1..  ', text)
        return re.sub(r'(?<!\w)([A-Z, a-z])\.', r'\1', text)

    def normalise_decimals(self, text):
        '''
        Remove the periods in decimal numbers and replace with POINT
        '''
        return re.sub(r'([0-9])\.([0-9])', r'\1POINT\2', text)

    def split_into_sentences(self, text):
        '''
        Sentence splitter adapted from https://stackoverflow.com/a/31505798
        '''
        text = text.replace("\n"," ")
        text = re.sub(self.prefixes,"\\1<prd>",text)
        text = re.sub(self.websites,"<prd>\\1",text)

        # my addition
        text = re.sub(self.htmltags, " ", text)
        text = re.sub(self.htmlspecial, " ", text)

        if "Ph.D" in text: 
            text = text.replace("Ph.D.","PhD")

        text = re.sub("\s" + self.alphabets + "[.] "," \\1",text)
        text = re.sub(self.acronyms+" "+self.starters,"\\1<stop> \\2",text)
        text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]" + self.alphabets + "[.]","\\1\\2\\3",text)
        text = re.sub(self.alphabets + "[.]" + self.alphabets + "[.]","\\1\\2",text)
        text = re.sub(" "+self.suffixes+"[.] "+self.starters," \\1 \\2",text)
        text = re.sub(" "+self.suffixes+"[.]"," \\1",text)
        text = re.sub(" " + self.alphabets + "[.]"," \\1",text)

        if "”" in text: 
            text = text.replace(".”","”.")
        if "\"" in text: 
            text = text.replace(".\"","\".")
        if "!" in text: 
            text = text.replace("!\"","\"!")
        if "?" in text: 
            text = text.replace("?\"","\"?")

        text = text.replace(".","<stop>")
        text = text.replace("?","<stop>")
        text = text.replace("!","<stop>")

        sentences = text.split("<stop>")
        sentences = [s.strip() for s in sentences]

        non_empty = []
        for s in sentences: 
            # we require that there be two alphanumeric characters in a row
            if len(re.findall("[A-Za-z0-9][A-Za-z0-9]", s)) > 0:
                non_empty.append(s)
        return non_empty

    def pad_sentences(self, sentences):
        '''
        Takes a list of sentences and returns a string in which:
            - The beginning of the abstract is indicated by DOCUMENTSTART
            - The end is indicated by DOCUMENTEND
            - Sentence boundaries are indicated by SENTENCEBOUNDARY

        The number of delimiters used is dependent on the ngram length
        '''
        sent_string = (' '+(self.sent_delimiter+' ')*(self.ngram_length-1)).join(sentences)

        return (self.start_delimiter+' ')*(self.ngram_length-1) + sent_string + (' '+self.end_delimiter)*(self.ngram_length-1)
    
    def cleaning_pipeline(self, title, abstract, pad=True):
        '''
        Takes a binary string and returns a list of cleaned sentences, stripped of punctuation and lemmatised
        '''
        
        # Check that title and abstract exist
        if type(title) is not float:
            title = self.normalise_decimals(self.normalise_acronymns(title))
        else:
            title = ''
            
        if type(abstract) is not float:
            abstract = self.normalise_decimals(self.normalise_acronymns(abstract))
        else:
            abstract = ''
        
        if pad:
            sentences = [title] + self.split_into_sentences(abstract)

            # strip out punctuation and make lowercase
            clean_sentences = []
            for s in sentences:

                # Deal with special cases
                s = re.sub(r'[-/]', ' ', s)

                # Remove all other punctuation
                s = re.sub(r'[^\w\s]','',s)

                clean_sentences.append(s.lower())

            # pad sentences with delimiters
            
            text = self.pad_sentences(clean_sentences)

        else:
            text = title + '. ' + abstract
            text = re.sub(r'[-/]', ' ', text)
            text = re.sub(r'[^\w\s]','',text)
            text = text.lower()

        # Lemmatise word by word
        lemmas = []
        for word in self.tokeniser(text):
            lemmas.append(self.wnl.lemmatize(word))

        return ' '.join(lemmas)
