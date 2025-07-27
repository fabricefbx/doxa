#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Doxa Investments SARL
Tests all endpoints including authentication, orders, messages, quotes, and prospects
"""

import requests
import sys
import json
from datetime import datetime
import uuid

class DoxaAPITester:
    def __init__(self, base_url="https://a65047d3-b7cc-4c89-ad46-35f4dbed54e8.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.user_data = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_user_email = f"test_user_{datetime.now().strftime('%H%M%S')}@doxa.test"
        self.test_user_password = "TestPass123!"
        
        print(f"🚀 Starting Doxa Investments SARL API Tests")
        print(f"📍 Base URL: {self.base_url}")
        print(f"👤 Test User: {self.test_user_email}")
        print("=" * 60)

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Test {self.tests_run}: {name}")
        print(f"   {method} {endpoint}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"   ✅ PASSED - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, dict) and len(response_data) <= 5:
                        print(f"   📄 Response: {json.dumps(response_data, indent=2)[:200]}...")
                    elif isinstance(response_data, list) and len(response_data) > 0:
                        print(f"   📄 Response: {len(response_data)} items returned")
                except:
                    print(f"   📄 Response: {response.text[:100]}...")
            else:
                print(f"   ❌ FAILED - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   📄 Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   📄 Error: {response.text}")

            return success, response.json() if response.text else {}

        except requests.exceptions.RequestException as e:
            print(f"   ❌ FAILED - Network Error: {str(e)}")
            return False, {}
        except Exception as e:
            print(f"   ❌ FAILED - Error: {str(e)}")
            return False, {}

    def test_health_check(self):
        """Test the health endpoint"""
        print("\n🏥 HEALTH CHECK TESTS")
        print("-" * 30)
        
        success, response = self.run_test(
            "Health Check",
            "GET",
            "api/health",
            200
        )
        
        if success and response.get('status') == 'healthy':
            print("   💚 Backend is healthy and running")
            return True
        else:
            print("   💔 Backend health check failed")
            return False

    def test_branches(self):
        """Test branches endpoint"""
        print("\n🏢 BRANCHES TESTS")
        print("-" * 30)
        
        success, response = self.run_test(
            "Get Business Branches",
            "GET",
            "api/branches",
            200
        )
        
        if success and isinstance(response, list) and len(response) == 7:
            print(f"   ✅ Found {len(response)} business branches")
            branch_names = [branch.get('name', 'Unknown') for branch in response]
            print(f"   📋 Branches: {', '.join(branch_names[:3])}...")
            return True
        else:
            print("   ❌ Branches test failed")
            return False

    def test_user_registration(self):
        """Test user registration"""
        print("\n👤 USER REGISTRATION TESTS")
        print("-" * 30)
        
        user_data = {
            "email": self.test_user_email,
            "password": self.test_user_password,
            "full_name": "Test User Doxa",
            "company": "Test Company SARL",
            "phone": "+243123456789",
            "address": "Kolwezi, DRC"
        }
        
        success, response = self.run_test(
            "Register New User",
            "POST",
            "api/auth/register",
            200,
            data=user_data
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.user_data = response.get('user', {})
            print(f"   🎫 Token received: {self.token[:20]}...")
            print(f"   👤 User ID: {self.user_data.get('id', 'Unknown')}")
            return True
        else:
            print("   ❌ User registration failed")
            return False

    def test_user_login(self):
        """Test user login with existing credentials"""
        print("\n🔐 USER LOGIN TESTS")
        print("-" * 30)
        
        # Clear token to test login
        old_token = self.token
        self.token = None
        
        login_data = {
            "email": self.test_user_email,
            "password": self.test_user_password
        }
        
        success, response = self.run_test(
            "Login Existing User",
            "POST",
            "api/auth/login",
            200,
            data=login_data
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            print(f"   🎫 New token received: {self.token[:20]}...")
            return True
        else:
            print("   ❌ User login failed")
            self.token = old_token  # Restore old token
            return False

    def test_user_profile(self):
        """Test getting current user profile"""
        print("\n👤 USER PROFILE TESTS")
        print("-" * 30)
        
        success, response = self.run_test(
            "Get Current User Profile",
            "GET",
            "api/auth/me",
            200
        )
        
        if success and response.get('email') == self.test_user_email:
            print(f"   👤 Profile: {response.get('full_name')} ({response.get('email')})")
            return True
        else:
            print("   ❌ User profile test failed")
            return False

    def test_orders(self):
        """Test order management"""
        print("\n📦 ORDER MANAGEMENT TESTS")
        print("-" * 30)
        
        # Create a new order
        order_data = {
            "branch": "construction",
            "service_type": "Vente de matériaux",
            "title": "Construction d'un entrepôt",
            "description": "Besoin de matériaux pour construire un entrepôt de 500m²",
            "priority": "high",
            "budget_range": "10000-50000"
        }
        
        success, response = self.run_test(
            "Create New Order",
            "POST",
            "api/orders",
            200,
            data=order_data
        )
        
        order_id = None
        if success and 'order_id' in response:
            order_id = response['order_id']
            print(f"   📦 Order created: {order_id}")
        else:
            print("   ❌ Order creation failed")
            return False
        
        # Get user orders
        success, response = self.run_test(
            "Get User Orders",
            "GET",
            "api/orders",
            200
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   📋 Found {len(response)} orders")
            return True
        else:
            print("   ❌ Get orders failed")
            return False
        
        # Get specific order
        if order_id:
            success, response = self.run_test(
                "Get Specific Order",
                "GET",
                f"api/orders/{order_id}",
                200
            )
            
            if success and response.get('id') == order_id:
                print(f"   📦 Order details: {response.get('title')}")
                return True
            else:
                print("   ❌ Get specific order failed")
                return False

    def test_messages(self):
        """Test support message system"""
        print("\n💬 SUPPORT MESSAGE TESTS")
        print("-" * 30)
        
        # Create a support message
        message_data = {
            "subject": "Question sur ma commande",
            "message": "J'aimerais avoir des informations sur l'état d'avancement de ma commande.",
            "priority": "normal"
        }
        
        success, response = self.run_test(
            "Create Support Ticket",
            "POST",
            "api/messages",
            200,
            data=message_data
        )
        
        if success and 'ticket_id' in response:
            ticket_id = response['ticket_id']
            print(f"   🎫 Ticket created: {ticket_id}")
        else:
            print("   ❌ Support ticket creation failed")
            return False
        
        # Get user messages
        success, response = self.run_test(
            "Get User Messages",
            "GET",
            "api/messages",
            200
        )
        
        if success and isinstance(response, list) and len(response) > 0:
            print(f"   📋 Found {len(response)} messages")
            return True
        else:
            print("   ❌ Get messages failed")
            return False

    def test_quotes(self):
        """Test quote request system"""
        print("\n💰 QUOTE REQUEST TESTS")
        print("-" * 30)
        
        quote_data = {
            "branch": "agriculture",
            "service_type": "Vente d'intrants agricoles",
            "description": "Besoin d'intrants pour une exploitation de 10 hectares",
            "contact_info": {
                "name": "Jean Kabila",
                "email": "jean.kabila@example.com",
                "phone": "+243987654321",
                "company": "Agri Congo SARL"
            },
            "timeline": "1month"
        }
        
        success, response = self.run_test(
            "Request Quote (Public)",
            "POST",
            "api/quotes",
            200,
            data=quote_data
        )
        
        if success and 'quote_id' in response:
            quote_id = response['quote_id']
            print(f"   💰 Quote requested: {quote_id}")
            return True
        else:
            print("   ❌ Quote request failed")
            return False

    def test_prospects(self):
        """Test prospect management"""
        print("\n🎯 PROSPECT MANAGEMENT TESTS")
        print("-" * 30)
        
        prospect_data = {
            "name": "Marie Tshisekedi",
            "email": "marie.tshisekedi@example.com",
            "phone": "+243456789123",
            "company": "Mode Congo",
            "interest": "Mode & Habillement",
            "message": "Intéressée par vos services de mode et habillement pour ma boutique."
        }
        
        success, response = self.run_test(
            "Create Prospect (Public)",
            "POST",
            "api/prospects",
            200,
            data=prospect_data
        )
        
        if success and 'message' in response:
            print(f"   🎯 Prospect created successfully")
            return True
        else:
            print("   ❌ Prospect creation failed")
            return False

    def test_authentication_security(self):
        """Test authentication security"""
        print("\n🔒 AUTHENTICATION SECURITY TESTS")
        print("-" * 30)
        
        # Test accessing protected endpoint without token
        old_token = self.token
        self.token = None
        
        success, response = self.run_test(
            "Access Protected Endpoint Without Token",
            "GET",
            "api/auth/me",
            401
        )
        
        if success:
            print("   🔒 Unauthorized access properly blocked")
        else:
            print("   ❌ Security test failed - unauthorized access allowed")
        
        # Test with invalid token
        self.token = "invalid_token_12345"
        
        success, response = self.run_test(
            "Access Protected Endpoint With Invalid Token",
            "GET",
            "api/auth/me",
            401
        )
        
        if success:
            print("   🔒 Invalid token properly rejected")
        else:
            print("   ❌ Security test failed - invalid token accepted")
        
        # Restore valid token
        self.token = old_token
        return True

    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 STARTING COMPREHENSIVE API TESTING")
        print("=" * 60)
        
        test_results = []
        
        # Core functionality tests
        test_results.append(self.test_health_check())
        test_results.append(self.test_branches())
        
        # Authentication tests
        test_results.append(self.test_user_registration())
        test_results.append(self.test_user_login())
        test_results.append(self.test_user_profile())
        
        # Business functionality tests
        test_results.append(self.test_orders())
        test_results.append(self.test_messages())
        test_results.append(self.test_quotes())
        test_results.append(self.test_prospects())
        
        # Security tests
        test_results.append(self.test_authentication_security())
        
        # Print final results
        print("\n" + "=" * 60)
        print("📊 FINAL TEST RESULTS")
        print("=" * 60)
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("🎉 ALL TESTS PASSED! Backend is fully functional.")
            return 0
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return 1

def main():
    """Main test execution"""
    tester = DoxaAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())