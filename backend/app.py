from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from flask_bcrypt import Bcrypt
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
Bcrypt(app)

mongodb_client = MongoClient(os.getenv("MONGO_URI"))

OPENROUTER_API_KEY = (os.getenv("SECRET_KEY"))
REFERER = "http://localhost:5173"
TITLE = "UnBlank AI Blog Generator"

db = mongodb_client["unblank"]
users = db["users"]
blogs = db["blogs"]


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if (
        not data
        or "username" not in data
        or "email" not in data
        or "password" not in data
    ):
        return {"error": "Invalid input"}, 400

    username = data["username"].strip().lower()
    email = data["email"].strip().lower()
    password = data["password"]

    if users.find_one({"email": email}):
        return {"erorr": "Email already present"}, 400
    if users.find_one({"username": username}):
        return {"erorr": "Username already present"}, 400

    hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")

    result = users.insert_one(
        {
            "username": username,
            "email": email,
            "password": hashed_password,
        }
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "User created successfully",
                "user_id": str(result.inserted_id),
                "username": username,
            }
        ),
        200,
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return {"error": "Invalid input"}, 400

    email = data["email"].strip().lower()
    password = data["password"]

    user = users.find_one({"email": email})

    if not user:
        return {"erorr": "User not found"}, 400

    if not Bcrypt().check_password_hash(user["password"], password):
        return {"erorr": "Invalid password"}, 400

    return (
        jsonify(
            {
                "success": True,
                "message": "Login successful",
                "user_id": str(user["_id"]),
            }
        ),
        200,
    )


@app.route("/blog", methods=["POST"])
def blog():
    data = request.json
    if (
        not data
        or "title" not in data
        or "tone" not in data
        or "content" not in data
        or "topic" not in data
    ):
        return {"error": "Invalid input"}, 400

    title = data["title"].strip()
    tone = data["tone"].strip()
    content = data["content"].strip()
    topic = data["topic"].strip()
    user_id = data.get("user_id")
    is_public = data.get(
        "public", True
    )  # this is to make sure that there's a distinction between public and private blogs
    published = data.get("published", True)  # This is for draft page
    result = blogs.insert_one(
        {
            "title": title,
            "tone": tone,
            "content": content,
            "topic": topic,
            "user_id": ObjectId(user_id) if user_id else None,
            "public": is_public,
            "published": published,  # This is for draft page
        }
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "Blog created!",
                "blod_id": str(result.inserted_id),
            },
        ),
        200,
    )


from bson import ObjectId, errors as bson_errors


@app.route("/blog/<user_id>", methods=["GET"])
def getBlog(user_id):
    try:
        # Validate user_id first
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400

        user_object_id = ObjectId(user_id)
        user = users.find_one({"_id": user_object_id})
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_blogs_cursor = blogs.find({"user_id": user_object_id})
        user_blogs = []
        for blog in user_blogs_cursor:
            blog["_id"] = str(blog["_id"])
            blog["user_id"] = str(blog["user_id"])
            user_blogs.append(blog)

        return jsonify({"username": user.get("username", ""), "blogs": user_blogs}), 200

    except Exception as e:
        print("Error fetching blogs:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/blog-feed", methods=["GET"])
def blogFeed():
    try:
        public_blogs_cursor = blogs.find({"public": True})
        public_blogs = []
        for blog in public_blogs_cursor:
            blog["_id"] = str(blog["_id"])
            blog["user_id"] = str(blog["user_id"])
            public_blogs.append(blog)
        return jsonify(public_blogs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/draft/<user_id>", methods=["GET"])
def draft(user_id):
    try:
        user_object_id = ObjectId(user_id)
        drafts = list(blogs.find({"user_id": user_object_id, "published": False}))
        for d in drafts:
            d["_id"] = str(d["_id"])
            d["user_id"] = str(d["user_id"])
        return jsonify({"drafts": drafts}), 200
    except Exception as e:
        print("ERROR while fetching drafts:", e)

        return jsonify({"error": str(e)}), 500


@app.route("/blog/<id>", methods=["PUT"])
def update_blog(id):
    data = request.get_json()

    updated_fields = {
        "title": data["title"],
        "tone": data["tone"],
        "content": data["content"],
        "topic": data["topic"],
        "public": data["public"],
        "published": data["published"],
    }

    result = blogs.update_one({"_id": ObjectId(id)}, {"$set": updated_fields})

    if result.matched_count == 0:
        return jsonify({"error": "Blog not found"}), 404

    return jsonify({"message": "Blog updated successfully"}), 200


@app.route("/private-blogs/<user_id>", methods=["GET"])
def get_private_blogs(user_id):
    private_blogs = list(
        blogs.find({"user_id": ObjectId(user_id), "published": True, "public": False})
    )
    for blog in private_blogs:
        blog["_id"] = str(blog["_id"])
        blog["user_id"] = str(blog["user_id"])
    return jsonify(private_blogs), 200


@app.route("/blog/<id>", methods=["DELETE"])
def delete_blog(id):
    result = blogs.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"error": "Blog not found"}), 404
    return jsonify({"message": "Blog deleted successfully"}), 200


@app.route("/single-blog/<id>", methods=["GET"])
def get_single_blog(id):
    try:
        blog = blogs.find_one({"_id": ObjectId(id)})
        if not blog:
            return jsonify({"error": "Blog not found"}), 404

        blog["_id"] = str(blog["_id"])
        blog["user_id"] = str(blog["user_id"])
        return jsonify({"blog": blog}), 200

    except Exception as e:
        print("Error fetching single blog:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/generate-blog", methods=["POST"])
def generate_blog():
    try:
        data = request.get_json()
        topic = data.get("topic")
        tone = data.get("tone")

        if not topic or not tone:
            return jsonify({"error": "Missing topic or tone"}), 400

        messages = [
            {
                "role": "system",
                "content": f"You are an expert blog writer. Write in a {tone} tone.",
            },
            {"role": "user", "content": f"Write a blog about: {topic}"},
        ]

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": REFERER,
                "X-Title": TITLE,
            },
            json={
                "model": "openai/gpt-3.5-turbo",  # you can also use 'meta-llama/llama-3-8b-instruct' or others
                "messages": messages,
            },
        )

        if response.status_code != 200:
            print("OpenRouter error:", response.text)
            return jsonify({"error": "OpenRouter failed"}), 500

        result = response.json()
        blog_content = result["choices"][0]["message"]["content"]

        return jsonify({"blog": blog_content}), 200

    except Exception as e:
        print("Error generating blog:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/delete-user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID"}), 400

        user_object_id = ObjectId(user_id)

        user = users.find_one({"_id": user_object_id})
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete the user
        users.delete_one({"_id": user_object_id})

        # Delete all blogs by this user
        result = blogs.delete_many({"user_id": user_object_id})

        return (
            jsonify(
                {
                    "message": "User and all associated blogs deleted.",
                    "blogs_deleted": result.deleted_count,
                }
            ),
            200,
        )

    except Exception as e:
        print("Error deleting user:", e)
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

