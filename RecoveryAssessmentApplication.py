import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Recovery Progress Assessment",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stSlider {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .metric-label {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .description {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Assessment areas
assessment_areas = [
    {"id": 1, "title": "Follow-up Care", "description": "Regularly attending healthcare appointments"},
    {"id": 2, "title": "Aftercare Programs", "description": "Participation in support groups and therapy"},
    {"id": 3, "title": "Self-Care", "description": "Maintaining physical and emotional well-being"},
    {"id": 4, "title": "Medication Management", "description": "Following prescribed medication schedules"},
    {"id": 5, "title": "Trigger Management", "description": "Identifying and coping with triggers"},
    {"id": 6, "title": "Support Network", "description": "Building and maintaining supportive relationships"},
    {"id": 7, "title": "Mindfulness Practice", "description": "Engaging in present-moment awareness"},
    {"id": 8, "title": "Goal Achievement", "description": "Setting and working towards recovery goals"},
    {"id": 9, "title": "Progress Monitoring", "description": "Tracking and celebrating recovery milestones"},
    {"id": 10, "title": "Patient Perseverance", "description": "Maintaining commitment through challenges"}
]

def get_color(value):
    if value <= 3:
        return "🔴 Needs Attention"
    elif value <= 6:
        return "🟡 Making Progress"
    else:
        return "🟢 Strong"

def main():
    st.title("Recovery Progress Assessment")
    st.markdown("Track your progress across different areas of recovery")

    # Initialize session state for storing values
    if 'assessment_values' not in st.session_state:
        st.session_state.assessment_values = {area['id']: 5 for area in assessment_areas}
    
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Self-Assessment")
        # Create sliders for each assessment area
        for area in assessment_areas:
            st.markdown(f"### {area['title']}")
            st.markdown(f"<p class='description'>{area['description']}</p>", unsafe_allow_html=True)
            value = st.slider(
                "Rate your progress (0-10)",
                min_value=0,
                max_value=10,
                value=st.session_state.assessment_values[area['id']],
                key=f"slider_{area['id']}"
            )
            st.session_state.assessment_values[area['id']] = value
            st.markdown(f"**Status:** {get_color(value)}")
            st.markdown("---")

    with col2:
        st.subheader("Summary")
        
        # Create radar chart of current values
        df = pd.DataFrame({
            'Area': [area['title'] for area in assessment_areas],
            'Score': [st.session_state.assessment_values[area['id']] for area in assessment_areas]
        })
        
        fig = px.line_polar(
            df,
            r='Score',
            theta='Area',
            line_close=True,
            range_r=[0,10],
            markers=True
        )
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            )
        )
        st.plotly_chart(fig)

        # Save assessment button
        if st.button("Save Current Assessment"):
            current_assessment = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'values': st.session_state.assessment_values.copy()
            }
            st.session_state.history.append(current_assessment)
            st.success("Assessment saved!")

        # Show history if available
        if st.session_state.history:
            st.subheader("History")
            for i, assessment in enumerate(reversed(st.session_state.history[-5:])):
                with st.expander(f"Assessment {assessment['timestamp']}"):
                    for area in assessment_areas:
                        st.write(f"{area['title']}: {assessment['values'][area['id']]} - {get_color(assessment['values'][area['id']])}")

        # Export data button
        if st.session_state.history:
            if st.button("Export Assessment History"):
                history_df = pd.DataFrame([
                    {
                        'Timestamp': assessment['timestamp'],
                        **{area['title']: assessment['values'][area['id']] for area in assessment_areas}
                    }
                    for assessment in st.session_state.history
                ])
                st.download_button(
                    label="Download CSV",
                    data=history_df.to_csv(index=False),
                    file_name="recovery_assessment_history.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
