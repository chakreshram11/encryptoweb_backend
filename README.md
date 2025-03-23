# Subdomain Finder API using Flask and Sublist3r

This project is a simple Flask-based API that utilizes [Sublist3r](https://github.com/aboul3la/Sublist3r) to find subdomains for a given domain. It includes error handling, dependency checks, and provides logs for debugging.

## Features
- Finds subdomains using Sublist3r.
- Provides IP addresses of discovered subdomains.
- Includes error handling and logs.
- Supports CORS for frontend integration.

## Prerequisites
Make sure you have the following installed:
- Python (>= 3.x)
- Flask
- Flask-CORS
- Sublist3r

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/subdomain-finder-api.git
   cd subdomain-finder-api
   ```
2. Install required dependencies:
   ```sh
   pip install flask flask-cors sublist3r
   ```

## Running the API
Start the Flask server:
```sh
python app.py
```
The API will be available at `http://127.0.0.1:5000/`

## API Usage
### Find Subdomains
**Endpoint:**
```
POST /find-subdomains
```
**Request Body:**
```json
{
  "domain": "example.com"
}
```
**Response:**
```json
{
  "subdomains": [
    { "subdomain": "sub.example.com", "ip": "192.168.1.1" },
    { "subdomain": "test.example.com", "ip": "192.168.1.2" }
  ],
  "logs": "Full Sublist3r output logs"
}
```

## Error Handling
- If Sublist3r is not installed or found, an appropriate error is returned.
- If the domain is invalid or missing, a `400 Bad Request` response is returned.
- If an internal error occurs, a `500 Internal Server Error` response is returned.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contribution
Feel free to open an issue or submit a pull request to improve the project!

---
**Author:** Your Name

