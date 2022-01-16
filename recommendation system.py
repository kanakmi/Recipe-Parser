# importing required libraries
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# read the data
df = pd.read_feather('recipes.feather')

# create a column with the combined text of the ingredients
def make_tags(ingredients):
    tags = []
    
    if "Key Ingredients: " in ingredients[0]:
        ingredients[0] = ingredients[0][17:]
        
    for ingredient in ingredients:
        ingredient = ingredient.replace(" ", "")
        x = ingredient.find('(')
        if x!=-1:
            tags.append(ingredient[:x])
        else:
            tags.append(ingredient)
            
    return tags

df["key_ingredients"] = df["key_ingredients"].apply(make_tags)

def truncate(text):
    l = ''
    for i in text:
        l = l + str(i) + ' '
    return l

df["key_ingredients"] = df["key_ingredients"].apply(truncate)

# creating the recommendation system based on key ingredients using cosine similarity
cv = CountVectorizer(max_features=500,stop_words='english')

vector = cv.fit_transform(df.key_ingredients).toarray()

similarity = cosine_similarity(vector)

# saving the similarity matrix for later use
import pickle
pickle.dump(similarity,open('similarity.pkl','wb'))