# 📘 Inkle Mini Twitter – Backend API  
**(Flask + JWT Authentication)**

A lightweight backend system that replicates core features of Twitter, such as **user authentication, posting, following, blocking, liking/unliking posts, and activity feeds**.  
All endpoints are **tested via Postman**, and the **Postman collection JSON file is included** in the project.

## Inkle Mini Twitter Backend.postman_collection.json : It is the postman documentation for all the features that’s mentioned


---

## 🚀 Features

### 🔐 Authentication
- User Signup  
- User Login  
- JWT-based Token Authentication  

### 📝 Posts
- Create a Post  
- Fetch All Posts  
- Like a Post  
- Unlike a Post  

### 👥 User Interactions
- Follow a User  
- Unfollow a User  
- Block a User  

### 📰 Activity Feed
- Displays posts, likes, follows, and blocks  
- Chronological sorting  
- Shows own + followed users' activity  

### 🧪 Postman Tested
- All API endpoints tested  
- Postman collection JSON included in project root  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|----------|
| Python 3 | Programming Language |
| Flask | Backend Framework |
| Flask-SQLAlchemy | ORM / Database Handling |
| Flask-JWT-Extended | Authentication |
| Flask-CORS | Cross-Origin Access |
| SQLite | Default Database |
| Postman | API Testing |

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
```
---
## ⚙️ Installation & Setup
### 1️⃣ Clone the repository
```bash
git clone <your-github-repo-url>
cd mini-twitter-backend
```
### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```
### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Run the server
```bash
python app.py
```
API will run at:
```bash
http://127.0.0.1:5000
```
---
## 🔐 Authentication Example
```bash
Login returns:

{
  "access_token": "<JWT_TOKEN>",
  "user": {
    "id": 1,
    "username": "testuser"
  }
}
```
Use in Postman:
```bash
Authorization → Bearer Token → <JWT_TOKEN>
```
---
## 📡 API Endpoints
## 🔑 AUTH ROUTES
| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| POST   | `/auth/signup` | Register a new user   |
| POST   | `/auth/login`  | Login and receive JWT |

## 📝 POST ROUTES
| Method | Endpoint                  | Description        |
| ------ | ------------------------- | ------------------ |
| POST   | `/posts/`                 | Create new post    |
| GET    | `/posts/`                 | Retrieve all posts |
| POST   | `/posts//like`           | Like a post        |
| POST   | `/posts//unlike`          | Unlike a post      |

## 👤 USER ROUTES
| Method | Endpoint                    | Description   |
| ------ | --------------------------- | ------------- |
| POST   | `/users/follow/`            | Follow user   |
| POST   | `/users/unfollow/`          | Unfollow user |
| POST   | `/users/block/`             | Block user    |

## 📰 ACTIVITY ROUTES
| Method | Endpoint     | Description                 |
| ------ | ------------ | --------------------------- |
| GET    | `/activity/` | View combined activity feed |

---
## 📦 Postman Collection
Your exported Postman JSON file should be added to the project root:
```bash
postman_collection.json
```
Import using:
```bash
Postman → Collections → Import → select JSON file
```
---
## 📝 Notes
SQLite database auto-creates inside the instance/ folder.
Modify token expiry and JWT settings in config.py.
All protected routes require the header:
```bash
Authorization: Bearer <token>
```
Suitable for assignment submission and basic deployment.
---
## 📄 requirements.txt
```bash
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
Flask-CORS
Werkzeug
```
---
## ✅ Final Output Includes
- Complete backend implementation
- Secure JWT authentication
- Posts + likes + follows + blocks
- Combined activity feed
- Postman-tested API endpoints
- Clean project structure
- Professional README
Submission-ready package
---
