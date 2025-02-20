from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from pydantic import ValidationError

from routes.guest_route import router as guest_router
from routes.confirmation_route import router as confirmation_router
from routes.picture_route import router as picture_router
from routes.gift_route import router as gift_router
from routes.category_route import router as category_router

from middlewares.logging_middleware import LoggingMiddleware

app = FastAPI(
    docs_url="/api/documentation",
    redoc_url="/api/documentation/remastered",
    openapi_url="/api/documentation/openapi.json",
    title="API Documentation for Wedding"
)

router = APIRouter(responses={404: {"description": "Not found"}})

origins = ["http://localhost", "http://localhost:8000", "http://localhost:3000", "*"]

# Adicionando middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

# app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(guest_router, prefix="/api", tags=["Guests"])
app.include_router(confirmation_router, prefix="/api", tags=["Confirmation"])
app.include_router(gift_router, prefix="/api", tags=["Gifts"])
app.include_router(category_router, prefix="/api", tags=["Categories"])
app.include_router(picture_router, prefix="/api", tags=["Pictures"])


# Handler para erros de validação do Pydantic/FastAPI
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    errors = exc.errors()
    formatted_errors = []

    for error in errors:
        field = ".".join(error["loc"])
        msg = error.get("ctx", {}).get("error", None)
        if msg is None:
            msg = error.get("msg", "Erro desconhecido")

        formatted_errors.append({
            "field": field,
            "message": str(msg)
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": formatted_errors}
    )
