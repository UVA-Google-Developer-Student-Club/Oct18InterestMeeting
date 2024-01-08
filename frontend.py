import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(
    page_title="Oct. 18 Sentiment Analysis",
    page_icon="📈",
    layout="wide",
)

url = "https://oct18interestmeeting-default-rtdb.firebaseio.com/"


def fetch_data():
    data = requests.get(url + "/submissions.json").json()
    print(data)
    df = pd.DataFrame(data).T
    df = df[["name", "review", "joy", "surprise",
             "disgust", "anger", "sadness", "fear", "others"]]

    df = df.sort_values(by="others", ascending=False)
    # for all columns except name and review, multiply by 100
    df.iloc[:, 2:] = df.iloc[:, 2:] * 100
    # rename the coluumns to say ___ %
    # df.columns = ["name", "review", "joy (%)", "surprise (%)",
    #               "disgust (%)", "anger (%)", "sadness (%)", "fear (%)", "others (%)"]
    df.index = range(1, len(df)+1)
    return df


st.title("Oct. 18 Sentiment Analysis")

# Initialize state variables
data_container = st.empty()


# update the data every 3 seconds
while True:
    with data_container.container():

        # Display the top review for each emotion

        df = fetch_data()

        st.header("Most Emotional Reviews")
        emotions = ["joy", "surprise", "disgust", "anger", "sadness", "fear"]
        emojis = ["😂", "😮", "🤢", "😡", "😢", "😨"]
        columns = st.columns(len(emotions))
        for index, column in enumerate(columns):
            with column:
                # center the emoji and make it bigg
                st.markdown(
                    f"<p style='text-align: left; font-size: 36px;'>{emojis[index]}</p>", unsafe_allow_html=True)
                # st.header(emojis[index])
                top_review = df.sort_values(
                    by=emotions[index], ascending=False).iloc[0]
                st.subheader(
                    f"{emotions[index].title()} ({top_review[emotions[index]]:.2f}%)")
                st.write(
                    f"**{top_review['name']}** - \"{top_review['review']}\"")
                st.markdown("---")
        st.header("All Reviews")
        # create new df with all same values except turn the emotions into percentages
        new_df = df.copy()
        # include the percent sign
        new_df.iloc[:, 2:] = new_df.iloc[:, 2:].applymap(
            lambda x: f"{x:.2f}%")
        st.dataframe(new_df)

        time.sleep(2)
