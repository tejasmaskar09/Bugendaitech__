import streamlit as st
import UI
from function import filter_conversational_prompts,safe_prompt_filter,get_prompt_type,solve_basic_math_expression,solve_advanced_math_expression,solve_geometry_expression,get_age_based_prompt

from model_logic import initialize_gemini_model, generate_learning_content

# Sidebar
UI.display_sidebar_instructions()
selected_model = st.sidebar.selectbox("🧠 Choose Ollama Model", ["gemma:2b", "mistral"], index=0)

# Input
age, user_query = UI.setup_ui()
filtered_query = filter_conversational_prompts(user_query)
safe_query = safe_prompt_filter(filtered_query)

if safe_query.startswith("[BLOCKED"):
    UI.display_warning("⚠️ This input was blocked. Try rephrasing.")
    st.stop()

prompt_type = get_prompt_type(safe_query)

# Try solving math locally
if prompt_type == "math":
    for fn in [solve_geometry_expression, solve_basic_math_expression, solve_advanced_math_expression]:
        result = fn(safe_query)
        if result:
            UI.display_response(result)
            st.stop()

# Build prompt with accurate role & format
if prompt_type == "code":
    full_prompt = f"""
You are a skilled coding teacher.

TASK:
- Write only working code, no greetings.
- Add a 1-2 line explanation in plain language.
- Do not speculate. If unsure, say: "I am not sure."

USER TASK: {safe_query}
""".strip()

elif prompt_type == "factual":
    full_prompt = f"""
You are an expert academic answerer.

TASK:
- Give a precise one-line factual answer.
- No intros or definitions. Just the fact.
- If unknown or disputed, reply: "I do not know."

QUESTION: {safe_query}
""".strip()

elif prompt_type == "math":
    full_prompt = f"""
You are a top-tier math tutor.

TASK:
- Solve step-by-step using formulas.
- Avoid guesses or vague explanations.
- Always provide clear math notation.

PROBLEM: {safe_query}
""".strip()

else:  # concept
    age_prompt = get_age_based_prompt(age)
    full_prompt = f"""
{age_prompt}

TOPIC:
{safe_query}

RULES:
- Use clean headings and bullet points.
- No greetings or "As an AI" style talk.
- Examples only when helpful. Be crisp and clear.
""".strip()

# Generate response
model = initialize_gemini_model(selected_model)

if user_query:
    with st.spinner("Thinking..."):
        result = generate_learning_content(model, full_prompt)

    if result:
        UI.display_response(result)
        feedback = st.radio("📊 Was this explanation helpful?", ["👍 Yes", "👎 No"], index=None)

        if feedback == "👎 No":
            st.info("🔁 Improving explanation...")
            better_prompt = full_prompt + "\n\nRephrase this for more clarity, correct detail, and simpler explanation."
            with st.spinner("Updating..."):
                improved = generate_learning_content(model, better_prompt)
            UI.display_response(improved)

            # Ask again — fresh radio with no default
            feedback2 = st.radio("✅ Is this better now?", ["👍 Yes", "👎 No"], index=None)
            if feedback2 == "👎 No":
                st.warning("Sorry. Please try rewording your question for a clearer explanation.")
    else:
        UI.display_warning("⚠️ Sorry, no explanation was generated.")
