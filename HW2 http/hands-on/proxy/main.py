import os
import httpx
import jwt
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

app = FastAPI()


JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-12345")
JWT_ALGORITHM = "HS256"

BACKEND_SERVICE_URL = os.getenv("BACKEND_SERVICE_URL", "http://legacy-app:8080")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def reverse_proxy(request: Request, path: str):

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Missing or malformed Authorization header. Expected 'Bearer <token>'"}
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Token has expired"}
        )
    except jwt.InvalidTokenError:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Invalid token"}
        )


    target_url = f"{BACKEND_SERVICE_URL}/{path}"
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"


    excluded_headers = ["host", "content-length"]
    forward_headers = {
        key: value for key, value in request.headers.items()
        if key.lower() not in excluded_headers
    }

    forward_headers["X-User-Id"] = str(payload.get("sub", "unknown"))

    body = await request.body()

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            backend_response = await client.request(
                method=request.method,
                url=target_url,
                headers=forward_headers,
                content=body
            )
        except httpx.RequestError as exc:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content={"error": f"Failed to connect to backend: {str(exc)}"}
            )


    response_headers = dict(backend_response.headers)
    response_headers.pop("content-encoding", None)
    response_headers.pop("content-length", None)

    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=response_headers,
        media_type=backend_response.headers.get("content-type")
    )