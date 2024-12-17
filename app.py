import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables import RunnableWithMessageHistory
import os
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()

    # STREAMLIT INTERFACE SETTINGS

    # === App Header/Page title =========
    st.set_page_config(page_title="Conversational RAG With PDF Uploads", layout="wide")

    # Load CSS file
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)


    # ==========SideBar ===========
    st.sidebar.title("API Key Selection")
    api_choice = st.sidebar.selectbox("Choose Additional Model API:", ["None", "Groq", "OpenAI", "Claude"])
    optional_api_key = st.sidebar.text_input(f"{api_choice} API Key", type="password") if api_choice != "None" else None

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Model selection
    if api_choice == "Groq" and optional_api_key:
        llm = ChatGroq(groq_api_key=optional_api_key, model_name="Gemma2-9b-It")
        st.sidebar.success("Using Groq API.")
    elif api_choice == "OpenAI" and optional_api_key:
        # Placeholder for OpenAI LLM initialization
        st.sidebar.success("Using OpenAI API.")
    elif api_choice == "Claude" and optional_api_key:
        # Placeholder for Claude LLM initialization
        st.sidebar.success("Using Claude API.")
    else:
        llm = None
        st.sidebar.info("No additional model API selected.")


    # ==========Chat Page===========
    st.markdown(
        """
        <div class="title-box">
            <h1>📝 Conversational RAG with PDFs</h1>
            <h2>Ask me any questions based on the uploaded file(s).</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


    # User input for questions
    user_input = st.text_input("Your question:")

    # File uploader for PDFs in sidebar
    uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

    documents = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            temp_pdf = f"./temp_{uploaded_file.name}"
            with open(temp_pdf, "wb") as file:
                file.write(uploaded_file.getvalue())

            loader = PyPDFLoader(temp_pdf)
            docs = loader.load()
            documents.extend(docs)



    if documents:
        # Splitting and creating a vector store
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        retriever = vectorstore.as_retriever()

        # Contextualized question retriever
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt) if llm else retriever

        # QA system prompt
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt) if llm else None
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain) if llm else None

        # Manage chat history
        def get_session_history(session: str) -> BaseChatMessageHistory:
            if 'store' not in st.session_state:
                st.session_state.store = {}
            if session not in st.session_state.store:
                st.session_state.store[session] = ChatMessageHistory()
            return st.session_state.store[session]

        session_id = "default_session"
        session_history = get_session_history(session_id)

        if rag_chain:
            conversational_rag_chain = RunnableWithMessageHistory(
                rag_chain, get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

            if user_input:
                # Add spinner while waiting for a response
                with st.spinner("Waiting for response..."):
                    response = conversational_rag_chain.invoke(
                        {"input": user_input},
                        config={"configurable": {"session_id": session_id}}
                    )
                similarity_score = response.get('similarity', 'N/A')

                from langchain.schema import HumanMessage, AIMessage, SystemMessage

                # Identify the last user and assistant messages to show them at the top
                last_user_msg = None
                last_assistant_msg = None

                if len(session_history.messages) >= 2:
                    last_user_msg = session_history.messages[-2]
                    last_assistant_msg = session_history.messages[-1]

                # If not found, fallback to find them individually
                if last_user_msg is None or not isinstance(last_user_msg, HumanMessage):
                    for i in range(len(session_history.messages) - 1, -1, -1):
                        if isinstance(session_history.messages[i], HumanMessage):
                            last_user_msg = session_history.messages[i]
                            break
                if last_assistant_msg is None or not isinstance(last_assistant_msg, AIMessage):
                    for i in range(len(session_history.messages) - 1, -1, -1):
                        if isinstance(session_history.messages[i], AIMessage):
                            if last_user_msg is None or i > session_history.messages.index(last_user_msg):
                                last_assistant_msg = session_history.messages[i]
                                break

                # Track displayed messages
                displayed_indices = set()
                if last_user_msg:
                    displayed_indices.add(session_history.messages.index(last_user_msg))
                    with st.chat_message("user"):
                        st.write(last_user_msg.content)

                if last_assistant_msg:
                    displayed_indices.add(session_history.messages.index(last_assistant_msg))
                    with st.chat_message("assistant"):
                        st.write(last_assistant_msg.content)

                # Display older messages at the bottom
                for i, msg in enumerate(session_history.messages):
                    if i in displayed_indices:
                        continue
                    if isinstance(msg, HumanMessage):
                        with st.chat_message("user"):
                            st.write(msg.content)
                    elif isinstance(msg, AIMessage):
                        with st.chat_message("assistant"):
                            st.write(msg.content)
                    else:
                        with st.chat_message("assistant"):
                            st.write(msg.content)

    else:
        # If no documents are uploaded or no question is asked
        if user_input:
            st.write("Assistant: Unfortunately, no documents are uploaded. Please upload a file or ask general questions.")
        else:
            st.write("Assistant: Please upload documents or enter your question above.")


if __name__ == "__main__":
    main()
