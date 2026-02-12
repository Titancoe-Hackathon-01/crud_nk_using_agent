"""
In-memory database for employee management with thread-safe operations.
"""
from typing import List, Optional, Dict, Any
from threading import Lock
from employee import Employee


class EmployeeDatabase:
    """Thread-safe in-memory database for employees."""
    
    def __init__(self):
        """Initialize the database."""
        self._employees: Dict[int, Employee] = {}
        self._next_id: int = 1
        self._lock = Lock()
    
    def create(self, employee_data: Dict[str, Any]) -> Employee:
        """
        Create a new employee.
        
        Args:
            employee_data: Dictionary containing employee information
        
        Returns:
            Created Employee instance
        
        Raises:
            ValueError: If validation fails or email already exists
        """
        with self._lock:
            # Check for duplicate email
            email = employee_data.get('email', '').strip().lower()
            for emp in self._employees.values():
                if emp.email == email:
                    raise ValueError(f"Employee with email {email} already exists")
            
            # Create employee with auto-generated ID
            employee = Employee.from_dict(employee_data)
            employee.id = self._next_id
            self._employees[self._next_id] = employee
            self._next_id += 1
            
            return employee
    
    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """
        Get employee by ID.
        
        Args:
            employee_id: Employee ID
        
        Returns:
            Employee instance or None if not found
        """
        with self._lock:
            return self._employees.get(employee_id)
    
    def get_all(self) -> List[Employee]:
        """
        Get all employees.
        
        Returns:
            List of all Employee instances
        """
        with self._lock:
            return list(self._employees.values())
    
    def update(self, employee_id: int, update_data: Dict[str, Any]) -> Optional[Employee]:
        """
        Update an existing employee.
        
        Args:
            employee_id: Employee ID
            update_data: Dictionary containing fields to update
        
        Returns:
            Updated Employee instance or None if not found
        
        Raises:
            ValueError: If validation fails or email conflict exists
        """
        with self._lock:
            employee = self._employees.get(employee_id)
            if not employee:
                return None
            
            # Check for email conflicts if email is being updated
            if 'email' in update_data:
                new_email = update_data['email'].strip().lower()
                for emp_id, emp in self._employees.items():
                    if emp_id != employee_id and emp.email == new_email:
                        raise ValueError(f"Employee with email {new_email} already exists")
            
            # Update employee
            employee.update(update_data)
            return employee
    
    def delete(self, employee_id: int) -> bool:
        """
        Delete an employee.
        
        Args:
            employee_id: Employee ID
        
        Returns:
            True if deleted, False if not found
        """
        with self._lock:
            if employee_id in self._employees:
                del self._employees[employee_id]
                return True
            return False
    
    def search_by_department(self, department: str) -> List[Employee]:
        """
        Search employees by department.
        
        Args:
            department: Department name to filter by (case-insensitive)
        
        Returns:
            List of Employee instances matching the department
        """
        with self._lock:
            department_lower = department.strip().lower()
            return [
                emp for emp in self._employees.values()
                if emp.department.lower() == department_lower
            ]
    
    def clear(self) -> None:
        """Clear all employees (useful for testing)."""
        with self._lock:
            self._employees.clear()
            self._next_id = 1
