import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import base64

ps = PorterStemmer()

def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )


side_bg = 'https://dazeinfo.com/wp-content/uploads/2020/08/spam-sms-blocking-apps-1.jpg'
sidebar_bg(side_bg)
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")
if st.button('predict'):
    # 1. preprocessing
    transform_sms = transform_text(input_sms)
    # 2. vectorize
    vector_input = tfidf.transform([transform_sms])
    # 3.predict
    result = model.predict(vector_input)[0]
    # 4. display
    if result == 1:
        st.header("Spam")
    else:
        st.header("Not spam")
