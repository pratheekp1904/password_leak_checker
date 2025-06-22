import streamlit as st
import requests
import hashlib

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0

def pwned_api_check(password):
    sha1Password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1Password[:5], sha1Password[5:]
    response = request_api_data(first5)
    return get_password_leaks_count(response, tail)

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 8px 20px rgb(0 0 0 / 0.1);
    }
    .title {
        color: #8be144;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        font-size: 2.8rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #34495e;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result {
        font-family: 'Courier New', Courier, monospace;
        font-size: 1.1rem;
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 6px;
    }
    .safe {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .pwned {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    .footer {
        margin-top: 3rem;
        font-size: 0.8rem;
        color: #888;
        text-align: center;
        font-style: italic;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">Password Leak Checker 🔐</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Check if your password(s) have been exposed in data breaches.</div>', unsafe_allow_html=True)

passwords_input = st.text_area(
    "Enter one or multiple passwords separated by space or new lines:",
    height=130,
    placeholder="e.x.\npassword123 12345\nqwerty"
)

if st.button("Check Passwords"):
    if not passwords_input.strip():
        st.warning("Please enter at least one password.")
    else:
        passwords = passwords_input.split()

        for pwd in passwords:
            try:
                count = pwned_api_check(pwd)
            except Exception as e:
                st.error(f"Error checking password '{pwd}': {e}")
                continue

            if count > 0:
                st.markdown(
                    f'<div class="result pwned">"{pwd}" found <b>{count}</b> times in data breaches. <b>Change it!</b></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="result safe">"{pwd}" not found. No worries!</div>',
                    unsafe_allow_html=True
                )

st.markdown('<div class="footer">Data sourced from <a href="https://haveibeenpwned.com/API/v3#PwnedPasswords" target="_blank">Have I Been Pwned API</a></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
