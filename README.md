To run the website (manually)
1. Download the project folder
2. Create virtual and activate environment
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