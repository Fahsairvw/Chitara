# Chitara - Music Platform API

A Django REST Framework API for managing music, users, and libraries.

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Fahsairvw/Chitara.git
cd Chitara
```

### 2. Create virtual environment and install dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Apply database migrations
```bash
python manage.py migrate
```

### 4. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

### 5. Run the development server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

Here is a link of CRUD evidence
https://docs.google.com/document/d/1byFzzkw_89gAtEnHXGaNv5JHO6FOuWLFFedegcLajpE/edit?usp=sharing

