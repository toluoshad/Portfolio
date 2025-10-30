import sys
import io
from django.test import TestCase
from graphene.test import Client
from taskmanager.schema import schema
from users.models import User

# Ensure UTF-8 encoding to avoid UnicodeEncodeError on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class UserMutationTest(TestCase):
    def setUp(self):
        print("\n[SETUP] Initializing test client and creating test user...")
        self.client = Client(schema)

        # Create a test user for update and delete tests
        self.test_user = User.objects.create(
            username="testuser",
            email="test@email.com",
            password="securepassword123"
        )
        print("[SETUP] Test user created.")

    def test_create_user(self):
        """Test creating a new user successfully"""
        print("\n[TEST] Running test_create_user...")
        mutation = '''
        mutation {
            createUser(username: "newuser", email: "newuser@email.com", password: "securepassword") {
                user {
                    id
                    username
                    email
                }
            }
        }
        '''
        response = self.client.execute(mutation)
        self.assertIsNone(response.get("errors"), msg=f"[ERROR] User creation failed: {response.get('errors')}")
        data = response.get("data", {}).get("createUser", {}).get("user")
        self.assertIsNotNone(data, msg="[ERROR] No user data returned.")
        self.assertEqual(data["username"], "newuser")
        self.assertEqual(data["email"], "newuser@email.com")
        print("[SUCCESS] User creation test passed!")

    def test_update_user(self):
        """Test updating an existing user's email"""
        print("\n[TEST] Running test_update_user...")
        mutation = f'''
        mutation {{
            updateUser(id: {self.test_user.id}, email: "updated@email.com") {{
                user {{
                    id
                    email
                }}
            }}
        }}
        '''
        response = self.client.execute(mutation)
        self.assertIsNone(response.get("errors"), msg=f"[ERROR] User update failed: {response.get('errors')}")
        data = response.get("data", {}).get("updateUser", {}).get("user")
        self.assertIsNotNone(data, msg="[ERROR] No user data returned.")
        self.assertEqual(data["email"], "updated@email.com")
        print("[SUCCESS] User update test passed!")

    def test_delete_user(self):
        """Test deleting an existing user"""
        print("\n[TEST] Running test_delete_user...")
        mutation = f'''
        mutation {{
            deleteUser(id: {self.test_user.id}) {{
                success
            }}
        }}
        '''
        response = self.client.execute(mutation)
        self.assertIsNone(response.get("errors"), msg=f"[ERROR] User deletion failed: {response.get('errors')}")
        data = response.get("data", {}).get("deleteUser", {})
        self.assertTrue(data.get("success"), msg="[ERROR] User deletion response was unsuccessful.")

        # Check if the user is actually deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.test_user.id)

        print("[SUCCESS] User deletion test passed!")
