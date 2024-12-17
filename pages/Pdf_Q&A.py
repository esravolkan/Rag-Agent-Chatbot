import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables import RunnableWithMessageHistory
from langchain.schema import HumanMessage, AIMessage
from utils import sidebar_setup, initialize_embeddings, initialize_llm
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    st.set_page_config(page_title="Conversational RAG With PDF Uploads", layout="wide")

    # Load CSS file
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

    # Page title
    st.markdown(
        """
        <div class="title-box">
            <h1>🧑‍🏫 PDF Q&A Assistant with RAG 📚</h1>
            <h3> Share your files, ask questions, and let me do the searching.</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar setup (API and key input)
    api_choice, optional_api_key, engine = sidebar_setup()

    # Initialize embeddings
    embeddings = initialize_embeddings()

    # Initialize LLM
    llm = initialize_llm(api_choice, optional_api_key, engine)

    # File upload
    uploaded_files = st.file_uploader("", type="pdf", accept_multiple_files=True)
    user_input = st.text_input("", placeholder="Your question based on your file:")

    # Process uploaded PDFs
    documents = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            temp_pdf = f"./temp_{uploaded_file.name}"
            with open(temp_pdf, "wb") as file:
                file.write(uploaded_file.getvalue())

            loader = PyPDFLoader(temp_pdf)
            docs = loader.load()
            documents.extend(docs)

    # RAG pipeline setup
    if documents and llm:
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)

        # Create vectorstore
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        retriever = vectorstore.as_retriever()

        # Define prompts
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        # Create RAG chain
        rag_chain = create_retrieval_chain(retriever, create_stuff_documents_chain(llm, qa_prompt))

        # Manage chat history
        def get_session_history(session: str) -> BaseChatMessageHistory:
            if 'store' not in st.session_state:
                st.session_state.store = {}
            if session not in st.session_state.store:
                st.session_state.store[session] = ChatMessageHistory()
            return st.session_state.store[session]

        session_id = "default_session"
        session_history = get_session_history(session_id)

        # Process user input
        if rag_chain and user_input:
            with st.spinner("Generating response..."):
                response = RunnableWithMessageHistory(
                    rag_chain, get_session_history,
                    input_messages_key="input",
                    history_messages_key="chat_history",
                    output_messages_key="answer"
                ).invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": session_id}}
                )

            # Display messages
            for msg in session_history.messages:
                role = "user" if isinstance(msg, HumanMessage) else "assistant"
                with st.chat_message(role):
                    st.write(msg.content)
    else:
        # Handle missing LLM or documents
        if not llm:
            st.write("Please provide valid API Keys/Model selection in the sidebar.")
        elif user_input:
            st.write("No documents uploaded. Please upload your file.")


if __name__ == "__main__":
    main()
