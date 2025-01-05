import requests
import random
from faker import Faker

fake = Faker()

BASE_URL = "http://127.0.0.1:8000"  # URL вашего приложения

# Функция для создания операторов
def create_operators(count=10):
    for _ in range(count):
        data = {
            "name": fake.company(),
            "operator_code": fake.unique.numerify("###"),
            "number_count": random.randint(1000, 10000)
        }
        response = requests.post(f"{BASE_URL}/operators/", json=data)
        if response.status_code == 200:
            print(f"Operator created: {response.json()}")
        else:
            print(f"Failed to create operator: {response.text}")

# Функция для создания абонентов
def create_subscribers(count=50):
    for _ in range(count):
        data = {
            "passport_data": fake.unique.bothify("????########"),
            "full_name": fake.name(),
            "address": fake.address()
        }
        response = requests.post(f"{BASE_URL}/subscribers/", json=data)
        if response.status_code == 200:
            print(f"Subscriber created: {response.json()}")
        else:
            print(f"Failed to create subscriber: {response.text}")

# Функция для создания подключений
def create_connections(count=100):
    # Получаем операторов и абонентов
    operators = requests.get(f"{BASE_URL}/operators/").json()
    subscribers = requests.get(f"{BASE_URL}/subscribers/").json()
    if not operators or not subscribers:
        print("Not enough operators or subscribers to create connections.")
        return

    for _ in range(count):
        data = {
            "operator_id": random.choice(operators)["operator_id"],
            "subscriber_id": random.choice(subscribers)["subscriber_id"],
            "number": fake.unique.numerify("89#########"),
            "tariff_plan": fake.word(),
            "debt": round(random.uniform(0, 1000), 2),
            "installation_date": fake.date_between(start_date="-2y", end_date="today").isoformat()
        }
        response = requests.post(f"{BASE_URL}/connections/", json=data)
        if response.status_code == 200:
            print(f"Connection created: {response.json()}")
        else:
            print(f"Failed to create connection: {response.text}")

if __name__ == "__main__":
    print("Creating operators...")
    create_operators(10)
    print("Creating subscribers...")
    create_subscribers(50)
    print("Creating connections...")
    create_connections(100)
