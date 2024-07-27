import subprocess
import time
import requests
import unittest


class APITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_process = subprocess.Popen(["python", "tests/run_app.py"])
        time.sleep(5) # Adjust wait time for application initialization
        cls.token = cls.fetch_auth_token("testuser@example.com", "testpassword")

    @classmethod
    def tearDownClass(cls):
        cls.app_process.terminate()
        cls.app_process.wait()

    @classmethod
    def fetch_auth_token(cls, email, password):
        response = requests.post('http://localhost:8000/register', json={
            "name": email.split('@')[0],
            "email": email,
            "password": password
        })
        if response.status_code == 400:
            response = requests.post('http://localhost:8000/login', json={
                "email": email,
                "password": password
            })
        assert response.status_code == 200, f"Failed to fetch auth token, status code: {response.status_code}"
        response_data = response.json()
        assert 'token' in response_data
        return response_data['token']

    def test_register(self):
        response = requests.post('http://localhost:8000/register', json={
            "name": "testuser2",
            "email": "testuser2@example.com",
            "password": "testpassword"
        })
        self.assertIn(response.status_code, [200, 409, 400])  # Handle already registered user

    def test_login(self):
        response = requests.post('http://localhost:8000/login', json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('token', response_data)

    def test_create_and_read_device(self):
        create_response = requests.post('http://localhost:8000/device', json={
            "name": "Device1",
            "type": "Sensor",
            "login": "device_login",
            "password": "device_pass",
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        create_data = create_response.json()
        self.assertIn('id', create_data)
        device_id = create_data['id']

        read_response = requests.get(f'http://localhost:8000/device/{device_id}',
                                     headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(read_response.status_code, 200)
        read_data = read_response.json()
        self.assertEqual(read_data['id'], device_id)
        self.assertEqual(read_data['name'], "Device1")
        self.assertEqual(read_data['type'], "Sensor")
        self.assertEqual(read_data['login'], "device_login")
        self.assertEqual(read_data['password'], "device_pass")

    def test_update_device(self):
        create_response = requests.post('http://localhost:8000/device', json={
            "name": "Device1",
            "type": "Sensor",
            "login": "device_login",
            "password": "device_pass",
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        create_data = create_response.json()
        device_id = create_data['id']

        update_response = requests.put(f'http://localhost:8000/device/{device_id}', json={
            "name": "Updated Device"
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(update_response.status_code, 200)
        update_data = update_response.json()
        self.assertEqual(update_data['name'], "Updated Device")

    def test_delete_device(self):
        create_response = requests.post('http://localhost:8000/device', json={
            "name": "Device1",
            "type": "Sensor",
            "login": "device_login",
            "password": "device_pass",
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        create_data = create_response.json()
        device_id = create_data['id']

        delete_response = requests.delete(f'http://localhost:8000/device/{device_id}',
                                          headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(delete_response.status_code, 200)
        delete_data = delete_response.json()
        self.assertEqual(delete_data['status'], 'success')

    def test_create_device_without_auth(self):
        response = requests.post('http://localhost:8000/device', json={
            "name": "Device1",
            "type": "Sensor",
            "login": "device_login",
            "password": "device_pass",
        })
        self.assertEqual(response.status_code, 401)

    def test_update_device_without_auth(self):
        response = requests.put('http://localhost:8000/device/1', json={
            "name": "Updated Device"
        })
        self.assertEqual(response.status_code, 401)

    def test_delete_device_without_auth(self):
        response = requests.delete('http://localhost:8000/device/1')
        self.assertEqual(response.status_code, 401)

    def test_update_device_as_different_user(self):
        different_user_token = self.fetch_auth_token("testuser2@example.com", "testpassword")
        create_response = requests.post('http://localhost:8000/device', json={
            "name": "Device1",
            "type": "Sensor",
            "login": "device_login",
            "password": "device_pass",
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        create_data = create_response.json()
        device_id = create_data['id']

        update_response = requests.put(f'http://localhost:8000/device/{device_id}', json={
            "name": "Updated Device"
        }, headers={'Authorization': f'Bearer {different_user_token}'})
        self.assertEqual(update_response.status_code, 403)

    def test_delete_device_as_different_user(self):
        different_user_token = self.fetch_auth_token("testuser2@example.com", "testpassword")
        create_response = requests.post('http://localhost:8000/device', json={
            "name": "Device1",
            "type": "Sensor",
            "login": "device_login",
            "password": "device_pass",
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(create_response.status_code, 201)
        create_data = create_response.json()
        device_id = create_data['id']

        delete_response = requests.delete(f'http://localhost:8000/device/{device_id}',
                                          headers={'Authorization': f'Bearer {different_user_token}'})
        self.assertEqual(delete_response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
