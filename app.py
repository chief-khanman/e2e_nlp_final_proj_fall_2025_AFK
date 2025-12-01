import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from rag_pipeline import IEPRAGPipeline
from config import config

# Page configuration
st.set_page_config(
    page_title="IEP Goal Generator",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_iep' not in st.session_state:
    st.session_state.generated_iep = None
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None

def initialize_pipeline():
    """Initialize the RAG pipeline"""
    if st.session_state.pipeline is None:
        with st.spinner("Initializing IEP Generation System... This may take a moment."):
            try:
                use_openai = config.OPENAI_API_KEY is not None and config.OPENAI_API_KEY != ""
                st.session_state.pipeline = IEPRAGPipeline(use_openai=use_openai)
                return True
            except Exception as e:
                st.error(f"Error initializing system: {str(e)}")
                return False
    return True

def main():
    # Header
    st.markdown('<h1 class="main-header">IEP Transition Goal Generator</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>Welcome to the IEP Goal Generator!</strong><br>
    This system uses AI to generate individualized education program (IEP) transition goals
    aligned with industry standards and educational frameworks. Enter student information below
    to generate comprehensive, measurable goals.
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.header("About This System")
        st.write("""
        This RAG-based system generates IEP transition goals by:

        1. Analyzing student interests and assessments
        2. Retrieving relevant career information from the Occupational Outlook Handbook
        3. Aligning goals with 21st Century Skills
        4. Ensuring IDEA 2004 compliance

        **Data Sources:**
        - Bureau of Labor Statistics OOH
        - 21st Century Skills Framework
        - Employability Skills Standards
        - IEP Best Practices
        """)

        st.divider()

        st.header("Sample Student")
        if st.button("Load Clarence Example"):
            st.session_state.sample_loaded = True

    # Main content area with two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown('<div class="section-header">Student Information</div>', unsafe_allow_html=True)

        # Check if sample should be loaded
        sample_loaded = st.session_state.get('sample_loaded', False)

        # Student information form
        student_name = st.text_input(
            "Student Name",
            value="Clarence" if sample_loaded else "",
            help="Enter the student's first name"
        )

        col_age, col_grade = st.columns(2)
        with col_age:
            age = st.text_input(
                "Age",
                value="15" if sample_loaded else "",
                help="Student's current age"
            )
        with col_grade:
            grade = st.text_input(
                "Grade",
                value="10th grade (Sophomore)" if sample_loaded else "",
                help="Current grade level"
            )

        disability = st.text_input(
            "Disability/Diagnosis",
            value="Behavior disorder" if sample_loaded else "",
            help="Primary disability category"
        )

        interests = st.text_area(
            "Interests and Strengths",
            value="Enterprising activities, hands-on learning, prefers hands-on over academic instruction" if sample_loaded else "",
            help="What does the student enjoy? What are they good at?",
            height=100
        )

        career_interest = st.text_input(
            "Career Interest(s)",
            value="Retail sales, driver/sales worker, working at Walmart" if sample_loaded else "",
            help="What jobs or careers is the student interested in?"
        )

        assessment_results = st.text_area(
            "Assessment Results",
            value="O*Net Interest Profiler shows strength in Enterprising category. Vision for the Future interview indicates interest in working at Walmart as a sales associate." if sample_loaded else "",
            help="Results from career assessments, interest inventories, etc.",
            height=100
        )

        additional_info = st.text_area(
            "Additional Information (Optional)",
            value="",
            help="Any other relevant information about the student",
            height=80
        )

        st.divider()

        # Generate button
        generate_button = st.button("Generate IEP Goals", type="primary")

        if generate_button:
            # Validate inputs
            if not student_name or not age or not grade:
                st.error("Please fill in at least Name, Age, and Grade.")
            elif not career_interest:
                st.error("Please provide at least one career interest.")
            else:
                # Initialize pipeline
                if not initialize_pipeline():
                    st.error("Failed to initialize the system. Please check your configuration.")
                else:
                    # Prepare student info
                    student_info = {
                        "name": student_name,
                        "age": age,
                        "grade": grade,
                        "disability": disability,
                        "interests": interests,
                        "career_interest": career_interest,
                        "assessment_results": assessment_results,
                        "additional_info": additional_info
                    }

                    # Generate IEP
                    with st.spinner("Generating IEP goals... This may take up to a minute."):
                        try:
                            result = st.session_state.pipeline.generate_complete_iep(student_info)
                            st.session_state.generated_iep = result
                            st.success("IEP goals generated successfully!")
                        except Exception as e:
                            st.error(f"Error generating IEP: {str(e)}")
                            st.error("Please check your API key configuration in the .env file.")

    with col2:
        st.markdown('<div class="section-header">Generated IEP Goals</div>', unsafe_allow_html=True)

        if st.session_state.generated_iep:
            result = st.session_state.generated_iep

            # Display generated IEP
            st.markdown(result["complete_iep"])

            st.divider()

            # Show retrieved context
            with st.expander("View Retrieved Context and Sources"):
                st.write("**Documents used to generate these goals:**")
                for i, doc in enumerate(result.get("context_documents", []), 1):
                    st.write(f"**Document {i}:**")
                    st.write(f"- Source: {doc['metadata'].get('source', 'Unknown')}")
                    st.write(f"- Type: {doc['metadata'].get('type', 'Unknown')}")
                    st.write(f"- Content Preview: {doc['content'][:200]}...")
                    st.divider()

            # Download button
            st.download_button(
                label="Download IEP Goals",
                data=result["complete_iep"],
                file_name=f"IEP_Goals_{student_name.replace(' ', '_')}.txt",
                mime="text/plain"
            )

        else:
            st.info("Fill in the student information and click 'Generate IEP Goals' to see results here.")

    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    <strong>Note:</strong> This system is designed to assist special education professionals in creating IEP goals.
    All generated goals should be reviewed and customized by qualified educators before use.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
