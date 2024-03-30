from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

## This is going to be a simple financal stub for the online car dealership ##

@app.get("/test")
def test():
    response = make_response("Test is Hit!")
    response.headers["response"] = "Test is Actually Being Hit!"
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8001)