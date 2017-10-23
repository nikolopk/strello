#  -*- coding: utf-8 -*-
""" Module for Nikolo filtering """
import datetime
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from newsfeed.models import UserProfile, RateArticle, Article


class NikoloEngine(object):
    """ Class for Nikolo filtering """
    def __call__(self):
        """ Constructor """
        user_mongo_ids = self.user_vectorize()
        return user_mongo_ids

    def user_vectorize(self):
        """ Build users preferences vectors """
        user_mongo_ids = []
        try:
            db_users = UserProfile.objects.all()
            for row_user in db_users:
                if (not row_user.ratingsEnabled) or (not row_user.preferencesEnabled):
                    continue
                user_mongo_ids.append(row_user.id)
        except:
            pass
        return user_mongo_ids

    def train(self, user_mongo_ids):
        """ Build similar vector """
        preferences_matrix = []
        user_vector = []
        similar_vector = []
        base = 0.25
        try:
            db_users = UserProfile.objects.all()
            for row_user in db_users:
                if (not row_user.ratingsEnabled) or (not row_user.preferencesEnabled):
                    continue

                world_pref = row_user.worldPref*base
                business_pref = row_user.businessPref*base
                technology_pref = row_user.technologyPref*base
                science_pref = row_user.sciencePref*base
                health_pref = row_user.healthPref*base
                sports_pref = row_user.sportsPref*base
                politics_pref = row_user.politicsPref*base
                user_vector = [world_pref,
                               business_pref,
                               technology_pref,
                               science_pref,
                               health_pref,
                               sports_pref,
                               politics_pref]
                preferences_matrix.append(user_vector)

            cosine_similarities = cosine_similarity(preferences_matrix)
            cosine_similarities_array = np.asarray(cosine_similarities)

            for i in range(0, len(cosine_similarities_array)):
                max_element = -1
                max_element_position = -1
                for z in range(0, len(cosine_similarities_array[0])):
                    if (cosine_similarities_array[i][z] > max_element) and (i != z):
                        max_element = cosine_similarities_array[i][z]
                        max_element_position = z
                similar_vector.append(user_mongo_ids[max_element_position])
        except Exception as ex:
            print ex
            pass
        return similar_vector

    def predict(self, similar_vector, user_mongo_ids, user_index):
        """ Recommend articles for the user. Returns only the article's id. """
        user_a_mongo_id = user_mongo_ids[user_index]
        user_a_objects = RateArticle.objects.filter(userId=user_a_mongo_id)
        user_a_aricles = []
        for row in user_a_objects:
            user_a_aricles.append(row.articleId)

        user_b_mongo_id = similar_vector[user_index]
        user_b_objects = RateArticle.objects.filter(userId=user_b_mongo_id, rating__gte=1)
        user_b_aricles = []
        for row in user_b_objects:
            user_b_aricles.append(row.articleId)

        today = datetime.datetime.utcnow()
        fixed_date = datetime.datetime.strptime(str(today), '%Y-%m-%d %H:%M:%S.%f')
        fixed_date_final = fixed_date - datetime.timedelta(days=2)
        db_articles = Article.objects.filter(timestamp__gte=fixed_date_final)
        valid_articles = []
        for row in db_articles:
            valid_articles.append(row.articleId)

        recommendation_articles = []
        for i in user_b_aricles:
            if (i not in user_a_aricles) and (i in valid_articles):
                recommendation_articles.append(i)
        return recommendation_articles
