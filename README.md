# Collaborate - Django Project

## About
Collaborate is a Django-based web application that enables project collaboration among team members. With Collaborate, users can share their projects with other members and manage permissions to control access levels effectively. 

## Framework Used
Collaborate is developed using the Django framework, a high-level Python web framework known for its scalability, security, and rapid development capabilities. The project utilizes the SQLite database managed through Django's Object-Relational Mapping (ORM) system, providing an efficient data management solution.

## Installation and Run
To run Collaborate locally, follow these steps:

1. Clone the repository:
```
git clone https://github.com/anbrikzone/Django-Project.git
```


2. Navigate to the project directory:
```
cd collaborate_project
```


3. Create a virtual environment (optional but recommended):
```
python3 -m venv myenv
```

4. Activate the virtual environment:
- For Windows:
  ```
  myenv\Scripts\activate
  ```
- For macOS/Linux:
  ```
  source myenv/bin/activate
  ```

5. Install dependencies:
```
pip install -r requirements.txt
```

6. Apply migrations:
```
python manage.py migrate
```

8. Start the development server:
```
python manage.py runserver
```


9. Access the application in your web browser at `http://127.0.0.1:8000/`.


## Features
- **Sharing Projects with Members**: Users can share their projects with other team members by inviting them to collaborate, fostering collaboration and teamwork.
- **Permissions for Users**: Collaborate allows administrators to assign various permissions to users, controlling access to project resources and functionalities based on roles and responsibilities within the team.

Feel free to contribute to this project by submitting pull requests or reporting issues. Happy collaborating!


## Screenshots
