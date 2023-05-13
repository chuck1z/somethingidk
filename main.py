import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema
from app.model import PostSchema, UserSchema, UserLoginSchema, getComponent
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

import mysql.connector


posts = [
    {
        "id": 1,
        "title": "rent-a-gf",
        "text":"stupid *ss anime only psychopath watch this"

    },
    {
        "id": 2,
        "title": "kimi-no-nawa",
        "text": "overrated but ok"

    },
    {
        "id": 3,
        "title":"demon-slayer",
        "text":"overrated af and also it's the equivalent of fortnite in anime industry (only 5 yolds love it)"

    }


]

mydb = mysql.connector.connect(
    host="34.69.199.102",
    user="root",
    password="J]91kx6G&S:^]'Gu",
    database="components"
)



users = []

app = FastAPI()

def check_user(data: UserLoginSchema):
    mycursor = mydb.cursor()

    email = data.email
    password = data.password
    res = (email,)

    mycursor.execute("SELECT * FROM users WHERE email= %s", res)
    myresult = mycursor.fetchall()

    if (len(myresult) == 1):
        res_pass = myresult[0][3]
        if (password == res_pass):
            return True
    return False

def getCreden(data: UserLoginSchema):
    if check_user(data):
        mycursor = mydb.cursor()
        email = data.email
        res = (email,)
        mycursor.execute("SELECT * FROM users WHERE email= %s", res)
        myresult = mycursor.fetchall()
        resId = myresult[0][0]
        resName = myresult[0][1]
        return{
            "id":resId,
            "Username":resName
        }
    else:
        return{"error"}
 




def pushUser(data: UserSchema):
    mycursor = mydb.cursor()

    name = data.fullname
    email = data.email
    password = data.password
    resq = (email,)

    mycursor.execute("SELECT * FROM users WHERE email= %s", resq)

    myresult = mycursor.fetchall()

    isTaken = "undefined"
    if (len(myresult) == 1):
        isTaken = True
    else:
        isTaken = False 

    if (isTaken):
        return False
    else:
        query = "insert into users (name, email, password) values (%s, %s, %s);" 
        res = (name,email,password)
        mycursor.execute(query, res)
        mydb.commit()
        return True


def getbyId(name):
    mycursor = mydb.cursor()

    # mycursor.execute("SELECT * FROM3 comps")
    res=(name,)
    mycursor.execute("SELECT * FROM comps WHERE name= %s", res)

    myresult = mycursor.fetchall()
    id=myresult[0][0]
    name=myresult[0][1]
    desc=myresult[0][2]
    example=myresult[0][3]
    
    myresult={
        "id":id,
        "name":name,
        "desc":desc,
        "example":example
    }

    return myresult


def getArticlebyId(compid):
    mycursor = mydb.cursor()
    
    res=(compid,)
    mycursor.execute("SELECT * FROM articles WHERE componentId= %s", res)
    myresult = mycursor.fetchall()
    id=myresult[0][0]
    name=myresult[0][1]
    desc=myresult[0][2]
    imgurl=myresult[0][3]
    compid=myresult[0][4]

    humu={
        "id":id,
        "name":name,
        "desc":desc,
        "imgurl":imgurl,
        "compid":compid,
    }

    return humu


# Get test
@app.get("/", tags=["test"])
def greet():
    return{"Hello":"World!"}


# Get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return{"data": posts}

# get single post by id
@app.get("/post/{id}", tags=["posts"])
def get_one_post(id:int):
    if id > len(posts):
        return{
            "error":"erm, there is no post..."
        }
    for post in posts:
        if post["id"]==id:
            return {
                "data":post
            }
        



@app.get("/component{id}", dependencies=[Depends(jwtBearer())], tags=["components"])
def comps(name: str):
    result = getbyId(name)
    return {
        "componentList":result
    }



@app.get("/article{id}", dependencies=[Depends(jwtBearer())], tags=["articles"])
def comps(compid: str):
    result = getArticlebyId(compid)
    return {
        "articleList":result
    }




# Post new post
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts)+1
    posts.append(post.dict())
    return{
        "info":"degenericity added"
    }

# User thingy I forgor basically
#@app.post("/user/signup", tags=["user"])
#def user_signup(user : UserSchema = Body(...)):
#    users.append(user)
#    return signJWT(user.email)



@app.post("/user/signup", tags=["user"])
def user_signup(user : UserSchema = Body(...)):
    users.append(user)

    if pushUser(user):
        return {
            "error":"false",
            "message":"User Created",
            "signupToken":signJWT(user.email)
            }
    else:
        return{
            "error":"true",
            "message":"Email already taken 🗿"
        }





@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return {
            "error":"false",
            "message":"login success",
            "loginResult":{
            "userId":getCreden(user),
            "token":signJWT(user.email)}}
    else:
        return{
            "error":"Invalid login details! 🗿"
        }
    




