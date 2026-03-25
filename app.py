import streamlit as st
from utils.detector import detect_known_issue, handle_known_issue
from ai_engine.analyzer import analyze_log

st.title("AI DevOps Debugging Assistant")

log_input = st.text_area("Enter logs here")

if st.button("Analyze"):
    if log_input:
        issue = detect_known_issue(log_input)

        if issue:
            st.subheader("Rule-Based Analysis")
            st.text(handle_known_issue(issue))
        else:
            st.subheader("AI Analysis")
            result = analyze_log(log_input)
            st.text(result)
    else:
        st.warning("Please enter logs")