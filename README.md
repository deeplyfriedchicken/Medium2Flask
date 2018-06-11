# Medium2Flask

This application serves as a Flask backend for users who want a simple Medium API for their various Medium blog posts.

## Setup
1. Clone the repository
2. Run `pip install -r requirements.txt` after cloning the repository
3. Duplicate `secrets.example.py` and rename it `secrets.py` to include your actual information. This includes your secret key, sqlite database path, and email / password for a single user login
4. Start the actual app using `python app.py` and navigate to `/api/posts` to create the database
5. Run `python cron.py` file to start the scheduler for routine data pulls 

## Scheduling
Scheduling can be adjusted in `cron.py` for various times. See `schedule` for more information.

## Endpoints

The following endpoints can be accessed via URL calls. Note which need authorization and given fields.

| URL                            | METHOD | FUNCTION           | FIELDS |AUTH? |
| ------------------------------ | ------ | ------------------ | ------ | ---- |
| `/api/posts`                     | GET    | Gets all **active** account posts | None | No |
| `/api/posts/account/:name:`      | GET    | Gets all **active** posts by that account | None | No |
| `/api/posts/category/:category:` | GET    | Gets all **active** posts from that category      | None | No | 
| `/api/categories`                | GET    | Gets all categories | None | No |
| `/api/accounts`                  | GET    | Gets all accounts   | None | No |
| `/api/account/:name:`            | POST   | Adds a **new** account | `is_active` | Yes |
| `/api/account/:name:`            | PUT    | Updates an account | `is_active` | Yes |
| `/login`                         | POST   | Signs an existing user in | `email`, `password` | No |
| `/logout`                        | POST   | Signs a user out | None | Yes

