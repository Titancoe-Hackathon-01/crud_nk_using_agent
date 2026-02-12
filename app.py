"""
Employee Management System - RESTful API
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from database import EmployeeDatabase
from employee import Employee
from typing import Tuple, Dict, Any


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize database
db = EmployeeDatabase()


def success_response(data: Any, status_code: int = 200) -> Tuple[Dict, int]:
    """Create a success response."""
    return jsonify({
        'success': True,
        'data': data
    }), status_code


def error_response(message: str, status_code: int = 400) -> Tuple[Dict, int]:
    """Create an error response."""
    return jsonify({
        'success': False,
        'error': message
    }), status_code


@app.route('/api/employees', methods=['POST'])
def create_employee():
    """
    Create a new employee.
    
    Request Body:
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "department": "Engineering",
            "role": "Software Engineer",
            "hire_date": "2024-01-15"
        }
    
    Returns:
        201: Employee created successfully
        400: Validation error or duplicate email
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("Request body is required", 400)
        
        employee = db.create(data)
        return success_response(employee.to_dict(), 201)
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/api/employees', methods=['GET'])
def get_all_employees():
    """
    Get all employees.
    
    Returns:
        200: List of all employees
    """
    try:
        employees = db.get_all()
        return success_response([emp.to_dict() for emp in employees], 200)
    
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id: int):
    """
    Get a specific employee by ID.
    
    Args:
        employee_id: Employee ID
    
    Returns:
        200: Employee data
        404: Employee not found
    """
    try:
        employee = db.get_by_id(employee_id)
        if not employee:
            return error_response(f"Employee with ID {employee_id} not found", 404)
        
        return success_response(employee.to_dict(), 200)
    
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id: int):
    """
    Update an existing employee.
    
    Args:
        employee_id: Employee ID
    
    Request Body (all fields optional):
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "department": "Engineering",
            "role": "Senior Software Engineer",
            "hire_date": "2024-01-15"
        }
    
    Returns:
        200: Employee updated successfully
        400: Validation error
        404: Employee not found
    """
    try:
        data = request.get_json()
        if not data:
            return error_response("Request body is required", 400)
        
        # Don't allow ID to be updated
        if 'id' in data:
            return error_response("Employee ID cannot be updated", 400)
        
        employee = db.update(employee_id, data)
        if not employee:
            return error_response(f"Employee with ID {employee_id} not found", 404)
        
        return success_response(employee.to_dict(), 200)
    
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id: int):
    """
    Delete an employee.
    
    Args:
        employee_id: Employee ID
    
    Returns:
        200: Employee deleted successfully
        404: Employee not found
    """
    try:
        deleted = db.delete(employee_id)
        if not deleted:
            return error_response(f"Employee with ID {employee_id} not found", 404)
        
        return success_response({'message': f'Employee {employee_id} deleted successfully'}, 200)
    
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/api/employees/search', methods=['GET'])
def search_employees():
    """
    Search and filter employees by department.
    
    Query Parameters:
        department: Department name to filter by (case-insensitive)
    
    Returns:
        200: List of employees matching the department
        400: Missing department parameter
    """
    try:
        department = request.args.get('department')
        if not department:
            return error_response("Department parameter is required", 400)
        
        employees = db.search_by_department(department)
        return success_response([emp.to_dict() for emp in employees], 200)
    
    except Exception as e:
        return error_response(f"Internal server error: {str(e)}", 500)


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        200: Service is healthy
    """
    return success_response({'status': 'healthy'}, 200)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return error_response("Resource not found", 404)


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return error_response("Method not allowed", 405)


if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
