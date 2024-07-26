## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/safvan001/project_management_system.git
   cd project_management_system
2. **Set Up the Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Set Up the Database:**
   ```bash
   python manage.py migrate
5. **Run the Development Server:**
   ```bash
   python manage.py runserver

6. **Run the Celery:**
   ```bash
   celery -A project_management_system.celery worker --pool=solo -l info
   
