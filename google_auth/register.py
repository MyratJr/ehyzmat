from users.models import User
import os
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
import random
from string import ascii_lowercase


def generate_username(user_id):
    alphabet = ascii_lowercase
    random_letters = random.sample(alphabet, 5)
    return ''.join(random_letters)+str(user_id)


def register_social_user(provider, user_id, email):
    filtered_user_by_email = User.objects.get(email=email)

    if filtered_user_by_email:
        if provider == filtered_user_by_email.registration_method:
            authenticate(email=email, password=os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET'))
            return {
                "username": filtered_user_by_email.username,
                "email": filtered_user_by_email.email, 
                "tokens": filtered_user_by_email.tokens()    
            }
        else:
            raise AuthenticationFailed(
                detail="Please continue your login using" + filtered_user_by_email.registration_method
            )
        
    else:
        user = {
            'username': generate_username(user_id), 'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.registration_method = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }