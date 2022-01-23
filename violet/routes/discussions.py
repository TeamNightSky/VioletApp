from violet.app import app
from violet.models import Discussion


@app.get("/discussions/{snowflake}")
async def discussion(snowflake: int):
    pass


@app.put("/discussions/{snowflake}")
async def discussion(snowflake: int, discussion: Discussion):
    pass


@app.post("/discussions/{snowflake}")
async def discussion(snowflake: int, discussion: Discussion):
    pass


@app.delete("/discussions/{snowflake}")
async def discussion(snowflake: int):
    pass

