import pandas as pd


def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv("data/feedback.csv")

    if "feedback" not in data.columns:
        raise ValueError("Your CSV file must contain a column named 'feedback'.")

    return data