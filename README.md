Django User Profile & Authentication API
A robust RESTful API built with Django and Django REST Framework (DRF) integrated with the Firebase Admin SDK. This service handles user authentication, profile creation, phone number updates, and password resets using a custom, email‑based user model with strict Nigerian phone number formatting.
---

Features
- Custom User Model – uses email as the primary identifier (USERNAME_FIELD) instead of a traditional username.  
- Firebase Token Authentication – custom DRF permission class (IsFirebaseAuthenticated) that verifies and decodes incoming Firebase JWTs.  
- Custom Password Validation – built‑in SymbolValidator requiring at least one special character, paired with standard password strength checks.  
- Nigerian Phone Number Validation – enforces valid Nigerian mobile formats (+234... or 070..., 080..., 090...) via regex.  
- User Profile Lifecycle – support for registration, fetching current user details, updating phone numbers, resetting passwords, and profile deletion.  
- Centralized Error Handling – custom DRF exception handler providing clean, consistent JSON error responses.
---
## Tech Stack
- Backend Framework – Django 5.x, Django REST Framework (DRF)  
- Authentication – Firebase Admin SDK (firebase-admin), Firebase Client Auth  
- Validation – Django Password Validation Suite + Custom Regex Rules  
- Database – SQLite (default) / PostgreSQL (recommended for production)
---

Data Model Architecture

CustomUser Model
| Field           | Type            | Attributes & Validation                              |
|-----------------|-----------------|------------------------------------------------------|
| id              | BigAutoField    | Primary Key                                          |
| email           | EmailField      | Unique, Required (USERNAME_FIELD)                    |
| firebase_uid    | CharField       | Max length 255, Unique, Nullable                     |
| first_name      | CharField       | Max length 30, non‑empty validation                  |
| last_name       | CharField       | Max length 30, non‑empty validation                  |
| phone_number    | CharField       | Max length 15, Regex: ^(?:\+234|0)[789][01]\d{8}$   |
| is_active       | BooleanField    | Default: True                                        |
| is_staff        | BooleanField    | Default: False                                       |
---

Project Structure
├── profiles/
│ ├── settings.py # Includes SymbolValidator configuration
│ ├── urls.py # Main project URL routing
│ ├── validators.py # SymbolValidator class
│ ├── firebase_credentials.json # Firebase Admin SDK service key
│ ├── asgi.py
│ └── wsgi.py
├── user/
│ ├── apps.py # Firebase Admin SDK auto‑initialization
│ ├── admin.py # CustomUser admin registration
│ ├── firebase_utils.py # Token verification & custom exception handler
│ ├── models.py # CustomUser & CustomUserManager
│ ├── permissions.py # IsFirebaseAuthenticated permission class
│ ├── serializers.py # DRF serializers (Create, Retrieve, Update, Reset)
│ ├── urls.py # User API routes
│ └── views.py # Endpoint class views
└── manage.py

text

---

Installation & Setup

1. Prerequisites
- Python 3.10+
- Firebase project with **Authentication** enabled.

 2. Service Key Setup
1. Go to your [Firebase Console](https://console.firebase.google.com/) → Project Settings → Service Accounts.
2. Click **Generate New Private Key** and download the JSON.
3. Save the file at:
profiles/profiles/firebase_credentials.json

text
 
 3. Local Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd profiles
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install django djangorestframework firebase-admin
Run migrations:

bash
python manage.py migrate
Create a superuser:

bash
python manage.py createsuperuser
Start the development server:

bash
python manage.py runserver
API Documentation
Base URL: /api/user/

1. Register User Profile
Endpoint: POST /api/user/profile/create/

Auth Required: Yes (Bearer <Firebase_ID_Token>)

Request Body:

json
{
  "first_name": "Amina",
  "last_name": "Okafor",
  "phone_number": "08012345678",
  "password": "Password123!",
  "retype_password": "Password123!"
}
Response (201 Created):

json
{
  "id": 1,
  "first_name": "Amina",
  "last_name": "Okafor",
  "email": "amina@example.com",
  "phone_number": "08012345678"
}
2. Get Current Authenticated Profile
Endpoint: GET /api/user/profile/

Auth Required: Yes (IsFirebaseAuthenticated)

Headers: Authorization: Bearer <Firebase_ID_Token>

Response (200 OK): same as above

3. Firebase Direct Login
Endpoint: POST /api/user/firebase-login/

Auth Required: No

Request Body:

json
{
  "id_token": "<FIREBASE_ID_TOKEN>"
}
Response (200 OK):

json
{
  "message": "Login successful.",
  "uid": "a1b2c3d4e5",
  "email": "amina@example.com",
  "created": false,
  "full_name": "Amina Okafor"
}
4. Update Phone Number
Endpoint: PATCH /api/user/profile/<pk>/update-phone/

Auth Required: No

Request Body:

json
{
  "phone_number": "+2348098765432"
}
Response (200 OK):

json
{
  "message": "Phone number updated successfully."
}
5. Reset Password
Endpoint: POST /api/user/reset-password/

Auth Required: No

Request Body:

json
{
  "email": "amina@example.com",
  "new_password": "NewStrongPassword123!",
  "confirm_password": "NewStrongPassword123!"
}
Response (200 OK):

json
{
  "message": "Password updated successfully."
}
Endpoints Overview
Method	Endpoint	Description	Auth Standard
GET	/api/test-connection/	Health check	Public
POST	/api/user/profile/create/	Profile registration	Bearer ID Token
GET	/api/user/profile/	Fetch current user	IsFirebaseAuthenticated
GET	/api/user/profile/<pk>/	Retrieve user by ID	IsFirebaseAuthenticated
PATCH	/api/user/profile/<pk>/update-phone/	Update phone number	Public
DELETE	/api/user/profile/<pk>/delete/	Delete user profile	Public
POST	/api/user/firebase-login/	Direct Firebase token login	Public
POST	/api/user/reset-password/	Account password reset	Public
Testing
Run the test suite with:

bash
python manage.py test
Contributing
Fork the repository.

Create a feature branch: git checkout -b feature/amazing-feature.

Commit your changes: git commit -m 'Add some amazing feature'.

Push to the branch: git push origin feature/amazing-feature.

Open a Pull Request.

Ensure your code adheres to PEP8 and includes appropriate tests.

License
Distributed under the MIT License. See LICENSE for more information.
