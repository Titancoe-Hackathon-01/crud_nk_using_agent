"""
Employee model with validation.
"""
from datetime import datetime
from typing import Optional, Dict, Any
import re


class Employee:
    """Employee model with validation."""
    
    def __init__(
        self,
        name: str,
        email: str,
        department: str,
        role: str,
        hire_date: str,
        employee_id: Optional[int] = None
    ):
        """
        Initialize an Employee instance.
        
        Args:
            name: Employee's full name
            email: Employee's email address
            department: Department name
            role: Job role/title
            hire_date: Hire date in YYYY-MM-DD format
            employee_id: Unique identifier (auto-generated if not provided)
        
        Raises:
            ValueError: If any field validation fails
        """
        self.id = employee_id
        self.name = self._validate_name(name)
        self.email = self._validate_email(email)
        self.department = self._validate_department(department)
        self.role = self._validate_role(role)
        self.hire_date = self._validate_hire_date(hire_date)
    
    @staticmethod
    def _validate_name(name: str) -> str:
        """Validate employee name."""
        if not name or not isinstance(name, str):
            raise ValueError("Name is required and must be a string")
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if len(name) > 100:
            raise ValueError("Name must be less than 100 characters")
        return name
    
    @staticmethod
    def _validate_email(email: str) -> str:
        """Validate email format."""
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        email = email.strip().lower()
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        return email
    
    @staticmethod
    def _validate_department(department: str) -> str:
        """Validate department name."""
        if not department or not isinstance(department, str):
            raise ValueError("Department is required and must be a string")
        department = department.strip()
        if len(department) < 2:
            raise ValueError("Department must be at least 2 characters long")
        if len(department) > 50:
            raise ValueError("Department must be less than 50 characters")
        return department
    
    @staticmethod
    def _validate_role(role: str) -> str:
        """Validate role/title."""
        if not role or not isinstance(role, str):
            raise ValueError("Role is required and must be a string")
        role = role.strip()
        if len(role) < 2:
            raise ValueError("Role must be at least 2 characters long")
        if len(role) > 50:
            raise ValueError("Role must be less than 50 characters")
        return role
    
    @staticmethod
    def _validate_hire_date(hire_date: str) -> str:
        """Validate hire date format (YYYY-MM-DD)."""
        if not hire_date or not isinstance(hire_date, str):
            raise ValueError("Hire date is required and must be a string")
        
        try:
            # Parse and validate date
            parsed_date = datetime.strptime(hire_date.strip(), '%Y-%m-%d')
            
            # Check if date is not in the future
            if parsed_date > datetime.now():
                raise ValueError("Hire date cannot be in the future")
            
            # Check if date is reasonable (not before 1900)
            if parsed_date.year < 1900:
                raise ValueError("Hire date must be after 1900")
            
            return hire_date.strip()
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Hire date must be in YYYY-MM-DD format")
            raise
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert employee to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'role': self.role,
            'hire_date': self.hire_date
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Employee':
        """Create Employee instance from dictionary."""
        return cls(
            name=data.get('name'),
            email=data.get('email'),
            department=data.get('department'),
            role=data.get('role'),
            hire_date=data.get('hire_date'),
            employee_id=data.get('id')
        )
    
    def update(self, data: Dict[str, Any]) -> None:
        """Update employee fields from dictionary."""
        if 'name' in data:
            self.name = self._validate_name(data['name'])
        if 'email' in data:
            self.email = self._validate_email(data['email'])
        if 'department' in data:
            self.department = self._validate_department(data['department'])
        if 'role' in data:
            self.role = self._validate_role(data['role'])
        if 'hire_date' in data:
            self.hire_date = self._validate_hire_date(data['hire_date'])
