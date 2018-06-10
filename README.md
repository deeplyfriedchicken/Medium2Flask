# Medium2Flask

This application serves as a Flask backend for users who want a simple Medium API for their various Medium blog posts.

## Setup
1. Clone the repository
2. Run `pip install -r requirements.txt` after cloning the repository
3. Configure secrets.py which includes your secret key and the sqlite database path
4. Start the actual app using `python app.py` and navigate to `/api/posts` to create the database
5. Run `python cron.py` file to start the scheduler for routine data pulls 

## Scheduling
Scheduling can be adjusted in `cron.py` for various times. See `schedule` for more information.

## Endpoints
To be determined

