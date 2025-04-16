Team SuperSonics via TicTech 

Project -- Feature Development Backend: Create CRUD API's for Client

User Story

As a user of the backend API's, I want to call API's that can retrieve, update, and delete information of clients who have already registered with the CaseManagment service so that I more efficiently help previous clients make better decisions on how to be gainfully employed.

Acceptance Criteria
- Provide REST API endpoints so that the Frontend can use them to get information on an existing client.
- Document how to use the REST API
- Choose and create a database to hold client information
- Add tests


This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.

-------------------------How to Use-------------------------
1. In the virtual environment you've created for this project, install all dependencies in requirements.txt (pip install -r requirements.txt)

2. Create a .env file with the following fields:
```markdown
SECRET_KEY = "<your-secret-key-here>"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

3. Run the app (uvicorn app.main:app --reload)

4. Go to SwaggerUI (http://127.0.0.1:8000/docs) 

5. Load data into database (python initialize_data.py) (if receiving an error, make sure the app is running and open, then try again)

6. Log in as admin (username: admin password: admin123)

7. Click on each endpoint to use
-Create User (Only users in admin role can create new users. The role field needs to be either "admin" or "case_worker")

-Get clients (Display all the clients that are in the database)

-Get client (Allow authorized users to search for a client by id. If the id is not in database, an error message will show.)

-Update client (Allow authorized users to update a client's basic info by inputting in client_id and providing updated values.)

-Delete client (Allow authorized users to delete a client by id. If an id is no longer in the database, an error message will show.)

-Get clients by criteria (Allow authorized users to get a list of clients who meet a certain combination of criteria.)

-Get Clients by services (Allow authorized users to get a list of clients who meet a certain combination of service statuses.)

-Get clients services (Allow authorized users to view a client's services' status.)

-Get clients by success rate (Allow authorized users to search for clients whose cases have a success rate beyond a certain number.)

-Get clients by case worker (Allow users to view which clients are assigned to a specific case worker.)

-Update client services (Allow users to update the service status of a case.)

-Create case assignment (Allow authorized users to create a new case assignment.)

## Docker Instructions
1. Follow installation guide from Docker: https://www.docker.com/blog/how-to-dockerize-your-python-applications/
2. WINDOWS-SPECIFIC: Ensure virtualization is enabled in your system BIOS, or Docker cannot run
3. Open the Docker Desktop application
4. In a command prompt, navigate to the CommonAssessmentTool repo's directory on your machine (assumes you already cloned from GitHub) and run the command below (make sure the period at the end is included!):
```
docker build -t common_assessment_tool .
```
5. Now run  with the following Docker command:
```
docker run --rm -p 8000:8000 common_assessment_tool
```
6. Follow the steps to run the Swagger UI as described above (clicking link in step 5 should take you to the UI)
7. To run using Docker-Compose in the foreground, run the command below in the CommonAssessmentTool repo's directory
```
docker compose up
```
8. To run using Docker-Compose in the background, run the command below in the CommonAssessmentTool repo's directory
```
docker compose up -d
```
9. If running using the background command, you can stop the container gracefully with the following command:
```
docker compose stop
```

## Access public address
Backend application is now deployed to the AWS Cloud. 
Access the backend application from the endpoint by clicking: http://ec2-18-204-133-53.compute-1.amazonaws.com:8000/docs
