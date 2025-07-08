🔐 Password Strength Analyzer
A sleek, interactive password strength analyzer built using Python + Streamlit.

This tool helps users generate strong passwords, evaluate their strength, calculate entropy, and even check if they’ve been compromised in real-world data breaches using the HaveIBeenPwned API.

Live Demo 👉 [Streamlit App](https://pass-strength-bfacmapjdurs8vgee3j85y.streamlit.app/)

✨ Features
 Generate secure passwords with customizable options (length, character types)

 Analyze password strength with a 6-point scoring system

 View entropy (randomness) in bits

Real-time feedback with suggestions to improve

Checks if your password has been compromised in data breaches

 Copy-to-clipboard button

 Download generated password as .txt

 View recent password history (session-based)

 Clean layout with sectioned design and error-free widget handling

📸 Preview
(Add a screenshot if possible)
You can drag and drop a PNG image of the UI directly into this section after uploading it.

How to Run Locally
bash
Copy code
git clone https://github.com/your-username/password-checker.git
cd password-checker
pip install -r requirements.txt
streamlit run app.py
Requires Python 3.8+

🧪 Tech Stack
Python

Streamlit

requests (for API calls)

re, math, hashlib (for password analysis logic)

GitHub + Streamlit Cloud (deployment)

💡 Why This Project?
This app was built to demonstrate:

Real-world UX thinking in password generation

Data privacy awareness (via breach detection)

Scoring, entropy logic, and security best practices

A polished Streamlit UI with interactivity and personalization

