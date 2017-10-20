from newsfeed.models import UserProfile, RateArticle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class NikoloEngine(object):
    def __call__(self):
        user_mongo_ids = self.user_vectorize()
        return user_mongo_ids

    def user_vectorize(self):
        user_mongo_ids = []
        try:
            dbUsers = UserProfile.objects.all()
            for row_user in dbUsers:
                if not row_user.cfEnabled:
                    continue
                user_mongo_ids.append(row_user.id)
        except:
            pass
        return user_mongo_ids

    def train(self, user_mongo_ids):
        preferences_matrix = []
        user_vector = []
        similar_vector = []
        base = 0.25
        try:
            dbUsers = UserProfile.objects.all()
            for row_user in dbUsers:
                if not row_user.cfEnabled:
                    continue
                # print row_user.username
                worldPref = row_user.worldPref*base
                businessPref = row_user.businessPref*base
                technologyPref = row_user.technologyPref*base
                sciencePref = row_user.sciencePref*base
                healthPref = row_user.healthPref*base
                sportsPref = row_user.sportsPref*base
                politicsPref = row_user.politicsPref*base
                user_vector = [worldPref,
                               businessPref,
                               technologyPref,
                               sciencePref,
                               healthPref,
                               sportsPref,
                               politicsPref]
                # print user_vector
                preferences_matrix.append(user_vector)
            # print preferences_matrix

            cosine_similarities = cosine_similarity(preferences_matrix)
            # print cosine_similarities
            cosine_similarities_array = np.asarray(cosine_similarities)

            for i in range(0, len(cosine_similarities_array)):
                max_element = -1
                max_element_position = -1
                for z in range(0, len(cosine_similarities_array[0])):
                    if (cosine_similarities_array[i][z] > max_element) and (i != z):
                        max_element = cosine_similarities_array[i][z]
                        max_element_position = z
                similar_vector.append(user_mongo_ids[max_element_position])
            # print similar_vector
        except Exception as ex:
            print ex
            pass
        return similar_vector

    def predict(self, similar_vector, user_mongo_ids, user_index):
        user_a_mongo_id = user_mongo_ids[user_index]
        user_a_objects = RateArticle.objects.filter(userId=user_a_mongo_id)
        user_a_aricles = []
        for row in user_a_objects:
            user_a_aricles.append(row.articleId)
        # print user_a_aricles

        user_b_mongo_id = similar_vector[user_index]
        user_b_objects = RateArticle.objects.filter(userId=user_b_mongo_id, rating__gte=1)
        user_b_aricles = []
        for row in user_b_objects:
            user_b_aricles.append(row.articleId)
        # print user_b_aricles

        recommendation_articles = []
        for i in user_b_aricles:
            if i not in user_a_aricles:
                recommendation_articles.append(i)
        # print recommendation_articles
        return recommendation_articles
























