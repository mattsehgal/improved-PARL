import json
import math
import random
import numpy as np

from collections import Counter

STOP_WORDS = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"])

def make_lowercase_remove_punc(data):
    data['reviewText'] = data['reviewText'].lower()
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in data['reviewText']:
        if ele in punc:
            data['reviewText'] = data['reviewText'].replace(ele, "")
    return data

def remove_common_words(data, res):
    words_list = data['reviewText'].split()
    truncated_list = [word for word in words_list if res[word] <= 0.5 and word not in STOP_WORDS]
    data['reviewText'] = " ".join(truncated_list)
    return data


def read_file():
    print("Reading File")
    data_list = []
    with open('./Digital_Music_5.json') as f:
        for json_obj in f:
            data_dict = json.loads(json_obj)
            data_list.append(data_dict)
    return data_list

def clean_data(data_list):
    print("Cleaning Data")
    cleaned_data = [make_lowercase_remove_punc(data) for data in data_list]
    reviews = [data['reviewText'] for data in cleaned_data]
    mappd = Counter(" ".join(ele for ele in reviews).split())
    sum_map = sum(mappd.values())
    res = {key: val / sum_map for key,
       val in mappd.items()}
    data_list = [remove_common_words(data, res) for data in cleaned_data]
    return data_list

def assign_ids(data_list):
    print("Assigning IDS")
    item_mapping = dict()
    user_mapping = dict()

    for data in data_list:
        user_id = data['reviewerID']
        item_id = data['asin']

        if user_id not in user_mapping:
            user_mapping[user_id] = len(user_mapping)
        data['reviewerID'] = user_mapping[user_id]

        if item_id not in item_mapping:
            item_mapping[item_id] = len(item_mapping)
        data['asin'] = item_mapping[item_id]
    return data_list

def make_user_rating_dict(data_list):
    user_rating_dict = dict()
    for data in data_list:
        if data['reviewerID'] not in user_rating_dict:
            user_rating_dict[data['reviewerID']] = dict()
        user_rating_dict[data['reviewerID']][data['asin']] = data['overall']
    return user_rating_dict
    
def calculate_similarity(user_review_dict, a_id, b_id):
    ratings_a = []
    ratings_b = []
    for item_id in user_review_dict[a_id]:
        if item_id in user_review_dict[b_id]:
            ratings_a.append(user_review_dict[a_id][item_id])
            ratings_b.append(user_review_dict[b_id][item_id])
    a = np.asarray(ratings_a)
    b = np.asarray(ratings_b)
    return np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_most_similar(user_review_dict, user_id, other_reviews):
    most_similar = other_reviews[0]
    similarity = calculate_similarity(user_review_dict, user_id, other_reviews[0][0])
    for review in other_reviews:
        new_similarity = calculate_similarity(user_review_dict, user_id, review[0])
        if new_similarity > similarity:
            most_similar = review
            similarity = new_similarity
    return most_similar

def generate_word_dict(data_list):
    print("Generating Word Dictionary using TF-IDF")
    reviews = [data['reviewText'] for data in data_list]

    mappd = Counter(" ".join(ele for ele in reviews).split())

    sum_map = sum(mappd.values())

    res = {key: val / sum_map for key,
        val in mappd.items()}

    document_freq = {}
    for data in data_list:
        seen_words = set()
        for word in data['reviewText'].split():
            if word not in document_freq:
                document_freq[word] = 0
            if word not in seen_words:
                document_freq[word] += 1
                seen_words.add(word)

    tf_idf = []

    for key, val in document_freq.items():
        tf_idf.append((key, res[key] * math.log(len(data_list) / val)))
            
    tf_idf.sort(key = lambda x: x[1], reverse = True)

    tf_idf = tf_idf[:20000]

    tf_idf_dict = dict()
    counter = 0
    for key, _ in tf_idf:
        tf_idf_dict[key] = counter
        counter += 1    
    return tf_idf_dict


def pick_aux_review(user_id, item_id, rating, item_rating_dict, user_rating_dict, use_cos):
    if (item_id, rating) not in item_rating_dict:
        return None
    set = [user_review for user_review in item_rating_dict[(item_id, rating)] if user_review[0] != user_id]
    if len(set) == 0:
        return None
    rand_user_review = [-1, "Null"]
    if use_cos:
        aux_review = get_most_similar(user_rating_dict, user_id, set)
    else:
        aux_review = random.sample(set, 1)[0]
    rand_user_review[0] = user_id
    rand_user_review[1] = aux_review[1]
    return rand_user_review

def make_item_rating_dict(data_list):
    item_rating_dict = dict()
    for data in data_list:
        item_rating = (data['asin'], data['overall'])
        user_review = (data['reviewerID'], data['reviewText'])
        if item_rating not in item_rating_dict:
            item_rating_dict[item_rating] = [user_review]
        else:
            item_rating_dict[item_rating].append(user_review)
    return item_rating_dict
            
def make_user_aux_review_doc(data_list, use_cos=False):
    print("Making User Auxiliary Review document")
    document = []
    item_rating_dict = make_item_rating_dict(data_list)
    if use_cos:
        user_rating_dict = make_user_rating_dict(data_list)
    else:
        user_rating_dict = None
    for data in data_list:
        u = data['reviewerID']
        rating = float(data['overall'])
        item_id = data['asin']
        review = pick_aux_review(u, item_id, rating, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating+1, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating-1, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating+2, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating-2, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating+3, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating-3, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating+4, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            review = pick_aux_review(u, item_id, rating-4, item_rating_dict, user_rating_dict, use_cos)
        if review is None:
            print(rating, item_id)
        document.append(review)
    return document

def write_word_dict(tf_idf_dict):
    print("Writing word dict")
    with open('./PARL/data/WordDict.out', 'w') as word_dict:
        for word, id in tf_idf_dict.items():
            word_dict.write(word + '\t' + str(id) + '\n')

def write_aux_reviews(all_aux_reviews):
    print("Writing auxiliary reviews")
    with open('./PARL/data/UserAuxiliaryReviews.out', 'w') as aux_reviews:
        for review in all_aux_reviews:
            aux_reviews.write(str(review[0]) + '\t' + review[1] + '\n')

def write_user_and_item_reviews(data_list):
    print("Writing user and item reviews")
    with open('./PARL/data/UserReviews.out', 'w') as users:
        with open('./PARL/data/ItemReviews.out', 'w') as items:
            for data in data_list:
                users.write(str(data['reviewerID']) + '\t' + data['reviewText'] + '\n')
                items.write(str(data['asin']) + '\t' + data['reviewText'] + '\n')

def write_files(filename, x_list):
    with open(filename, 'w') as f:
        for data in x_list:
            line = str(str(data['reviewerID']))+'\t'+str(data['asin'])+'\t'+\
                   str(data['overall'])+'\t'+str(data['unixReviewTime'])+'\n'
            f.write(line)

def make_train_test_val_split(data_list):
    print("Spliting test, train, and validation data")
    random.shuffle(data_list)
    train_list = data_list[:int((len(data_list)+1)*.70)]
    test_list = data_list[int((len(data_list)+1)*.70):int((len(data_list)+1)*.90)]
    validation_list = data_list[int((len(data_list)+1)*.90):]
    files = ['./PARL/data/TestInteraction.out', './PARL/data/TrainInteraction.out', './PARL/data/ValidateInteraction.out']
    lists = [test_list, train_list, validation_list]
    for file, lst in zip(files, lists):
        write_files(file, lst)


if __name__ == '__main__':
    data_list = read_file()
    data_list = clean_data(data_list)
    data_list = assign_ids(data_list)
    tf_idf_dict = generate_word_dict(data_list)
    all_aux_reviews = make_user_aux_review_doc(data_list, use_cos=True)
    write_word_dict(tf_idf_dict)
    write_user_and_item_reviews(data_list)
    write_aux_reviews(all_aux_reviews)
    make_train_test_val_split(data_list)
    print("Data processing complete!")
