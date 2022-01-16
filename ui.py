import streamlit as st
import pandas as pd
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from streamlit import caching

with open('./Food_Classifier/Saved_Model/foodclassifier_model.json', 'r') as json_file:
    json_savedModel = json_file.read()

# load the model architecture
model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('./Food_Classifier/Saved_Model/foodclassifier_weights.h5')
opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt,loss="sparse_categorical_crossentropy", metrics=["accuracy"])

labels = ['adhirasam',
 'aloo_gobi',
 'aloo_matar',
 'aloo_methi',
 'aloo_shimla_mirch',
 'aloo_tikki',
 'anarsa',
 'ariselu',
 'bandar_laddu',
 'basundi',
 'bhatura',
 'bhindi_masala',
 'biryani',
 'boondi',
 'butter_chicken',
 'kheer',
 'cham_cham',
 'chana_masala',
 'chapati',
 'chhena_kheeri',
 'chicken_razala',
 'chicken_tikka',
 'chicken_tikka_masala',
 'chikki',
 'daal_baati_churma',
 'daal_puri',
 'dal_makhani',
 'dal_tadka',
 'dharwad_pedha',
 'doodhpak',
 'double_ka_meetha',
 'dum_aloo',
 'gajar_ka_halwa',
 'gavvalu',
 'ghevar',
 'gulab_jamun',
 'imarti',
 'jalebi',
 'kachori',
 'kadai_paneer',
 'kadhi_pakoda',
 'kajjikaya',
 'kakinada_khaja',
 'kalakand',
 'karela_bharta',
 'kofta',
 'kuzhi_paniyaram',
 'lassi',
 'ledikeni',
 'litti_chokha',
 'lyangcha',
 'maach_jhol',
 'makki_di_roti_sarson_da_saag',
 'malpua',
 'misi_roti',
 'misti_doi',
 'modak',
 'mysore_pak',
 'naan',
 'navrattan_korma',
 'palak_paneer',
 'paneer_butter_masala',
 'phirni',
 'pithe',
 'poha',
 'poornalu',
 'pootharekulu',
 'qubani_ka_meetha',
 'rabri',
 'rasmalai',
 'rasgulla',
 'sandesh',
 'shankarpali',
 'sheer_korma',
 'sheera',
 'shrikhand',
 'sohan_halwa',
 'sohan_papdi',
 'sutar_feni',
 'unniappam']

def classify_image(file_path):
    image = Image.open(file_path) # reading the image
    image = image.resize((128, 128)) # resizing the image
    img = np.asarray(image) # converting it to numpy array
    img = np.expand_dims(img, 0)
    predictions = model.predict(img) # predicting the class
    c = np.argmax(predictions[0]) # extracting the class with maximum probablity
    return labels[c]

similarity = pickle.load(open('similarity.pkl', 'rb'))

df = pd.read_feather('recipes.feather')

def recommend(title):
    index = df[df['title'] == title].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    ret = []
    for i in distances[1:3]:
        ret.append(i[0])
    return ret

# st.image('header.png', use_column_width=True)

def build_ui(option, image=None):
    st.subheader(option)
    details = df.iloc[df[df['title'] == option].index[0]]
    cols = st.columns([2, 1])
    if image is None:
        cols[0].image(details['image'], use_column_width=True)
    else:
        cols[0].image(image, use_column_width=True)

    cols[1].write("##### Prepration Time - " + "\n" + details['prep_time'])
    cols[1].write("##### Cooking Time - " + "\n" + details['cook_time'])
    cols[1].write("##### Servings - " + "\n" + details['serving'])
    # c[1].markdown(f'## {option}')
    st.write("#### Ingredients:")
    c = st.columns(2)
    for i in range(len(details['ingredients'])//2):
        c[0].write("- " + details['ingredients'][i])
        c[1].write("- " + details['ingredients'][i+len(details['ingredients'])//2])
    # for i in range(len(details['ingredients'])//2):
    #     c[0].write("- " + details['ingredients'][i])

    st.write("")

    st.write("#### Procedure:")
    for i in details['procedure']:
        st.write("- " + i)

    rec = recommend(option)
    
    st.subheader("Also Try: ")

    col = st.columns(2)

    for i in range(2):
        col[i].image(df.iloc[rec[i]].image , width=300, caption=df.iloc[rec[i]].title)

option = st.selectbox("Search for your Favorite Recipe", df['title'].values)

click = st.button("Search")

st.write("or")

file_uploaded = st.file_uploader("Choose the Image File", type=['jpg', 'jpeg', 'png'])

if file_uploaded is not None:
    c = classify_image(file_uploaded)
    c = c.replace('_', ' ')
    c = c.title()
    option = c
    build_ui(c, file_uploaded)

if click:
    build_ui(option)