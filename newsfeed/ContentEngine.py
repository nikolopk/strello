# -*- coding: utf-8 -*-
""" Content based filtering module """
import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class ContentEngine(object):
    """ Content based filtering class """

    def __call__(self, data_source):
        dataset = ContentEngine.train(data_source)
        return dataset

    @staticmethod
    def train(data_source):
        """ Load dataset """
        dataset = []
        dataset = pd.read_csv(data_source,
                              delimiter=';',
                              quoting=csv.QUOTE_NONE,
                              encoding='utf-8',
                              quotechar='"',
                              escapechar='\\',
                              error_bad_lines=False)
        return dataset

    @staticmethod
    def _train(dataset):
        """ Training data method """
        tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
        tfidf_matrix = tf.fit_transform(dataset['title'].values.astype('U'))
        # tfidf_matrix = tf.fit_transform(ds['title'])
        cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

        rec_table = []
        for idx, row in dataset.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-6:-1]
            similar_items = [(cosine_similarities[idx][i], dataset['id'][i])
                             for i in similar_indices]
            flattened = sum(similar_items[1:], ())
            rec_table.append(flattened)

        return rec_table

    @staticmethod
    def predict(item_id, rec_table):
        """ Gives the article predicts """
        try:
            table_to_return = []
            prev_zero = False

            for element in rec_table[item_id]:
                element = float(element)
                if (element % 1 == 0) and (element != 0) and (not prev_zero):
                    table_to_return.append(element)
                if element == 0.0:
                    prev_zero = True
                else:
                    prev_zero = False

        except Exception as ex:
            print ex
            table_to_return = []
            pass

        return table_to_return
