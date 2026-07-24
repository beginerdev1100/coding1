import ollama
import streamlit as st

messages = [
    {
        "role": "system",
        "content": (
            "You are a copy editor. You fix grammar, spelling, punctuation, and "
            "wording to make text read clearly and professionally.\n\n"
            "Rules:\n"
            "- Only fix grammar, spelling, punctuation, and phrasing.\n"
            "- Do NOT add any information, fact, or detail that is not already there.\n"
            "- Do NOT remove information.\n"
            "- Do NOT reorganize, restructure, summarize, or add headers or sections.\n"
            "- Keep the same order and the same meaning.\n"
            "- Do NOT add a diagnosis, assessment, plan, or any interpretation.\n"
            "- Do NOT explain what you changed.\n\n"
            "Output only the corrected text, nothing else.\n\n"
        ),
    }
]


def ui():
    prompt = st.chat_input("Say something")
    if prompt:
        st.write("Loading...")
        messages.append({"role": "user", "content": prompt})
        main(prompt)


def main(prompt):
    response = ollama.chat(
        model="mistral", messages=messages, options={"temperature": 0.0}
    )

    st.write(response["message"]["content"])


ui()
