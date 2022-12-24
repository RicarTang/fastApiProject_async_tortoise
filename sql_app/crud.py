from sql_app import models, schemas


async def create_test(test: schemas.TestIn):
    user = await models.Test.create(**test.dict())
    return user
