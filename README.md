
---

<h1 align="center">
🤖 MultiPage AI Chatbot
</h1>

<h3 align="center">
All-in-one AI assistant powered by LLMs, RAG pipelines, and agents for PDF Q&A, web search, and content summarization.
</h3>

---

## **Features**

- 🧑‍🏫 **PDF Q&A Assistant**: Upload PDFs and get accurate answers to your questions.  
- 🌐 **Web Search Agent**: Retrieve information from DuckDuckGo, Arxiv, and Wikipedia.  
- ▶️ **Content Summarizer**: Summarize YouTube videos and website text in seconds.  
- 💬 **Interactive Chat**: A user-friendly interface for seamless conversations.

---

## **Tech Stack**

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

---

## ♻️**Usage**

1. **Select an API & Model**: Enter API keys in the sidebar.  
2. **Navigate Between Pages**:  
   - 🧑‍🏫 **PDF Q&A**: Upload PDFs and ask questions.  
   - 🌐 **Web Search**: Query the web for answers.  
   - ▶️ **Summarize**: Summarize content from YouTube or web URLs. 
   - 💬 **Friendly Chat**: A simple, fun, and intuitive chat with ai. 
3. **Enjoy the Experience**: Interact through the chatbot interface.

---

## **Screenshots**

_(Add relevant screenshots showcasing the interface, sidebar, and key features.)_

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1080/1*nTHoUrFO1WIcovnwC3wS_Q.gif">
</p>

---

## **Directory Structure**

```plaintext
MultiPage-AI-Chatbot/
│-- pages/
│   │-- Summarize_Web_YT.py    # Summarize YouTube & web content
│   │-- Web_Search_Agent.py    # Web search functionality
│   │-- PDF_QA_Assistant.py    # PDF Q&A assistant
│
│-- utils.py                   # Shared utility functions
│-- ChatBot.py                     # Main app entry point
│-- static/                    # CSS styles, images
│-- requirements.txt           # Project dependencies
│-- README.md                  # Project documentation
│-- .env                       # API key storage
```

---

## 🤝**Contributing**

Contributions are welcome!  
- Fork the repository  
- Create a new branch: `feature/your-feature`  
- Submit a pull request

---


## 🌱 About Me

I'm Duygu Jones, a Data Scientist passionate about analyzing data and exploring machine learning. 

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
