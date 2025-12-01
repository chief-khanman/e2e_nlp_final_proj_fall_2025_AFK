# IEP Goal Generator - RAG System for Special Education

A Retrieval-Augmented Generation (RAG) system that assists special education professionals in creating Individualized Education Program (IEP) goals for students with disabilities. The system generates measurable postsecondary goals and short-term objectives aligned with industry standards and educational frameworks.

## Overview

This system uses advanced AI and retrieval techniques to generate high-quality IEP transition goals by:

1. **Retrieving relevant information** from:
   - Bureau of Labor Statistics Occupational Outlook Handbook
   - 21st Century Skills standards
   - Employability Skills frameworks
   - IEP best practices and templates

2. **Generating customized goals** that are:
   - Measurable and specific
   - Aligned with student interests and abilities
   - Compliant with IDEA 2004 requirements
   - Connected to industry and educational standards

## Features

- **Interactive Web Interface**: User-friendly Streamlit application
- **Comprehensive Goal Generation**: Creates postsecondary goals, annual goals, and short-term objectives
- **Standards Alignment**: Automatically aligns goals with OOH requirements and educational standards
- **Context-Aware**: Uses RAG to retrieve relevant career and skills information
- **Flexible LLM Support**: Works with OpenAI GPT models or local models via Ollama

## Project Structure

```
e2e_nlp_final_proj_fall_2025/
├── app.py                      # Streamlit web application
├── config.py                   # Configuration settings
├── setup.py                    # System setup script
├── test_system.py              # Testing script
├── requirements.txt            # Python dependencies
├── environment.yaml            # Conda environment file
├── .env.example               # Environment variables template
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   ├── data_collection.py     # Data collection and sample generation
│   ├── preprocessing.py       # Document preprocessing and chunking
│   ├── vector_store.py        # Vector database management
│   ├── prompts.py             # Prompt templates
│   └── rag_pipeline.py        # Main RAG pipeline
└── data/
    ├── raw/                   # Raw data files
    ├── processed/             # Processed documents
    └── chroma_db/             # Vector database storage
```


### Prerequisites

- Python 3.8 or higher
- Conda (recommended) or pip
- OpenAI API key (for using GPT models)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd /Users/aadit/Dev/e2e_nlp_final_proj_fall_2025
   ```

2. **Create and activate conda environment** :
   ```bash
   conda env create -f environment.yaml
   conda activate NLP
   ```

3. **Install dependencies** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```

5. **Run the setup script** to initialize data and vector database:
   ```bash
   python setup.py
   ```

   This will:
   - Create sample occupational data
   - Generate educational standards
   - Create IEP templates
   - Process all documents
   - Build the vector database

## Usage

### Running the Web Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Enter Student Information**:
   - Name, age, grade
   - Disability category
   - Interests and strengths
   - Career interests
   - Assessment results

2. **Click "Generate IEP Goals"**

3. **Review Generated Goals**:
   - Postsecondary employment and education goals
   - Annual measurable goal with standards alignment
   - Short-term objectives/benchmarks
   - Explanation of connections

4. **Download Results**: Click the download button to save the generated IEP goals

### Testing the System

Run the test script to verify everything works:

```bash
python test_system.py
```

This will:
- Test the retrieval component
- Generate a complete IEP for the sample student "Clarence"
- Display the results and context documents used

## Configuration

Edit `config.py` or `.env` file to customize:

- **Embedding Model**: Default is `sentence-transformers/all-MiniLM-L6-v2`
- **LLM Model**: Default is `gpt-4o-mini`
- **Chunk Size**: Default is 1000 characters
- **Retrieval Top K**: Default is 5 documents

## How It Works

### 1. Data Collection (`src/data_collection.py`)

Creates sample data including:
- Occupational information (retail sales, delivery drivers, customer service, etc.)
- Educational standards (21st Century Skills, Employability Skills)
- IEP templates and examples

### 2. Document Processing (`src/preprocessing.py`)

- Loads and processes all data sources
- Chunks documents into appropriate sizes
- Preserves metadata for retrieval

### 3. Vector Database (`src/vector_store.py`)

- Creates embeddings using HuggingFace or OpenAI models
- Stores in ChromaDB for efficient retrieval
- Enables semantic search

### 4. RAG Pipeline (`src/rag_pipeline.py`)

- Retrieves relevant context based on student information
- Uses carefully crafted prompts to guide generation
- Generates comprehensive IEP components
- Ensures alignment with standards

### 5. Prompt Engineering (`src/prompts.py`)

Specialized prompts for:
- Postsecondary goal generation
- Annual goal creation
- Short-term objectives
- Standards alignment
- Complete IEP generation

## Sample Output

For a student interested in retail sales, the system generates:

**Postsecondary Employment Goal**:
"After high school, Clarence will obtain a full-time job at Walmart as a sales associate."

**Annual Goal**:
"In 36 weeks, Clarence will demonstrate effective workplace communication and customer service skills by appropriately greeting customers, maintaining eye contact, listening actively, and responding to customer questions in 4 out of 5 observed opportunities."

**Standards Alignment**:
- OOH: Retail Sales Workers requirements
- 21st Century Skills: Communication, Interpersonal Skills
- Employability Skills: Customer Service, Workplace Appearance

**Short-term Objectives**: Progressive steps from role-play to work-based learning


## Resources Used

- **Occupational Outlook Handbook**: https://www.bls.gov/ooh/
- **Iowa Educational Standards**: https://educate.iowa.gov/media/2762/download?inline=
- **IDEA Transition Requirements**: https://sites.ed.gov/idea/regs/b/d/300.320/b
- **LangChain Documentation**: https://python.langchain.com/docs/

## Running Instructions Summary

```bash
# 1. Setup environment and install dependencies (already done)
conda activate iep_rag

# 2. Configure API key
# Edit .env file and add your OPENAI_API_KEY

# 3. Initialize the system
python setup.py

# 4. Run the web application
streamlit run app.py

# 5. Or test the system
python test_system.py
```


## License

This project is created for educational purposes as part of an NLP course final project.

## Acknowledgments

- Bureau of Labor Statistics for occupational data
- IDEA 2004 for transition planning requirements
- LangChain for RAG framework
- OpenAI for language models
