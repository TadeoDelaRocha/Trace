# Installing Dependencies

Before running the application, install all necessary dependencies using the requirements.txt file.

```bash
pip install -r requirements.txt
```

## Set Up Environment variables

Create a .env file containing the information required to connect to the database using the information in the Setup Channel of the Teams Group.

## Running the App

In order to run the application you will need to open two terminals and run the frontend and backend seperately.

Frontend run command
```bash
npm run dev
```
Backend run command
```bash
uvicorn main:app --reload --port 8000
```
