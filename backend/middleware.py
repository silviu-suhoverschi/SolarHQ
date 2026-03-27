from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class HAIngressMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract user info from Home Assistant Ingress headers.
    HA Ingress provides:
    - X-Ingress-Path
    - X-HASSIO-KEY
    - X-Remote-User-Id
    - X-Remote-User-Name
    - X-Remote-User-Display-Name
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        # Store user info in request state for later use
        request.state.user_id = request.headers.get("X-Remote-User-Id")
        request.state.user_name = request.headers.get("X-Remote-User-Name")
        request.state.user_display_name = request.headers.get("X-Remote-User-Display-Name")
        
        # Ingress path can be used for URL prefixing if needed
        # INGRESS_PATH is already exported in environmental variables by solarhq-api script
        
        response = await call_next(request)
        return response
