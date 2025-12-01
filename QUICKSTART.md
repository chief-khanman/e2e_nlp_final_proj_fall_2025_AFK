# Quick Start Guide

Follow these steps to get the IEP Goal Generator running on your system.

## Prerequisites

- Python 3.11+ installed
- Conda environment created and activated with dependencies installed
- OpenAI API key (get one from https://platform.openai.com/api-keys)

## Step-by-Step Setup

### 1. Configure Your API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file and add your OpenAI API key
# Replace "your_openai_api_key_here" with your actual key
```

**Important**: Never commit your `.env` file to version control!

### 2. Initialize the System

Run the setup script to create sample data and build the vector database:

```bash
python setup.py
```

This will take 1-2 minutes and will:
- Create sample occupational data (5 common occupations)
- Generate educational standards (21st Century Skills, Employability Skills)
- Create IEP templates and examples
- Process all documents into chunks
- Build the ChromaDB vector database with embeddings

You should see output like:
```
================================================================================
IEP RAG SYSTEM SETUP
================================================================================

Step 1: Collecting data...
--------------------------------------------------------------------------------
Creating sample OOH data with 5 occupations...
Created educational standards...
Created IEP samples...

Step 2: Processing documents and creating vector database...
--------------------------------------------------------------------------------
Processing all documents...
Created X occupation documents
Created X educational standard documents
Created X IEP sample documents
...
```

### 3. Run the Application

Start the Streamlit web interface:

```bash
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501`

### 4. Generate Your First IEP

In the web interface:

1. **Load the sample student**: Click "Load Clarence Example" in the sidebar
2. **Click "Generate IEP Goals"** button
3. **Wait 30-60 seconds** for the AI to generate the goals
4. **Review the results** in the right panel

### 5. Try Your Own Student

1. Clear the form and enter your own student information
2. Fill in at least: Name, Age, Grade, and Career Interest
3. Click "Generate IEP Goals"
4. Download the results using the download button

## Testing the System

To verify everything is working without the web interface:

```bash
python test_system.py
```

This will:
- Test the retrieval component with sample queries
- Generate a complete IEP for "Clarence"
- Show the retrieved context documents
- Display the generated goals

## Troubleshooting

### "Error initializing system"
- Check that you ran `python setup.py`
- Verify the `data/chroma_db` directory was created

### "OpenAI API key not found"
- Make sure you created the `.env` file (copy from `.env.example`)
- Add your actual API key to the `.env` file
- Restart the application

### "No module named 'src'"
- Make sure you're running commands from the project root directory
- The `src/__init__.py` file should exist

### Import errors
- Activate your conda environment: `conda activate NLP`
- Reinstall dependencies: `pip install -r requirements.txt`

### Slow generation
- First generation is slower (loading models)
- Subsequent generations should be faster
- Using GPT-4 is slower but higher quality than GPT-3.5

## What's Next?

- Customize the prompts in `src/prompts.py`
- Add more occupational data in `src/data_collection.py`
- Adjust retrieval settings in `config.py`
- Modify the UI in `app.py`

## File Locations

- **Generated data**: `data/raw/`
- **Processed documents**: `data/processed/`
- **Vector database**: `data/chroma_db/`
- **Configuration**: `config.py` and `.env`

## Need Help?

1. Check the full README.md for detailed documentation
2. Review error messages carefully
3. Verify all setup steps were completed
4. Check that your API key has sufficient credits

## Example Workflow

```bash
# Complete setup workflow
cd /Users/aadit/Dev/e2e_nlp_final_proj_fall_2025
conda activate NLP
cp .env.example .env
# Edit .env to add your API key
python setup.py
streamlit run app.py
```

That's it! You should now have a fully functional IEP Goal Generator.
