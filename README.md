# TB Study Data Collection Application

## 🆕 **UPDATED VERSION** - Enhanced Analytics & Visualization Platform

A comprehensive Streamlit web application for cross-sectional TB study data collection in Chennai, featuring digital pathway mapping, advanced data analytics, and eHealth literacy assessment with fabricated sample data for demonstration.

## 🏥 New Features & Enhancements

### 🎯 **Updated Delay Criteria Structure**
Completely restructured delay calculations to match clinical requirements:
- **Patient Delay**: Symptom onset → First healthcare visit
- **Healthcare Provider-related Delay**: First visit → Diagnosis confirmation  
- **Treatment Delay**: Diagnosis → Treatment start
- **Total Delay**: Complete symptom onset → Treatment timeline
- **TB Unit (TU)**: TB Unit-specific processing delays
- **Healthcare Providers**: Provider-related processing delays
- **No Delay**: Boolean flag for zero-delay cases

### � **Section 1: Streamlined Demographics** *(UPDATED)*
- **Removed excessive clinical details** for focus on core demographics
- Essential patient information: ID, age, gender, TB type
- Socio-economic profiling: education, occupation, income, residence
- **Simplified workflow** for faster data entry

### 📅 **Section 2: Enhanced Digital Pathway Mapping** *(UPDATED)*
- **Specific delay reason analysis** for each phase:
  - Patient delay reasons (financial, awareness, stigma, etc.)
  - Provider delay reasons (diagnostic delays, misdiagnosis, etc.)
  - Treatment delay reasons (drug availability, counseling, etc.)
- **Improved date validation** with logical sequence checking
- **Real-time delay calculation** as dates are entered

### 📊 **Section 4: Advanced Data Visualization & Analytics** *(NEW MAJOR UPDATE)*

#### 🔹 **Multi-Tab Interface**:
1. **Current Patient Analysis**: Individual delay breakdown and insights
2. **Gantt Chart Visualization**: Timeline view similar to clinical workflow charts
3. **Data Analytics Dashboard**: Population-level statistics and insights  
4. **Sample Dataset Viewer**: 30 fabricated patients for demonstration

#### 🔹 **Gantt Chart Features**:
- **Visual timeline representation** of patient care phases
- **Color-coded by TB type** and care stage (Pre-visit, Diagnosis, Pre-treatment)
- **Interactive timeline** showing 8 representative patients
- **Clinical workflow visualization** matching provided reference image

#### 🔹 **Data Analytics Dashboard**:
- **Descriptive Statistics**: Mean, median delays across population
- **Demographics Profiling**: Age distribution, education levels, gender breakdown
- **Delay Distribution Analysis**: Histograms and box plots
- **TB Type Comparisons**: Delay patterns by TB classification
- **eHealth Literacy Correlation**: Digital literacy vs treatment delays

### 💻 **Section 3: eHealth Literacy Scale (eHEALS)** *(UNCHANGED)*
- Complete 10-question eHEALS assessment
- Proper 5-point Likert scale implementation
- Automatic scoring and literacy level classification

### ✅ **Section 5: Enhanced Verification & Export** *(MAJOR UPDATE)*

#### 🔹 **Patient Details View**:
- **Complete current patient summary** with all calculated delays
- **Updated delay criteria display** (Patient, Provider-related, Treatment, Total, TB Unit, Healthcare Providers, No Delay)
- **eHEALS score interpretation** with literacy level

#### 🔹 **Advanced Export Options**:
1. **Current Patient Export**: Individual patient data with complete timeline
2. **Combined Dataset Export**: Current patient + 30 sample patients (31 total)
3. **Sample Dataset Export**: 30 fabricated patients for demo/training

### 🎯 **Fabricated Sample Dataset** *(NEW)*
- **30 realistic patient profiles** with varied demographics
- **Complete timeline data** for all critical events
- **Diverse delay patterns** and specific reasons
- **eHEALS score variations** across literacy levels
- **TB type diversity** (Pulmonary, Extra-pulmonary)
- **Realistic date ranges** and delay distributions

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