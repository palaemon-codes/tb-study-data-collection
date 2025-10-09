#!/usr/bin/env python3
"""
TB Study Data Collection Application
A comprehensive Streamlit web application for cross-sectional TB study data collection in Chennai.

This application implements:
- ICMR questionnaire for TB patients
- Digital pathway mapping with delay calculations
- Real-time visualization of delays
- Digital Health Literacy Instrument (DHLI) assessment
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
import random
import random

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
            
            # Calculated Delays (New Classification)
            # Delay calculations
            'Patient_Delay': 0.0,
            'Healthcare_Provider_Related_Delay': 0.0,
            'Treatment_Delay': 0.0,
            'Total_Delay': 0.0,
            'TB_Unit_TU': 0.0,
            'Healthcare_Providers': 0.0,
            'No_Delay': False,
            
            # Specific Delay Reasons for Each Gap
            'Patient_Delay_Specific_Reason': '',
            'Provider_Delay_Specific_Reason': '',
            'Treatment_Delay_Specific_Reason': '',
            
            # Questionnaire Responses (Key questions from the questionnaire)
            'Symptoms_Nature': [],
            'First_Care_Location': '',
            'Patient_Delay_Reason': [],
            'Healthcare_Visits_Count': 0,
            'Diagnostic_Tests': [],
            'Treatment_Delay_Experienced': '',
            'Treatment_Delay_Reason': [],
            'Provider_Awareness': '',
            'Provider_Explanation': '',
            'Provider_Difficulties': '',
            'Provider_Difficulties_Details': [],
            'Treatment_Satisfaction': '',
            'TB_Stigma': '',
            'Family_History': '',
            'Family_History_Year': '',
            'Additional_Support_Needed': [],
            
            # DHLI Assessment (Digital Health Literacy Instrument) - 10 Items
            'DHLI_Q1': 0,
            'DHLI_Q2': 0,
            'DHLI_Q3': 0,
            'DHLI_Q4': 0,
            'DHLI_Q5': 0,
            'DHLI_Q6': 0,
            'DHLI_Q7': 0,
            'DHLI_Q8': 0,
            'DHLI_Q9': 0,
            'DHLI_Q10': 0,
            'DHLI_Total_Score': 0,
            
            # Verification
            'Data_Verified': False,
            'Verification_Notes': ''
        }
    
    # Initialize current section for navigation
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 0

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
        data['Patient_Delay'] = (first_visit_date - symptom_date).days
        
        # Healthcare Provider-related delay: First visit to diagnosis confirmation
        data['Healthcare_Provider_Related_Delay'] = (diagnosis_date - first_visit_date).days
        
        # Treatment delay: Diagnosis to treatment start
        data['Treatment_Delay'] = (treatment_date - diagnosis_date).days
        
        # Total delay: Symptom onset to treatment start
        data['Total_Delay'] = (treatment_date - symptom_date).days
        
        # Set other delay types
        data['TB_Unit_TU'] = data['Healthcare_Provider_Related_Delay']  # TB Unit delay
        data['Healthcare_Providers'] = data['Healthcare_Provider_Related_Delay']  # Healthcare Providers delay
        data['No_Delay'] = (data['Total_Delay'] == 0)
        
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
    
    date_names = [
        "Symptom Onset",
        "First Visit", 
        "Diagnosis",
        "Treatment Start"
    ]
    
    # Check if dates are in chronological order
    for i in range(len(dates) - 1):
        if dates[i] and dates[i + 1] and dates[i] > dates[i + 1]:
            return False, f"Date sequence error: {date_names[i]} cannot be after {date_names[i + 1]}"
    
    return True, "Dates are valid"

def generate_sample_data():
    """Generate fabricated sample data for 30 patients for demo purposes."""
    random.seed(42)  # For reproducible results
    np.random.seed(42)
    
    sample_data = []
    
    # Demographics data pools
    names = [f"Patient_{i+1:03d}" for i in range(30)]
    genders = ['Male', 'Female']
    education_levels = ['No formal education', 'Primary school', 'Secondary school', 'Higher secondary', 'Graduate', 'Postgraduate']
    occupations = ['Unemployed', 'Manual laborer', 'Skilled worker', 'Clerical', 'Professional', 'Business', 'Student', 'Homemaker']
    income_levels = ['< ₹10,000', '₹10,000 - ₹25,000', '₹25,000 - ₹50,000', '₹50,000 - ₹75,000', '> ₹75,000']
    locations = ['Urban', 'Semi-urban', 'Rural']
    tb_types = ['Pulmonary TB', 'Extra-pulmonary TB']
    
    # Delay reasons
    patient_delay_reasons = [
        'Financial constraints', 'Lack of awareness about symptoms', 
        'Self-medication attempts', 'Fear of stigma', 'Distance to healthcare facility',
        'Work commitments', 'Family responsibilities'
    ]
    
    provider_delay_reasons = [
        'Misdiagnosis as other condition', 'Inadequate diagnostic facilities',
        'Delayed test results', 'Multiple consultations required',
        'Referral delays', 'Staff shortage', 'Equipment breakdown'
    ]
    
    treatment_delay_reasons = [
        'Drug availability issues', 'Patient counseling delays',
        'Administrative procedures', 'Bed availability',
        'Comorbidity management', 'Contact tracing', 'Insurance processing'
    ]
    
    for i in range(30):
        # Generate base date (symptom onset) - random date in last 6 months
        base_date = datetime(2024, 4, 1) + timedelta(days=random.randint(0, 180))
        
        # Generate delays (in days)
        patient_delay = random.randint(1, 90)
        provider_delay = random.randint(1, 60) 
        treatment_delay = random.randint(1, 30)
        
        # Calculate dates based on delays
        first_visit_date = base_date + timedelta(days=patient_delay)
        diagnosis_date = first_visit_date + timedelta(days=provider_delay)
        treatment_date = diagnosis_date + timedelta(days=treatment_delay)
        
        # Generate patient data to match export structure
        patient = {
            # Core identifiers
            'Participant_ID': f'TB{i+1:03d}',
            'Name_Initials': names[i],
            'Data_Collection_Date': datetime.now().strftime('%Y-%m-%d'),
            
            # Demographics
            'Age': random.randint(18, 80),
            'Gender': random.choice(genders),
            'Address': f"Address {i+1}, Chennai",
            'Occupation': random.choice(occupations),
            'Education': random.choice(education_levels),
            'Monthly_Income': random.choice(income_levels),
            'Marital_Status': random.choice(['Single', 'Married', 'Divorced', 'Widowed']),
            'Residence_Type': random.choice(locations),
            'Comorbidities': random.choice(['None', 'Diabetes', 'Hypertension', 'HIV', 'Other']),
            'Comorbidities_Details': '',
            'TB_Type': random.choice(tb_types),
            'Addictive_Substances': random.choice(['None', 'Tobacco', 'Alcohol', 'Other']),
            'Addictive_Substances_Details': '',
            
            # Critical dates
            'Date_Symptom_Onset': base_date.strftime('%Y-%m-%d'),
            'Date_First_Visit': first_visit_date.strftime('%Y-%m-%d'),
            'Date_Diagnosis': diagnosis_date.strftime('%Y-%m-%d'),
            'Date_Treatment_Start': treatment_date.strftime('%Y-%m-%d'),
            
            # Calculated delays
            'Patient_Delay': patient_delay,
            'Healthcare_Provider_Related_Delay': provider_delay,
            'Treatment_Delay': treatment_delay,
            'Total_Delay': patient_delay + provider_delay + treatment_delay,
            'TB_Unit_TU': provider_delay,
            'Healthcare_Providers': provider_delay,
            'No_Delay': (patient_delay + provider_delay + treatment_delay == 0),
            
            # Specific delay reasons
            'Patient_Delay_Specific_Reason': random.choice(patient_delay_reasons),
            'Provider_Delay_Specific_Reason': random.choice(provider_delay_reasons),
            'Treatment_Delay_Specific_Reason': random.choice(treatment_delay_reasons),
            
            # Questionnaire responses (empty for sample data)
            'Symptoms_Nature': '',
            'First_Care_Location': '',
            'Patient_Delay_Reason': '',
            'Healthcare_Visits_Count': random.randint(1, 5),
            'Diagnostic_Tests': '',
            'Treatment_Delay_Experienced': '',
            'Treatment_Delay_Reason': '',
            'Provider_Awareness': '',
            'Provider_Explanation': '',
            'Provider_Difficulties': '',
            'Provider_Difficulties_Details': '',
            'Treatment_Satisfaction': '',
            'TB_Stigma': '',
            'Family_History': '',
            'Family_History_Year': '',
            'Additional_Support_Needed': '',
            
            # DHLI Assessment (Digital Health Literacy)
            'DHLI_Q1': random.randint(0, 1),
            'DHLI_Q2': random.randint(0, 1),
            'DHLI_Q3': random.randint(0, 1),
            'DHLI_Q4': random.randint(0, 1),
            'DHLI_Q5': random.randint(0, 1),
            'DHLI_Q6': random.randint(0, 1),
            'DHLI_Q7': random.randint(0, 1),
            'DHLI_Q8': random.randint(0, 1),
            'DHLI_Q9': random.randint(0, 1),
            'DHLI_Q10': random.randint(0, 1),
            'DHLI_Total_Score': 0,  # Will be calculated
            
            # Verification
            'Data_Verified': random.choice([True, False]),
            'Verification_Notes': f'Sample patient {i+1} - fabricated data for demo'
        }
        
        # Calculate DHLI total score
        patient['DHLI_Total_Score'] = sum([patient[f'DHLI_Q{j}'] for j in range(1, 11)])
        

        
        sample_data.append(patient)
    
    return pd.DataFrame(sample_data)

def section_demographics():
    """Section 1: Demographics and Key Clinical Questions."""
    st.header("📋 Section 1: Demographics & Clinical Information")
    
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
            options=['', '< ₹10,000', '₹10,000 - ₹25,000', '₹25,000 - ₹50,000', '₹50,000 - ₹75,000', '> ₹75,000'],
            index=['', '< ₹10,000', '₹10,000 - ₹25,000', '₹25,000 - ₹50,000', '₹50,000 - ₹75,000', '> ₹75,000'].index(st.session_state.participant_data['Monthly_Income']) if st.session_state.participant_data['Monthly_Income'] else 0
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
            help="When did the patient first notice TB symptoms?",
            key="date_symptom_onset"
        )
        
        st.session_state.participant_data['Date_First_Visit'] = st.date_input(
            "🏥 Date of First Healthcare Visit",
            value=st.session_state.participant_data['Date_First_Visit'],
            help="When did the patient first visit any healthcare provider for these symptoms?",
            key="date_first_visit"
        )
    
    with col2:
        st.session_state.participant_data['Date_Diagnosis'] = st.date_input(
            "🔬 Date of TB Diagnosis Confirmation",
            value=st.session_state.participant_data['Date_Diagnosis'],
            help="When was TB diagnosis confirmed through tests?",
            key="date_diagnosis"
        )
        
        st.session_state.participant_data['Date_Treatment_Start'] = st.date_input(
            "💊 Date of Treatment Initiation",
            value=st.session_state.participant_data['Date_Treatment_Start'],
            help="When did the patient start Anti-TB treatment?",
            key="date_treatment_start"
        )
    
    # Add delay reason dropdowns immediately after date inputs
    st.subheader("🔍 Delay Reason Analysis")
    st.write("Please specify the primary reason for delay in each phase:")
    
    col_reason1, col_reason2, col_reason3 = st.columns(3)
    
    with col_reason1:
        st.write("**Patient Delay Reason**")
        st.write("*Gap: Symptom onset → First visit*")
        
        patient_delay_options = [
            '',
            'Did not recognize symptoms as serious',
            'Financial constraints',
            'Lack of awareness about TB',
            'Fear of stigma related to TB',
            'Unavailability of healthcare services',
            'Transportation issues',
            'Work/family commitments',
            'Self-medication attempts',
            'Other'
        ]
        
        st.session_state.participant_data['Patient_Delay_Specific_Reason'] = st.selectbox(
            "Primary reason for patient delay:",
            options=patient_delay_options,
            index=patient_delay_options.index(st.session_state.participant_data['Patient_Delay_Specific_Reason']) if st.session_state.participant_data['Patient_Delay_Specific_Reason'] in patient_delay_options else 0,
            key="patient_delay_reason"
        )
    
    with col_reason2:
        st.write("**Provider Delay Reason**")
        st.write("*Gap: First visit → Diagnosis*")
        
        provider_delay_options = [
            '',
            'Delay in diagnostic tests',
            'Waiting for test results',
            'Misdiagnosis/incorrect initial diagnosis',
            'Unavailability of healthcare provider',
            'Inadequate clinical assessment',
            'Referral delays between facilities',
            'Equipment/facility unavailability',
            'Administrative delays',
            'Other'
        ]
        
        st.session_state.participant_data['Provider_Delay_Specific_Reason'] = st.selectbox(
            "Primary reason for provider delay:",
            options=provider_delay_options,
            index=provider_delay_options.index(st.session_state.participant_data['Provider_Delay_Specific_Reason']) if st.session_state.participant_data['Provider_Delay_Specific_Reason'] in provider_delay_options else 0,
            key="provider_delay_reason"
        )
    
    with col_reason3:
        st.write("**Treatment Delay Reason**")
        st.write("*Gap: Diagnosis → Treatment start*")
        
        treatment_delay_options = [
            '',
            'Delay in availability of medicines',
            'Waiting for additional test results',
            'Financial reasons',
            'Patient counseling and preparation',
            'Administrative/paperwork delays',
            'Referral to specialized center',
            'Patient readiness/consent issues',
            'Lack of awareness of treatment urgency',
            'Other'
        ]
        
        st.session_state.participant_data['Treatment_Delay_Specific_Reason'] = st.selectbox(
            "Primary reason for treatment delay:",
            options=treatment_delay_options,
            index=treatment_delay_options.index(st.session_state.participant_data['Treatment_Delay_Specific_Reason']) if st.session_state.participant_data['Treatment_Delay_Specific_Reason'] in treatment_delay_options else 0,
            key="treatment_delay_reason"
        )
    
    st.subheader("Delay Calculation & Summary")
    
    # Automatically calculate delays when dates are available
    if all([st.session_state.participant_data['Date_Symptom_Onset'], 
            st.session_state.participant_data['Date_First_Visit'],
            st.session_state.participant_data['Date_Diagnosis'], 
            st.session_state.participant_data['Date_Treatment_Start']]):
        
        # Validate dates first
        is_valid, message = validate_dates()
        
        if not is_valid:
            st.error(message)
        else:
            # Calculate delays automatically
            calculate_delays()
            
            # Display calculated delays
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Patient Delay",
                    f"{st.session_state.participant_data['Patient_Delay']} days",
                    help="Time from symptom onset to first healthcare visit"
                )
            
            with col2:
                st.metric(
                    "Healthcare Provider Delay",
                    f"{st.session_state.participant_data['Healthcare_Provider_Related_Delay']} days",
                    help="Time from first visit to diagnosis confirmation"
                )
            
            with col3:
                st.metric(
                    "Treatment Delay",
                    f"{st.session_state.participant_data['Treatment_Delay']} days",
                    help="Time from diagnosis to treatment start"
                )
            
            with col4:
                st.metric(
                    "Total Delay",
                    f"{st.session_state.participant_data['Total_Delay']} days",
                    help="Total time from symptom onset to treatment start"
                )
            
            # Visual delay summary
            st.subheader("📊 Delay Summary")
            delay_summary_data = {
                'Phase': ['Patient Phase', 'Healthcare Provider Phase', 'Treatment Phase'],
                'Days': [st.session_state.participant_data['Patient_Delay'], 
                        st.session_state.participant_data['Healthcare_Provider_Related_Delay'], 
                        st.session_state.participant_data['Treatment_Delay']],
                'Primary Reason': [
                    st.session_state.participant_data['Patient_Delay_Specific_Reason'] or 'Not specified',
                    st.session_state.participant_data['Provider_Delay_Specific_Reason'] or 'Not specified',
                    st.session_state.participant_data['Treatment_Delay_Specific_Reason'] or 'Not specified'
                ]
            }
            
            import pandas as pd
            delay_df = pd.DataFrame(delay_summary_data)
            st.dataframe(delay_df, use_container_width=True, hide_index=True)
    
    else:
        st.info("⏳ Please enter all four dates above to automatically calculate delays and view summary.")

def create_gantt_chart():
    """Create a Gantt chart showing patient timelines."""
    sample_df = generate_sample_data()
    
    # Prepare data for Gantt chart - only show first 8 patients for clarity
    gantt_data = []
    
    for idx, row in sample_df.head(8).iterrows():
        participant_id = row['Participant_ID']
        tb_type = row['TB_Type']
        
        # Convert dates
        symptom_date = pd.to_datetime(row['Date_Symptom_Onset'])
        first_visit_date = pd.to_datetime(row['Date_First_Visit'])
        diagnosis_date = pd.to_datetime(row['Date_Diagnosis'])
        treatment_date = pd.to_datetime(row['Date_Treatment_Start'])
        
        # Pre-visit phase (symptoms to first visit)
        gantt_data.append(dict(
            Task=participant_id,
            Start=symptom_date,
            Finish=first_visit_date,
            Resource=f"{tb_type}, Pre-visit"
        ))
        
        # Diagnosis phase (first visit to diagnosis)
        gantt_data.append(dict(
            Task=participant_id,
            Start=first_visit_date,
            Finish=diagnosis_date,
            Resource=f"{tb_type}, Diagnosis"
        ))
        
        # Pre-treatment phase (diagnosis to treatment)
        gantt_data.append(dict(
            Task=participant_id,
            Start=diagnosis_date,
            Finish=treatment_date,
            Resource=f"{tb_type}, Pre-treatment"
        ))
    
    gantt_df = pd.DataFrame(gantt_data)
    
    # Create color mapping for different TB types and stages
    color_map = {
        'Pulmonary TB, Pre-visit': '#1f77b4',
        'Pulmonary TB, Diagnosis': '#aec7e8',
        'Pulmonary TB, Pre-treatment': '#c5dbf7',
        'Extra-pulmonary TB, Pre-visit': '#2ca02c',
        'Extra-pulmonary TB, Diagnosis': '#98df8a',
        'Extra-pulmonary TB, Pre-treatment': '#c4e6c0'
    }
    
    # Create Gantt chart
    fig = px.timeline(
        gantt_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource",
        color_discrete_map=color_map,
        title="TB Patient Care Timelines"
    )
    
    fig.update_layout(
        height=600,
        xaxis_title="Date",
        yaxis_title="Patient ID",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="left",
            x=0
        )
    )
    
    return fig

def section_visualization():
    """Section 4: Real-time Delay Visualization with Data Analytics."""
    st.header("📊 Section 4: Data Visualization & Analytics")
    
    # Tab structure for different visualizations
    tab1, tab2, tab3 = st.tabs(["Current Patient", "Gantt Chart", "Data Analytics"])
    
    with tab1:
        st.subheader("Current Patient Delay Analysis")
        data = st.session_state.participant_data
        
        # Check if delays have been calculated
        if data['Total_Delay'] > 0:
            # Create horizontal bar chart
            delays = {
                'Patient Delay': data['Patient_Delay'],
                'Healthcare Provider-related Delay': data['Healthcare_Provider_Related_Delay'],
                'Treatment Delay': data['Treatment_Delay']
            }
            
            # Create Plotly figure
            fig = go.Figure()
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            
            for i, (delay_type, days) in enumerate(delays.items()):
                fig.add_trace(go.Bar(
                    x=[days],
                    y=[delay_type],
                    orientation='h',
                    marker_color=colors[i],
                    text=[f'{days} days'],
                    textposition='auto',
                    name=delay_type
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
                st.metric("Total Delay", f"{data['Total_Delay']} days")
                st.metric("Patient Delay", f"{data['Patient_Delay']} days")
                st.metric("Provider Delay", f"{data['Healthcare_Provider_Related_Delay']} days")
            
            with col2:
                st.metric("Treatment Delay", f"{data['Treatment_Delay']} days")
                
                # Determine delay category
                total_days = data['Total_Delay']
                if total_days <= 30:
                    category = "Low Delay"
                    color = "green"
                elif total_days <= 60:
                    category = "Moderate Delay"
                    color = "orange"
                else:
                    category = "High Delay"
                    color = "red"
                
                st.markdown(f"**Delay Category:** :{color}[{category}]")
        
        else:
            st.info("⏳ Please complete Section 2 (Digital Pathway Mapping) to view delay analysis.")
    
    with tab2:
        st.subheader("Patient Care Timeline - Gantt Chart")
        st.write("Visual representation of TB patient care timelines across different phases")
        
        gantt_fig = create_gantt_chart()
        st.plotly_chart(gantt_fig, use_container_width=True)
    
    with tab3:
        st.subheader("Data Analytics Dashboard")
        sample_df = generate_sample_data()
        
        # Descriptive Statistics
        st.write("### Descriptive Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Patients", len(sample_df))
            st.metric("Mean Total Delay", f"{sample_df['Total_Delay'].mean():.1f} days")
            st.metric("Median Total Delay", f"{sample_df['Total_Delay'].median():.1f} days")
        
        with col2:
            st.metric("Mean Patient Delay", f"{sample_df['Patient_Delay'].mean():.1f} days")
            st.metric("Mean Provider Delay", f"{sample_df['Healthcare_Provider_Related_Delay'].mean():.1f} days")
            st.metric("Mean Treatment Delay", f"{sample_df['Treatment_Delay'].mean():.1f} days")
        
        with col3:
            male_count = len(sample_df[sample_df['Gender'] == 'Male'])
            female_count = len(sample_df[sample_df['Gender'] == 'Female'])
            st.metric("Male Patients", male_count)
            st.metric("Female Patients", female_count)
            pulm_tb = len(sample_df[sample_df['TB_Type'] == 'Pulmonary TB'])
            st.metric("Pulmonary TB", pulm_tb)
        
        # Delay Distribution
        st.write("### Delay Distribution Analysis")
        
        fig_hist = px.histogram(
            sample_df, 
            x='Total_Delay', 
            nbins=20,
            title='Distribution of Total Delays',
            labels={'Total_Delay': 'Total Delay (days)', 'count': 'Number of Patients'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Box plot by TB Type
        fig_box = px.box(
            sample_df,
            x='TB_Type',
            y='Total_Delay',
            title='Delay Distribution by TB Type'
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Demographics Analysis
        st.write("### Demographics Profile")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Age distribution
            fig_age = px.histogram(
                sample_df,
                x='Age',
                title='Age Distribution',
                nbins=15
            )
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            # Education distribution
            education_counts = sample_df['Education'].value_counts()
            fig_edu = px.pie(
                values=education_counts.values,
                names=education_counts.index,
                title='Education Distribution'
            )
            st.plotly_chart(fig_edu, use_container_width=True)
        
        # DHLI Score Analysis
        st.write("### Digital Health Literacy Analysis")
        
        fig_dhli = px.scatter(
            sample_df,
            x='Total_Delay',
            y='DHLI_Total_Score',
            color='TB_Type',
            title='DHLI Score vs Total Delay',
            labels={'Total_Delay': 'Total Delay (days)', 'DHLI_Total_Score': 'DHLI Score'}
        )
        st.plotly_chart(fig_dhli, use_container_width=True)
    


def section_dhli():
    """Section 3: Digital Health Literacy Instrument (DHLI) Assessment."""
    st.header(" Section 3: Digital Health Literacy Assessment (DHLI)")
    
    st.write("""
    **Instructions (வழிமுறைகள்):** This assessment evaluates your ability to use digital tools for health information. 
    Please answer honestly based on your experience with mobile phones and digital health services.
    
    
    *இந்த மதிப்பீடு சுகாதார தகவல்களுக்கான டிஜிட்டல் கருவிகளைப் பயன்படுத்தும் உங்கள் திறனை மதிப்பிடுகிறது।*
    """)
    
    # DHLI Questions (10-item simplified version for oral administration)
    dhli_questions = {
        'DHLI_Q1': {
            'english': "Do you have access to a mobile phone for health info?",
            'tamil': "உங்கள் மொபைல் போனில் சுகாதார தகவல்களைப் பெற முடியுமா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)']
        },
        'DHLI_Q2': {
            'english': "Can you use a phone to call for medical advice?",
            'tamil': "மருத்துவ ஆலோசனைக்காக போன் செய்ய முடியுமா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)']
        },
        'DHLI_Q3': {
            'english': "Do you know how to send/receive SMS health messages?",
            'tamil': "SMS சுகாதார செய்திகளை அனுப்ப/பெற முடியுமா?",
            'options': ['Disagree (ஒப்புக்கொள்ளவில்லை)', 'Agree (ஒப்புக்கொள்கிறேன்)']
        },
        'DHLI_Q4': {
            'english': "Can you find health info using voice calls or simple apps?",
            'tamil': "குரல் அழைப்பு அல்லது எளிய ஆப் மூலம் சுகாதார தகவலைத் தேட முடியுமா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)']
        },
        'DHLI_Q5': {
            'english': "Do you check if phone/online health info is reliable?",
            'tamil': "போன்/ஆன்லைன் சுகாதார தகவல் நம்பகமானதா என சரிபார்க்கிறீர்களா?",
            'options': ['Disagree (ஒப்புக்கொள்ளவில்லை)', 'Agree (ஒப்புக்கொள்கிறேன்)']
        },
        'DHLI_Q6': {
            'english': "Can you understand health videos/audio on phone?",
            'tamil': "போனில் சுகாதார வீடியோ/ஆடியோவைப் புரிந்து கொள்ள முடியுமா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)']
        },
        'DHLI_Q7': {
            'english': "Do you use digital tools (e.g., SMS) to remember appointments?",
            'tamil': "appointment-களை நினைவூட்ட எஸ்எம்எஸ் போன்ற டிஜிட்டல் கருவிகளைப் பயன்படுத்துகிறீர்களா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)']
        },
        'DHLI_Q8': {
            'english': "Can you share health info with family via phone?",
            'tamil': "குடும்பத்துடன் சுகாதார தகவலை போன் மூலம் பகிர முடியுமா?",
            'options': ['Disagree (ஒப்புக்கொள்ளவில்லை)', 'Agree (ஒப்புக்கொள்கிறேன்)']
        },
        'DHLI_Q9': {
            'english': "Do you face problems using digital health services due to language/tech barriers?",
            'tamil': "மொழி/டெக் காரணமாக டிஜிட்டல் சுகாதார சேவைகளில் சிக்கல்கள் உண்டா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)'],
            'reverse_score': True
        },
        'DHLI_Q10': {
            'english': "Would you use phone-based TB reminders if available?",
            'tamil': "கிடைக்குமானால் போன் அடிப்படையிலான டிபி நினைவூட்டிகளைப் பயன்படுத்துவீர்களா?",
            'options': ['No (இல்லை)', 'Yes (ஆம்)']
        }
    }
    
    st.subheader("📋 DHLI Questions (டிஜிட்டல் சுகாதார)")
    st.write("*Please select your response for each question. Score: Yes/Agree = 1, No/Disagree = 0*")
    
    # Display questions
    for q_num in range(1, 11):
        q_key = f'DHLI_Q{q_num}'
        question_data = dhli_questions[q_key]
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.write(f"**Q{q_num}.** {question_data['english']}")
            st.write(f"*{question_data['tamil']}*")
            
            # Radio button for response
            response = st.radio(
                f"Response Q{q_num}",
                options=[0, 1],
                format_func=lambda x: question_data['options'][x],
                index=st.session_state.participant_data[q_key],
                key=f"radio_{q_key}",
                label_visibility="collapsed"
            )
            
            # Handle reverse scoring for Q9
            if question_data.get('reverse_score', False):
                st.session_state.participant_data[q_key] = 1 - response  # Reverse score
                st.caption("*Note: This question is reverse-scored (No = 1, Yes = 0)*")
            else:
                st.session_state.participant_data[q_key] = response
        
        with col2:
            actual_score = st.session_state.participant_data[q_key]
            st.metric(f"Q{q_num} Score", actual_score)
        
        st.divider()
    
    # Calculate total DHLI score
    total_score = sum([st.session_state.participant_data[f'DHLI_Q{i}'] for i in range(1, 11)])
    st.session_state.participant_data['DHLI_Total_Score'] = total_score
    
    st.subheader("📊 Digital Health Literacy Score Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total DHLI Score",
            f"{total_score}/10",
            help="Sum of all 10 DHLI questions (0-10 scale)"
        )
    
    with col2:
        # DHLI interpretation based on score
        if total_score >= 7:
            level = "High"
            color = "🟢"
        elif total_score >= 4:
            level = "Moderate" 
            color = "🟡"
        else:
            level = "Low"
            color = "🔴"
        
        st.metric(
            "Digital Health Literacy Level",
            f"{color} {level}",
            help=f"Based on DHLI score: {total_score}/10. ≤6 indicates low digital health literacy"
        )
    
    with col3:
        # Clinical interpretation for TB care
        if total_score <= 6:
            interpretation = "May need extra support with digital TB care tools"
            delta = "⚠️ Low literacy flagged"
        else:
            interpretation = "Can likely use digital TB care tools effectively"
            delta = "✅ Adequate literacy"
        
        st.metric(
            "Clinical Interpretation",
            interpretation[:20] + "..." if len(interpretation) > 20 else interpretation,
            delta=delta,
            help=f"Full interpretation: {interpretation}"
        )
    
    # Additional information box
    st.info("""
    **DHLI Scoring & Interpretation:**
    - **Score 0-6**: Low digital health literacy - may experience 1.5-2x longer patient delays
    - **Score 7-10**: Adequate digital health literacy - can effectively use digital health tools
    - **Clinical relevance**: Low scores correlate with treatment delays and may require additional support for digital TB care interventions
    """)
    
    # Display individual question breakdown
    with st.expander("📈 View Individual Question Scores"):
        score_data = []
        for i in range(1, 11):
            q_key = f'DHLI_Q{i}'
            score_data.append({
                'Question': f'Q{i}',
                'English': dhli_questions[q_key]['english'][:50] + "...",
                'Score': st.session_state.participant_data[q_key],
                'Response': dhli_questions[q_key]['options'][st.session_state.participant_data[q_key]]
            })
        
        import pandas as pd
        df_scores = pd.DataFrame(score_data)
        st.dataframe(df_scores, use_container_width=True)

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
        st.write(f"• Patient Delay: {data['Patient_Delay']} days")
        st.write(f"• Healthcare Provider-related Delay: {data['Healthcare_Provider_Related_Delay']} days")
        st.write(f"• Treatment Delay: {data['Treatment_Delay']} days")
        st.write(f"• Total Delay: {data['Total_Delay']} days")
        st.write(f"• TB Unit (TU): {data['TB_Unit_TU']} days")
        st.write(f"• Healthcare Providers: {data['Healthcare_Providers']} days")
        st.write(f"• No Delay: {data['No_Delay']}")
        
        st.write("**DHLI Score:**")
        st.write(f"• Total Score: {data['DHLI_Total_Score']}/10")
        
        # DHLI level
        if data['DHLI_Total_Score'] >= 7:
            level = "High"
        elif data['DHLI_Total_Score'] >= 4:
            level = "Moderate"
        else:
            level = "Low"
        st.write(f"• Digital Health Literacy Level: {level}")
    
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
        if st.button("📊 Export Patient Data", type="primary"):
            # Get sample data
            sample_df = generate_sample_data()
            
            # Create current patient DataFrame
            current_patient_df = create_export_dataframe()
            
            # Ensure columns match between current patient and sample data
            # Get common columns that exist in both datasets
            current_columns = set(current_patient_df.columns)
            sample_columns = set(sample_df.columns)
            common_columns = list(current_columns & sample_columns)
            
            # Add missing columns to sample data to match current patient structure
            for col in current_columns:
                if col not in sample_df.columns:
                    if col in ['Verification_Notes', 'Data_Verified']:
                        sample_df[col] = ['' if col == 'Verification_Notes' else False] * len(sample_df)
                    else:
                        sample_df[col] = [''] * len(sample_df)
            
            # Add missing columns to current patient data to match sample structure
            for col in sample_columns:
                if col not in current_patient_df.columns:
                    current_patient_df[col] = ['']
            
            # Align column order - use current patient column order as primary
            final_columns = list(current_patient_df.columns)
            
            # Reorder both DataFrames to have same column order
            current_patient_aligned = current_patient_df[final_columns]
            sample_df_aligned = sample_df[final_columns]
            
            # Combine the datasets - current patient first, then sample data
            combined_df = pd.concat([current_patient_aligned, sample_df_aligned], ignore_index=True)
            
            # Display preview
            st.subheader(f"📋 Combined Dataset Export Preview ({len(combined_df)} Patients)")
            st.write(f"**Includes:** Current patient + {len(sample_df)} sample patients")
            st.dataframe(combined_df, use_container_width=True)
            
            # Generate CSV for download
            csv_data = combined_df.to_csv(index=False)
            
            # Create filename
            participant_id = data['Participant_ID'] if data['Participant_ID'] else 'UNKNOWN'
            filename = f"tb_study_combined_data_{participant_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            st.download_button(
                label="💾 Download Combined Dataset (CSV)",
                data=csv_data,
                file_name=filename,
                mime="text/csv",
                help="Download current patient data combined with sample patients"
            )
            
            st.success(f"✅ Combined dataset ready with {len(combined_df)} patients!")

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
        'Patient_Delay': [data['Patient_Delay']],
        'Healthcare_Provider_Related_Delay': [data['Healthcare_Provider_Related_Delay']],
        'Treatment_Delay': [data['Treatment_Delay']],
        'Total_Delay': [data['Total_Delay']],
        'TB_Unit_TU': [data['TB_Unit_TU']],
        'Healthcare_Providers': [data['Healthcare_Providers']],
        'No_Delay': [data['No_Delay']],
        
        # Specific delay reasons for each gap
        'Patient_Delay_Specific_Reason': [data['Patient_Delay_Specific_Reason']],
        'Provider_Delay_Specific_Reason': [data['Provider_Delay_Specific_Reason']],
        'Treatment_Delay_Specific_Reason': [data['Treatment_Delay_Specific_Reason']],
        
        # Questionnaire responses
        'Symptoms_Nature': ['; '.join(data['Symptoms_Nature'])],
        'First_Care_Location': [data['First_Care_Location']],
        'Patient_Delay_Reason': ['; '.join(data['Patient_Delay_Reason'])],
        'Healthcare_Visits_Count': [data['Healthcare_Visits_Count']],
        'Diagnostic_Tests': ['; '.join(data['Diagnostic_Tests'])],
        'Treatment_Delay_Experienced': [data['Treatment_Delay_Experienced']],
        'Treatment_Delay_Reason': ['; '.join(data['Treatment_Delay_Reason'])],
        'Provider_Awareness': [data['Provider_Awareness']],
        'Provider_Explanation': [data['Provider_Explanation']],
        'Provider_Difficulties': [data['Provider_Difficulties']],
        'Provider_Difficulties_Details': ['; '.join(data['Provider_Difficulties_Details'])],
        'Treatment_Satisfaction': [data['Treatment_Satisfaction']],
        'TB_Stigma': [data['TB_Stigma']],
        'Family_History': [data['Family_History']],
        'Family_History_Year': [data['Family_History_Year']],
        'Additional_Support_Needed': ['; '.join(data['Additional_Support_Needed'])],
        
        # DHLI scores (individual questions)
        'DHLI_Q1': [data['DHLI_Q1']],
        'DHLI_Q2': [data['DHLI_Q2']],
        'DHLI_Q3': [data['DHLI_Q3']],
        'DHLI_Q4': [data['DHLI_Q4']],
        'DHLI_Q5': [data['DHLI_Q5']],
        'DHLI_Q6': [data['DHLI_Q6']],
        'DHLI_Q7': [data['DHLI_Q7']],
        'DHLI_Q8': [data['DHLI_Q8']],
        'DHLI_Q9': [data['DHLI_Q9']],
        'DHLI_Q10': [data['DHLI_Q10']],
        'DHLI_Total_Score': [data['DHLI_Total_Score']],
        
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
    
    # Define sections
    sections = [
        ("📋 Demographics & Clinical Info", section_demographics),
        ("📅 Digital Pathway Mapping", section_digital_pathway),
        ("📱 DHLI Assessment", section_dhli),
        ("� Data Visualization", section_visualization),
        ("✅ Verification & Export", section_verification)
    ]
    
    # Current section indicator
    current_section_name = sections[st.session_state.current_section][0]
    st.write(f"**Section {st.session_state.current_section + 1}/{len(sections)}:** {current_section_name}")
    
    st.markdown("---")
    
    # Sidebar info
    st.sidebar.title("📋 Study Information")
    st.sidebar.markdown("**Cross-sectional TB Study**")
    st.sidebar.markdown("Chennai, Tamil Nadu")
    st.sidebar.markdown("---")
    
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
        ("Delays", st.session_state.participant_data['Total_Delay'] > 0),
        ("DHLI", st.session_state.participant_data['DHLI_Total_Score'] > 0),
        ("Verified", st.session_state.participant_data['Data_Verified'])
    ]
    
    for item, completed in progress_items:
        status = "✅" if completed else "⏳"
        st.sidebar.markdown(f"{status} {item}")
    
    # Display current section
    current_section_func = sections[st.session_state.current_section][1]
    current_section_func()
    
    # Navigation buttons at bottom
    st.markdown("---")
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
    
    with col_nav1:
        if st.button("⬅️ Previous", disabled=(st.session_state.current_section == 0)):
            st.session_state.current_section = max(0, st.session_state.current_section - 1)
            st.rerun()
    
    with col_nav2:
        if st.button("➡️ Next", disabled=(st.session_state.current_section == len(sections) - 1)):
            st.session_state.current_section = min(len(sections) - 1, st.session_state.current_section + 1)
            st.rerun()
    
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