# RAG based Website assistant

import streamlit as st  # to build the frontend

# here process_urls and generate_answer are the functions  is dowloading dat from urls and storing into chromdb
# generate_answer is the function which is taking the query and generating the answer from the chromadb
from rag import process_urls, generate_answer # to process the urls and generate answer

st.title("RAG based Website assistant")

url1 = st.sidebar.text_input("URL-1")
url2 = st.sidebar.text_input("URL-2")
url3 = st.sidebar.text_input("URL-3")

# placeholder is the space which used show  the progress
placeholder = st.empty()

process_url_button = st.sidebar.button("Process URL's")

if process_url_button:
    # pick the url which in not empty and store in urls list
    urls = [url for url in (url1, url2, url3) if url!=""]

    if len(urls) == 0:
        placeholder.text("Please mention atleast one URL")
    else:
        for status in process_urls(urls):
            placeholder.text(status)

query = placeholder.text_input("question")


if query:
    try:
        answer, sources  = generate_answer(query)

        st.header("Answer")
        st.write(answer)
        if sources:
            st.header("Sources")
            for s in sources.split("\n"):
                st.write(s)
    except Exception as e:
        placeholder.text("Please first click on process URL")