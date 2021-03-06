import time

from flask import Flask, Response, request, json

from user_details_service import UserDetailsService

app = Flask(__name__)

USER_DETAILS_SERVICE = UserDetailsService()


@app.route("/", methods=["POST"])
def get_user_details():
    start = time.time_ns()
    if validate(request.json):
        user_details = USER_DETAILS_SERVICE.get_user_details(request.json["user_name"])
        result = (time.time_ns() - start) / 1_000_000
        print("Message processed in: " + str(result) + " milliseconds.")
        return user_details or Response(response=json.dumps({"message": "Unable to retrieve user details."}), status=204, mimetype="application/json")

    else:
        return Response(response=json.dumps({"message": "Required user_name value is invalid."}), status=422, mimetype="application/json")


def validate(json):
    user_name = json.get("user_name")
    return user_name and isinstance(user_name, str) and user_name.strip()

