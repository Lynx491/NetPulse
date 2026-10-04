from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from sqlmodel import SQLModel, Field,select,delete, desc,JSON
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
import time
import dotenv
import os
import json
import asyncio
import uvicorn
from contextlib import asynccontextmanager


dotenv.load_dotenv() #Required to read the .env file


class Data(SQLModel, table = True): #Create tabe
    __table_args__={"extend_existing":True}
    primary_id:Optional[int] = Field(default=None,primary_key=True)
    agent_name: str
    host_name:str
    procc_temp:float
    ram_usage:float
    swap_usage:float
    gpu_temp:float
    download:float
    upload:float
    cpu_list: List[float] = Field(default=[],sa_type=JSON)
    time:float


class Manager(): #Table manager
    def __init__(self):
        self.async_engine = create_async_engine(os.getenv("DATABASE_URL")) #Data is retrieved from `env`, and an asynchronous motor is created
        self.async_session_factory = sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )#Session maker, I set it up for temporary use if needed
       

    async def Update(self): #It saves the table asynchronously
        async with self.async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
            
    #Asynchronous data insertion
    async def AddData(self,agent_name,hostname,ram_usage,procc_temp,gpu_temp,swap_usage,download,upload,cpu_list:list):
        if (not agent_name is None) and (not hostname is None) and (not ram_usage is None) and (not procc_temp is None) and (not gpu_temp is None) and (not swap_usage is None)and (not download is None)and (not upload is None) and (cpu_list != []):
            
            async with self.async_session_factory() as s:
                
                data = Data(agent_name=agent_name,host_name=hostname,ram_usage=ram_usage,procc_temp=procc_temp,swap_usage=swap_usage,gpu_temp=gpu_temp,download=download,upload=upload,cpu_list=cpu_list,time=time.time())

                s.add(data)
                await s.commit()

    #retrieves the most recently added data
    async def NewTake(self,value=1):
        """value, asks how many we're going to get"""
        async with self.async_session_factory() as s:
            #Retrieve the value with the largest time value from the database
            search = select(Data).order_by(desc(Data.time)).limit(value)
            result = (await s.exec(search)).all() #desc sorts from highest to lowest; first takes the highest value

            return result

            
monitor_computers = [] #To send the monitor list in bulk
agent_list = [] #It's necessary because it retrieves as much new data as there are agents.
mg = Manager()


async def sender():
    try:
        while True:
            if agent_list and monitor_computers: #if the agent_list and monitor_list are not empty
                
                await asyncio.sleep(5) #Wait 5 seconds
                data_liste = await mg.NewTake(len(agent_list)) #fetch the latest data
                
                if data_liste: #If the retrieved data is empty,
                    datas=[]
                    
                    for i in data_liste: #Browse through the data_liste and convert it to Python code using model_dump
                        datas.append(i.model_dump()) # Add the converted data to the list named “datas”
                    
                    data = {"type":"info","data":datas} # Generate data
                    jsdata = json.dumps(data) #Convert to a JSON string
                    
                    dead_monitors = []
                    
                    for i in monitor_computers: #Browse the monitor list
                        
                        try:
                            await i.send_text(jsdata) #If you can send it, please do.
                        
                        except Exception:
                            dead_monitors.append(i) #If you can't send it, add it to the list named “dead_monitors”

                    for dead in dead_monitors: # Clear the dead monitors from the dead_monitors list
                        if dead in monitor_computers:
                            monitor_computers.remove(dead)
            
            else: #If the monitor and agent lists are empty,
                await asyncio.sleep(1) # Wait 1 second so it doesn't freeze



    except asyncio.CancelledError:
        pass #This runs when the client disconnects.

    except Exception as e:
        print(f"Sender Error: {e}")


@asynccontextmanager #To safely start and safely shut down the server
async def lifespan(app: FastAPI):
    # Initially, create the tables asynchronously
    await mg.Update()
    # Start the background broadcast task
    sender_task = asyncio.create_task(sender())
    yield
    # Cancel the background task at shutdown
    sender_task.cancel()

app = FastAPI(lifespan=lifespan)



@app.websocket("/ws")
async def websocket(user:WebSocket):

    await user.accept() #accept the connection

    recv = await user.receive_text()# listen
    dict_recv = json.loads(recv)# Convert the incoming data from a JSON string to a Python dictionary

    #If it's a monitor, add it to the monitor list; if it's an agnet, add it to the agnet list
    if dict_recv["type"] == "monitor": 
        monitor_computers.append(user)

    elif dict_recv["type"] == "agent":
        agent_list.append(user)


    try:
        while True:
            recv = await user.receive_text()
            dict_recv = json.loads(recv) #Convert the incoming data to dick

            if dict_recv["type"] == "info":#The agent is providing information
                #Add data
                await mg.AddData(dict_recv["agent_name"],dict_recv["hostname"],dict_recv["ram_usage"],dict_recv["procc_temp"],dict_recv["gpu_temp"],dict_recv["swap_usage"],dict_recv["download"],dict_recv["upload"],dict_recv["cpu_list"])
    
    except WebSocketDisconnect: #Run when there is a timeout or the connection is lost

        if user in monitor_computers: #If a user is monitored, remove them from the monitor list
            monitor_computers.remove(user)

        if user in agent_list: #If it's in the user agent list, remove it from the user agent list
            agent_list.remove(user)
        
        print("Connected Closed")

    except Exception as e:
        print(e)

    

if __name__ == "__main__": #Run the server with uvicorn
    uvicorn.run("main:app", host="localhost", port=8563,reload=True)




