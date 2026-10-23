import streamlit as st
from lang import answer_question

st.set_page_config(page_title="YouTube Video Analyzer", page_icon=":video_camera:", layout="centered")

st.title(":video_camera: YouTube Video Analyzer")
st.write("This app allows you to analyze YouTube videos by summarizing their content and answering questions based on the transcript.")

video_url= st.text_input("Enter YouTube Video URL")

question = st.text_input("Enter your question about the video")

if st.button("Get Answer"):
    if not video_url.strip() or not question.strip():
        st.warning("Please enter both the URL and your question.")

    else:
        try:
            with st.spinner("Reading the video and generating your answer..."):
                answer = answer_question(video_url, question)

            st.subheader("Answer")
            st.write(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
