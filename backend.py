from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import shutil
import sys
import traceback
import socket
import os

app = Flask(__name__)
CORS(app)

# Function to locate Sublist3r
def find_sublist3r():
    """Finds the installed path of Sublist3r dynamically."""
    try:
        result = subprocess.run(["pip", "show", "sublist3r"], capture_output=True, text=True, check=True)
        for line in result.stdout.split("\n"):
            if line.startswith("Location:"):
                path = os.path.join(line.split(": ")[1].strip(), "sublist3r.py")
                print(f"✅ Sublist3r found at: {path}")  # Debugging log
                return path
    except subprocess.CalledProcessError:
        print("❌ Sublist3r is not installed.")
        return None

# Detect Sublist3r path
SUBLIST3R_PATH = find_sublist3r()

# Check required tools
def check_dependencies():
    """Ensures required tools exist before running."""
    missing = []
    
    if not shutil.which("python"):
        missing.append("Python is not found in system PATH.")
    
    if not SUBLIST3R_PATH or not os.path.exists(SUBLIST3R_PATH):
        missing.append("Sublist3r is not installed or not found.")

    if missing:
        print("❌ Missing dependencies:", missing)
    
    return missing

# Run Sublist3r
def run_sublist3r(domain):
    """Runs Sublist3r and returns subdomains along with logs."""
    missing_tools = check_dependencies()
    if missing_tools:
        return [], "; ".join(missing_tools), ""

    if not os.path.exists(SUBLIST3R_PATH):
        return [], f"Sublist3r script not found at: {SUBLIST3R_PATH}", ""

    try:
        print(f"🔍 Running Sublist3r for domain: {domain}")
        result = subprocess.run(
            [sys.executable, SUBLIST3R_PATH, "-d", domain], 
            capture_output=True, text=True, check=True
        )

        output_log = result.stdout  # Capture full logs
        print(f"📜 Sublist3r Output:\n{output_log}")

        subdomains = [
            sub.strip() for sub in output_log.split("\n")
            if domain in sub and "Enumerating subdomains" not in sub
        ]

        return subdomains, None, output_log  # Include logs
    except subprocess.CalledProcessError as e:
        return [], f"Sublist3r error: {e}", ""
    except FileNotFoundError:
        return [], "Sublist3r file not found.", ""
    except Exception as e:
        return [], f"Unexpected error running Sublist3r: {traceback.format_exc()}", ""

# Get subdomain details (only IP and domain name)
def get_subdomain_info(subdomain):
    """Fetches IP address for a subdomain."""
    try:
        ip = socket.gethostbyname(subdomain)
    except socket.gaierror:
        ip = "Unknown"

    return {"subdomain": subdomain, "ip": ip}

# Update API Route
@app.route("/find-subdomains", methods=["POST"])
def find_subdomains():
    """API endpoint to find subdomains and return logs."""
    data = request.get_json()
    domain = data.get("domain")

    if not domain:
        return jsonify({"error": "Domain is required"}), 400

    try:
        print(f"🔍 Received domain: {domain}")

        subdomains, error, logs = run_sublist3r(domain)

        if error:
            print(f"❌ Error: {error}")
            return jsonify({"error": error, "logs": logs}), 500

        subdomain_details = [get_subdomain_info(sub) for sub in subdomains]
        return jsonify({"subdomains": subdomain_details, "logs": logs})

    except Exception as e:
        print(f"🔥 Exception occurred: {traceback.format_exc()}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
