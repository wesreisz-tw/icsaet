"""Mock ICAET server for testing."""

from flask import Flask, jsonify, request
from typing import Optional


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = True
    
    @app.route("/query", methods=["POST"])
    def query_endpoint():
        api_key = request.headers.get("x-api-key")
        
        if not api_key:
            return jsonify({"error": "Invalid API key"}), 401
        
        try:
            data = request.get_json()
        except Exception:
            return jsonify({"error": "Invalid JSON"}), 400
        
        if "question" not in data:
            return jsonify({"error": "Missing required field: question"}), 400
        
        if "email" not in data:
            return jsonify({"error": "Missing required field: email"}), 400
        
        question = data["question"]
        
        if question == "trigger_server_error":
            return jsonify({"error": "Internal server error"}), 500
        
        return jsonify({
            "answer": "This is a mock response to your question.",
            "sources": ["mock_source.txt"],
            "confidence": 0.95
        }), 200
    
    return app

