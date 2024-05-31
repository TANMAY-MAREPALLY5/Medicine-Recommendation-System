

import numpy as np 
import pandas as pd 

meds = pd.read_csv('Medicine_Details.csv')

meds = meds[['Medicine Name', 'Composition', 'Uses', 'Side_effects', 'Image URL', 'Manufacturer', 'Excellent Review %', 'Average Review %', 'Poor Review %']]

medicines = meds.drop_duplicates()

salts_name = list(meds['Composition'].value_counts().keys())[0:20]
count_of_meds_with_that_salt = list(meds['Composition'].value_counts())[0:20]

manu_name = list(meds['Manufacturer'].value_counts().keys())[0:30]
count_manufacture_name = list(meds['Manufacturer'].value_counts())[0:30]

def convert(input_string):
    
    salts = [item.strip() for item in input_string.split(' + ')]
    return salts

meds['Composition'] = meds['Composition'].apply(convert)

meds['Uses'] = meds['Uses'].apply(lambda x:x.split())

meds['Side_effects'] = meds['Side_effects'].apply(lambda x: x.split())

meds['Composition'] = meds['Composition'].apply(lambda x:[i.replace(" ","") for i in x])



meds['Medicine Score'] = round((meds['Excellent Review %']/100 * 5.0) + (meds['Average Review %']/100 * 3.0) + (meds['Poor Review %']/100 *1.0), 2)

medicine_scores = list(meds['Medicine Score'].value_counts().keys())
count_medicine_score = list(meds['Medicine Score'].value_counts())

index = []
new_scores = []
for i in medicine_scores:
    if i>3.1:
        index.append(medicine_scores.index(i))
        new_scores.append(i)
    else :
        pass

scores_count = []
for i in index:
    scores_count.append(count_medicine_score[i])

meds['tags'] = meds['Composition'] + meds['Uses']

meds['tags_with_side_effects'] = meds['Side_effects'].astype(str)

new_df = meds[['Medicine Name', 'Uses', 'Composition', 'Side_effects','tags', 'tags_with_side_effects', 'Manufacturer', 'Medicine Score', 'Image URL']]


new_df['tags'] = new_df['tags'].apply(lambda x:' '.join(x))

new_df['tags_with_side_effects'] = new_df['tags_with_side_effects'].apply(lambda x: ''.join(x))


new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())
new_df['tags_with_side_effects'] = new_df['tags_with_side_effects'].apply(lambda x:x.lower())

new_df.rename(columns = {'Medicine Name':'Name', }, inplace = True)
new_df.rename(columns = {'Medicine Score':'Score'}, inplace = True)
new_df.rename(columns = {'Image URL':'img_url', }, inplace = True)


import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
        
    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

new_df['tags_with_side_effects'] = new_df['tags_with_side_effects'].apply(stem)


#Feature Vectorization
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 5000, stop_words='english')
vector  = cv.fit_transform(new_df['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)

# Recommendations based on medicine name
def recommend(medicine):
    recommended_medicine = []
    med_index = new_df[new_df['Name'] == medicine].index[0]
    distances = similarity[med_index]
    med_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:51]
    for i in med_list:
        recommended_medicine.append([new_df.iloc[i[0]].Name, new_df.iloc[i[0]].Score])

    recommendations = sorted(recommended_medicine,reverse = True, key = lambda x:x[1])
    seen = set()
    recommended_medicines = [x for x in recommendations if tuple(x) not in seen and not seen.add(tuple(x))]
    
    for i in recommended_medicines:
        print(i)

# Recommendations based on medicine composition

def recommend_medicine(composition_queries):
    recommendations = []

    
    for index, row in new_df.iterrows():
        composition = row['Composition']
        if isinstance(composition, list):
            
            if all(query.lower() in ' '.join(composition).lower() for query in composition_queries):
                recommendations.append([row['Name'],  row['Score']])

   

    if recommendations:
        
        medicine_list = sorted(recommendations, reverse = True, key = lambda x:x[1])[:50]
        seen = set()
        recommended_medicines = [x for x in medicine_list if tuple(x) not in seen and not seen.add(tuple(x))]
        return recommended_medicines
    else:
        return "No matching medicines found."


def recommend_medicine1(use_query):
    recommendations = []


    for index, row in new_df.iterrows():
        use = row['Uses']
        if isinstance(use, list):
            
            if all(query.lower() in ' '.join(use).lower() for query in use_query):
                recommendations.append([row['Name'],  row['Score']])

   

    if recommendations:
        
        medicine_list = sorted(recommendations, reverse = True, key = lambda x:x[1])[:50]
        seen = set()
        recommended_medicines = [x for x in medicine_list if tuple(x) not in seen and not seen.add(tuple(x))]
        return recommended_medicines
    else:
        return "No medicines found for this disease."

def get_composition(medicine_name):
    
    med_row = meds[meds['Medicine Name'] == medicine_name].iloc[0]
    return ', '.join(med_row['Composition'])
    pass

def get_side_effects(medicine_name):
    
    med_row = meds[meds['Medicine Name'] == medicine_name].iloc[0]
    return ', '.join(med_row['Side_effects'])

def get_manufacturer(medicine_name):
    
    med_row = meds[meds['Medicine Name'] == medicine_name].iloc[0]
    return med_row['Manufacturer']

def get_image_url(medicine_name):
    
    med_row = meds[meds['Medicine Name'] == medicine_name].iloc[0]
    return med_row['Image URL']






