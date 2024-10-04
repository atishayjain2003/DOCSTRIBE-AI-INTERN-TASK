# DOCSTRIBE-AI-INTERN-TASK
Instructions for running the application locally :
1. Clone the Project Repository (git clone https://github.com/atishayjain2003/DOCSTRIBE-AI-INTERN-TASK.git)
2. Set Up and activate virtual Environment (virtualenv env, env/scripts/activate)
3. Install Project Dependencies (pip install -r requirements.txt)
4. Navigate to the Project Directory (cd patient_etl)
5. Set Up the Database (python manage.py migrate)
6. Create a Superuser (python manage.py createsuperuser) for admin interface
7. Run the server (python manage.py runserver)
* Project Screenshots have been added in the repository including proof of Mobile Number being stored in Encrypted format in the database
* Mobile Number Encryption is handled using fernet encryption technique that guarantees confidentiality by using a secure key for both encryption and decryption of data.
* python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" command was run in the terminal and the received key was stored as ENCRYPTION_KEY in the project's settings file.
  
