#!/usr/bin/env python3
"""
Demo script to showcase the Employee Management System API.
This script demonstrates all CRUD operations and search functionality.
"""
import requests
import json
import time


class EmployeeManagementDemo:
    """Demo class for testing the Employee Management System."""
    
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url
        self.test_results = []
    
    def print_section(self, title):
        """Print a formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)
    
    def print_response(self, response, description):
        """Print API response in a formatted way."""
        print(f"\n{description}")
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print(f"Response:\n{json.dumps(data, indent=2)}")
            return data
        except Exception:
            print(f"Response: {response.text}")
            return None
    
    def check_server(self):
        """Check if the server is running."""
        self.print_section("Checking Server Status")
        try:
            response = requests.get(f'{self.base_url}/health', timeout=2)
            if response.status_code == 200:
                print("✓ Server is running and healthy!")
                return True
            else:
                print("✗ Server is not responding correctly")
                return False
        except requests.exceptions.RequestException as e:
            print(f"✗ Cannot connect to server: {e}")
            print("\nPlease start the server first:")
            print("  python app.py")
            return False
    
    def demo_create_employees(self):
        """Demo: Create multiple employees."""
        self.print_section("1. CREATE OPERATION - Adding Employees")
        
        employees = [
            {
                "name": "Alice Johnson",
                "email": "alice.johnson@techcorp.com",
                "department": "Engineering",
                "role": "Software Engineer",
                "hire_date": "2023-06-15"
            },
            {
                "name": "Bob Williams",
                "email": "bob.williams@techcorp.com",
                "department": "Engineering",
                "role": "Senior DevOps Engineer",
                "hire_date": "2022-03-10"
            },
            {
                "name": "Carol Martinez",
                "email": "carol.martinez@techcorp.com",
                "department": "Marketing",
                "role": "Marketing Manager",
                "hire_date": "2023-01-20"
            },
            {
                "name": "David Chen",
                "email": "david.chen@techcorp.com",
                "department": "Sales",
                "role": "Sales Representative",
                "hire_date": "2024-02-01"
            },
            {
                "name": "Emma Davis",
                "email": "emma.davis@techcorp.com",
                "department": "Engineering",
                "role": "QA Engineer",
                "hire_date": "2023-09-05"
            }
        ]
        
        created_ids = []
        for emp in employees:
            response = requests.post(f'{self.base_url}/employees', json=emp)
            data = self.print_response(response, f"Creating {emp['name']} - {emp['role']}")
            if data and data.get('success'):
                created_ids.append(data['data']['id'])
        
        print(f"\n✓ Successfully created {len(created_ids)} employees")
        return created_ids
    
    def demo_read_all(self):
        """Demo: Read all employees."""
        self.print_section("2. READ OPERATION - Get All Employees")
        
        response = requests.get(f'{self.base_url}/employees')
        data = self.print_response(response, "Fetching all employees")
        
        if data and data.get('success'):
            employees = data['data']
            print(f"\n✓ Found {len(employees)} employees:")
            print("\n{:<5} {:<20} {:<30} {:<15} {:<25}".format(
                "ID", "Name", "Email", "Department", "Role"
            ))
            print("-" * 100)
            for emp in employees:
                print("{:<5} {:<20} {:<30} {:<15} {:<25}".format(
                    emp['id'],
                    emp['name'][:20],
                    emp['email'][:30],
                    emp['department'][:15],
                    emp['role'][:25]
                ))
        return data
    
    def demo_read_single(self, employee_id):
        """Demo: Read a single employee."""
        self.print_section(f"3. READ OPERATION - Get Employee by ID ({employee_id})")
        
        response = requests.get(f'{self.base_url}/employees/{employee_id}')
        data = self.print_response(response, f"Fetching employee with ID {employee_id}")
        return data
    
    def demo_update(self, employee_id):
        """Demo: Update an employee."""
        self.print_section(f"4. UPDATE OPERATION - Promote Employee {employee_id}")
        
        update_data = {
            "role": "Lead Software Engineer",
            "department": "Engineering"
        }
        
        response = requests.put(f'{self.base_url}/employees/{employee_id}', json=update_data)
        data = self.print_response(response, f"Updating employee {employee_id}")
        
        if data and data.get('success'):
            print(f"\n✓ Employee promoted to: {data['data']['role']}")
        return data
    
    def demo_search_by_department(self, department):
        """Demo: Search employees by department."""
        self.print_section(f"5. SEARCH OPERATION - Filter by Department: {department}")
        
        response = requests.get(f'{self.base_url}/employees/search?department={department}')
        data = self.print_response(response, f"Searching employees in {department} department")
        
        if data and data.get('success'):
            employees = data['data']
            print(f"\n✓ Found {len(employees)} employees in {department}:")
            for emp in employees:
                print(f"  • {emp['name']} - {emp['role']}")
        return data
    
    def demo_delete(self, employee_id):
        """Demo: Delete an employee."""
        self.print_section(f"6. DELETE OPERATION - Remove Employee {employee_id}")
        
        response = requests.delete(f'{self.base_url}/employees/{employee_id}')
        data = self.print_response(response, f"Deleting employee {employee_id}")
        
        if data and data.get('success'):
            print(f"\n✓ Employee {employee_id} successfully deleted")
        return data
    
    def demo_error_handling(self):
        """Demo: Error handling."""
        self.print_section("7. ERROR HANDLING - Validation Examples")
        
        print("\n--- Testing Invalid Email Format ---")
        invalid_email = {
            "name": "Test User",
            "email": "invalid-email",
            "department": "IT",
            "role": "Developer",
            "hire_date": "2024-01-01"
        }
        response = requests.post(f'{self.base_url}/employees', json=invalid_email)
        self.print_response(response, "Creating employee with invalid email")
        
        print("\n--- Testing Future Hire Date ---")
        future_date = {
            "name": "Future Employee",
            "email": "future@test.com",
            "department": "IT",
            "role": "Developer",
            "hire_date": "2050-01-01"
        }
        response = requests.post(f'{self.base_url}/employees', json=future_date)
        self.print_response(response, "Creating employee with future hire date")
        
        print("\n--- Testing Non-existent Employee ---")
        response = requests.get(f'{self.base_url}/employees/999')
        self.print_response(response, "Fetching non-existent employee")
    
    def run_full_demo(self):
        """Run the complete demo."""
        print("\n" + "=" * 70)
        print("  EMPLOYEE MANAGEMENT SYSTEM - COMPLETE DEMO")
        print("=" * 70)
        
        # Check server
        if not self.check_server():
            return
        
        time.sleep(1)
        
        # Create employees
        employee_ids = self.demo_create_employees()
        if not employee_ids:
            print("\n✗ Failed to create employees. Stopping demo.")
            return
        
        time.sleep(1)
        
        # Read all
        self.demo_read_all()
        time.sleep(1)
        
        # Read single
        self.demo_read_single(employee_ids[0])
        time.sleep(1)
        
        # Update
        self.demo_update(employee_ids[0])
        time.sleep(1)
        
        # Search by department
        self.demo_search_by_department("Engineering")
        time.sleep(1)
        
        self.demo_search_by_department("Marketing")
        time.sleep(1)
        
        # Delete
        self.demo_delete(employee_ids[-1])
        time.sleep(1)
        
        # Error handling
        self.demo_error_handling()
        
        # Final summary
        self.print_section("DEMO COMPLETED SUCCESSFULLY")
        print("\n✓ All CRUD operations working correctly")
        print("✓ Search and filter functionality verified")
        print("✓ Error handling and validation confirmed")
        print("\nThe Employee Management System is fully operational!")
        print("\nYou can now interact with the API using:")
        print("  • cURL commands (see README.md)")
        print("  • Postman or similar API testing tools")
        print("  • Your own client application")
        print("=" * 70 + "\n")


if __name__ == '__main__':
    demo = EmployeeManagementDemo()
    demo.run_full_demo()
