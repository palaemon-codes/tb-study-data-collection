# TB Study Data Collection Application

A comprehensive Streamlit web application for cross-sectional TB study data collection in Chennai, featuring digital pathway mapping and eHealth literacy assessment.

## 🏥 Features

### 📋 Section 1: Demographics & Clinical Information
- Complete demographic data collection
- TB type classification
- Symptom assessment
- Clinical history and comorbidities
- **Delay reason assessment** with specific causes

### 📅 Section 2: Digital Pathway Mapping
- Critical timeline events tracking:
  - Date of symptom onset
  - Date of first healthcare visit
  - Date of TB diagnosis confirmation
  - Date of treatment initiation
- **Automatic delay calculations** (Patient, Provider, Treatment, Total)
- Date validation with chronological sequence checking

### 📊 Section 3: Advanced Data Visualization
- **Horizontal bar chart** showing delay magnitudes
- **eHEALS Score vs Treatment Delay** correlation analysis
- **Patient delay reasons** frequency analysis
- WHO benchmark comparisons (7-day targets)
- Real-time delay insights and categorization

### 💻 Section 4: eHealth Literacy Scale (eHEALS)
- Complete 10-question eHEALS assessment
- Proper 5-point Likert scale implementation
- Automatic scoring and literacy level classification
- Separate handling of supplementary vs formal scale questions

### ✅ Section 5: Verification & Export
- Data verification against medical records
- Field worker notes and observations
- **Complete CSV export** with all calculated values
- Dynamic filename generation with timestamps

## 🚀 Key Improvements

### Enhanced Delay Analysis
- **Specific delay reasons**: Financial constraints, lack of awareness, stigma, healthcare access
- **Provider-related challenges**: Diagnostic delays, information gaps, empathy issues
- **Treatment barriers**: Medicine availability, test results, urgency awareness

### Advanced Analytics
- **Correlation analysis** between digital literacy and treatment delays
- **Delay pattern visualization** with color-coded insights
- **Benchmark comparisons** against WHO recommended targets

### Improved User Experience
- **Next/Previous button navigation** for streamlined workflow
- **Progress tracking** with visual indicators
- **Section jumping** for quick navigation
- **Real-time validation** with specific error messages

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation
```bash
# Clone the repository
git clone https://github.com/palaemon-codes/tb-study-data-collection.git
cd tb-study-data-collection

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run tb_study_app.py
```

The application will open in your browser at `http://localhost:8501`

### Online Deployment (Streamlit Community Cloud)

1. **Fork/Clone this repository** to your GitHub account
2. **Visit [share.streamlit.io](https://share.streamlit.io)**
3. **Sign in** with your GitHub account
4. **Click "New app"** and select this repository
5. **Set main file** as `tb_study_app.py`
6. **Click "Deploy"**

Your app will be live at: `https://your-username-tb-study-data-collection-tb-study-app-xyz123.streamlit.app`

## 📊 Data Structure

The application exports comprehensive data including:

### Core Identifiers
- Participant ID, Name/Initials, Collection Date

### Demographics
- Age, Gender, Address, Occupation, Education
- Income level, Marital status, Residence type
- Comorbidities, TB type, Substance use

### Timeline Data
- All four critical dates
- Calculated delays (Patient, Provider, Treatment, Total)

### Delay Analysis
- Specific reasons for each delay type
- Provider-related challenges
- Treatment barriers and solutions

### eHealth Literacy
- Individual question scores (Q1-Q10)
- Total eHEALS score and literacy level

### Verification
- Data verification status
- Field worker notes and observations

## 🎯 Use Cases

### Research Applications
- **Cross-sectional TB studies** with delay analysis
- **Digital health literacy** assessment in healthcare
- **Healthcare pathway mapping** and optimization
- **Provider performance** analysis and improvement

### Clinical Applications
- **Patient intake** and assessment
- **Care coordination** and timeline tracking
- **Quality improvement** initiatives
- **Staff training** and standardization

### Public Health Applications
- **Epidemiological surveillance** and reporting
- **Healthcare system** performance monitoring
- **Policy development** and evidence generation
- **Community health** program evaluation

## 📈 Analytics Dashboard

### Real-time Insights
- **Delay categorization** (Patient vs Provider vs Treatment)
- **Risk assessment** with WHO benchmark comparisons
- **Correlation analysis** between literacy and delays

### Export Capabilities
- **Single-patient CSV** export for immediate use
- **Comprehensive data structure** for analysis
- **Timestamp tracking** for audit trails
- **Field verification** status for quality control

## 🔐 Data Privacy & Security

- **Local data storage** in session state (no cloud storage)
- **Manual export control** - data only saved when explicitly exported
- **Session isolation** - each user session is independent
- **No automatic data transmission** - full user control over data sharing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is developed for research purposes in TB care analysis and digital health assessment.

## 📞 Support

For questions about the application or deployment, please create an issue in this repository.

---

**TB Study Data Collection App** | Cross-sectional TB Study, Chennai | Digital pathway mapping and eHealth literacy assessment platform