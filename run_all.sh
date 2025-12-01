#!/bin/bash

# Complete setup and run script for IEP RAG System
# This script will guide through the entire setup process

echo "=========================================="
echo "IEP RAG System - Complete Setup"
echo "=========================================="
echo ""

# Check if conda environment is activated
if [[ -z "${CONDA_DEFAULT_ENV}" ]]; then
    echo "  Warning: No conda environment detected"
    echo "Please activate your conda environment first:"
    echo "  conda activate iep_rag"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
else
    echo " Conda environment active: ${CONDA_DEFAULT_ENV}"
fi

echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "  .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "  IMPORTANT: You need to edit .env and add your OpenAI API key"
    echo "Open .env in a text editor and replace 'your_openai_api_key_here' with your actual API key"
    echo ""
    read -p "Press Enter after you've added your API key to .env..."
else
    echo " .env file exists"
fi

echo ""
echo "Step 1: Running setup to initialize data and vector store..."
echo "=========================================="
python setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo " Setup failed. Please check the error messages above."
    exit 1
fi

echo ""
echo " Setup completed successfully!"
echo ""
echo "=========================================="
echo "Would you like to:"
echo "  1) Run the Streamlit web application"
echo "  2) Run the test script"
echo "  3) Exit"
echo "=========================================="
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Streamlit application..."
        echo "The app will open in your browser at http://localhost:8501"
        echo ""
        streamlit run app.py
        ;;
    2)
        echo ""
        echo "Running test script..."
        echo "=========================================="
        python test_system.py
        ;;
    3)
        echo ""
        echo "Setup complete! You can run the application anytime with:"
        echo "  streamlit run app.py"
        echo ""
        echo "Or run tests with:"
        echo "  python test_system.py"
        ;;
    *)
        echo ""
        echo "Invalid choice. Exiting."
        echo "You can run the application with: streamlit run app.py"
        ;;
esac

echo ""
echo "Done!"
