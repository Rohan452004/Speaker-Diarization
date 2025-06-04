import streamlit as st
import requests
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

def get_api_keys():
    """
    Get API keys from various sources with fallback order:
    1. Try Streamlit secrets first (for production/Streamlit Cloud)
    2. Try environment variables (for local development with .env)
    3. Show error if no keys found
    """
    
    # Try Streamlit secrets first (for production deployment)
    try:
        assemblyai_key = st.secrets["api_keys"]["ASSEMBLYAI_API_KEY"]
        worqhat_key = st.secrets["api_keys"]["WORQHAT_API_KEY"]
        
        # Validate keys are not empty
        if assemblyai_key and worqhat_key:
            return assemblyai_key, worqhat_key, "streamlit_secrets"
    except (KeyError, FileNotFoundError, AttributeError):
        pass
    
    # Try environment variables (for local development)
    assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
    worqhat_key = os.getenv("WORQHAT_API_KEY")
    
    if assemblyai_key and worqhat_key:
        return assemblyai_key, worqhat_key, "environment_variables"
    
    # If no keys found, show comprehensive error message
    st.error("🚨 API keys not found!")
    
    st.markdown("""
    ### Please configure your API keys using one of these methods:
    
    #### 🔧 For Local Development:
    1. **Create a `.env` file** in your project root:
    ```bash
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
    WORQHAT_API_KEY=your_worqhat_api_key_here
    ```
    
    2. **Or set environment variables** in your terminal:
    ```bash
    export ASSEMBLYAI_API_KEY="your_assemblyai_api_key_here"
    export WORQHAT_API_KEY="your_worqhat_api_key_here"
    ```
    
    #### ☁️ For Streamlit Cloud (Production):
    1. Go to your **Streamlit app settings**
    2. Navigate to the **"Secrets"** section  
    3. Add your keys in **TOML format**:
    ```toml
    [api_keys]
    ASSEMBLYAI_API_KEY = "your_assemblyai_api_key_here"
    WORQHAT_API_KEY = "your_worqhat_api_key_here"
    ```
    
    #### 🔑 How to get API keys:
    - **AssemblyAI**: Sign up at [assemblyai.com](https://www.assemblyai.com/)
    - **WorqHat**: Sign up at [worqhat.com](https://worqhat.com/)
    """)
    
    st.stop()

# Get API keys using the hybrid approach
ASSEMBLYAI_API_KEY, WORQHAT_API_KEY, source = get_api_keys()


# === Custom CSS for modern UI ===
st.set_page_config(
    page_title="Conversation Analyzer",
    page_icon="🎙️",
    layout="wide",
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1f1f1f, #3a3a3a, #0f2027, #203a43, #2c5364);
        color: white;
    }

    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: blue !important;
        color: white !important;
        border: none !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
    }
    .stSpinner>div {
        border-color: #007bff;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .transcript-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .speaker-text {
        margin: 10px 0;
        padding: 10px;
        border-radius: 5px;
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        color: black;
    }
    h1, h2, h3 {
        color: #1a1a1a;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        width: 100px;
        white-space: pre-wrap;
        background-color: #f8f9fa;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 10px;
        padding-right: 10px;
        color: blue;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def identify_speaker_names(utterances):
    url = "https://api.worqhat.com/api/ai/content/v4"
    
    training_prompt = """
    You are an expert speaker diarizer. Your task is to identify the correct speaker names for each dialogue turn in the conversation, using clues in the language (e.g., if they mention each other by name). Return the labeled conversation in the correct sequence.

    You will be given a list of utterances, like this:
    [
      {"Speaker A": "Hi Jamie, how's your day?"},
      {"Speaker B": "Hey Alex, going well. Just prepping for the test."}
    ]

    From the speech, infer who the speakers are (if names are mentioned), or label them as 'Unknown' if not clear. Do not guess names that aren't present in the dialogue.

    Respond in this exact JSON format:
    [
      {
        "speaker": "<Identified Name or 'Unknown'>",
        "text": "<Dialogue text>"
      },
      ...
    ]
    """

    payload = {
        "question": f"Given this conversation, identify speaker names from their dialogue: {utterances}",
        "model": "aicon-v4-nano-160824",
        "randomness": 0.5,
        "stream_data": False,
        "training_data": training_prompt,
        "response_type": "json",
        "conversation_id": "conv_1724236791746",
    }

    headers = {
        "Authorization": f"Bearer {WORQHAT_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = json.loads(response.text)
    
    # Parse and format the response
    raw_text = json.loads(data['content'])
    formatted = []
    for entry in raw_text:
        speaker = entry['speaker']
        text = entry['text']
        formatted.append({
            "speaker": speaker,
            "text": text.strip()
        })
    
    return formatted

# === Main UI ===
st.markdown("<h1 style='text-align: center; color: white;'>🎙️ Conversation Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Upload an audio file to transcribe and analyze conversations</p>", unsafe_allow_html=True)

# Create two columns for the upload section
col1, col2, col3 = st.columns([1,2,1])
with col2:
    uploaded_file = st.file_uploader("", type=["mp3", "wav"], help="Upload an audio file (.mp3, .wav)")

if uploaded_file:
    with st.spinner("Uploading file to AssemblyAI..."):
        headers = {
            "authorization": ASSEMBLYAI_API_KEY,
            "content-type": "application/octet-stream"
        }
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, data=uploaded_file)
        upload_url = response.json()["upload_url"]

    st.markdown("<div class='success-message'>✅ File uploaded successfully!</div>", unsafe_allow_html=True)

    # === Request Transcription ===
    with st.spinner("Sending file for transcription..."):
        json_data = {
            "audio_url": upload_url,
            "speaker_labels": True
        }
        transcription_headers = {
            "authorization": ASSEMBLYAI_API_KEY,
            "content-type": "application/json"
        }
        response = requests.post("https://api.assemblyai.com/v2/transcript", json=json_data, headers=transcription_headers)
        transcript_id = response.json()["id"]

    # === Poll for Completion ===
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    status = "queued"
    progress = 0

    while status not in ["completed", "error"]:
        time.sleep(10)
        polling_response = requests.get(polling_endpoint, headers=transcription_headers)
        status = polling_response.json()['status']
        progress = min(progress + 10, 90)
        progress_bar.progress(progress)
        status_text.text(f"Status: {status}")

    if status == "completed":
        progress_bar.progress(100)
        st.markdown("<div class='success-message'>✅ Transcription completed!</div>", unsafe_allow_html=True)
        transcript_data = polling_response.json()
        utterances = transcript_data.get("utterances", [])

        # Format transcript for summary and Q&A
        formatted_conversation = [
            {"speaker": entry['speaker'], "text": entry['text']}
            for entry in utterances
        ]

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📝 Transcript", "🔍 Analysis", "❓ Q&A"])

        with tab1:
            st.markdown("<h2 style='color: white;'>Original Transcript</h2>", unsafe_allow_html=True)
            st.markdown("<div class='transcript-box'>", unsafe_allow_html=True)
            for entry in formatted_conversation:
                st.markdown(f"""
                    <div class='speaker-text'>
                        <strong>{entry['speaker']}</strong>: {entry['text']}
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("Identify Speaker Names", key="identify_names"):
                with st.spinner("Identifying speaker names..."):
                    identified_speakers = identify_speaker_names(formatted_conversation)
                    
                    st.markdown("<h2 style='color: white;'>Transcript with Identified Speakers</h2>", unsafe_allow_html=True)
                    st.markdown("<div class='transcript-box'>", unsafe_allow_html=True)
                    for entry in identified_speakers:
                        st.markdown(f"""
                            <div class='speaker-text'>
                                <strong>{entry['speaker']}</strong>: {entry['text']}
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<h2 style='color: white;'>Conversation Summary</h2>", unsafe_allow_html=True)
            if st.button("Generate Summary", key="generate_summary"):
                with st.spinner("Generating summary with WorqHat..."):
                    summary_prompt = """
                    You are an expert at summarizing conversations. Your task is to create a concise yet comprehensive summary
                    of the conversation provided. Focus on key points, decisions, action items, and important information.

                    The summary should:
                    1. Be approximately 2-3 paragraphs
                    2. Highlight the main topics discussed
                    3. Note any decisions made or conclusions reached
                    4. Identify any action items or follow-ups mentioned
                    5. Maintain a neutral, professional tone

                    Please provide only the summary without additional commentary.
                    """

                    conversation_text = ""
                    for entry in formatted_conversation:
                        conversation_text += f"{entry['speaker']}: {entry['text']}\n\n"

                    payload = {
                        "question": f"Please summarize the following conversation:\n\n{conversation_text}",
                        "model": "aicon-v4-nano-160824",
                        "randomness": 0.3,
                        "stream_data": False,
                        "training_data": summary_prompt,
                        "response_type": "text",
                        "conversation_id": "conv_12345"
                    }

                    headers = {
                        "Authorization": f"Bearer {WORQHAT_API_KEY}",
                        "Content-Type": "application/json"
                    }

                    response = requests.post("https://api.worqhat.com/api/ai/content/v4", json=payload, headers=headers)
                    try:
                        summary = json.loads(response.text)['content']
                        st.markdown("<div class='transcript-box'>", unsafe_allow_html=True)
                        st.write(summary)
                        st.markdown("</div>", unsafe_allow_html=True)
                    except:
                        st.error("Failed to generate summary.")

        with tab3:
            st.markdown("<h2 style='color: white;'>Ask Questions About the Conversation</h2>", unsafe_allow_html=True)
            user_question = st.text_input("Enter your question here", key="question_input")
            
            if user_question:
                with st.spinner("Fetching answer..."):
                    qa_prompt = """
                    You are an AI assistant specialized in answering questions about meeting transcripts.
                    You have access to a meeting conversation transcript, and your task is to answer questions
                    about the content of this meeting accurately and concisely.

                    When answering:
                    1. Only use information explicitly mentioned in the transcript
                    2. If the answer isn't in the transcript, say "I don't have enough information from the transcript to answer this question"
                    3. Cite the relevant parts of the conversation by mentioning the speaker when appropriate
                    4. Keep answers concise but complete
                    5. Maintain a helpful, professional tone

                    Answer the question based solely on the conversation provided.
                    """

                    conversation_text = ""
                    for entry in formatted_conversation:
                        conversation_text += f"{entry['speaker']}: {entry['text']}\n\n"

                    payload = {
                        "question": f"""Based on the following conversation transcript, please answer this question: "{user_question}"\n\nTranscript:\n{conversation_text}""",
                        "model": "aicon-v4-nano-160824",
                        "randomness": 0.2,
                        "stream_data": False,
                        "training_data": qa_prompt,
                        "response_type": "text",
                        "conversation_id": "conv_12345"
                    }

                    headers = {
                        "Authorization": f"Bearer {WORQHAT_API_KEY}",
                        "Content-Type": "application/json"
                    }

                    response = requests.post("https://api.worqhat.com/api/ai/content/v4", json=payload, headers=headers)
                    try:
                        answer = json.loads(response.text)['content']
                        st.markdown("<div class='transcript-box'>", unsafe_allow_html=True)
                        st.write(f"**Answer:** {answer}")
                        st.markdown("</div>", unsafe_allow_html=True)
                    except:
                        st.error("Failed to get answer from WorqHat.")

    elif status == "error":
        st.error("Transcription failed. Please try again.")