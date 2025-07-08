import streamlit as st
import re
import random
import string

# ---- Password Generator ----
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

# ---- Strength Checker ----
common_passwords = ['123456', 'password', 'qwerty', 'abc123', 'admin', 'letmein']

def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password too short (min 8 characters)")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add digits")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters")

    if password.lower() in common_passwords:
        feedback.append("Avoid common passwords")
    else:
        score += 1

    return score, feedback

# ---- Streamlit UI ----
st.set_page_config(page_title="Password Checker", layout="centered")
st.title("🔐 Password Strength Checker")

# Generate password
generated = None
if st.button("✨ Generate Strong Password"):
    generated = generate_password()
    st.success(f"Generated: `{generated}`")

# Input
password = st.text_input("Enter your password", value=generated if generated else "", type="password")

# Analysis
if password:
    score, feedback = check_strength(password)

    # Strength label and bar
    strength_labels = {
        0: "Very Weak 🔴",
        1: "Weak 🔴",
        2: "Below Average 🟠",
        3: "Moderate 🟡",
        4: "Good 🟢",
        5: "Strong 🟢",
        6: "Very Strong 💪🟢"
    }

    st.markdown("### 🔎 Strength Analysis")
    st.markdown(f"**Strength:** {strength_labels[score]}")
    st.progress(score / 6)

    st.markdown(f"**Score:** `{score}` out of 6")

    if feedback:
        st.markdown("#### 💡 Suggestions to Improve:")
        for tip in feedback:
            st.write("- " + tip)

