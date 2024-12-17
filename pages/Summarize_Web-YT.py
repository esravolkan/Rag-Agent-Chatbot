import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.docstore.document import Document
from yt_dlp import YoutubeDL
from dotenv import load_dotenv
from utils import sidebar_setup, initialize_llm  # Import utilities

def main():
    # Load environment variables
    load_dotenv()
    st.set_page_config(page_title="Summarize Text From YT or Website", page_icon="📝", layout="wide")

    # Load CSS
    with open("static/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Sidebar setup
    api_choice, optional_api_key, engine = sidebar_setup()

    # Title and description
    st.markdown(
        """
        <div class="title-box">
            <h1>📋 Simplify Your Learning ▶️</h1>
            <h3>Drop a YouTube or website URL, and get a quick, clear summary in seconds.</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Input for URL
    url = st.text_input("", placeholder="Paste a YouTube or Website URL here...")

    # Initialize LLM
    llm = initialize_llm(api_choice, optional_api_key, engine)

    # Prompt template for summary
    prompt_template = """
    Provide a summary of the following content in 300 words:
    Content:{text}
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Function to fetch YouTube transcript
    def fetch_youtube_transcript(url):
        try:
            ydl_opts = {"noplaylist": True, "quiet": True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get("description", "No transcript or description available.")
        except Exception as e:
            st.error(f"Error fetching YouTube video: {e}")
            return None

    # Button to summarize content
    if st.button("Summarize Content"):
        # Check API key and URL validity
        if not optional_api_key or not url.strip():
            st.error("Please provide a valid API key and URL.")
            return
        elif not validators.url(url):
            st.error("Invalid URL. Please enter a valid URL.")
            return

        if not llm:
            st.error("Select a valid API and provide the required API key.")
            return

        # Fetch and process content
        try:
            with st.spinner("Processing..."):
                if "youtube.com" in url or "youtu.be" in url:
                    content = fetch_youtube_transcript(url)
                    if not content:
                        st.error("Failed to fetch YouTube content.")
                        return
                    docs = [Document(page_content=content)]
                else:
                    loader = UnstructuredURLLoader(urls=[url], ssl_verify=False)
                    docs = loader.load()

                # Generate summary
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                summary = chain.run(docs)
                st.success(summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
