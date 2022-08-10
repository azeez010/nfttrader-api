import jwt
from nft_api.validate import validate_email_and_password, validate_user
from flask import request, jsonify, url_for
from nft_api.helpers import get_paginated_list
from nft_api import app, env 
import cloudinary.uploader
from flask_cors import cross_origin
from nft_api import models
from nft_api.jwt_auth import admin_token_required

@app.route("/api/userNonce")
def user_nonce():
    address = request.args.get("address")
    get_nonce = models.User().get_nonce(address)
    if get_nonce:
        return {
            "message": "Nonce retrieved successfully",
            "data": get_nonce,
        }, 200
    else:
        return {
            "message": "No nonce found",
            "data": get_nonce,
        }, 401


@app.route("/api/upload", methods=['POST'])
@admin_token_required
def upload_file(current_user):
  print('in upload route')
  upload_result = None
  if request.method == 'POST':
    print("No 1", request.files)
    file_to_upload = request.files['file']
    print('%s file_to_upload', file_to_upload)
    if file_to_upload:
        cloudinary.config(cloud_name = env.str('IMAGE_CLOUD_NAME'), api_key=env.str('IMAGE_API_KEY'), api_secret=env.str('IMAGE_API_SECRET'))
        upload_result = cloudinary.uploader.upload(file_to_upload)
        print(upload_result)
        return jsonify(upload_result)

@app.route("/api/verify")
@admin_token_required
def verify(current_user):
    return {
        "message": "Login Success",
        "data": current_user,
    }, 200

@app.route("/api/user/del/<user_id>", methods=["DELETE"])
# @admin_token_required
def delete_user(user_id):
    models.User().delete_one(user_id)
    return {
        "message": "Delete Successful",
    }, 200

@app.route("/api/create-user", methods=["POST"])
def add_user():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # is_validated = validate_user(**user)
        # if is_validated is not True:
        #     return dict(message='Invalid data', data=None, error=is_validated), 400
        if user.get('secret'):
            user.pop('secret')
            user["admin"] = True
            
        user = models.User().create(**user)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        return {
            "message": "Successfully created new user",
            "data": user
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@cross_origin
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        
        user = models.User().login(
            data["email"],
            data["password"]
        )
        
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"user_id": user["id"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Login successful",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500

@app.route("/api/admin/users", methods=["GET"])
@admin_token_required
def admin_get_users(current_user):
    try:
        users = models.User().get_all()
        if request.args.get('start') and request.args.get('limit'):
            if request.args.get('start').isnumeric() and request.args.get('limit').isnumeric():
                users = get_paginated_list(
                    users, 
                    url_for("admin_get_users"), 
                    start=request.args.get('start', 1), 
                    limit=request.args.get('limit', 20)
                )

        return jsonify({
            "message": "successfully retrieved all users",
            "data": users
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all users",
            "error": str(e),
            "data": None
        }), 500


@app.route("/api/user/<user_id>", methods=["POST"])
# @admin_token_required
def update_user(user_id):
    try:
        user = models.User().get_by_id(user_id)
        user_update = request.json
        # is_validated = validate_user(**user)
        # if is_validated is not True:
            # return {
            #     "message": "Invalid data",
            #     "data": None,
            #     "error": is_validated
            # }, 400
        print(user_update)
        models.User().update_one(user_id, **user_update)
        return jsonify({
            "message": "successfully updated a user",
            "data": user
        }), 201
    
    except Exception as e:
        return jsonify({
            "message": "failed to update a user",
            "error": str(e),
            "data": None
        }), 400

@app.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403

@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404


if __name__ == "__main__":
    app.run(debug=True)