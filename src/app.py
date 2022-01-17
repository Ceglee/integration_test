from flask import Flask, Response, request, json

from user_details_service import UserDetailsService

app = Flask(__name__)

USER_DETAILS_SERVICE = UserDetailsService()


@app.route("/", methods=["POST"])
def get_user_details():
    if validate(request.json):
        return USER_DETAILS_SERVICE.get_user_details(request.json["user_name"]).__dict__

    else:
        return Response(response=json.dumps({"message": "Required user_name value is invalid."}), status=422, mimetype='application/json')


def validate(json):

    if "user_name" in json:
        user_name = request.json["user_name"]
        return user_name is not None and isinstance(user_name, str) and user_name

    return False
