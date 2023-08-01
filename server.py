# Import the Flask application instance from the module flask_app
from flask_app import app 

# Import the controller module for users. The users_controller module is expected to contain 
# the routes and handlers for user-related HTTP requests.
from flask_app.controllers import users_controller 

# Python assigns the name "__main__" to the script when the script is executed.
# If the script is imported from another script, the script keeps its original name (e.g. flask_app).
# Here we're saying, "if this script is run directly, then execute the following."
if __name__ == "__main__": 
    # Run the application.
    # The argument debug=True enables the debug mode of the Flask application. 
    # Debug mode is a feature that provides a debugger in the browser when an error occurs. 
    # It also ensures the server reloads itself whenever code is updated.
    app.run(debug=True)

        

