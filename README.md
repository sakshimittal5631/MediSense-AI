# MediSense-AI

MediSense-AI is a web-based application designed to assist users in diagnosing diseases based on reported symptoms and to recommend appropriate medications. Leveraging machine learning algorithms, the platform aims to provide accurate and personalized healthcare advice.

## Features
- **Symptom-Based Diagnosis:** Users can input their symptoms, and the system will predict potential diseases.  
- **Medication Recommendations:** Based on the diagnosed condition, the application suggests suitable medications.  
- **User-Friendly Interface:** A responsive and intuitive interface designed for a seamless user experience.  

## Installation

To set up the project locally:  

### Clone the Repository
```sh
git clone https://github.com/sakshimittal5631/MediSense-AI.git
cd MediSense-AI
```

## Create and Activate a Virtual Environment

**On Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

**On macOS and Linux:**
```sh
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies
```sh
pip install -r requirements.txt
```

## Run the Application
```sh
uvicorn main:app --reload
```
The application will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Project Structure
```
MediSense-AI/
├── datasets/           # Contains CSV files with medical data
├── models/             # Stores machine learning models (e.g., svc.pkl)
├── routers/            # Contains FastAPI route handlers
├── static/             # Static files like images and CSS
├── templates/          # HTML templates for rendering pages
├── main.py             # Main application entry point
├── requirements.txt    # List of project dependencies
└── .gitignore          # Specifies files and directories to be ignored by Git
```

## Dependencies
- **FastAPI**: Web framework for building APIs.
- **scikit-learn**: Machine learning library for Python.
- **pandas**: Data analysis and manipulation library.
- **numpy**: Numerical computing library.

For a complete list, refer to `requirements.txt`.

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-branch
   ```
3. Make your changes and commit them:
   ```sh
   git commit -m "Add new feature"
   ```
4. Push your changes:
   ```sh
   git push origin feature-branch
   ```
5. Open a Pull Request on GitHub.
