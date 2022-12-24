from datetime import timedelta, datetime
from fastapi import FastAPI, Depends, Request, HTTPException
from . import models, schemas, crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union, List
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

# from tortoise import run_async
# from sql_app.models import init
# run_async(init())


app = FastAPI(
    title="api swagger",
    version="1.0",
    description="test fastapi"
)
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# exception_handler
class ResponseException(Exception):
    def __init__(self, content: str):
        self.content = content


@app.exception_handler(ResponseException)
def response_exception(request: Request, exc: ResponseException):
    return JSONResponse(
        status_code=200,
        content={
            "success": False,
            "detail": f"{exc.content}"
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """修改默认的请求验证错误模型"""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "detail": exc.errors()
        }
    )


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    创建token Depends
    :param data:带有用户标识的键值对，sub为JWT的规范
    :param expires_delta:过期时间
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/", response_model=schemas.BaseOut)
async def root():
    return {"message": "Hello World"}


@app.post("/create_test/",
          response_model=schemas.TestTo,
          tags=["test"],
          summary="create a test")
async def create_test(test: schemas.TestIn):
    """test"""
    result = crud.create_test(test)

    return result

# @app.post("/user/create/",
#           response_model=schemas.UserOut,
#           # response_model_exclude_unset=True,
#           tags=["User"],
#           summary="create user")
# def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
#     """create user"""
#     if crud.get_user(db=db, username=user.username):
#         raise ResponseException(content="username already exist!")
#     return schemas.UserOut(data=crud.create_user(db=db, user=user))
#
#
# @app.get("/user/verifypwd/{username}",
#          tags=["User"],
#          summary="verify password",
#          response_model=schemas.BaseOut)
# def verify_pw(password: str, username: str, db: Session = Depends(get_db)):
#     """verify password"""
#     result = crud.verify_pw(db=db, username=username, password=password)
#     return JSONResponse(
#         status_code=200,
#         content={
#             "success": True,
#             "result": result
#         }
#     )
#
#
# @app.patch("/user/update",
#            response_model=schemas.UserOut,
#            tags=["User"],
#            summary="update user")
# def update_user(user: schemas.UserIn, db: Session = Depends(get_db)):
#     """update user"""
#     if crud.get_user(db=db, username=user.username):
#         return schemas.UserOut(data=crud.update_user(db=db, user=user))
#     raise ResponseException(content="user is not exist!")
#
#
# @app.delete("/user/delete/{username}",
#             tags=["User"],
#             summary="delete user")
# def delete_user(username: str, db: Session = Depends(get_db)):
#     """delete user"""
#     if crud.get_user(db=db, username=username):
#         crud.delete_user(db=db, username=username)
#         return JSONResponse(
#             status_code=200,
#             content={
#                 "success": True,
#                 "detail": "delete user success!"
#             }
#         )
#     raise ResponseException(content="user is not exist!")
#
#
# @app.get("/users/me", tags=["oauth2"], response_model=schemas.TokenOut)
# async def read_users_me(current_user: schemas.UserTo = Depends(get_current_user)):
#     """get current user info"""
#     return schemas.TokenOut(data=current_user)
#
#
# @app.post("/login/",
#           tags=["oauth2"],
#           response_model=schemas.TokenOut)
# async def login(form_data: schemas.TokenIn, db: Session = Depends(get_db)):
#     """login"""
#     db_user = crud.get_user(db=db, username=form_data.username)
#     if not db_user:
#         raise ResponseException(content="user is not exist!")
#     if not crud.verify_pw(db=db, username=form_data.username, password=form_data.password):
#         raise ResponseException(content="Password Error!")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": db_user.username}, expires_delta=access_token_expires
#     )
#     db_user.access_token = access_token
#
#     return schemas.TokenOut(data=db_user.__dict__)
#
#
# @app.get('/user/users/',
#          response_model=schemas.UsersOut,
#          tags=['User'])
# def get_users(db: Session = Depends(get_db)):
#     return schemas.UsersOut(data=crud.get_users(db=db))
