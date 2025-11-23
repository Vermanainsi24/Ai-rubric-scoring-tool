# AI-Rubric Scoring Tool 🤖

A tool that uses **Artificial Intelligence (AI)** to automate rubric-based scoring of assignments, projects, or any rubric-driven evaluation. It combines a frontend UI, backend API, and a machine-learning model to help educators, assessors, or trainers apply consistent rubric scoring at scale.

---

## Table of Contents

- [Motivation](#motivation)  
- [Features](#features)  
- [Architecture](#architecture)  
- [Tech Stack](#tech-stack)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Running the Application](#running-the-application)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  
- [Configuration](#configuration)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact](#contact)  

---

## Motivation

In educational and training settings, applying rubrics manually can be **time-consuming, subjective, and inconsistent**. This tool aims to leverage AI and **Natural Language Processing (NLP)** to streamline rubric scoring, ensure fairness and scalability, and provide meaningful, actionable feedback quickly.

---

## Features ✨

* **Submission Upload:** Upload student submissions (text, or various file uploads like PDF, DOCX).
* **Custom Rubrics:** Define or import custom rubrics, including criteria and weightages.
* **AI/NLP Evaluation:** Uses an AI/NLP model to evaluate submissions against the rubric and generate a score plus feedback.
* **Backend API:** Built on a REST API for extensibility and integration.
* **Intuitive UI:** A user-friendly **React frontend** for ease of use by instructors or admins.
* **Processing Modes:** Supports both real-time (for individual submissions) and batch processing (for large classes).
* **Reporting:** Export results (**CSV/JSON**) and detailed feedback reports.

---

## Architecture

The system follows a three-tier architecture connecting the user interface, the application logic, and the scoring model.



* **`frontend/`**: The **React** web application that provides the user interface.
* **`backend/`**: The Python **Flask** REST API that handles requests, business logic, and orchestrates the scoring process.
* **`text/`**: Contains the Machine Learning **Model**, preprocessing scripts, and data required for NLP evaluation.
* **Database/Storage (Optional)**: For storing rubrics, evaluation results, and user data.

---

## Tech Stack 🛠️

* **Frontend**: **React**, JavaScript, CSS/HTML
* **Backend**: **Python**, **Flask**
* **Machine Learning / NLP**: Python, libraries such as **scikit-learn**, **TensorFlow / PyTorch** (as needed)
* **Data & Storage**: **SQLite** (for simple setup) / **PostgreSQL** / **MongoDB** (for production-scale data)
* **Deployment**: **Docker** (for containerisation), AWS/GCP (optional)
* **Version Control**: Git & GitHub

---

## Getting Started

Follow these steps to get a local copy of the project up and running.

### Prerequisites

You need the following software installed on your machine:

* **Node.js & npm** (for the frontend)
* **Python 3.8+** (for the backend & ML component)
* **pip / virtualenv** for Python dependencies
* (Optional) **Docker** for containerised setup

### Installation

1.  **Clone this repository**
    ```bash
    git clone [https://github.com/Sarthak8954/AI-rubric-scoring-tool.git](https://github.com/Sarthak8954/AI-rubric-scoring-tool.git)
    cd AI-rubric-scoring-tool
    ```

2.  **Setup Backend**
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Setup Frontend**
    ```bash
    cd ../frontend
    npm install
    ```

### Running the Application

1.  **Start the Backend Server**
    ```bash
    cd backend
    flask run --host=0.0.0.0 --port=5000
    ```

2.  **Start the Frontend**
    ```bash
    cd ../frontend
    npm start
    ```

3.  Open your browser and navigate to **`http://localhost:3000`** (or whichever port the React app serves).

---

## Usage 🧑‍💻

1.  Log in (if authentication is enabled) or access the scoring UI.
2.  Upload or enter the student submission text.
3.  Select or define a rubric (criteria + weights).
4.  Hit **“Evaluate”**.
    * The tool runs the submission through its NLP/ML model.
    * It produces: **A total score**, **Criterion-wise breakdown**, and **Feedback comments** for each criterion.
5.  Export results/report if needed.
6.  (Optional) Review or edit the score and feedback manually before finalising.

---

## How It Works

The core of the tool is the NLP scoring pipeline.

1.  **Input:** The system takes the **submission text** and the **rubric definition** as input.
2.  **Preprocessing:** The submission text undergoes standard NLP preprocessing (tokenization, cleaning) and is transformed into a numerical format, typically using advanced **embeddings** (e.g., based on BERT) or simpler techniques like **TF-IDF**.
3.  **Matching:** The system compares the features extracted from the submission with the features associated with each criterion in the rubric.
4.  **Scoring:** The trained Machine Learning model derives a numeric score for each criterion based on the quality/relevance match, and these are aggregated according to their defined weightages.
5.  **Feedback:** Natural-language comments are generated based on the model's prediction for each criterion (e.g., *“Your explanation of concept X was strong, but depth was lacking in part Y.”*).

> **Note:** You can train or fine-tune the underlying model with domain-specific data for improved results and customisation.

---

## Configuration ⚙️

Configuration settings are primarily handled via `config.yaml` or environment variables in the backend.

**Example `config.yaml` entries:**

```yaml
RUBRIC_FILE_PATH: ./rubrics/default.json
MODEL_PATH: ./text/model/score_model.pkl
MAX_UPLOAD_SIZE_MB: 10
ALLOWED_FILE_TYPES: [".txt", ".pdf", ".docx"]
EXPORT_FORMATS: ["csv","json"]
