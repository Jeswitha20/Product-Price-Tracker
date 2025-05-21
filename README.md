# Product-Price-Tracker
![image](https://github.com/user-attachments/assets/fa5cbaae-4661-4031-9de2-89c0a5239175)
![image](https://github.com/user-attachments/assets/a4efe25a-4f11-426a-8587-2a76c7ee530a)
![Screenshot 2025-05-21 163347(1)](https://github.com/user-attachments/assets/cf19f6a6-8034-48ed-99b0-8e1c384c23b7)



# Description:

This is a full-stack application that tracks product prices from e-commerce websites and notifies users via email every 10 minutes about price updates (decreased, increased, or unchanged). The project combines a React frontend for a seamless user experience and a Flask backend for API handling and web scraping.

# Tech Stack:

* Frontend: React, Axios (for API calls), Material-UI or Bootstrap (if used for styling).
* Backend: Flask (Python).
* Other Tools: BeautifulSoup for web scraping, APScheduler for periodic tasks, SMTP for email notifications.

# Features:

* User-friendly React interface for adding and managing tracked products.
* Real-time status updates about price changes.
* API integration between React and Flask.
  
# Setup Instructions: 

* Backend: Install dependencies and run the Flask server.
* Frontend: Install React dependencies and start the development server.

 Below are the detailed steps for setting up both the **backend** (Flask server) and the **frontend** (React app):
-

### **Backend Setup: Flask Server**
The backend is written in Python using Flask. Follow these steps to set it up:

#### **1. Install Python**
- Ensure Python is installed on your system (version 3.6 or later). Verify by running:
  ```bash
  python --version
  ```

#### **2. Create a Virtual Environment (Optional but Recommended)**
- Create a virtual environment to isolate your Python dependencies:
  ```bash
  python -m venv venv
  ```
- Activate the virtual environment:
  - **Windows**:
    ```bash
    .\venv\Scripts\activate
    ```
  - **Mac/Linux**:
    ```bash
    source venv/bin/activate
    ```

#### **3. Install Backend Dependencies**
- Install required Python packages listed in `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```
  If you don’t have a `requirements.txt`, you can manually install the dependencies:
  ```bash
  pip install flask flask-cors beautifulsoup4 requests apscheduler
  ```

#### **4. Configure Email Settings**
- Update the `send_email` function in the backend code with your email credentials:
  ```python
  from_email = "your-email@example.com"
  from_password = "your-email-password"
  ```

#### **5. Start the Flask Server**
- Run the server:
  ```bash
  python app.py
  ```
- By default, the server will run at `http://127.0.0.1:5000`. You can test it using tools like Postman or a browser.

---

### **Frontend Setup: React App**
The frontend is built with React. Here’s how to set it up:

#### **1. Install Node.js and npm**
- Ensure Node.js and npm (Node Package Manager) are installed. Verify installation by running:
  ```bash
  node --version
  npm --version
  ```
- If not installed, download and install them from [Node.js official website](https://nodejs.org).

#### **2. Navigate to the React App Directory**
- If the React app is in a folder named `my-react-app`, navigate to it:
  ```bash
  cd my-react-app
  ```

#### **3. Install Frontend Dependencies**
- Install the required React packages using npm:
  ```bash
  npm install
  ```

#### **4. Configure the Backend URL**
- Ensure the React app is pointing to the Flask backend's URL. If there’s a `.env` file or configuration file in the React app, update the API endpoint:
  ```env
  REACT_APP_API_URL=http://127.0.0.1:5000
  ```

#### **5. Start the React Development Server**
- Start the React development server:
  ```bash
  npm start
  ```
- This will typically launch the app in your default browser at `http://localhost:3000`.

---

### **Testing the Full Stack Application**
1. **Start the Backend**
   - Ensure the Flask server is running at `http://127.0.0.1:5000`.
2. **Start the Frontend**
   - The React app should be accessible at `http://localhost:3000`.
3. **Use the Application**
   - Interact with the frontend to make API requests to the backend and verify functionality.

---


