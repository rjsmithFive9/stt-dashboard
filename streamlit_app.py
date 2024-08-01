import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def run(csv_filename):
    st.set_page_config(layout="wide")
    df = get_dataframe_from_csv(csv_filename)
    if df is not None:
        render_dashboard(df)

def get_dataframe_from_csv(csv_filename):
    if csv_filename is None:
        csv_filename = st.file_uploader("Choose a file:")
    if csv_filename is not None:
        return pd.read_csv(csv_filename)
    return None


def render_dashboard(df):
    df.sort_values(by="percent_of_quota", inplace=True, ascending=False)

    st.dataframe(df, width=1600, height=800)
    # st.write(df)

    df.sort_values(by="percent_of_quota", inplace=True, ascending=True)

    df["domain_id"] = df["domain_id"].astype(str)
    df["y_label"] = df[['domain_id', 'domain_name', 'project_id']].agg(' | '.join, axis=1)

    n = len(df["project_id"])

    y_pos = np.arange(len(df))
    width = 0.5

    fig, ax = plt.subplots(figsize=(10, 0.4*n))
    quota_bar = ax.barh(y_pos, df.stt_quota_audio_seconds, width, color='red', label='Quota')
    ax.bar_label(quota_bar, label_type="edge")
    usage_bar = ax.barh(y_pos, df.stt_usage_audio_seconds, width, color='green', label='Usage')
    ax.bar_label(usage_bar, label_type="edge")

    ax.set(yticks=y_pos, yticklabels=df.y_label, ylim=[width, len(df)])
    ax.set_title('Audio Seconds Usage vs. Quota\nSort: % Used')
    ax.legend()

    st.write(fig)

if __name__ == "__main__":
    run(None)
