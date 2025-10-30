"""
Supabase Authentication Backend
Enhanced with error handling, logging, and token refresh
"""
import logging
from datetime import datetime
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from supabase import create_client, Client
from django.conf import settings

logger = logging.getLogger(__name__)
User = get_user_model()

class SupabaseAuthBackend(BaseBackend):
    """
    Custom authentication backend for Supabase with enhanced error handling
    """
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Client = None
        if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
            try:
                self.supabase = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_ANON_KEY
                )
                logger.info("Supabase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not configured")
    
    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticate user with Supabase
        
        Args:
            request: Django request object
            email: User email
            password: User password
            **kwargs: Additional authentication data
        
        Returns:
            User object if authenticated, None otherwise
        """
        if not self.supabase:
            logger.error("Cannot authenticate: Supabase client not initialized")
            return None
        
        if not email or not password:
            logger.warning("Authentication attempted without email or password")
            return None
        
        try:
            # Authenticate with Supabase
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Check email verification status
                email_verified = response.user.email_confirmed_at is not None
                
                # Try to get existing user by supabase_user_id first
                user = None
                try:
                    user = User.objects.get(supabase_user_id=response.user.id)
                    # Update user info if it already exists
                    user.supabase_email = response.user.email
                    user.email = response.user.email
                    user.is_active = True
                    user.email_verified = email_verified
                    user.last_login_at = datetime.now()
                    
                    # Sync user metadata from Supabase if available
                    if hasattr(response.user, 'user_metadata'):
                        metadata = response.user.user_metadata
                        if metadata:
                            user.first_name = metadata.get('first_name', user.first_name)
                            user.last_name = metadata.get('last_name', user.last_name)
                    
                    user.save()
                    logger.info(f"User updated successfully: {email}")
                except User.DoesNotExist:
                    # User doesn't exist yet, try to get by email
                    try:
                        existing_user = User.objects.get(email=response.user.email)
                        # Update existing user with Supabase ID
                        existing_user.supabase_user_id = response.user.id
                        existing_user.supabase_email = response.user.email
                        existing_user.is_active = True
                        existing_user.email_verified = email_verified
                        existing_user.last_login_at = datetime.now()
                        existing_user.save()
                        user = existing_user
                        logger.info(f"User linked with Supabase successfully: {email}")
                    except User.DoesNotExist:
                        # Create new user
                        try:
                            user = User.objects.create(
                                supabase_user_id=response.user.id,
                                email=response.user.email,
                                supabase_email=response.user.email,
                                username=response.user.email,
                                is_active=True,
                                email_verified=email_verified,
                                last_login_at=datetime.now(),
                            )
                            logger.info(f"New user created successfully: {email}")
                        except IntegrityError as e:
                            logger.error(f"Integrity error creating user for {email}: {e}")
                            # Try to get user by email as fallback
                            try:
                                user = User.objects.get(email=response.user.email)
                                logger.info(f"Retrieved existing user by email: {email}")
                            except User.DoesNotExist:
                                logger.error(f"Failed to create or retrieve user for {email}")
                                return None
                
                # Store access token and session data in Django session
                if user and hasattr(response, 'session') and response.session:
                    request.session['supabase_access_token'] = response.session.access_token
                    request.session['supabase_refresh_token'] = response.session.refresh_token
                    request.session['supabase_user_id'] = response.user.id
                    request.session['supabase_email'] = response.user.email
                    
                    # Store token expiry timestamp using provider TTL when available
                    from time import time
                    expires_in = getattr(response.session, 'expires_in', None)
                    if isinstance(expires_in, (int, float)) and expires_in > 0:
                        # Refresh a bit early (buffer 60s)
                        request.session['supabase_token_expires_at'] = time() + max(0, expires_in - 60)
                    else:
                        request.session['supabase_token_expires_at'] = time() + 3600  # Fallback 1 hour
                
                if user:
                    logger.info(f"User authenticated successfully: {email}")
                    return user
                else:
                    logger.error(f"User object is None for {email}")
                    return None
            else:
                logger.warning(f"Authentication failed: No user in response")
                return None
            
        except Exception as e:
            logger.error(f"Authentication error for {email}: {str(e)}")
            return None
    
    def get_user(self, user_id):
        """
        Retrieve user by ID
        
        Args:
            user_id: User ID
        
        Returns:
            User object or None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            logger.warning(f"User not found: {user_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {e}")
            return None

