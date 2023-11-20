# Approval Framework Project

This project is an Approval Framework application built with Django. It allows for the management of approval workflows involving multiple users, company details, and various approval processes.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Creating a Superuser](#creating-a-superuser)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/approval-framework.git
cd approval-framework

```
2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:
on windows:
```bash
venv\Scripts\activate
```
on  mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Apply migrations:
```bash
pip install -r requirements.txt
```

# Usage
Run the development server:
```bash
python manage.py runserver
```
Visit http://localhost:8000 in your browser to access the application.

# Creating a Superuser
To create a superuser for managing workflows and companies, use the following command:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up the superuser account.

After creating a superuser. With th esuper user account , one can manage the companies, workflows sequences and approval authorizers of the total project.