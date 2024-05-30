import pandas as pd
import streamlit as st
import cleantext
import shap
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer

# Load the model and tokenizer
model_name = "ElKulako/cryptobert"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding='max_length')
#why not pload?
st.header('Sentiment Analysis')

with st.expander('Analyze Text'):
    text = st.text_input('Text here: ')
    if text:
        with st.spinner('Calculating...'):
            explainer = shap.Explainer(pipe)
            shap_values = explainer([text])  # Pass text directly as a list

        st.subheader('SHAP Values:')
        st.text("Explanation of SHAP values...")
        print(shap_values)
        st.pyplot(shap.plots.text(shap_values[:, :, "Bullish"]))
        st.pyplot(shap.plots.text(shap_values[:, :, "Neutral"]))
        st.pyplot(shap.plots.text(shap_values[:, :, "Bearish"]))

        #st.subheader('Mean SHAP Values for Bearish:')
        #st.text("Explanation of mean SHAP values for Bearish...")
        #st.image(shap.plots.bar(shap_values[:, :, "Bearish"].mean(0)), use_column_width=True)
