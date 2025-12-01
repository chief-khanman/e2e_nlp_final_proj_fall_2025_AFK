# START HERE - IEP RAG System

## Quick Steps to Run

### Step 1: Add Your OpenAI API Key (2 minutes)

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# OR
code .env
# OR
nvim .env

# Replace this line:
OPENAI_API_KEY=your_openai_api_key_here

# With your actual key (starts with sk-):
OPENAI_API_KEY='sk-proj-xxxxxxxxxxxxx'
```

**Get an API key**: https://platform.openai.com/api-keys

### Step 2: Initialize the System (1-2 minutes)

```bash
python setup.py
```

This will:
- Create sample occupational data (5 common jobs)
- Generate educational standards
- Create IEP templates
- Process all documents
- Build the vector database

**Expected output**: You should see "SETUP COMPLETE!" at the end.

### Step 3: Run the Application

```bash
streamlit run app.py
```

OR use the interactive script:

```bash
./run_all.sh
```

Your browser will open to http://localhost:8501

## Test It Out

1. Click **"Load Clarence Example"** in the sidebar
2. Click **"Generate IEP Goals"** button
3. Wait 30-60 seconds
4. Review the generated goals!

---

**Ready?** Run these three commands:

```bash
cp .env.example .env
# Edit .env to add your API key
python setup.py
streamlit run app.py
```


