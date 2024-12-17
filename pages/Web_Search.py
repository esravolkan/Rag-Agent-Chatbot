import streamlit as st
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.tools import Tool
import time
from dotenv import load_dotenv
from utils import sidebar_setup, initialize_llm

# Limit DuckDuckGo search to max 1 call
def limited_duckduckgo_call(tool_func, max_calls=1):
    call_counter = {"count": 0}
    def wrapper(*args, **kwargs):
        if call_counter["count"] >= max_calls:
            return "DuckDuckGo search limit reached."
        call_counter["count"] += 1
        return tool_func(*args, **kwargs)
    return wrapper

def main():
    load_dotenv()
    st.set_page_config(page_title="Conversational Web Search Agent", page_icon="🔎", layout="wide")

    # Load CSS
    with open("static/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Page title
    st.markdown(
        """
        <div class="title-box">
            <h1> 🌐Your Personal Web Detective🕵️</h1>
            <h4>I search the web, papers, and articles <br> using DuckDuckGo, Arxiv, and Wikipedia to answer your questions.</h4>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sidebar setup
    api_choice, optional_api_key, engine = sidebar_setup()

    # Initialize LLM
    llm = initialize_llm(api_choice, optional_api_key, engine)

    # Initialize tools
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)

    # Limit DuckDuckGo tool
    search = DuckDuckGoSearchRun(name="Search")
    def safe_search(query):
        time.sleep(3)
        return search.run(query)

    duckduckgo_tool = Tool(
        name="Safe Search",
        func=limited_duckduckgo_call(safe_search, max_calls=1),  # Limit to 1 call
        description="Search the web using DuckDuckGo (limited to 1 search)."
    )

    # Page message history
    page_key = "web_search_messages"
    if page_key not in st.session_state:
        st.session_state[page_key] = [{"role": "assistant", "content": "Hi, how can I assist you today?"}]

    # Display chat history
    for msg in st.session_state[page_key]:
        st.chat_message(msg["role"]).write(msg["content"])

    # User input
    if prompt := st.chat_input(placeholder="Ask me something..."):
        st.session_state[page_key].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Check API key
        if not optional_api_key or api_choice == "None":
            st.error("Please select an API and provide a valid API Key.")
            return

        # Tools setup
        tools = [arxiv, wiki, duckduckgo_tool]

        # Run the agent
        try:
            search_agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                handle_parsing_errors=True
            )

            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = search_agent.run(prompt, callbacks=[st_cb])
                st.session_state[page_key].append({"role": "assistant", "content": response})
                st.write(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
