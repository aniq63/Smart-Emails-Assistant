# app.py
import os
import streamlit as st
import imaplib
import email
from email.policy import default
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_groq.chat_models import ChatGroq

# App configuration
st.set_page_config(
    page_title="InboxMind - AI Email Assistant",
    page_icon="✉️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean interface
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
    }
    .stChatInput input {
        background-color: #f8f9fa !important;
    }
    .st-bd {
        background-color: #f8f9fa !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("✉️ InboxMind - Your AI Email Assistant")
    st.caption("Securely analyze your Gmail inbox with AI | Last 5 emails only")

    # Initialize session state
    if 'emails' not in st.session_state:
        st.session_state.emails = None
    if 'chain' not in st.session_state:
        st.session_state.chain = None

    # Login form
    with st.form("gmail_auth"):
        email_user = st.text_input("Gmail Address", placeholder="user@gmail.com")
        app_password = st.text_input("App Password", type="password", 
                                   help="Create in Google Account → Security → App Passwords")
        submitted = st.form_submit_button("Connect to Gmail 🔒")
        
        if submitted:
            with st.spinner("Securely accessing your inbox..."):
                try:
                    # Original email fetching logic
                    mail = imaplib.IMAP4_SSL("imap.gmail.com")
                    mail.login(email_user, app_password)
                    mail.select("inbox")

                    status, data = mail.search(None, "ALL")
                    email_ids = data[0].split()[-5:]  # Last 5 emails

                    email_container = []
                    for e_id in email_ids:
                        status, data = mail.fetch(e_id, "(RFC822)")
                        raw_email = data[0][1]
                        msg = email.message_from_bytes(raw_email, policy=default)

                        # Your original email processing logic
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))

                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body += part.get_content()
                        else:
                            body = msg.get_content()

                        email_container.append({
                            "from": msg['from'],
                            "subject": msg['subject'],
                            "body": body[:500] + "..." if len(body) > 500 else body  # Your truncation logic
                        })

                    st.session_state.emails = email_container
                    st.success(f"Connected! Analyzed {len(email_container)} recent emails")

                    # Initialize LLM with your original settings
                    llm = ChatGroq(
                        model_name="llama3-8b-8192",
                        temperature=0.2,
                        api_key=os.getenv("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")
                    )

                    # Your original system message creation
                    def create_system_message(emails):
                        formatted_emails = "\n".join([
                            f"EMAIL #{idx}:\nFROM: {e['from']}\nSUBJECT: {e['subject']}\nBODY:\n{e['body']}\n"
                            f"----------------------------------------"
                            for idx, e in enumerate(emails, 1)
                        ])

                        return f"""You are a professional Gmail summarization assistant. Your task is to help users understand and interact with their emails.

The user has {len(emails)} emails in their inbox. Here they are:

{formatted_emails}

BASIC INSTRUCTIONS:
1. When asked to summarize emails, you MUST summarize ALL {len(emails)} emails
2. Number your summaries from 1 to {len(emails)}
3. Be concise but informative
4. The email you summarize is in a form paragraphs and bullet points
5. For specific questions about emails, provide accurate answers based only on the email content

If asked about information not in these emails, respond with:
"I don't see that information in your retrieved emails."

Format your summaries as:
1. From: [sender]
   Subject: [subject]
   Summary: [brief summary of key points]

2. From: [sender]
   Subject: [subject]
   Summary: [brief summary of key points]
                        """

                    # Your original chain creation logic
                    memory = ConversationBufferMemory(
                        memory_key="chat_history",
                        return_messages=True,
                        output_key="answer"
                    )

                    prompt = ChatPromptTemplate.from_messages([
                        ("system", create_system_message(email_container)),
                        MessagesPlaceholder(variable_name="chat_history"),
                        ("human", "{question}")
                    ])

                    st.session_state.chain = LLMChain(
                        llm=llm,
                        prompt=prompt,
                        memory=memory,
                        output_key="answer",
                        verbose=False
                    )

                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")

    # Chat interface
    if st.session_state.emails:
        st.subheader("Email Analysis Chat")
        st.info("Ask me to summarize emails or ask specific questions about their content!")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "I've analyzed your last 5 emails. How can I help?"
            })

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Process user input
        if prompt := st.chat_input("Ask about your emails..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = st.session_state.chain({"question": prompt})["answer"]
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
