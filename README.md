# Manhua Translator Bot

Manhua Translator Bot is a smart Streamlit application that translates speech bubbles in manhua panels into fluent English—making your favorite stories accessible across languages. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and DeepSeek, the bot extracts original dialogue from comic images and delivers clear, tone-aware translations with optional word-level footnotes.

## 📁 Folder Structure

```
Manhua-Translator-Bot/
├── manhua-translator-bot.py
├── README.md
└── requirements.txt
```

- **manhua-translator-bot.py**: The main Streamlit application.
- **requirements.txt**: Required Python packages.
- **README.md**: This documentation file.

## ✨ Features

- **Image Upload & Preferences Input**  
  Upload any manhua or manga panel image and choose your preferred translation tone and footnote setting.

- **Dialogue Extraction**  
  The Speech Bubble Extractor agent identifies and extracts dialogue from top to bottom inside speech bubbles—regardless of whether it's in Chinese, Japanese, Korean, or another language.

- **AI-Powered Translation**  
  The Manhua Dialogue Translator agent converts dialogue into fluent English based on your tone preference and can optionally generate word-level footnotes for deeper understanding.

- **Structured Markdown Output**  
  Translations are returned in a clean format: numbered by speech bubble and styled with Markdown headings for easy readability.

- **Download Option**  
  Save the translated dialogue to a `.txt` file for later reading or sharing.

- **Clean Streamlit UI**  
  Built with Streamlit to ensure an intuitive, responsive, and distraction-free user experience.

## 🧩 Prerequisites

- Python 3.11 or higher  
- An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))  
- A DeepSeek API key ([Get one here](https://platform.deepseek.com/api_keys))

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akash301191/Manhua-Translator-Bot.git
   cd Manhua-Translator-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🧪 Usage

1. **Run the app**:
   ```bash
   streamlit run manhua-translator-bot.py
   ```

2. **In your browser**:
   - Enter your OpenAI and DeepSeek API keys in the sidebar.
   - Upload a manhua image and select your translation tone and footnote preferences.
   - Click **🌐 Translate Manhua**.
   - View the translated bubbles and optional glossary.
   - Use the **📥 Download Translation** button to save the result.

## 🔍 Code Overview

- **`render_translation_preferences()`**: Captures image upload and translation settings like tone and footnote inclusion.
- **`render_sidebar()`**: Stores and manages OpenAI and DeepSeek API keys in Streamlit session state.
- **`generate_translations()`**:  
  - Uses the `Speech Bubble Extractor` agent to extract multilingual dialogue.  
  - Feeds extracted content into the `Manhua Dialogue Translator` agent for tone-aware English translation.  
  - Formats the final output in a Markdown-friendly layout with optional footnotes.
- **`main()`**: Sets up the page layout, handles user interactions, and displays the translation results.

## 🤝 Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Make sure your changes are clean, purposeful, and align with the app’s goals.