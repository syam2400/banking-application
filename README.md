# banking-application
This is a Django RESTful API for a banking application. Existing registered users can manage their bank accounts and perform various banking transactions.
it designed to simulate various banking operations such as account registration, fund transfers, bill payments, and user authentication. The API leverages Django and Django REST Framework, providing robust security features through JWT authentication.

Features
Account Registration: Allows new users to register and create bank accounts.
Backend Account Creation:
This API has an endpoint for user accounts creation and are created through a separate backend process ,with that data you can use the banking api for further banking activities.

MPIN Setup: Users can set up an MPIN via an email link, which is required for login and transaction authorizations.users registered email id is automaticaly fetch from the db using account number and username created during user registration process .
User Authentication: Secure login using JWT for token generation and validation 
Fund Transfers: Supports transfers within the same bank as well as to other banks.
Bill Payments: Facilitates bill payments with confirmation and transaction recording.
Transaction History: Users can view detailed logs of all their transactions.
Robust Security: Uses JWT for secure access to endpoints, ensuring data protection.
Technologies Used
Python: Programming language.
Django: High-level Python web framework for rapid development and clean design.
Django REST Framework: Powerful toolkit for building Web APIs.
JWT Authentication: Secures endpoints by validating tokens.

swagger link for checking api endpoints :
https://app.swaggerhub.com/apis/syamprasadshaji/Banking-Application/1.0.0

Running the API:

Clone this repository.
Create a virtual environment and activate it.
Install dependencies: pip install -r requirements.txt
Apply database migrations: python manage.py migrate
Run the development server: python manage.py runserver
Notes:

This is a basic implementation of a banking API and may require further security measures for production use.
Error handling and validation are implemented in the serializers and views.
The API uses pagination for retrieving transaction history.
