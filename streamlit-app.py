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
        pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, max_length=64, truncation=True, padding='max_length')
        return pipe
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Streamlit UI
st.header('Sentiment Analysis')

# Model selection
model_options = [
    "nlptown/bert-base-multilingual-uncased-sentiment",
    "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
    "ElKulako/cryptobert",
    "Own Model"
]

selected_model1 = st.selectbox("Select Hugging Face model 1", model_options)
selected_model2 = st.selectbox("Select Hugging Face model 2", model_options)

# Check if "Own Model" is selected for model 1
if selected_model1 == "Own Model":
    custom_model_name = st.text_input("Enter custom Hugging Face model name for Model 1 (optional)")
    if custom_model_name:
        pipe1 = load_model(custom_model_name)
else:
    pipe1 = load_model(selected_model1)

# Check if "Own Model" is selected for model 2
if selected_model2 == "Own Model":
    custom_model_name = st.text_input("Enter custom Hugging Face model name for Model 2 (optional)")
    if custom_model_name:
        pipe2 = load_model(custom_model_name)
else:
    pipe2 = load_model(selected_model2)

with st.expander('Analyze Text'):
    text = st.text_input('Text here: ')
    if text:
        with st.spinner('Calculating...'):
            # Update text to indicate the progress
            st.text("Model 1: Calculating SHAP values...")
            explainer1 = shap.Explainer(pipe1)
            shap_values1 = explainer1([text])  # Pass text directly as a list
            st.text("Model 1: SHAP values calculated.")

            # Update text to indicate the progress
            st.text("Model 2: Calculating SHAP values...")
            explainer2 = shap.Explainer(pipe2)
            shap_values2 = explainer2([text])  # Pass text directly as a list
            st.text("Model 2: SHAP values calculated.")

        if selected_model1 == "nlptown/bert-base-multilingual-uncased-sentiment":
            st.text("Negative: Negative sentiment, Neutral: Neutral sentiment, Positive: Positive sentiment")
            st.text("Negative")
            st_shap(shap.plots.text(shap_values1[:, :, "Negative"]))
            st_shap(shap.plots.text(shap_values2[:, :, "Negative"]))
            st.text("Neutral")
            st_shap(shap.plots.text(shap_values1[:, :, "Neutral"]))
            st_shap(shap.plots.text(shap_values2[:, :, "Neutral"]))
            st.text("Positive")
            st_shap(shap.plots.text(shap_values1[:, :, "Positive"]))
            st_shap(shap.plots.text(shap_values2[:, :, "Positive"]))
        elif selected_model1 == "mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis":
            st.text("Negative: Negative sentiment, Neutral: Neutral sentiment, Positive: Positive sentiment")
            st.text("Negative")
            st_shap(shap.plots.text(shap_values1[:, :, "negative"]))
            st_shap(shap.plots.text(shap_values2[:, :, "negative"]))
            st.text("Neutral")
            st_shap(shap.plots.text(shap_values1[:, :, "neutral"]))
            st_shap(shap.plots.text(shap_values2[:, :, "neutral"]))
            st.text("Positive")
            st_shap(shap.plots.text(shap_values1[:, :, "positive"]))
            st_shap(shap.plots.text(shap_values2[:, :, "positive"]))
        elif selected_model1 == "ElKulako/cryptobert":
            st.text("Bullish: Positive sentiment, Neutral: Neutral sentiment, Bearish: Negative sentiment")
            st.text("Bullish")
            st_shap(shap.plots.text(shap_values1[:, :, "Bullish"]))
            st_shap(shap.plots.text(shap_values2[:, :, "Bullish"]))
            st.text("Neutral")
            st_shap(shap.plots.text(shap_values1[:, :, "Neutral"]))
            st_shap(shap.plots.text(shap_values2[:, :, "Neutral"]))
            st.text("Bearish")
            st_shap(shap.plots.text(shap_values1[:, :, "Bearish"]))
            st_shap(shap.plots.text(shap_values2[:, :, "Bearish"]))