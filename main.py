import streamlit as st
from lang import answer_question , process_video

st.set_page_config(page_title="YouTube Video Analyzer", page_icon=":video_camera:", layout="centered")

st.title(":video_camera: YouTube Video Analyzer")
st.write("This app allows you to analyze YouTube videos by summarizing their content and answering questions based on the transcript.")

if "video_url" not in st.session_state:
    st.session_state.video_url=""

video_url= st.text_input("Enter YouTube Video URL")

if "retriever" not in st.session_state:
    st.session_state.retriever=None

if st.button("Process Video"):
    if not video_url:
        st.warning("Please enter a valid YouTube video URL")
    else:
        try:
            with st.spinner("Processing video..."):
                retriever=process_video(video_url.strip())
                st.session_state.retriever=retriever
                st.session_state.video_url=video_url.strip()

                st.success("Video processed successfully! Now you can ask questions about the video.")
        except Exception as e:
            st.error(f"Error processing video: {e}")

if st.session_state.retriever:
    question=st.text_input("Ask a question about the video")
    if st.button("Answer"):
        if not question:
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Generating Answer...."):
                    answer=answer_question(st.session_state.retriever , question)

                st.subheader("Answer")
                st.write(answer)

            except Exception as e:
                st.error(f"Could not generate an answer : {e}")

