#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from PIL import Image

# Load logo
logo = Image.open("nescan_logo.png")
st.image(logo, width=100)

# Custom CSS for black background, white text, and radio button styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .stRadio label {
        color: white !important;
    }
    .stRadio > div {
        border: 2px solid white;
        padding: 5px;
        border-radius: 5px;
    }
    .stRadio input[type="radio"] {
        accent-color: white;
    }
    .stHeader {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the 10 questions and their scale labels
questions = [
    {
        "text": "Q1: Alignment with Mission & Vision: How closely do the stakeholder's core mission, values, and strategic objectives align with NESCAN's vision for community climate action and a just transition?",
        "label_1": "Completely misaligned",
        "label_5": "Aligned",
        "label_10": "Perfectly aligned"
    },
    {
        "text": "Q2: Influence on Policy & Decisions: What is the stakeholder's capacity to directly influence or shape policy, project approvals, or key decisions within their sector or geographic area?",
        "label_1": "No influence",
        "label_5": "Moderately influential",
        "label_10": "Directly influences major decisions"
    },
    {
        "text": "Q3: Control of Critical Resources: To what extent does this stakeholder control financial resources (e.g., grant funding, sponsorship), skills, or in-kind assets that are essential for NESCAN's work?",
        "label_1": "No control",
        "label_5": "Controls some resources",
        "label_10": "Controls significant resources"
    },
    {
        "text": "Q4: Current Level of Engagement: How actively engaged is the stakeholder with NESCAN's activities, communications, or network? Is there an existing relationship that is active and mutually beneficial?",
        "label_1": "No prior contact",
        "label_5": "Occasional engagement",
        "label_10": "Engaged in regular, high-level interaction"
    },
    {
        "text": "Q5: Potential for Partnership & Collaboration: How strong is the opportunity for a high-impact collaboration or a new project with this stakeholder?",
        "label_1": "No potential",
        "label_5": "Moderate potential",
        "label_10": "Immediate, high-potential opportunities exist"
    },
    {
        "text": "Q6: Public Standing & Reputation: What is the stakeholder's ability to affect NESCAN's reputation, either positively or negatively, through their public influence and standing as a trusted partner?",
        "label_1": "No effect",
        "label_5": "Moderate effect",
        "label_10": "Significant positive or negative influence on public trust"
    },
    {
        "text": "Q7: Overlap of Services & Competitiveness: To what degree do this stakeholder's services or objectives complement NESCAN's, rather than compete for the same funding, members, or projects?",
        "label_1": "Direct competitor",
        "label_5": "Some overlap",
        "label_10": "Provides highly complementary, non-competitive services"
    },
    {
        "text": "Q8: Impact on Target Audience: How significant is this stakeholder's reach and influence over the communities, organizations, or individuals that NESCAN aims to serve or engage?",
        "label_1": "Minimal reach",
        "label_5": "Moderate reach",
        "label_10": "Influences a large portion of the target audience"
    },
    {
        "text": "Q9: Strategic Value to Future Goals: How critical is this stakeholder to achieving one or more of NESCAN's long-term strategic objectives, such as scaling a program, influencing policy, or securing major funding?",
        "label_1": "Not critical",
        "label_5": "Somewhat critical",
        "label_10": "Essential for long-term success"
    },
    {
        "text": "Q10: Internal Champions & Relationships: Is there a specific individual or department within the stakeholder organization that is a known champion or ally for NESCAN's work?",
        "label_1": "No known contact",
        "label_5": "Some contacts",
        "label_10": "Multiple high-level, internal champions"
    }
]

# Load organizations from Excel (skip header row)
@st.cache_data
def load_orgs():
    df = pd.read_excel("Organisations Name.xlsx", sheet_name="Stakeholders", header=None)
    orgs = df.iloc[1:, 0].dropna().tolist()  # Start from row 2, column A
    return orgs

# Main app
st.title("NESCAN Stakeholder Rating App")

# Session state initialization
if 'orgs' not in st.session_state:
    st.session_state.orgs = load_orgs()
    st.session_state.index = 0
    st.session_state.ratings = pd.DataFrame(columns=["Organization", "Rater"] + [q["text"] for q in questions])
    st.session_state.rater_name = ""

# Get rater's name with custom heading
if not st.session_state.rater_name:
    st.subheader("Stakeholder Management Prioritization")
    st.session_state.rater_name = st.text_input("Enter your name (to track who rated):")
    if st.session_state.rater_name:
        st.rerun()  # Refresh to proceed

if st.session_state.rater_name:
    total_orgs = len(st.session_state.orgs)
    current_index = st.session_state.index
    if current_index >= total_orgs:
        st.success("All organizations rated! Download your file below.")
    else:
        org = st.session_state.orgs[current_index]
        st.header(f"Rate: {org} ({current_index + 1}/{total_orgs})")
        st.progress((current_index + 1) / total_orgs)

        # Display radio buttons with custom labels
        ratings = {}
        for q in questions:
            st.subheader(q["text"])
            st.write(f"{q['label_1']} (1) ................................................ {q['label_5']} (5) ................................................ {q['label_10']} (10)")
            rating = st.radio(
                "",
                options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                key=f"radio_{q['text']}",
                horizontal=True
            )
            if rating is not None:  # Only store if a value is selected
                ratings[q["text"]] = rating

        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit & Next"):
                if ratings:  # Only save if at least one rating is provided
                    new_row = {"Organization": org, "Rater": st.session_state.rater_name, **ratings}
                    st.session_state.ratings = pd.concat([st.session_state.ratings, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    new_row = {"Organization": org, "Rater": st.session_state.rater_name, **{q["text"]: "Not rated" for q in questions}}
                    st.session_state.ratings = pd.concat([st.session_state.ratings, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state.index += 1
                st.rerun()
        with col2:
            if st.button("Skip"):
                new_row = {"Organization": org, "Rater": st.session_state.rater_name, **{q["text"]: "Skipped" for q in questions}}
                st.session_state.ratings = pd.concat([st.session_state.ratings, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state.index += 1
                st.rerun()

    # Export button (always available)
    if not st.session_state.ratings.empty:
        output_file = f"ratings_by_{st.session_state.rater_name}.xlsx"
        from io import BytesIO
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            st.session_state.ratings.to_excel(writer, index=False)
        st.download_button(
            label="Export Your Ratings as Excel",
            data=buffer.getvalue(),
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

