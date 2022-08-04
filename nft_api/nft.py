from flask import request, jsonify
from nft_api.jwt_auth import token_required, admin_token_required
from nft_api import app, db, models
from nft_api.validate import validate_nft
import requests

@app.route("/api/nft/", methods=["POST"])
@token_required
def add_nft(current_user):
    try:

#     import fetch from 'node-fetch';

#   var requestOptions = {
#     method: 'GET',
#     redirect: 'follow'
#   };  
        nft = request.json

        for _nft in nft:
            apiKey = "23eL-CvsUZDMJ-qvtj7UVg_VFiy4LMrj"
            baseURL = f"https://eth-mainnet.alchemyapi.io/nft/v2/{apiKey}/getNFTMetadata"
            contractAddr = _nft.get("nftToken")
            # "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
            tokenId = "2"
            tokenType = "erc721"
            fetchURL = f"{baseURL}?contractAddress={contractAddr}&tokenId={tokenId}&tokenType={tokenType}"

            headers = {"Accept": "application/json"}

            # response = requests.get(fetchURL, headers=headers)

            # print(response.json())
            
            nft = request.json
            # print(_nft, 2)

        if not nft:
            return {
                "message": "Invalid data, you need to give the nft name, image and address",
                "data": None,
                "error": "Bad Request"
            }, 400
        # if not request.files["cover_image"]:
        #     return {
        #         "message": "cover image is required",
        #         "data": None
        #     }, 400

        # nft["image"] = "" #request.host_url+"static/nft/"+save_pic(request.files["cover_image"])
        nft["owner"] = current_user["id"]
        is_validated = validate_nft(**nft)
        if is_validated is not True:
            return {
                "message": "Invalid data",
                "data": None,
                "error": is_validated
            }, 400
        nft = models.NFT().create(**nft)
        if not nft:
            return {
                "message": "The nft has been created by user",
                "data": None,
                "error": "Conflict"
            }, 400
        return jsonify({
            "message": "successfully created a new nft",
            "data": nft
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to create a new nft",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/admin/nft", methods=["GET"])
@admin_token_required
def admin_get_nfts(current_user):
    try:
        nft = models.NFT().get_all()
        return jsonify({
            "message": "successfully retrieved all nft",
            "data": nft
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all nft",
            "error": str(e),
            "data": None
        }), 500


@app.route("/api/nft", methods=["GET"])
@admin_token_required
def get_nfts(current_user):
    try:
        nft = models.NFT().user_get_all(current_user["id"])
        return jsonify({
            "message": "successfully retrieved all nft",
            "data": nft
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all nft",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/nft/<nft_id>", methods=["GET"])
@token_required
def get_nft(current_user, nft_id):
    try:
        nft = models.NFT().get_by_id(nft_id)
        if not nft:
            return {
                "message": "nft not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a nft",
            "data": nft
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/nft/<nft_id>", methods=["PUT"])
@token_required
def update_nft(current_user, nft_id):
    try:
        nft = models.NFT().get_by_id(nft_id)
        if not nft or nft["owner"] != current_user["id"]:
            return {
                "message": "nft not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        
        nft = request.json
        is_validated = validate_nft(**nft)
        if is_validated is not True:
            return {
                "message": "Invalid data",
                "data": None,
                "error": is_validated
            }, 400
        
        nft = models.NFT().update_one(nft_id, **nft)
        return jsonify({
            "message": "successfully updated a nft",
            "data": nft
        }), 201
    
    except Exception as e:
        return jsonify({
            "message": "failed to update a nft",
            "error": str(e),
            "data": None
        }), 400

@app.route("/nft/<nft_id>", methods=["DELETE"])
@token_required
def delete_nft(current_user, nft_id):
    try:
        nft = nft().get_by_id(nft_id)
        if not nft or nft["user_id"] != current_user["_id"]:
            return {
                "message": "nft not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        nft().delete(nft_id)
        return jsonify({
            "message": "successfully deleted a nft",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to delete a nft",
            "error": str(e),
            "data": None
        }), 400