from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class HAIngressMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate Home Assistant Ingress authentication.
    Bypasses /health and /api/docs.
    Returns 401 if X-Remote-User-Name is missing.
    """
    async def dispatch(self, request: Request, call_next):
        # Paths that bypass authentication
        bypass_paths = ["/health", "/api/docs", "/api/openapi.json"]
        
        if request.url.path in bypass_paths or request.url.path.startswith("/static"):
            return await call_next(request)

        # Authenticate via Ingress headers
        user_name = request.headers.get("X-Remote-User-Name")
        
        if not user_name:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized: Home Assistant Ingress authentication required."}
            )

        # Store user info in request state
        request.state.user_id = request.headers.get("X-Remote-User-Id")
        request.state.user_name = user_name
        request.state.user_display_name = request.headers.get("X-Remote-User-Display-Name")
        
        return await call_next(request)
