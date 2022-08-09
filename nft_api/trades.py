import datetime
from flask import request, jsonify, url_for
from nft_api.helpers import get_paginated_list
from nft_api.jwt_auth import form_admin_token_required, token_required, admin_token_required
from nft_api import app, env, models
from flask_expects_json import expects_json
from nft_api.validate import trade_validation_schema
import cloudinary.uploader
# from nft_api.validate import validate_trades

@app.route("/api/trades", methods=["POST"])
# @form_admin_token_required
# current_user
def add_trades():
    try:
        trades = request.form.to_dict()
        print(trades)
        file_to_upload = request.files
        print('%s file_to_upload', file_to_upload)
        for file_name in file_to_upload:
            print('%s file_name', file_name)
            if file_name:
                cloudinary.config(cloud_name = env.str('IMAGE_CLOUD_NAME'), api_key=env.str('IMAGE_API_KEY'), api_secret=env.str('IMAGE_API_SECRET'))
                upload_result = cloudinary.uploader.upload(file_to_upload[file_name])
                trades[file_name] = upload_result["secure_url"]
                print(upload_result)
                # return jsonify(upload_result)
        
        
        
        trades.pop("Authorization")
        # date_in = trades.get("expiry_date")
        # date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
        # date_processing = [int(v) for v in date_processing]
        # date_out = datetime.datetime(*date_processing)
        # trades["expiry_date"] = date_out
        
        if not trades:
            return {
                "message": "Invalid data, you need to give the trades name, image and address",
                "data": None,
                "error": "Bad Request"
            }, 400
        # if not request.files["cover_image"]:
        #     return {
        #         "message": "cover image is required",
        #         "data": None
        #     }, 400

        # trades["image"] = "" #request.host_url+"static/trades/"+save_pic(request.files["cover_image"])
        trades["owner"] = current_user["id"]
        trades = models.Trades().create(**trades)
        if not trades:
            return {
                "message": "The trades has been created by user",
                "data": None,
                "error": "Conflict"
            }, 400
        return jsonify({
            "message": "successfully created a new trades",
            "data": trades
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to create a new trades",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/admin/trades", methods=["GET"])
@admin_token_required
def admin_get_trades(current_user):
    try:
        trades = models.Trades().get_all()
        if request.args.get('start') and request.args.get('limit'):
            if request.args.get('start').isnumeric() and request.args.get('limit').isnumeric():
                trades = get_paginated_list(
                    trades, 
                    url_for("admin_get_trades"), 
                    start=request.args.get('start', 1), 
                    limit=request.args.get('limit', 20)
                )

        return jsonify({
            "message": "successfully retrieved all trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all trades",
            "error": str(e),
            "data": None
        }), 500


@app.route("/api/client-trades/<client_address>", methods=["GET"])
@admin_token_required
def get_client_trades(current_user, client_address):
    try:
        trades = models.Trades().get_client_trades(client_address)
        return jsonify({
            "message": "successfully retrieved all trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all trades",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades", methods=["GET"])
@admin_token_required
def get_trades(current_user):
    try:
        trades = models.Trades().user_get_all(current_user["id"])
        return jsonify({
            "message": "successfully retrieved all trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all trades",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades/<trade_id>/nfts", methods=["GET"])
@admin_token_required
def get_nft_trades(current_user, trade_id):
    try:
        trades = models.Trades().get_trade_nfts(trade_id)
        return jsonify({
            "message": "successfully retrieved all nft from trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all nft from trades",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades/search/<trade_str>", methods=["GET"])
@token_required
def search(current_user, trade_str):
    try:
        trades = models.Trades().search(trade_str)
        if request.args.get('start') and request.args.get('limit'):
            if request.args.get('start').isnumeric() and request.args.get('limit').isnumeric():
                trades = get_paginated_list(
                    trades, 
                    url_for("search", trade_str=trade_str),
                    start=request.args.get('start', 1), 
                    limit=request.args.get('limit', 20)
                )

        if not trades:
            return {
                "message": "trades not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades/<trades_id>", methods=["GET"])
@token_required
def get_trade(current_user, trades_id):
    try:
        trades = models.Trades().get_by_id(trades_id)
        if not trades:
            return {
                "message": "trades not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades/<trades_id>", methods=["PUT"])
@admin_token_required
def update_trades(current_user, trades_id):
    try:
        trades = models.Trades().get_by_id(trades_id)
        if not trades or trades["owner"] != current_user["id"]:
            return {
                "message": "trades not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        
        trades = request.json
        # is_validated = validate_trades(**trades)
        # if is_validated is not True:
            # return {
            #     "message": "Invalid data",
            #     "data": None,
            #     "error": is_validated
            # }, 400
        trades = models.Trades().update_one(trades_id, **trades)
        return jsonify({
            "message": "successfully updated a trades",
            "data": trades
        }), 201
    
    except Exception as e:
        return jsonify({
            "message": "failed to update a trades",
            "error": str(e),
            "data": None
        }), 400

@app.route("/api/trades/<trades_id>", methods=["DELETE"])
@admin_token_required
def delete_trades(current_user, trades_id):
    try:
        trades = models.Trades().get_by_id(trades_id)
        print(trades["owner"])
        if not trades or trades["owner"] != current_user["id"]:
            return {
                "message": "trades not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        models.Trades().delete_one(trades_id)
        return jsonify({
            "message": "successfully deleted a trades",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to delete a trades",
            "error": str(e),
            "data": None
        }), 400