# Install required dependencies
install:
	pip install -r requirements.txt

# Run the Flask application locally on http://localhost:3000
# Added sleep to ensure server has time to start
run:
	set FLASK_APP=app.py&& set FLASK_ENV=development&& flask run --host=0.0.0.0 --port=3000&
	sleep 10
