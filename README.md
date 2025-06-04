# Conversation Analyzer 🎙️

A powerful AI-powered conversation analyzer that transcribes audio files, identifies speakers, generates summaries, and enables Q&A about the conversation content.

<img width="1440" alt="Screenshot 2025-06-04 at 2 01 43 PM" src="https://github.com/user-attachments/assets/4bce1889-441e-4ae8-be29-581fe114b295" />


## Features ✨

- **Audio Transcription**: Convert MP3/WAV audio files to text using AssemblyAI
- **Speaker Diarization**: Automatically identify and separate different speakers
- **Smart Speaker Identification**: AI-powered speaker name identification from conversation context
- **Conversation Summarization**: Generate comprehensive summaries of discussions
- **Interactive Q&A**: Ask questions about the conversation and get AI-powered answers
- **Modern UI**: Beautiful, responsive interface with dark theme and smooth animations

## Screenshots 📸

<img width="1359" alt="Screenshot 2025-06-04 at 2 04 48 PM" src="https://github.com/user-attachments/assets/f138d180-6c40-4dcd-95e6-9fedaa216481" />

<img width="1387" alt="Screenshot 2025-06-04 at 2 05 03 PM" src="https://github.com/user-attachments/assets/39eeb8e5-ff27-43e4-9a20-29e04f733e2c" />



## Installation 🚀

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/conversation-analyzer.git
   cd conversation-analyzer
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Streamlit (if not included):**
   ```bash
   pip install streamlit>=1.28.0
   ```

4. **Set up API keys:**
   - Get your AssemblyAI API key from [AssemblyAI](https://www.assemblyai.com/)
   - Get your WorqHat API key from [WorqHat](https://worqhat.com/)
   - Update the API keys in the code:
     ```python
     ASSEMBLYAI_API_KEY = "your_assemblyai_api_key"
     WORQHAT_API_KEY = "your_worqhat_api_key"
     ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Dependencies 📦

```txt
streamlit>=1.28.0
requests>=2.28.0
```

## App Usage 💡

### 1. Upload Audio File
- Drag and drop or browse to select your audio file
- Supported formats: MP3, WAV
- Maximum file size: As per AssemblyAI limits

### 2. Transcription Process
- File automatically uploads to AssemblyAI
- Real-time progress tracking
- Speaker diarization enabled by default

### 3. View Results in Tabs

#### 📝 **Transcript Tab**
- View original transcript with speaker labels (Speaker A, Speaker B, etc.)
- Click "Identify Speaker Names" to use AI for smart speaker identification
- Clean, readable format with speaker-specific styling

#### 🔍 **Analysis Tab**
- Generate comprehensive conversation summaries
- Key points, decisions, and action items highlighted
- Professional, neutral tone maintained

#### ❓ **Q&A Tab**
- Ask specific questions about the conversation
- AI-powered answers based solely on transcript content
- Cite relevant parts of the conversation

## API Integration 🔌

### AssemblyAI Features Used:
- Audio file upload and storage
- Speech-to-text transcription
- Speaker diarization
- Real-time status polling

### WorqHat AI Features Used:
- Speaker name identification from context
- Conversation summarization
- Question-answering capabilities
- JSON and text response formats

## Technical Architecture 🏗️

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   AssemblyAI     │    │    WorqHat      │
│   Frontend      │───▶│   Transcription  │───▶│   AI Analysis   │
│                 │    │   Service        │    │   Service       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ File Upload     │    │ Speaker          │    │ Summary &       │
│ Progress Track  │    │ Diarization      │    │ Q&A Generation  │
│ UI Components   │    │ Transcription    │    │ Speaker ID      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Use Cases 🎯

- **Meeting Transcription**: Convert recorded meetings to searchable text
- **Interview Analysis**: Analyze job interviews or research interviews
- **Podcast Processing**: Extract key insights from podcast episodes
- **Educational Content**: Process lectures and educational discussions
- **Customer Service**: Analyze customer support calls
- **Legal Documentation**: Transcribe depositions and legal proceedings

### Common Issues:

1. **API Key Errors**: Ensure your API keys are valid and have sufficient credits
2. **File Upload Failures**: Check file format (MP3/WAV) and size limits
3. **Transcription Timeout**: Large files may take longer; be patient during processing
4. **Speaker Identification Issues**: Works best when speakers mention each other's names

## Acknowledgments 🙏

- [AssemblyAI](https://www.assemblyai.com/) for powerful speech-to-text capabilities
- [WorqHat](https://worqhat.com/) for advanced AI analysis features  
- [Streamlit](https://streamlit.io/) for the amazing web app framework

**Made with ❤️ for better conversation analysis**
