import tempfile
import streamlit as st

from agno.agent import Agent
from agno.media import Image
from agno.models.openai import OpenAIChat
from agno.models.deepseek import DeepSeek

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # DeepSeek API Key input
    deepseek_api_key = st.sidebar.text_input(
        "DeepSeek API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.deepseek.com/api_keys)."
    )
    if deepseek_api_key:
        st.session_state.deepseek_api_key = deepseek_api_key
        st.sidebar.success("✅ DeepSeek API key updated!")

    st.sidebar.markdown("---")

def render_translation_preferences():
    col1, col2 = st.columns(2)

    # Column 1: Image Upload
    with col1:
        st.subheader("🖼️ Upload Manhua Panel")
        uploaded_image = st.file_uploader(
            "Choose a manhua image",
            type=["jpg", "jpeg", "png"]
        )

    # Column 2: Translation Preferences
    with col2:
        st.subheader("🗣️ Translation Preferences")
        translation_tone = st.selectbox(
            "How should the translated dialogue sound?",
            ["Neutral and clear", "Casual and friendly", "Formal and respectful", "Playful and expressive", "Dramatic or emotional"]
        )

        include_word_notes = st.radio(
            "Include individual word translations as footnotes?",
            ["Yes", "No"],
            index=1,
            horizontal=True
        )


    return {
        "uploaded_image": uploaded_image,
        "translation_tone": translation_tone,
        "include_word_notes": include_word_notes,
        "output_format": "Bubble-wise Breakdown"
    }

def generate_translations(preferences):
    image_path = preferences["uploaded_image"]

    # === Step 1: Create the Bubble Extractor Agent ===
    bubble_extractor_agent = Agent(
        model=OpenAIChat(id="gpt-4o", api_key=st.session_state.openai_api_key),
        name="Speech Bubble Extractor",
        role="Extracts original dialogue from manhua or manga speech bubbles in top-to-bottom order.",
        description=(
            "You're a panel reading specialist trained to identify and extract dialogue text "
            "from speech bubbles in comic or manhua images, regardless of the language."
        ),
        instructions=[
            "Extract only the text that appears **inside speech bubbles** in the image.",
            "Do not extract sound effects, narration, signs, or decorative text outside bubbles.",
            "The dialogue may be in Chinese, Korean, Japanese, or any other language—preserve it as is.",
            "List the extracted text as follows, in top-to-bottom order:\n\n"
            "**Bubble 1**: <original dialogue>\n"
            "**Bubble 2**: <original dialogue>\n"
            "...and so on.",
            "Do not translate, rewrite, or explain anything—just extract and format cleanly."
        ],
        markdown=True
    )

    # === Step 2: Run the extractor agent ===
    extraction_response = bubble_extractor_agent.run(
        "Extract the texts from speech bubbles in the image.",
        images=[Image(filepath=image_path)]
    )
    extracted_bubbles = extraction_response.content

    # === Step 3: Prepare Translation Agent ===
    translator_agent = Agent(
        model=DeepSeek(api_key=st.session_state.deepseek_api_key),
        markdown=True,
        name="Manhua Dialogue Translator",
        role="Translates multi-language comic dialogue into fluent English with an optional word-level glossary.",
        description="You're a multilingual comic translator. Your goal is to translate each speech bubble into fluent English, preserving the tone and providing a clean, readable output."
    )

    # === Step 4: Construct Prompt Based on Preferences ===
    tone = preferences["translation_tone"]
    include_notes = preferences["include_word_notes"]

    if include_notes == "Yes":
        footnote_instruction = """
Include a footnotes section after the translated bubbles, titled '📘 Footnotes'. 
List important or culturally significant word-level translations as follows:

## 📘 Footnotes
Glossary of selected word-level translations:

1. **<Original Word>** — <English Meaning>
2. **<Original Word>** — <English Meaning>
"""
    else:
        footnote_instruction = "Do not include any footnotes or word-by-word translations."

    translation_prompt = f"""
You are given dialogue from a manhua page, extracted in top-to-bottom speech bubble order. Your task is to translate each bubble into fluent English with a **{tone.lower()}** tone.

Respond in the following format:

## 🈂️ Translation
Below are the dialogue translations organized in the order of speech bubbles from top to bottom:

**Bubble 1**: <English translation>  
**Bubble 2**: <English translation>  

{footnote_instruction}

Here is the dialogue to translate:
{extracted_bubbles}
"""

    # === Step 5: Run the translator agent ===
    translator_response = translator_agent.run(translation_prompt.strip())
    translation_content = translator_response.content

    return translation_content

def main() -> None:
    # Page config
    st.set_page_config(page_title="Manhua Translator Bot", page_icon="📚", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>📚 Manhua Translator Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Manhua Translator Bot — a smart Streamlit application that translates speech bubbles in manhua panels into fluent English, making your favorite stories accessible across languages.",
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Sidebar + user preferences
    render_sidebar()
    translation_preferences = render_translation_preferences()

    st.markdown("---")

    # Translation Trigger Button
    if st.button("🌐 Translate Manhua Panel"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "deepseek_api_key"):
            st.error("Please provide your DeepSeek API key in the sidebar.")
        elif not translation_preferences["uploaded_image"]:
            st.error("Please upload an image to proceed.")
        else:
            with st.spinner("Translating dialogue from your panel..."):
                # Save image to temporary path
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    tmp.write(translation_preferences["uploaded_image"].getvalue())
                    image_path = tmp.name

                # Patch filepath into preferences
                translation_preferences["uploaded_image"] = image_path

                # Generate translation
                translation = generate_translations(translation_preferences)

                # Store results in session state
                st.session_state.translation = translation
                st.session_state.uploaded_image = translation_preferences["uploaded_image"]

    # Display Result if available
    if "translation" in st.session_state and "uploaded_image" in st.session_state:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("## 🖼️ Uploaded Image")
            st.image(st.session_state.uploaded_image, use_container_width=False)

        with col2:
            st.markdown(st.session_state.translation, unsafe_allow_html=True)

        st.markdown("---")

        st.download_button(
            label="📥 Download Translation",
            data=st.session_state.translation,
            file_name="translated_dialogue.txt",
            mime="text/plain"
        )

if __name__ == "__main__": 
    main()