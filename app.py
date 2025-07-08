import streamlit as st
import re
import random
import string
import math
import hashlib
import requests


# ---- Password Generator ----
def generate_password(length=12, upper=True, lower=True, digits=True, special=True):
    pool = ''
    if upper:
        pool += string.ascii_uppercase
    if lower:
        pool += string.ascii_lowercase
    if digits:
        pool += string.digits
    if special:
        pool += "!@#$%^&*()"

    if not pool:
        return "Choose at least one character type!"

    return ''.join(random.choice(pool) for _ in range(length))

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

def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"\d", password): charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): charset += 32
    entropy = len(password) * math.log2(charset) if charset > 0 else 0
    return round(entropy, 2)

def check_pwned_api(password):
       sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
       prefix = sha1[:5]
       suffix = sha1[5:]
   
       url = f"https://api.pwnedpasswords.com/range/{prefix}"
       res = requests.get(url)
   
       if res.status_code != 200:
           return None  # API down
   
       hashes = (line.split(':') for line in res.text.splitlines())
       for h, count in hashes:
           if h == suffix:
               return int(count)
   
       return 0

# ---- Streamlit UI ----
st.set_page_config(page_title="Password Checker", page_icon="🔐", layout="centered")
st.title("🔐 Password Strength Checker")

st.markdown("---")

st.markdown("### Customize Password Generator")
col1, col2 = st.columns(2)
with col1:
    length = st.slider("Password Length", 6, 32, 12)
with col2:
    use_upper = st.checkbox("Include Uppercase", True)
    use_lower = st.checkbox("Include Lowercase", True)
    use_digits = st.checkbox("Include Digits", True)
    use_special = st.checkbox("Include Special Characters", True)

generated = None
if st.button("✨ Generate Password"):
    generated = generate_password(length, use_upper, use_lower, use_digits, use_special)

    if "history" not in st.session_state:
        st.session_state.history = []

    if generated:
       st.session_state.history.append(generated)

    if st.session_state.history:
       st.markdown("#### 🕓 Recent Passwords")
       for p in reversed(st.session_state.history[-5:]):
           st.code(p, language="text")

    st.success(f"Generated Password: `{generated}`")
    st.download_button("📥 Download Password", generated, file_name="password.txt")



password = st.text_input("🔑 Enter your password to check", value=generated if generated else "", type="password")

if password:


    breach_count = check_pwned_api(password)
    if breach_count is None:
        st.warning("⚠️ Couldn't check breach status (API issue).")
    elif breach_count > 0:
        st.error(f"🚨 This password has been found in {breach_count:,} data breaches. Avoid using it.")
    else:
        st.success("✅ This password has **not** been found in known breaches.")
    
        score, feedback = check_strength(password)
        entropy = calculate_entropy(password)
    
        strength_labels = {
            0: "Very Weak 🔴",
            1: "Weak 🔴",
            2: "Below Average 🟠",
            3: "Moderate 🟡",
            4: "Good 🟢",
            5: "Strong 🟢",
            6: "Very Strong 💪🟢"
        }
    
        st.markdown("---")
        st.markdown("###  Strength Analysis")
        st.markdown(f"**Strength:** {strength_labels[score]}")
        st.progress(score / 6)
        st.markdown(f"**Score:** `{score}` out of 6")
        st.markdown(f"**Entropy:** `{entropy}` bits")
    
        if feedback:
            st.markdown("#### 📌 Suggestions to Improve:")
            for tip in feedback:
                st.write("- " + tip)