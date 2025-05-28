from django.shortcuts import redirect

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs that don't require authentication
        non_auth_urls = ['/', '/logout/', '/admin/']
        
        # Allow POST requests to the login page
        if request.path_info == '/' and request.method == 'POST':
            return self.get_response(request)
            
        # Check if user is authenticated
        if not request.path_info in non_auth_urls and 'user_id' not in request.session:
            # Add cache control headers to prevent browser caching
            response = redirect('index')
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
            
        response = self.get_response(request)
        # Also add cache headers to regular responses
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response