# MediSense-AI

MediSense-AI is a web-based application designed to assist users in diagnosing diseases based on reported symptoms and to recommend appropriate medications. Leveraging machine learning algorithms, the platform aims to provide accurate and personalized healthcare advice.

## Features

- **Symptom-Based Diagnosis:** Users can input their symptoms, and the system will predict potential diseases.
- **Medication Recommendations:** Based on the diagnosed condition, the application suggests suitable medications.
- **User-Friendly Interface:** A responsive and intuitive interface designed for seamless user experience.

## Installation

To set up the project locally:

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/sakshimittal5631/MediSense-AI.git
   cd MediSense-AI
   
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS and Linux
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Application:
uvicorn main:app --reload

# Project Structure
MediSense-AI/
├── datasets/           # Contains CSV files with medical data
├── models/             # Stores machine learning models (e.g., svc.pkl)
├── routers/            # Contains FastAPI route handlers
├── static/             # Static files like images and CSS
├── templates/          # HTML templates for rendering pages
├── main.py             # Main application entry point
├── requirements.txt    # List of project dependencies
└── .gitignore          # Specifies files and directories to be ignored by Git

# Dependencies

  FastAPI: Web framework for building APIs.

  scikit-learn: Machine learning library for Python.

  pandas: Data analysis and manipulation library.

  numpy: Numerical computing library.

# For a complete list, refer to requirements.txt.
Contributing

# Contributions are welcome! Please follow these steps:

  Fork the repository.

  Create a new branch (git checkout -b feature-branch).

  Commit your changes (git commit -m 'Add new feature').

  Push to the branch (git push origin feature-branch).

  Open a Pull Request.
