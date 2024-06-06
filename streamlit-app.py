import pandas as pd
import streamlit as st
import cleantext
from streamlit_shap import st_shap
import shap
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer
import matplotlib.pyplot as plt
import numpy as np

# Function to load the selected Hugging Face model
def load_model(model_name):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
        pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, top_k=None, padding='max_length')
        return pipe
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Function to display SHAP values and explanations based on model type
def display_shap_values(shap_values, prediction):
    print("Displaying SHAP values...")
        # Display SHAP values
    st_shap(shap.plots.text(shap_values))
    # Convert prediction to proper case
    predicted_label = prediction.capitalize()
    st.write(f"Predicted label: {predicted_label}")
    predicted_label

# Function to display all labels and their scores
def display_all_labels(predictions):
    st.write("All labels and scores:")
    for label_score in predictions[0]:
        label = label_score['label'].capitalize()
        score = label_score['score']
        st.write(f"{label}: {score:.4f}")


# Streamlit UI
st.header('Sentiment Analysis')

# Model selection
model_options = [
    "nlptown/bert-base-multilingual-uncased-sentiment",
    "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
    "ElKulako/cryptobert",
    "Own Model"
]

selected_model = st.selectbox("Select Hugging Face model", model_options)

# Check if "Own Model" is selected
if selected_model == "Own Model":
    custom_model_name = st.text_input("Enter custom Hugging Face model name (optional)")
    if custom_model_name:
        pipe = load_model(custom_model_name)
else:
    pipe = load_model(selected_model)

with st.expander('Analyze Text'):
    text = st.text_input('Text here: ')
    if text:
        with st.spinner('Calculating...'):
            # Model predictions and SHAP values
            if pipe:
                st.text("Calculating SHAP values and predicting label...")
                explainer = shap.Explainer(pipe)
                shap_values = explainer([text])  # Pass text directly as a list
                predictions = pipe(text)
                prediction = predictions[0][0]['label']
                st.write("SHAP values and prediction calculated.")
                st.write(f"Prediction: {prediction}")
                display_all_labels(predictions)
                display_shap_values(shap_values, prediction)