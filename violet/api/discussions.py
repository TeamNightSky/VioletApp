from violet.api.app import api
from violet.models import Discussion


@api.get("/discussions/{snowflake}")
async def get_discussion(snowflake: int):
    pass


@api.put("/discussions/{snowflake}")
async def put_discussion(snowflake: int, discussion: Discussion):
    pass


@api.post("/discussions/{snowflake}")
async def post_discussion(snowflake: int, discussion: Discussion):
    pass


@api.delete("/discussions/{snowflake}")
async def delete_discussion(snowflake: int):
    pass

