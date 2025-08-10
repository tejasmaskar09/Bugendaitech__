import streamlit as st
import re

def setup_ui():
    """Sets up the Streamlit interface and gets user input."""
    st.set_page_config(
        page_title="📘 Learn It Easy",
        page_icon="🎓",
        layout="centered"
    )

    st.markdown("""
        <h1 style='text-align: center; color: #CCCCCC; font-size: 38px;'>
            🌟 Personalized Learning Assistant 🌟
        </h1>
        <p style='text-align: center; font-size: 18px; color: #555555;'>
            Get simple, accurate explanations tailored to your age—just like a human teacher!
        </p>
    """, unsafe_allow_html=True)

    st.markdown("## 🧠 Let's Start Learning!")

    age = st.slider("👤 Select your age:", min_value=3, max_value=80, value=12)

    user_query = st.text_area(
        label="📘 What do you want to learn today?",
        placeholder="Type a topic or question here (e.g. 'Photosynthesis', 'What is gravity?')",
        height=100
    )

    st.markdown("---")
    return age, user_query


def display_sidebar_instructions():
    """Shows how to use the app in the sidebar."""
    st.sidebar.header("📝 How to Use")
    st.sidebar.markdown("""
    - 🧠 Select your **AI model** from the dropdown  
    - ✅ Ensure Ollama is running on `localhost:11434`  
    - 📌 Enter your **age** and **topic**  
    - 💡 Press **Ctrl + R** or click **Run** to start  
    """)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ using **Streamlit + Ollama**")


def display_response(content: str):
    """
    Displays the response from the model in a styled block.
    Handles code and explanation cleanly.
    """
    parts = re.split(r"(```.*?```)", content, flags=re.DOTALL)
    formatted = ""

    for part in parts:
        if part.startswith("``") and part.endswith("`` " \
        ""):
            code = part.strip("```").strip()
            formatted += f"<pre style='background:#f4f4f4; padding:12px; border-radius:6px; color:#222; font-size:15px'>{code}</pre>"
        else:
            # Format text nicely
            part = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", part)
            part = re.sub(r"^##\s+(.*)", r"<h3>\1</h3>", part, flags=re.MULTILINE)
            part = part.replace("\n", "<br>")
            formatted += f"<p style='margin: 6px 0;'>{part}</p>"

    st.markdown("## 📖 Your Personalized Explanation")
    st.markdown(f"""
        <div style='background-color: #f0f4f8; padding: 20px; border-radius: 10px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.05); font-size: 16px;
                    color: #333; line-height: 1.7'>
            {formatted}
        </div>
    """, unsafe_allow_html=True)


def display_warning(message: str):
    st.warning(message)

def display_error(message: str):
    st.error(message)

def display_info(message: str):
    st.info(message)

def show_spinner(text: str = "Thinking..."):
    return st.spinner(text)
