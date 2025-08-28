# Data Cleaning Agent

A modular and extensible pipeline designed for data cleaning, transformation, and preprocessing, built on top of pandas with support for custom cleaning logic and LLM-assisted handling of ambiguous or unstructured data.
The pipeline automates repetitive tasks such as handling missing values, type enforcement, formatting, and text processing, while also enabling AI-driven decision-making for edge cases.

This project is fully containerized with Docker for portability and ease of deployment. It includes both a backend (FastAPI + agents for pipeline orchestration and LLM integration) and a frontend interface that allows users to upload datasets, configure cleaning rules, and visualize outputs interactively.

---

## 📂 Project Structure

```
data-cleaning-agent/
├── backend/
│   ├── __pycache__/
│   ├── prompts/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── column_types.py
│   │   ├── ordinal_mapping.py
│   │   ├── ordinal_nominal.py
│   │   ├── preprocssing_prompts.py
│   ├── __init__.py
│   ├── .dockerignore
│   ├── agent.py
│   ├── data_cleaning.py
│   ├── Dockerfile
│   ├── llm.py
│   ├── main.py
│   └── requirements.txt
│
├── data/
│   └── sample.csv
│
├── frontend/
│   ├── .dockerignore
│   ├── app.py
│   └── requirements.txt
│
├── venv/
├── .env
├── .gitignore
├── docker-compose.yml
├── graph.png

```

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Faiq-Ali10/data-cleaning-agent.git
cd data-cleaning-agent
```

### 2. Setup environment
```bash
Using venv:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 3. Setup environment variables

Create a .env file in the project root:

store environment variables

### 4. 🚀 Usage
Run with Docker Compose
docker-compose up --build


Backend: runs FastAPI app for data cleaning and preprocessing

Frontend: runs a lightweight frontend to interact with the pipeline

Run locally (without Docker)
cd backend
uvicorn main:app

### 5. 🔄 Data Cleaning & Preprocessing Agent

The Agent in backend/agent.py creates a pipeline using StateGraph with the following nodes:

Start Missing Handling → fills missing values in the raw input

LLM Handling → applies LLM-based cleaning or transformations (batch size configurable)

Encoding → encodes categorical features

Final Missing Handling → ensures cleaned output is ready

Pipeline graph is automatically saved as graph.png for visualization.

### 6. 🛠 Tech Stack

Python 3.11+

Pandas for data processing

LangGraph for pipeline orchestration

FastAPI for backend API

Docker & Docker Compose for containerization

### 7. 📌 Future Improvements

Add unit tests for each pipeline step

Extend LLM handling to support multiple providers

Improve frontend UI for interactive dataset uploads

Add monitoring/logging for pipeline runs

### 8. 📷 Pipeline Graph

The preprocessing pipeline is visualized in graph.png:

##
### 👨‍💻 Author

Faiq Ali
Data Scientist & ML Engineer