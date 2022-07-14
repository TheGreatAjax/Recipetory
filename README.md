To run the website (manually)
1. Download the project folder
2. Create virtual environment and activate it
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install the packages
    ```
    pip3 install -r requirements.txt
    ```
4. Setup and run flask app
    ```
    export FLASK_APP=App
    export FLASK_ENV=development
    flask init-db
    flask run
    ```
5. Go to http://127.0.0.1:5000/ in your browser