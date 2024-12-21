
---

<h1 align="center">
🌐MultiPage LLM Chatbot Demo: RAG-Agent-Assistanst🤖
</h1>

<h3 align="center">
All-in-one AI assistant powered by LLMs, RAG pipelines, and agents for PDF Q&A, web search, and content summarisation.
</h3>

- This demo version of the app allows seamless interaction with LLMs using Python snd Streamlit framework.  
- It supports multiple AI models, including Groq's Gemma and OpenAI GPT, and combines RAG pipelines with agent-based search tools.  
- It can process PDFs by splitting them into chunks, perform web searches with agent tools using DuckDuckGo, Arxiv, and Wikipedia, and summarise YouTube videos or web content.  

💡Easily adaptable for integration with other APIs or models with minimal changes.


## **Features**

Let's break it down, page by page:
- 🧑‍🏫 PDF Q&A Assistant: Upload multiple PDF files and get the most relevant answers to your questions.
- 🌐 Web Search Agent: Retrieve information from Google, Arxiv, and Wikipedia.
- ▶️ Content Summariser: Summarise YouTube videos or website text in seconds.
- 💬 Friendly Chat:  Enjoy fun, creative, and engaging conversations with an AI a


<p align="center">
  <img src="https://github.com/Duygu-Jones/Rag-Agent-Chatbot/blob/main/static/multipage-chatbot.gif">
</p>


## ♻️**Usage**

**Try it Out**: [Experience the app live on Streamlit Cloud](https://YOUR-STREAMLIT-LINK-HERE). 

1. **Select an API & Model**: Enter API keys in the sidebar.  
2. **Navigate Between Pages**:  
   - 🧑‍🏫 **PDF Q&A**: Upload PDFs and ask questions based on your files.  
   - 🌐 **Web Search**: Query the web for answers.  
   - ▶️ **Summarise**: Summarise content from YouTube or web URLs.  
   - 💬 **Friendly Chat**: A simple, fun, and intuitive chat with AI.   
3. **Enjoy the Experience**: Interact through the chatbot interface.  



## 🛠️**Tech Stack**

- **Framework**: Streamlit  
- **AI Models**: Groq's Gemma, OpenAI GPT  
- **Tools**: LangChain for RAG pipelines and agents  
- **Vector Storage**: ChromaDB  
- **Document Processing**: PyPDFLoader  
- **Web Tools**: DuckDuckGo, Arxiv, and Wikipedia APIs

---

## ⬇️ **Installation**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Duygu-Jones/Rag-Agent-Chatbot
   cd Rag-Agent-Chatbot
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Add API Keys**  
   Create a `.env` file and add your API keys:  
   ```plaintext
   GROQ_API_KEY= "your_groq_api_key"
   OPENAI_API_KEY= "your_openai_api_key"
   ```

4. **Run the Application**  
   ```bash
   streamlit run ChatBot.py
   ```


## **Directory Structure**

```plaintext
MultiPage-AI-Chatbot/
│-- pages/
│   │-- Summarise_Web_YT.py    # Summarise YouTube & web content
│   │-- Web_Search_Agent.py    # Web search functionality
│   │-- PDF_QA_Assistant.py    # PDF Q&A assistant
│
│-- utils.py                   # Shared utility functions
│-- ChatBot.py                 # Main app entry point
│-- static/                    # CSS styles, images
│-- requirements.txt           # Project dependencies
│-- README.md                  # Project documentation
│-- .env                       # API key storage
```


## 🤝**Contributing**

Contributions are welcome!  
- Fork the repository  
- Create a new branch: `feature/your-feature`  
- Submit a pull request


---


## 🌱 About Me

I'm Duygu Jones, a Data Scientist passionate about Machine Learning and exploring Generative AI. 

You can learn more about me and my work at:
- **LinkedIn**: [Linkedin/duygujones](https://www.linkedin.com/in/duygujones/)
- **Website**: [duygujones.com](https://duygujones.vercel.app/)
- **Kaggle**: [kaggle.com/duygujones](https://www.kaggle.com/duygujones)
- **GitHub**: [github.com/Duygu-Jones](https://github.com/Duygu-Jones)
- **Medium**: [medium.com/@duygujones](https://medium.com/@duygujones)

Feel free to connect!

🎯 Expand your skills,<br>
💡 Share your insights,<br>
✨ And if you find this repository helpful, consider giving it a star. ⭐

Happy coding! 👩‍💻✨

---

##### 📜 License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
