import pytest
from fastapi.testclient import TestClient
from main import app
import logging

client = TestClient(app)
tag = "tag"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ingestion_for_csv():
    csv_file = open("./../src/api/src/tests/test1.csv", "rb")
    csv = csv_file.read()

    response = client.post(
        "/ingest",
        files={"files": ("test1.csv", csv, "text/csv")},
        data={"tags": "s2"}
    )

    response_data = response.json()
    print("Response:", response_data)

    tag = response.json()["results"][0]["data"]["tag"]
    assert response.status_code == 200
    assert response.json()["message"] == "Processamento concluído"
    assert response.json()["results"][0]["status"] == "success"
    assert response.json()["results"][0]["file"] == "test1.csv"
    assert response.json()["results"][0]["data"]["tag"].startswith(
        "test1_csv_")


def test_visualize():
    csv_file = open("./../src/api/src/tests/test2.csv", "rb")
    csv = csv_file.read()

    response = client.post(
        "/ingest",
        files={"files": ("test2.csv", csv, "text/csv")},
        data={"tags": "s2"}
    )

    response_data = response.json()

    tag = response.json()["results"][0]["data"]["tag"]

    print("Tag:", tag)

    response = client.get(f"/ingest/visualize/{tag}")

    print("Response:", response.json())

    assert response.status_code == 200
    assert response.json()["message"] == "Data retrieved successfully"
    assert response.json()["data"][0]["tag"] == tag


def test_ingestion_for_xlsx():
    xlsx_file = open("./../src/api/src/tests/test3.xlsx", "rb")
    xlsx = xlsx_file.read()

    response = client.post(
        "/ingest",
        files={"files": (
            "test3.xlsx", xlsx, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
        data={"tags": "s2"}
    )

    response_data = response.json()
    print("Response:", response_data)
    print(f"Response: {response.json()}\n{response.status_code}")

    assert response.json()["message"] == "Processamento concluído"
    assert response.json()["results"][0]["status"] == "error"
    assert response.json()["results"][0]["file"] == "test3.xlsx"
    assert response.json()[
        "results"][0]["error"] == "Invalid file format. Please upload a CSV file."
        
