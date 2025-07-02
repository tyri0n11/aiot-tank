from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def users():
    """Get list of users"""
    return jsonify([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])

if __name__ == "__main__":
    app.run(debug=True, port=8080)