"""
from enum import Enum
from fastapi import FastAPI
import boto3

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
app = FastAPI()

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
"""

"""
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
"""

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import boto3

app = FastAPI()
templates = Jinja2Templates(directory="C:/Users/mithr/Desktop/")


@app.get('/')
def read_form():
    return 'Testing FastAPI'

@app.get("/create_machine")
def form_post(request: Request):
    result = "Enter AMI ID"
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/create_machine")
def form_post(request: Request, num: str = Form(...)):
    result = f"Creating EC2 instance with ami ID = {num}"
    ec2 = boto3.resource('ec2')
    # ami-0a23ccb2cdd9286bb
    instance_id = ec2.create_instances(
        ImageId=num,
        MinCount=1,
        MaxCount=2,
        InstanceType='t2.micro',
        KeyName='Laptopkey'
    )
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result, "instance_id": instance_id[0]})

@app.get("/machine_status")
def form_post(request: Request):
    result = "Enter Machine ID"
    return templates.TemplateResponse('form_new.html', context={'request': request, 'result': result})


@app.post("/machine_status")
def form_post(request: Request, num: str = Form(...)):
    client = boto3.client('ec2')
    result = client.describe_instances(InstanceIds=[num],)
    return templates.TemplateResponse('form_new.html', context={'request': request, 'result': result['Reservations'][0]['Instances'][0]['State']['Name']})