from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from exceptions import ValidationException
from schemas import ContributionInfo
from services.contribution_service import get_contribution


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def invalid_json_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": f"Invalid JSON data"},
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.error},
    )


@app.exception_handler(Exception)
async def server_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Server error"},
    )


@app.post("/getdata")
async def getdata(data: ContributionInfo):
    return get_contribution(data=data)
