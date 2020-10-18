import os
import sys
import json
import asyncio
import sqlite3
import requests
from flask import Flask
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

app = Flask(__name__)
db_filename = 'quotes.db'
schema_filename = 'quotes_schema.sql'
website = 'https://friends-quotes-api.herokuapp.com/quotes/random'

async def run(loop):
    nc = NATS()

    await nc.connect("demo.nats.io:4222", loop=loop)

    async def store(msg):
        data = msg.data.decode()
        if (data == "end"): return
        
        data_json = json.loads(data)
        character = data_json["character"]
        quote = data_json["quote"]

        with sqlite3.connect(db_filename) as conn:
            conn.execute("INSERT INTO quote VALUES (?, ?)", (character, quote)) 

    sid = await nc.subscribe("QueueA", cb=store)

    quote = requests.get(website)
    await nc.publish("QueueA", quote.content)

    try:
        await nc.request("QueueA", b'end')
    except ErrTimeout:
        await nc.unsubscribe(sid)
        await nc.close()

def setup_db():
    if (not os.path.exists(db_filename)):
        with sqlite3.connect(db_filename) as conn:
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)

@app.route("/")
def start():
    setup_db()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()

    res = ""
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quote")
        for row in cursor.fetchall():
            character, quote = row
            res += character + ": " + quote + "\n"
        return res

if __name__ == '__main__':
    app.run(host='0.0.0.0')
