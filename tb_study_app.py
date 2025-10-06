#!/usr/bin/env python3
"""
TB Study Data Collection Application
A comprehensive Streamlit web application for cross-sectional TB study data collection in Chennai.

This application implements:
- ICMR questionnaire for TB patients
- Digital pathway mapping with delay calculations
- Real-time visualization of delays
- eHealth Literacy Scale (eHEALS) assessment
- Data verification and export functionality

Author: Digital TB Study Team
Date: October 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

# Page configuration
st.set_page_config(
    page_title="TB Study Data Collection",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables for data collection."""
    if 'participant_data' not in st.session_state:
        st.session_state.participant_data = {
            # Demographics
            'Participant_ID': '',
            'Name_Initials': '',
            'Age': 0,
            'Gender': '',
            'Address': '',
            'Occupation': '',
            'Education': '',
            'Monthly_Income': '',
            'Marital_Status': '',
            'Residence_Type': '',
            'Comorbidities': '',
            'Comorbidities_Details': '',
            'TB_Type': '',
            'Addictive_Substances': '',
            'Addictive_Substances_Details': '',
            
            # Critical Dates
            'Date_Symptom_Onset': None,
            'Date_First_Visit': None,
            'Date_Diagnosis': None,
            'Date_Treatment_Start': None,
            
            # Calculated Delays
            'Delay_Patient': 0.0,
            'Delay_Provider': 0.0,
            'Delay_Treatment': 0.0,
            'Delay_Total': 0.0,
            
            # ICMR Questions (Key questions from the questionnaire)
            'Symptoms_Nature': [],
            'First_Care_Location': '',
            'Delay_Reason': '',
            'Healthcare_Visits_Count': 0,
            'Diagnostic_Tests': [],
            'Treatment_Delay_Reason': '',
            'Provider_Awareness': '',
            'Provider_Explanation': '',
            'Treatment_Satisfaction': '',
            'TB_Stigma': '',
            'Family_History': '',
            'Additional_Support_Needed': '',
            
            # eHEALS Questions (Q1-Q10)
            'eHEALS_Q1': 3,
            'eHEALS_Q2': 3,
            'eHEALS_Q3': 3,
            'eHEALS_Q4': 3,
            'eHEALS_Q5': 3,
            'eHEALS_Q6': 3,
            'eHEALS_Q7': 3,
            'eHEALS_Q8': 3,
            'eHEALS_Q9': 3,
            'eHEALS_Q10': 3,
            'eHEALS_Total_Score': 24,
            
            # Verification
            'Data_Verified': False,
            'Verification_Notes': ''
        }

def calculate_delays():
    """Calculate patient, provider, treatment, and total delays based on dates."""
    data = st.session_state.participant_data
    
    # Get dates
    symptom_date = data['Date_Symptom_Onset']
    first_visit_date = data['Date_First_Visit']
    diagnosis_date = data['Date_Diagnosis']
    treatment_date = data['Date_Treatment_Start']
    
    # Calculate delays if all dates are available
    if all([symptom_date, first_visit_date, diagnosis_date, treatment_date]):
        # Patient delay: Symptom onset to first healthcare visit
        data['Delay_Patient'] = (first_visit_date - symptom_date).days
        
        # Provider delay: First visit to diagnosis confirmation
        data['Delay_Provider'] = (diagnosis_date - first_visit_date).days
        
        # Treatment delay: Diagnosis to treatment start
        data['Delay_Treatment'] = (treatment_date - diagnosis_date).days
        
        # Total delay: Symptom onset to treatment start
        data['Delay_Total'] = (treatment_date - symptom_date).days
        
        return True
    return False

def validate_dates():
    """Validate that dates are in logical sequence."""
    data = st.session_state.participant_data
    dates = [
        data['Date_Symptom_Onset'],
        data['Date_First_Visit'],
        data['Date_Diagnosis'],
        data['Date_Treatment_Start']
    ]
    
    # Check if dates are in chronological order
    for i in range(len(dates) - 1):
        if dates[i] and dates[i + 1] and dates[i] > dates[i + 1]:
            return False, f"Date sequence error: Please ensure dates are in chronological order"
    
    return True, "Dates are valid"

def section_demographics():
    """Section 1: Demographics and Key ICMR Questions."""
    st.header("📋 Section 1: Demographics & Key Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        
        # Generate or input Participant ID
        if st.button("Generate New Participant ID"):
            st.session_state.participant_data['Participant_ID'] = str(uuid.uuid4())[:8].upper()
        
        st.session_state.participant_data['Participant_ID'] = st.text_input(
            "Participant ID", 
            value=st.session_state.participant_data['Participant_ID']
        )
        
        st.session_state.participant_data['Name_Initials'] = st.text_input(
            "Name/Initials", 
            value=st.session_state.participant_data['Name_Initials']
        )
        
        st.session_state.participant_data['Age'] = st.number_input(
            "Age", 
            min_value=0, 
            max_value=120, 
            value=st.session_state.participant_data['Age']
        )
        
        st.session_state.participant_data['Gender'] = st.selectbox(
            "Gender",
            options=['', 'Male', 'Female', 'Other'],
            index=['', 'Male', 'Female', 'Other'].index(st.session_state.participant_data['Gender']) if st.session_state.participant_data['Gender'] else 0
        )
        
        st.session_state.participant_data['TB_Type'] = st.selectbox(
            "TB Type",
            options=['', 'Pulmonary', 'Extra pulmonary', 'DR-TB', 'Other'],
            index=['', 'Pulmonary', 'Extra pulmonary', 'DR-TB', 'Other'].index(st.session_state.participant_data['TB_Type']) if st.session_state.participant_data['TB_Type'] else 0
        )
    
    with col2:
        st.subheader("Socio-economic Information")
        
        st.session_state.participant_data['Occupation'] = st.selectbox(
            "Occupation",
            options=['', 'Unemployed', 'Salaried', 'Self employed', 'Daily wage/Casual', 'Other'],
            index=['', 'Unemployed', 'Salaried', 'Self employed', 'Daily wage/Casual', 'Other'].index(st.session_state.participant_data['Occupation']) if st.session_state.participant_data['Occupation'] else 0
        )
        
        st.session_state.participant_data['Education'] = st.selectbox(
            "Education Level",
            options=['', 'Illiterate', 'Primary', 'Secondary', 'Senior secondary', 'Graduate and above'],
            index=['', 'Illiterate', 'Primary', 'Secondary', 'Senior secondary', 'Graduate and above'].index(st.session_state.participant_data['Education']) if st.session_state.participant_data['Education'] else 0
        )
        
        st.session_state.participant_data['Residence_Type'] = st.selectbox(
            "Type of Residence",
            options=['', 'Urban', 'Rural', 'Semi-Urban', 'Slum'],
            index=['', 'Urban', 'Rural', 'Semi-Urban', 'Slum'].index(st.session_state.participant_data['Residence_Type']) if st.session_state.participant_data['Residence_Type'] else 0
        )
        
        st.session_state.participant_data['Monthly_Income'] = st.selectbox(
            "Monthly Household Income",
            options=['', 'Above poverty line', 'Below poverty line'],
            index=['', 'Above poverty line', 'Below poverty line'].index(st.session_state.participant_data['Monthly_Income']) if st.session_state.participant_data['Monthly_Income'] else 0
        )
    
    st.subheader("Key Clinical Information")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Symptoms
        symptoms_options = ['Fever', 'Cough (>2 weeks)', 'Cough with blood', 'Chills', 'Night sweats', 
                           'Weight loss', 'Weakness/Fatigue', 'Loss of appetite', 'Chest pain', 'Breathlessness']
        st.session_state.participant_data['Symptoms_Nature'] = st.multiselect(
            "Nature of Symptoms (Select all applicable)",
            options=symptoms_options,
            default=st.session_state.participant_data['Symptoms_Nature']
        )
        
        st.session_state.participant_data['First_Care_Location'] = st.selectbox(
            "Where did you first seek care?",
            options=['', 'Government hospital', 'Private hospital', 'Private clinic', 'Primary health centre/CHC', 
                    'Pharmacy', 'Home remedies/Self medication', 'Homeopathy clinic', 'Other'],
            index=['', 'Government hospital', 'Private hospital', 'Private clinic', 'Primary health centre/CHC', 
                   'Pharmacy', 'Home remedies/Self medication', 'Homeopathy clinic', 'Other'].index(st.session_state.participant_data['First_Care_Location']) if st.session_state.participant_data['First_Care_Location'] else 0
        )
    
    with col4:
        st.session_state.participant_data['Healthcare_Visits_Count'] = st.number_input(
            "Number of healthcare visits before TB diagnosis",
            min_value=0,
            max_value=50,
            value=st.session_state.participant_data['Healthcare_Visits_Count']
        )
        
        diagnostic_tests = ['Sputum smear', 'GeneXpert', 'CB NAAT', 'Chest X-ray', 'Other']
        st.session_state.participant_data['Diagnostic_Tests'] = st.multiselect(
            "What tests were done for diagnosis?",
            options=diagnostic_tests,
            default=st.session_state.participant_data['Diagnostic_Tests']
        )

def section_digital_pathway():
    """Section 2: Digital Pathway Mapping with Critical Events."""
    st.header("📅 Section 2: Digital Pathway Mapping")
    
    st.subheader("Critical Timeline Events")
    st.write("Please enter the exact dates for each critical event in the patient's TB journey:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.participant_data['Date_Symptom_Onset'] = st.date_input(
            "🤒 Date of Symptom Onset",
            value=st.session_state.participant_data['Date_Symptom_Onset'],
            help="When did the patient first notice TB symptoms?"
        )
        
        st.session_state.participant_data['Date_First_Visit'] = st.date_input(
            "🏥 Date of First Healthcare Visit",
            value=st.session_state.participant_data['Date_First_Visit'],
            help="When did the patient first visit any healthcare provider for these symptoms?"
        )
    
    with col2:
        st.session_state.participant_data['Date_Diagnosis'] = st.date_input(
            "🔬 Date of TB Diagnosis Confirmation",
            value=st.session_state.participant_data['Date_Diagnosis'],
            help="When was TB diagnosis confirmed through tests?"
        )
        
        st.session_state.participant_data['Date_Treatment_Start'] = st.date_input(
            "💊 Date of Treatment Initiation",
            value=st.session_state.participant_data['Date_Treatment_Start'],
            help="When did the patient start Anti-TB treatment?"
        )
    
    st.subheader("Delay Calculation")
    
    if st.button("🧮 Calculate Delays", type="primary"):
        # Validate dates first
        is_valid, message = validate_dates()
        
        if not is_valid:
            st.error(message)
        else:
            if calculate_delays():
                st.success("✅ Delays calculated successfully!")
                
                # Display calculated delays
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Patient Delay",
                        f"{st.session_state.participant_data['Delay_Patient']} days",
                        help="Time from symptom onset to first healthcare visit"
                    )
                
                with col2:
                    st.metric(
                        "Provider Delay",
                        f"{st.session_state.participant_data['Delay_Provider']} days",
                        help="Time from first visit to diagnosis confirmation"
                    )
                
                with col3:
                    st.metric(
                        "Treatment Delay",
                        f"{st.session_state.participant_data['Delay_Treatment']} days",
                        help="Time from diagnosis to treatment start"
                    )
                
                with col4:
                    st.metric(
                        "Total Delay",
                        f"{st.session_state.participant_data['Delay_Total']} days",
                        help="Total time from symptom onset to treatment start"
                    )
            else:
                st.warning("⚠️ Please enter all four dates to calculate delays.")

def section_visualization():
    """Section 3: Real-time Delay Visualization."""
    st.header("📊 Section 3: Real-time Delay Visualization")
    
    data = st.session_state.participant_data
    
    # Check if delays have been calculated
    if data['Delay_Total'] > 0:
        # Create horizontal bar chart
        delays = {
            'Patient Delay': data['Delay_Patient'],
            'Provider Delay': data['Delay_Provider'],
            'Treatment Delay': data['Delay_Treatment']
        }
        
        # Create Plotly figure
        fig = go.Figure()
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        for i, (delay_type, days) in enumerate(delays.items()):
            fig.add_trace(go.Bar(
                y=[delay_type],
                x=[days],
                orientation='h',
                name=delay_type,
                marker_color=colors[i],
                text=[f'{days} days'],
                textposition='inside',
                textfont=dict(color='white', size=14)
            ))
        
        fig.update_layout(
            title=f'TB Care Delays Timeline - Participant {data["Participant_ID"]}',
            xaxis_title='Days',
            yaxis_title='Delay Type',
            showlegend=False,
            height=300,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional insights
        st.subheader("📈 Delay Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Delay breakdown pie chart
            fig_pie = px.pie(
                values=list(delays.values()),
                names=list(delays.keys()),
                title="Delay Breakdown (%)",
                color_discrete_sequence=colors
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.write("**Delay Insights:**")
            
            max_delay = max(delays.items(), key=lambda x: x[1])
            st.write(f"• Longest delay: **{max_delay[0]}** ({max_delay[1]} days)")
            
            if data['Delay_Total'] > 30:
                st.error("⚠️ Total delay exceeds 30 days - requires attention")
            elif data['Delay_Total'] > 14:
                st.warning("⚠️ Total delay exceeds 14 days")
            else:
                st.success("✅ Total delay within acceptable range")
            
            # Delay categorization
            if data['Delay_Patient'] > data['Delay_Provider']:
                st.write("• **Patient-side delay** is the primary concern")
            elif data['Delay_Provider'] > data['Delay_Patient']:
                st.write("• **Provider-side delay** is the primary concern")
            else:
                st.write("• Patient and provider delays are balanced")
    
    else:
        st.info("📝 Please complete Section 2 (Digital Pathway Mapping) and calculate delays to view visualization.")
        
        # Show placeholder chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=['Patient Delay', 'Provider Delay', 'Treatment Delay'],
            x=[0, 0, 0],
            orientation='h',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'],
            text=['0 days', '0 days', '0 days'],
            textposition='inside'
        ))
        
        fig.update_layout(
            title='TB Care Delays Timeline - Awaiting Data',
            xaxis_title='Days',
            yaxis_title='Delay Type',
            showlegend=False,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

def section_eheals():
    """Section 4: eHealth Literacy Scale (eHEALS) Assessment."""
    st.header("💻 Section 4: eHealth Literacy Scale (eHEALS)")
    
    st.write("""
    **Instructions:** For each statement, please select the response that best reflects your opinion and experience with using the Internet for health information.
    """)
    
    # eHEALS Questions (Questions 1-2 are supplementary, 3-10 are the formal scale)
    eheals_questions = {
        'eHEALS_Q1': "How useful do you feel the Internet is in helping you in making decisions about your health?",
        'eHEALS_Q2': "How important is it for you to be able to access health resources on the Internet?",
        'eHEALS_Q3': "I know what health resources are available on the Internet",
        'eHEALS_Q4': "I know where to find helpful health resources on the Internet",
        'eHEALS_Q5': "I know how to find helpful health resources on the Internet",
        'eHEALS_Q6': "I know how to use the Internet to answer my questions about health",
        'eHEALS_Q7': "I know how to use the health information I find on the Internet to help me",
        'eHEALS_Q8': "I have the skills I need to evaluate the health resources I find on the Internet",
        'eHEALS_Q9': "I can tell high quality health resources from low quality health resources on the Internet",
        'eHEALS_Q10': "I feel confident in using information from the Internet to make health decisions"
    }
    
    # Different response scales for different questions
    scale_1_2 = {
        1: "Not useful/important at all",
        2: "Not useful/important",
        3: "Unsure",
        4: "Useful/Important",
        5: "Very useful/important"
    }
    
    scale_3_10 = {
        1: "Strongly Disagree",
        2: "Disagree",
        3: "Undecided",
        4: "Agree",
        5: "Strongly Agree"
    }
    
    st.subheader("📋 eHEALS Questions")
    
    # Questions 1-2 (Supplementary)
    st.write("**Supplementary Questions:**")
    
    for q_num in [1, 2]:
        q_key = f'eHEALS_Q{q_num}'
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Q{q_num}.** {eheals_questions[q_key]}")
            st.session_state.participant_data[q_key] = st.radio(
                f"Response Q{q_num}",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {scale_1_2[x]}",
                index=st.session_state.participant_data[q_key] - 1,
                key=f"radio_{q_key}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.metric(f"Q{q_num} Score", st.session_state.participant_data[q_key])
    
    st.divider()
    
    # Questions 3-10 (Formal eHEALS Scale)
    st.write("**Formal eHEALS Scale (Questions 3-10):**")
    
    for q_num in range(3, 11):
        q_key = f'eHEALS_Q{q_num}'
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Q{q_num}.** {eheals_questions[q_key]}")
            st.session_state.participant_data[q_key] = st.radio(
                f"Response Q{q_num}",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: f"{x} - {scale_3_10[x]}",
                index=st.session_state.participant_data[q_key] - 1,
                key=f"radio_{q_key}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.metric(f"Q{q_num} Score", st.session_state.participant_data[q_key])
    
    # Calculate total eHEALS score (formal scale questions 3-10)
    formal_scale_score = sum([st.session_state.participant_data[f'eHEALS_Q{i}'] for i in range(3, 11)])
    st.session_state.participant_data['eHEALS_Total_Score'] = formal_scale_score
    
    st.subheader("📊 eHEALS Score Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        all_questions_score = sum([st.session_state.participant_data[f'eHEALS_Q{i}'] for i in range(1, 11)])
        st.metric(
            "Total Score (All Questions)",
            f"{all_questions_score}/50",
            help="Sum of all 10 questions (Q1-Q10)"
        )
    
    with col2:
        st.metric(
            "Formal eHEALS Score",
            f"{formal_scale_score}/40",
            help="Sum of formal scale questions (Q3-Q10)"
        )
    
    with col3:
        # eHEALS interpretation
        if formal_scale_score >= 32:
            level = "High"
            color = "green"
        elif formal_scale_score >= 24:
            level = "Moderate"
            color = "orange"
        else:
            level = "Low"
            color = "red"
        
        st.metric(
            "eHealth Literacy Level",
            level,
            help=f"Based on formal eHEALS score: {formal_scale_score}/40"
        )

def section_verification():
    """Section 5: Data Verification and Export."""
    st.header("✅ Section 5: Data Verification & Export")
    
    data = st.session_state.participant_data
    
    st.subheader("📋 Data Summary")
    
    # Display key information for verification
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Participant Information:**")
        st.write(f"• ID: {data['Participant_ID']}")
        st.write(f"• Age: {data['Age']}")
        st.write(f"• Gender: {data['Gender']}")
        st.write(f"• TB Type: {data['TB_Type']}")
        
        st.write("**Timeline:**")
        if data['Date_Symptom_Onset']:
            st.write(f"• Symptom Onset: {data['Date_Symptom_Onset']}")
        if data['Date_First_Visit']:
            st.write(f"• First Visit: {data['Date_First_Visit']}")
        if data['Date_Diagnosis']:
            st.write(f"• Diagnosis: {data['Date_Diagnosis']}")
        if data['Date_Treatment_Start']:
            st.write(f"• Treatment Start: {data['Date_Treatment_Start']}")
    
    with col2:
        st.write("**Calculated Delays:**")
        st.write(f"• Patient Delay: {data['Delay_Patient']} days")
        st.write(f"• Provider Delay: {data['Delay_Provider']} days")
        st.write(f"• Treatment Delay: {data['Delay_Treatment']} days")
        st.write(f"• Total Delay: {data['Delay_Total']} days")
        
        st.write("**eHEALS Score:**")
        st.write(f"• Formal Scale Score: {data['eHEALS_Total_Score']}/40")
        
        # eHEALS level
        if data['eHEALS_Total_Score'] >= 32:
            level = "High"
        elif data['eHEALS_Total_Score'] >= 24:
            level = "Moderate"
        else:
            level = "Low"
        st.write(f"• eHealth Literacy Level: {level}")
    
    st.subheader("🔍 Verification")
    
    # Verification checkbox
    st.session_state.participant_data['Data_Verified'] = st.checkbox(
        "✅ Data Verified against Medical Records",
        value=st.session_state.participant_data['Data_Verified'],
        help="Check this box to confirm that all data has been verified against medical records"
    )
    
    # Verification notes
    st.session_state.participant_data['Verification_Notes'] = st.text_area(
        "Verification Notes",
        value=st.session_state.participant_data['Verification_Notes'],
        placeholder="Enter any notes about data verification, discrepancies, or additional observations...",
        height=100
    )
    
    st.subheader("💾 Data Export")
    
    # Check if essential data is complete
    essential_fields = ['Participant_ID', 'Age', 'Gender', 'TB_Type']
    missing_fields = [field for field in essential_fields if not data[field]]
    
    if missing_fields:
        st.warning(f"⚠️ Please complete the following essential fields before export: {', '.join(missing_fields)}")
    else:
        if st.button("📊 Generate Export Data", type="primary"):
            # Create DataFrame for export
            export_data = create_export_dataframe()
            
            # Display preview
            st.subheader("📋 Export Preview")
            st.dataframe(export_data, use_container_width=True)
            
            # Generate CSV for download
            csv_data = export_data.to_csv(index=False)
            
            # Create filename
            participant_id = data['Participant_ID'] if data['Participant_ID'] else 'UNKNOWN'
            filename = f"data_{participant_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            st.download_button(
                label="💾 Download Data (CSV)",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                help="Download the complete participant data as CSV file"
            )
            
            st.success("✅ Data export ready! Click the download button above to save the file.")

def create_export_dataframe():
    """Create a comprehensive DataFrame for data export."""
    data = st.session_state.participant_data
    
    # Create export dictionary with all required columns
    export_dict = {
        # Core identifiers
        'Participant_ID': [data['Participant_ID']],
        'Name_Initials': [data['Name_Initials']],
        'Data_Collection_Date': [datetime.now().strftime('%Y-%m-%d')],
        
        # Demographics
        'Age': [data['Age']],
        'Gender': [data['Gender']],
        'Address': [data['Address']],
        'Occupation': [data['Occupation']],
        'Education': [data['Education']],
        'Monthly_Income': [data['Monthly_Income']],
        'Marital_Status': [data['Marital_Status']],
        'Residence_Type': [data['Residence_Type']],
        'Comorbidities': [data['Comorbidities']],
        'Comorbidities_Details': [data['Comorbidities_Details']],
        'TB_Type': [data['TB_Type']],
        'Addictive_Substances': [data['Addictive_Substances']],
        'Addictive_Substances_Details': [data['Addictive_Substances_Details']],
        
        # Critical dates
        'Date_Symptom_Onset': [data['Date_Symptom_Onset']],
        'Date_First_Visit': [data['Date_First_Visit']],
        'Date_Diagnosis': [data['Date_Diagnosis']],
        'Date_Treatment_Start': [data['Date_Treatment_Start']],
        
        # Calculated delays
        'Delay_Patient': [data['Delay_Patient']],
        'Delay_Provider': [data['Delay_Provider']],
        'Delay_Treatment': [data['Delay_Treatment']],
        'Delay_Total': [data['Delay_Total']],
        
        # ICMR questionnaire responses
        'Symptoms_Nature': ['; '.join(data['Symptoms_Nature'])],
        'First_Care_Location': [data['First_Care_Location']],
        'Delay_Reason': [data['Delay_Reason']],
        'Healthcare_Visits_Count': [data['Healthcare_Visits_Count']],
        'Diagnostic_Tests': ['; '.join(data['Diagnostic_Tests'])],
        'Treatment_Delay_Reason': [data['Treatment_Delay_Reason']],
        'Provider_Awareness': [data['Provider_Awareness']],
        'Provider_Explanation': [data['Provider_Explanation']],
        'Treatment_Satisfaction': [data['Treatment_Satisfaction']],
        'TB_Stigma': [data['TB_Stigma']],
        'Family_History': [data['Family_History']],
        'Additional_Support_Needed': [data['Additional_Support_Needed']],
        
        # eHEALS scores (individual questions)
        'eHEALS_Q1': [data['eHEALS_Q1']],
        'eHEALS_Q2': [data['eHEALS_Q2']],
        'eHEALS_Q3': [data['eHEALS_Q3']],
        'eHEALS_Q4': [data['eHEALS_Q4']],
        'eHEALS_Q5': [data['eHEALS_Q5']],
        'eHEALS_Q6': [data['eHEALS_Q6']],
        'eHEALS_Q7': [data['eHEALS_Q7']],
        'eHEALS_Q8': [data['eHEALS_Q8']],
        'eHEALS_Q9': [data['eHEALS_Q9']],
        'eHEALS_Q10': [data['eHEALS_Q10']],
        'eHEALS_Total_Score': [data['eHEALS_Total_Score']],
        
        # Verification
        'Data_Verified': [data['Data_Verified']],
        'Verification_Notes': [data['Verification_Notes']]
    }
    
    return pd.DataFrame(export_dict)

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Application header
    st.title("🏥 TB Study Data Collection Application")
    st.markdown("### Cross-sectional TB Study - Chennai")
    st.markdown("**Digital pathway mapping and eHealth literacy assessment platform**")
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    st.sidebar.markdown("---")
    
    sections = {
        "📋 Demographics & ICMR": "section_1",
        "📅 Digital Pathway": "section_2", 
        "📊 Visualization": "section_3",
        "💻 eHEALS Assessment": "section_4",
        "✅ Verification & Export": "section_5"
    }
    
    selected_section = st.sidebar.radio("Select Section:", list(sections.keys()))
    
    # Display participant info in sidebar if available
    if st.session_state.participant_data['Participant_ID']:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Current Participant:**")
        st.sidebar.markdown(f"ID: `{st.session_state.participant_data['Participant_ID']}`")
        if st.session_state.participant_data['Age'] > 0:
            st.sidebar.markdown(f"Age: {st.session_state.participant_data['Age']}")
        if st.session_state.participant_data['TB_Type']:
            st.sidebar.markdown(f"TB Type: {st.session_state.participant_data['TB_Type']}")
    
    # Progress indicator
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Progress:**")
    
    progress_items = [
        ("Demographics", bool(st.session_state.participant_data['Participant_ID'])),
        ("Dates", bool(st.session_state.participant_data['Date_Symptom_Onset'])),
        ("Delays", st.session_state.participant_data['Delay_Total'] > 0),
        ("eHEALS", st.session_state.participant_data['eHEALS_Total_Score'] > 24),
        ("Verified", st.session_state.participant_data['Data_Verified'])
    ]
    
    for item, completed in progress_items:
        status = "✅" if completed else "⏳"
        st.sidebar.markdown(f"{status} {item}")
    
    # Display selected section
    if selected_section == "📋 Demographics & ICMR":
        section_demographics()
    elif selected_section == "📅 Digital Pathway":
        section_digital_pathway()
    elif selected_section == "📊 Visualization":
        section_visualization()
    elif selected_section == "💻 eHEALS Assessment":
        section_eheals()
    elif selected_section == "✅ Verification & Export":
        section_verification()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**TB Study Data Collection App** | Developed for Cross-sectional TB Study, Chennai | "
        f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    # Reset button in sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reset Session", help="Clear all data and start fresh"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()