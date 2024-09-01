# property-management-app
## I - Project Overview
This project is a Property Management Application that allows users to manage properties, tenants, and rental payments. The application provides an API for handling property details, tenant information, and payment tracking, including reminders for upcoming payments.

## II - Features
- User Authentication: Secure registration and login system using JWT.
- Property Management: Add, edit, and view properties with associated details.
- Tenant Management: Add and manage tenants linked to specific properties.
- Payment Tracking: Record and track rental payments, including overdue and upcoming payments.
- Payment Reminders: Automatically send reminders for payments that are due soon.

## III - Technologies Used
- Backend: Django, Django REST Framework
- Authentication: Custom User Model, JWT
- Database: Sqlite

## IV - Installation and Setup
### 1 - Clone the Repo:
```
git clone https://github.com/alaajili/property-management-app.git
cd property-management-app
```

### 2 - Setup Virtual Environment and Install Dependencies:
```
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

pip install -r requirements.txt
```

### 3 - Run migrations and Dev server:
```
python3 manage.py migrate

python3 manage.py runserver
```
## V - Testing Endpoints in Swagger
Navigate to http://localhost:8000/swagger/ in your web browser. You should see the Swagger UI, which provides an interactive interface for testing your API endpoints.

### step 1: Register a user
1. Select POST /api/auth/register/: This endpoint allows you to register a new user.
2. Click on "Try it out": This will enable the input fields.
3. Input the required data: Provide details like email, username, firstname, lastname, and password.
4. Click "Execute": Swagger will make a request to the registration endpoint, and you'll see the response in the "Response" section.
### step 2: Log in the User
1. Select POST /api/auth/login/: This endpoint allows you to log in and get a JWT token.
2. Click on "Try it out".
3. Input the credentials: Provide email and password for the user you just registered.
4. Click "Execute": Swagger will return a response with the JWT token in the "Response" section.
### step 3: Authorize with access token
To make authenticated requests, you'll need to include the JWT access token obtained from the login response in your subsequent requests.
1. Copy the JWT Access Token: From the login response, copy the token.
2. Authorize: At the top right corner of Swagger UI, click the "Authorize" button.
3. Input the Token: In the authorization modal, input the token in the following format: ```Bearer <access_token>```.
4. Click "Authorize": Now, all requests made through Swagger will include the token in the Authorization header.
### final step: test endpints and view the response
for each of the endpoints:
- Click on the endpoint you want to test.
- Click "Try it out".
- Fill in the required fields (if any).
- Click "Execute" to send the request and view the response.

Finally Swagger will display the request URL, request body, and the response from the server.