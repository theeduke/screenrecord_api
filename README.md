# REST API for screen recording chrome extension

The REST API is built using Django framework

## Table of Contents
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Link to api](#link-to-api)  

## Prerequisites
Before getting started, ensure you have the following installed on your system:
- Python  
- Django  
## Installation
Follow these steps to set up and run the project:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/theeduke/screenrecord_api.git
   ```

2. Run the following command to set up your virtual environment:
   ```bash
   python -m venv virtual
   ```
   ```bash
   virtual/Scripts/activate
   ```
   
4. Run the following to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a .env file in the project root and configure your secret key and other sensitive information:
   ```bash
   touch .env
   ```
6. Use the following command to make migrations:
   ```bash
   python manage.py makemigrations
   ```
   ```bash
   python manage.py migrate
   ```

7. Use the following command to run server:
   ```bash
   python manage.py runserver
   ```
Your django project should now be running at http://localhost:8000.

## Link to API 
 The documentation include test to verify the API's fun
 ```bash
 https://screenrecord-5b9n.onrender.com
 ```
