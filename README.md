# VueCourse

VueCourse is a college project that combines the concepts I've learned in two courses. It uses Vue.js for the frontend, and Flask for the backend. The goal was to implement an RTF (Rich Text Format) editor with the ability to create, edit, and save text documents with rich formatting options such as bold, italics, bullet points. On the backend, Flask handles database storage, user authentication, and the logic for saving and retrieving the saved text.

## Prerequisites:

- NodeJS (used v20.18.1)
- Python (used v3.13.1)
- MySQL Server (used v8.4)

## Instructions:

- **Backend**

  - Open a terminal and navigate to the `backend` folder
  - Run the command `python -m venv myvenv`
  - On Windows: `myenv\Scripts\activate`
  - Now run `pip install -r requirements.txt`
  - Create the database with `python database.py`
  - To start Flask, run `python app.py`
  - If using VSCode: Press `Ctrl Shift P` > Python: Select Interpreter > Enter interpreter path... > Find > Navigate to `myenv` > Scripts > python.exe. You can now run app.py by pressing a button

- **Frontend**

  - Open a terminal and navigate to the `frontend` folder
  - Run `npm ci`
  - To start, use `npm run dev`

##

![Home page](1.png)
![Admin panel - Courses](2.png)
![Editing lesson content](3.png)
