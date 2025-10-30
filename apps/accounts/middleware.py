"""
Supabase Authentication Middleware
Enhanced with token refresh and validation logic
"""
import logging
import time
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import resolve
from supabase import create_client
from django.conf import settings

logger = logging.getLogger(__name__)

class SupabaseAuthMiddleware(MiddlewareMixin):
    """
    Middleware to handle Supabase authentication, session management, and token refresh
    """
    
    def __init__(self, get_response):
        """Initialize middleware with Supabase client"""
        super().__init__(get_response)
        self.supabase = None
        if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
            try:
                self.supabase = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_ANON_KEY
                )
                logger.info("Supabase client initialized in middleware")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client in middleware: {e}")
    
    def process_request(self, request):
        """Process each request to check authentication and refresh tokens"""
        # Skip for non-authenticated endpoints
        if self._should_skip_middleware(request):
            return None
        
        # Check if user is authenticated via Supabase
        if request.user.is_authenticated and hasattr(request.user, 'supabase_user_id'):
            # Check and refresh token if needed
            self._refresh_token_if_needed(request)
            
            # Check session timeout
            if 'last_activity' in request.session:
                elapsed = time.time() - request.session['last_activity']
                if elapsed > 3600:  # 1 hour timeout
                    logger.info(f"Session timed out for user {request.user.email}")
                    logout(request)
                    if not self._is_login_page(request):
                        return redirect('accounts:login')
            else:
                request.session['last_activity'] = time.time()
        
        return None
    
    def process_response(self, request, response):
        """Process each response to update last activity"""
        if request.user.is_authenticated:
            request.session['last_activity'] = time.time()
        return response
    
    def _refresh_token_if_needed(self, request):
        """Refresh Supabase access token if it's about to expire"""
        try:
            access_token = request.session.get('supabase_access_token')
            refresh_token = request.session.get('supabase_refresh_token')
            
            if not access_token or not refresh_token:
                logger.warning("No Supabase tokens in session")
                return
            
            # Check if token is about to expire (within 5 minutes)
            token_expires_at = request.session.get('supabase_token_expires_at', 0)
            time_until_expiry = token_expires_at - time.time()
            
            if time_until_expiry < 300:  # Less than 5 minutes
                logger.info("Refreshing Supabase access token")
                
                if self.supabase:
                    # Refresh the token
                    try:
                        # Ensure auth client has the current session set
                        self.supabase.auth.set_session(access_token, refresh_token)
                        response = self.supabase.auth.refresh_session()
                        
                        if response and hasattr(response, 'session') and response.session:
                            # Update tokens in session
                            request.session['supabase_access_token'] = response.session.access_token
                            request.session['supabase_refresh_token'] = response.session.refresh_token
                            
                            # Recompute expiry from provider if available
                            expires_in = getattr(response.session, 'expires_in', None)
                            if isinstance(expires_in, (int, float)) and expires_in > 0:
                                request.session['supabase_token_expires_at'] = time.time() + max(0, expires_in - 60)
                            else:
                                request.session['supabase_token_expires_at'] = time.time() + 3600
                            
                            logger.info("Supabase token refreshed successfully")
                        else:
                            logger.warning("Failed to refresh token: Invalid response")
                            
                    except Exception as e:
                        logger.error(f"Error refreshing token: {e}")
                        # Token refresh failed, logout user
                        logout(request)
                        
        except Exception as e:
            logger.error(f"Error in token refresh middleware: {e}")
    
    def _should_skip_middleware(self, request):
        """Check if middleware should be skipped"""
        # Skip for static files, admin, login, and signup
        path = request.path
        skip_paths = ['/static/', '/media/', '/admin/', '/accounts/login/', '/accounts/signup/', '/accounts/password-reset/']
        return any(path.startswith(skip) for skip in skip_paths)
    
    def _is_login_page(self, request):
        """Check if current page is login page"""
        try:
            resolver = resolve(request.path)
            return resolver.url_name == 'login'
        except:
            return False

