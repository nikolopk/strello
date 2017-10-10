import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import csv


def info(msg):
    print (msg)


class ContentEngine(object):

    def __call__(self, data_source):
        ds = self.train(data_source)
        return ds

    def train(self, data_source):
        ds = []
        ds = pd.read_csv(data_source,
                         delimiter=';',
                         quoting=csv.QUOTE_NONE,
                         encoding='utf-8',
                         quotechar='"',
                         escapechar='\\',
                         error_bad_lines=False)
        # ds = pd.read_table(data_source,
        #                        delimiter=';',
        #                        quoting=csv.QUOTE_NONE,
        #                        encoding='utf-8',
        #                        quotechar='"',
        #                        escapechar='\\',
        #                        )
        print str(ds)
        # new_docs = ['He watches basketball and baseball', 'Julie likes to play basketball', 'Jane loves to play baseball']
        return ds

    def _train(self, ds):
        tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['title'].values.astype('U'))
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        rec_table = []
        for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-6:-1]
            similar_items = [(cosine_similarities[idx][i], ds['id'][i])
                             for i in similar_indices]
            flattened = sum(similar_items[1:], ())
            rec_table.append(flattened)

        return rec_table

    def predict(self, item_id, rec_table):
        # print str(rec_table[item_id])
        table_to_return = []
        prev_zero = False
        for element in rec_table[item_id]:

            print element
            element = float(element)
            if (element % 1 == 0) and (element != 0) and (not prev_zero):
                table_to_return.append(element)
            if element == 0:
                prev_zero = True
            else:
                prev_zero = False
        print str(table_to_return)
        return table_to_return