# Stroke Patient Record Management System
A secure Flask web application for managing patient stroke data using SQLite and MongoDB.

# Overview
This project is a lightweight yet secure web application designed to help a hospital maintain and manage patient stroke records. It integrates SQLite for user authentication and MongoDB for storing patient health data, providing a clean separation between user access control and medical records.

The application focuses on simplicity, security, and usability so that staff members can easily log in, create patient records, and update or review existing data.

# Features
# User Authentication
- Registration & login system  
- Password hashing using (Flask-Bcrypt) 
- CSRF-protected forms  
- Session-based access control  

# Patient Record Management
- Add, view, update, and delete patient stroke records  
- Stores clinical attributes like age, BMI, hypertension, smoking status, etc.  
- Data stored in MongoDB  

# Security Measures
- CSRF protection through Flask-WTF  
- Server-side session protection  
- Password hashing using bcrypt  
- Input validation for correct formats (email, numeric fields)  
- Automatic XSS protection via Jinja2 templating  

# User-Friendly Interface
- Flash messages to guide the user  
- Clean and organized HTML templates  
- Simple workflow for navigating between records  

# Technologies Used
# Backend
- Flask  
- Flask-Bcrypt  
- Flask-WTF  
- SQLite (authentication database)  
- MongoDB (patient records)  
- PyMongo  

# Frontend
- HTML, CSS  
- Jinja2 Templates  


# Project Structure

app.py– Includes routing logic, user auth, and patient CRUD operations.  
config.py– Contains session, cookie, and secret key configurations.  
database/auth.db – SQLite database for user authentication.  
MongoDB Atlas – Stores patient medical records.  


# Application Workflow
1. The environment is set up and dependencies installed.  
2. SQLite initializes user records after registration.  
3. MongoDB Atlas connects automatically for patient data.  
4. Users register, log in, and access their dashboard.  
5. Authorized users can:
   - Add patient records  
   - View all stored patients  
   - Edit existing records  
   - Delete records  
6. Users can securely log out of the system.

# Security Practices Implemented
# Password Hashing  
Using bcrypt ensures credentials are never stored in plain text.

# CSRF Protection  
Enabled on all forms via Flask-WTF.

# Input Validation  
Checks ensure safe and correct values for email, numbers, and fields.

# Enforced Session Handling  
Flask session configuration enhances cookie safety.

# Auto-Escaping  
Prevents XSS attacks via Jinja2 templates.

# Database Separation  
Authentication (SQLite) and patient data (MongoDB) are kept separate to reduce security risks.


# Setup Instructions
1. Clone the repository
2. Create & activate a virtual environment
bash
python -m venv venv
# for Windows
venv\Scripts\activate
# for macOS/Linux
source venv/bin/activate

3 Install dependencies
bash
pip install -r requirements.txt
4. Configure MongoDB connection
Update your MongoDB URI in app.py.

5. Run the application
bash
python app.py

6.  Open in browser

# Testing
To run the unit tests for the application, use the following command:
bash
pytest

# Use of AI
This assignment used generative AI in the following ways for the purposes of completing the assignment more efficiently:
- Research : unserstanding best practice for secure web application developement with flask.
- Feedback and suggestions :  checked for implemented approach and suggestions for improvement.
- Editing : reviewing readme file for better readiability and structure.

# Tools Used
- ChatGPT - for code review, understanding concepts, and reviewing documentation. 

# Useful Resources
1. **Flask Documentation** – Routing, sessions, forms  
2. **PyMongo Documentation** – MongoDB queries  
3. **Flask-WTF Docs** – Form + CSRF handling  
4. **Bcrypt Docs** – Password security  

