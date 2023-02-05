from fastapi import FastAPI

from schemas import ContributionInfo
from services.contribution_service import get_contribution


app = FastAPI()


@app.post("/getdata")
async def getdata(data: ContributionInfo):
    return get_contribution(data=data)
