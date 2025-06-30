import requests

backend_url = "http://0.0.0.0:8000"

def test_ask_endpoint():
    query = "belia india lelaki di Selangor?"
    response = requests.post(f"{backend_url}/ask", json={"user_query": query})
    print("Response from /ask:")
    print(response.json())

def test_health_check():
    response = requests.get(f"{backend_url}/health")
    print("Health check response:", response.json())

if __name__ == "__main__":
    test_health_check()
    test_ask_endpoint()
