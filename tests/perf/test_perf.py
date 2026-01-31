import requests
import pytest

BASE_URL = "http://127.0.0.1:5000/api/accounts"

class TestPerf:

    @pytest.fixture
    def person(self):
        return {
            "name": "Jane",
            "surname": "Doe",
            "pesel": "06230145678"
        }

    @pytest.fixture
    def timeout(self):
        return 0.5

    def test_time_of_creation_and_deletion(self, person, timeout):
        for i in range(100):
            pesel = f"{person['pesel'][:-2]}{i:02d}"
            data = {**person, "pesel": pesel}

            r = requests.post(BASE_URL, json=data, timeout=timeout)
            assert r.status_code == 201

            r = requests.delete(f"{BASE_URL}/{pesel}", timeout=timeout)
            assert r.status_code == 200

    def test_time_of_logging_transfers(self, person, timeout):
        r = requests.post(BASE_URL, json=person, timeout=timeout)
        assert r.status_code == 201

        for _ in range(100):
            r = requests.post(
                f"{BASE_URL}/{person['pesel']}/transfer",
                json={"amount": 1, "type": "incoming"},
                timeout=timeout
            )
            assert r.status_code == 200

        r = requests.get(f"{BASE_URL}/{person['pesel']}")
        assert r.status_code == 200
        assert r.json()["balance"] == 100

        r = requests.delete(f"{BASE_URL}/{person['pesel']}", timeout=timeout)
        assert r.status_code == 200