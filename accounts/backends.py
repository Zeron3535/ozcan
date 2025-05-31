from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

# Create a logger
logger = logging.getLogger(__name__)

class CaseInsensitiveModelBackend(ModelBackend):
    """Authentication backend which allows case-insensitive username authentication."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            
        logger.info(f"Attempting authentication for username: {username}")
        
        try:
            # Perform a case-insensitive lookup for the username.
            query = {f"{UserModel.USERNAME_FIELD}__iexact": username}
            logger.info(f"Query: {query}")
            user = UserModel.objects.get(**query)
            logger.info(f"User found: {user.username}, is_active: {user.is_active}")
        except UserModel.DoesNotExist:
            logger.warning(f"User with username '{username}' not found")
            return None
        else:
            # Ensure password is not None
            if password is None:
                logger.warning("Password is None")
                return None
                
            # Check password and user_can_authenticate
            if user.check_password(password):
                logger.info("Password check passed")
                if self.user_can_authenticate(user):
                    logger.info("User can authenticate, returning user")
                    return user
                else:
                    logger.warning("User can't authenticate (likely inactive)")
            else:
                logger.warning("Password check failed")
                
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None 