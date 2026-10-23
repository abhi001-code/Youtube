
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_getyoutubetranscript import GetYouTubeTranscriptLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda
)
from dotenv import load_dotenv
import os

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
youtube_api_key = os.getenv("GETYOUTUBETRANSCRIPT_API_KEY")


def con(retrieved_doc):
    context_text = "\n\n".join(
        doc.page_content for doc in retrieved_doc
    )
    return context_text


def answer_question(video_url, question):

    model = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model="gemini-3.6-flash"
    )

    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=google_api_key,
        model="gemini-embedding-001"
    )

    loader = GetYouTubeTranscriptLoader(
        [video_url],
        language="en",
        api_key=youtube_api_key
    )

    docs = loader.load()
    transcript = docs[0].page_content

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents([transcript])

    vector_store = Chroma.from_documents(chunks, embeddings)

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.
Answer only from the provided transcript context.
If the context is insufficient, just say "I don't know".

Context:
{context}

Question: {question}
""",
        input_variables=["context", "question"]
    )

    parallel_chain = RunnableParallel({
        "context": (
            RunnableLambda(lambda x: x["question"])
            | retriever
            | RunnableLambda(con)
        ),
        "question": RunnableLambda(lambda x: x["question"])
    })

    parser = StrOutputParser()

    main_chain = parallel_chain | prompt | model | parser

    answer = main_chain.invoke({"question": question})

    return answer
