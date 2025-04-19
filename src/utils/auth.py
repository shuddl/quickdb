'''
Authentication utilities for QuickDB
'''

def is_admin(user):
    """
    Check if a user has admin role
    
    Args:
        user: The user object to check
        
    Returns:
        bool: True if the user has admin role, False otherwise
    """
    return user.role == 'Admin'
