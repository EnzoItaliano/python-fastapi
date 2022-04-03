from dotenv import load_dotenv
load_dotenv()

import os
url = os.environ.get('DATABASE_URL')

from model import Todo

import asyncio
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(url)
client.get_io_loop = asyncio.get_running_loop
database = client.TodoList
collection = database.todo

async def fetch_one_todo(title):
    document = await collection.find_one({'title': title})
    return document

async def fetch_all_todos():
    todos = []
    cursor = collection.find()
    async for document in cursor:
        todos.append(Todo(**document))
    return todos

async def create_todo(todo):
    document = todo
    try:
        await collection.insert_one(document)
        document['_id'] = str(document['_id'])
        return document
    except NameError:
        return NameError

async def update_todo(title, desc):
    await collection.update_one({"title":title},{"$set":{"description":desc}})
    document = await collection.find_one({"title":title})
    return document

async def remove_todo(title):
    await collection.delete_one({"title":title})
    return True