# Smart Email Assistant

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://8suxjtt72jrfzgsbmnapp9y.streamlit.app/)

An intelligent email analysis tool that helps you understand and interact with your Gmail inbox using AI. Securely analyzes your last 5 emails through natural language conversations.

## Features

- 🔒 Secure Gmail integration using App Passwords
- ✨ AI-powered email summarization
- 💬 Natural language Q&A about email content
- 📝 Conversation memory for contextual interactions
- ⚡ Real-time processing with Groq's Llama-3-8b
- 🔄 Automatic retrieval of last 5 emails

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/InboxMind.git
cd InboxMind
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Create `.streamlit/secrets.toml` with:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. **Run the application**
```bash
streamlit run app.py
```

## Configuration

1. **Gmail Setup**
- Enable IMAP access in your [Google Account Settings](https://myaccount.google.com/security)
- Create an App Password:
  1. Go to Google Account → Security
  2. Under "Signing in to Google," enable 2-Step Verification
  3. Create App Password (Select "Other" as device type)

2. **API Key**
- Get your Groq API key from [console.groq.com](https://console.groq.com/keys)

## Usage

1. **Launch the app**
```bash
streamlit run app.py
```

2. **Enter credentials**
- Gmail address (e.g., user@gmail.com)
- App Password (16-digit code from Google)

3. **Interact with your emails**
Example queries:
- "Summarize my emails"
- "What's the latest from Amazon?"
- "Find any important deadlines"
- "Show me shipping updates"

## Technical Stack

- **Frontend**: Streamlit
- **AI Backend**: Groq (Llama-3-8b)
- **Email Processing**: Imaplib
- **Memory Management**: LangChain
- **Security**: Google App Passwords

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Disclaimer

- This application only accesses your last 5 emails
- No credentials are stored after session ends
- Always use App Passwords instead of real Gmail passwords
- Email content is processed temporarily in memory

## Acknowledgments

- [Groq](https://groq.com/) for the lightning-fast LLM API
- [Streamlit](https://streamlit.io/) for the web framework
- Google for the Gmail integration capabilities
