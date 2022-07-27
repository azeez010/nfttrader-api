"""Validator Module"""
import re
from . import env

def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False

def validate_password(password: str):
    """Password Validator"""
    reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)

def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)

def validate_user(**args):
    """User Validator"""

    if  not args.get('email') or not args.get('password') or not args.get('name'):
        return {
            'email': 'Email is required',
            'password': 'Password is required',
            'name': 'Name is required'
        }
    
    if not isinstance(args.get('name'), str) or \
        not isinstance(args.get('email'), str) or not isinstance(args.get('password'), str):
        return {
            'email': 'Email must be a string',
            'password': 'Password must be a string',
            'name': 'Name must be a string'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    if len(args.get('password')) < 6:
        return {
            'password': 'Password is invalid, Should be atleast 6 characters' 
        }

    if args.get('secret'):
        if not validate_secret(args.get('secret')):
            return {
                'secret': 'Secret is invalid, The page is for the site author'
            }
    return True

def validate_secret(secret):
    secret_key = env.str("SECRET_KEY", default="123456asdfghjkl;.,mnbvcxz")
    if secret == secret_key:
        return True
    return False

def validate_email_and_password(email, password):
    """Email and Password Validator"""
    if not (email and password):
        return {
            'email': 'Email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True

def validate_email_and_password(email, password):
    """email and Password Validator"""
    if not (email and password):
        return {
            'email': 'email is required',
            'password': 'Password is required'
        }
    if not validate_email(email):
        return {
            'email': 'Email is invalid, Should be a valid email, ending with *@****.com'
        }

    if len(password) < 6:
        return {
            'password': 'Password is invalid, Should be atleast 6 characters' 
        }
    
    return True

def validate_nft(**args):
    """NFT Validator"""
    if not args.get('name') or not args.get('address') or not args.get('image') or not args.get('owner'):
        return {
            'name': 'Name is required',
            'address': 'address is required',
            'image': 'Image is required'
        }
    if not isinstance(args.get('name'), str) or \
        not isinstance(args.get('address'), str) or not isinstance(args.get('image'), str):
        return {
            'name': 'Name must be a string',
            'address': 'address must be a string',
            'image': 'Image must be a string'
        }
    if not args.get('owner').isnumeric():
        return {
            'owner': 'owner is not an int'
        }
    return True

trade_validation_schema = {
  "type": "object",
  "properties": {
    "unique_string": { "type": "string" },
    "status": { "type": "boolean" },
    "owner": { "type": "integer" }
  },
  "required": ["unique_string"]
}