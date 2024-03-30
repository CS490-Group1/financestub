from flask import Flask, request, jsonify

app = Flask(__name__)

## This is going to be a simple financal stub for the online car dealership ##

@app.post("/test")
def test():
    return True


if __name__ == "__main__":
    app.run(debug=True, port=8001)