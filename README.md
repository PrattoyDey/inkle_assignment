# 📘 Inkle Mini Twitter – Backend API (Flask + JWT)

A lightweight backend implementing core Twitter-like features: signup/login, posting, following, blocking, liking, unliking, and a combined activity feed.  
All routes are tested using Postman, and the Postman collection JSON is included.

---

## 🚀 Features Implemented

### 🔐 Authentication
- User Signup  
- User Login  
- JWT Token Authentication  

### 📝 Posts
- Create Post  
- Get All Posts  
- Like Post  
- Unlike Post  

### 👥 User Interactions
- Follow User  
- Unfollow User  
- Block User  

### 📰 Activity Feed
- Shows posts, likes, follows, blocks  
- Sorted chronologically  
- Includes user + following activity  

### 🧪 Postman Tested
- All endpoints tested  
- Exported Postman JSON included  

---

## 🛠 Tech Stack

- Python 3  
- Flask  
- Flask-SQLAlchemy  
- Flask-JWT-Extended  
- Flask-CORS  
- SQLite (default DB)  
- Postman  

---

## 📁 Project Structure

```plaintext
mini-twitter-backend/
│
├── app.py
├── config.py
├── models.py
├── auth_routes.py
├── user_routes.py
├── post_routes.py
├── activity_routes.py
│
├── helpers.py
├── requirements.txt
├── README.md
│
└── instance/
    └── database.sqlite
~~~

## ⚙️ Installation & Setup
~~~
1️⃣ Clone the repo
git clone <your-github-repo-url>
cd mini-twitter-backend
~~~
~~~
2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
~~~
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Run the server
python app.py
API will run at:

http://127.0.0.1:5000
##🔐 Authentication Example
Login returns:

{
  "access_token": "<JWT_TOKEN>",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
Use in Postman:

Authorization → Bearer Token → <JWT_TOKEN>
📡 API Endpoints
🔑 AUTH ROUTES
Method	Endpoint	Description
POST	/auth/signup	Register user
POST	/auth/login	Login & get JWT
📝 POST ROUTES
Method	Endpoint	Description
POST	/posts/	Create new post
GET	/posts/	Get all posts
POST	/posts//like	Like a post
POST	/posts//unlike	Unlike a post
👤 USER ROUTES
Method	Endpoint	Description
POST	/users/follow/	Follow a user
POST	/users/unfollow/	Unfollow a user
POST	/users/block/	Block a user
📰 ACTIVITY ROUTES
Method	Endpoint	Description
GET	/activity/	Combined activity feed
📦 Postman Collection
Your exported Postman JSON file should be added to the project root:

postman_collection.json
Import using:

Postman → Collections → Import → select JSON file
📝 Notes
SQLite database auto-creates inside the instance/ folder.
Modify token expiry and JWT settings in config.py.
All protected routes require the header:
Authorization: Bearer <token>
Suitable for assignment submission and basic deployment.
📄 requirements.txt
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-CORS
Werkzeug
✅ Final Output Includes
Complete backend implementation
Secure JWT authentication
Posts + likes + follows + blocks
Combined activity feed
Postman-tested API endpoints
Clean project structure
Professional README
Submission-ready package
