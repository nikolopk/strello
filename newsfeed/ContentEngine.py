import pandas as pd
import time
# from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import csv


def info(msg):
    print (msg)


class ContentEngine(object):
    SIMKEY = 'p:smlr:%s'

    def __call__(self, data_source):
        self.train(data_source)

    def train(self, data_source):
        # start = time.time()
        ds = pd.read_table(data_source,
                           delimiter=';',
                           quoting=csv.QUOTE_NONE,
                           encoding='utf-8',
                           quotechar='"',
                           escapechar='\\'
                           )
        print 'ds size: ' + str(len(ds))
        # info("Training data ingested in %s seconds." % (time.time() - start))

        # start = time.time()
        new_docs = ['He watches basketball and baseball', 'Julie likes to play basketball', 'Jane loves to play baseball']
        self._train(ds)
        # info("Engine trained in %s seconds." % (time.time() - start))

    def _train(self, ds):
        tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['description'])
        info(tf.vocabulary_)
        info(str(tfidf_matrix))

        cosine_similarities = linear_kernel(tfidf_matrix)
        info(str(cosine_similarities))

        items, nRows = 6, ;
        # Matrix = [[0 for x in range(w)] for y in range(h)]
        for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-6:-1]
            # print str(similar_indices)
            similar_items = [(cosine_similarities[idx][i], ds['id'][i])
                             for i in similar_indices]
            print str(row['id']) + '\n'
            print str(similar_items)

            flattened = sum(similar_items[1:], ())
            # rec_table[idx+1] = flattened
            # print str(flattened)
            print '\n \n'
            # _r.zadd(ContentEngine.SIMKEY % row['id'], *flattened)
