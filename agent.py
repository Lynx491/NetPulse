#Agent
import platform
import psutil
import aiohttp
import asyncio
import json

try: #To prevent it from crashing if there's no graphics card
    import GPUtil
except ImportError:
    GPUtil = None


class app():
    def __init__(self):
        self.agent_name = "test_agent" # The name “agnet”
        self.computer_name = platform.node() #Get the PC name

    async def get_network_speed(self,interval=1): #Calculate download and upload speeds
        net1 = psutil.net_io_counters() 

        await asyncio.sleep(interval) 

        net2 = psutil.net_io_counters() 

        #Calculate the difference and convert from kilobytes to megabytes
        download_speed = (net2.bytes_recv - net1.bytes_recv) / interval / 1024
        upload_speed = (net2.bytes_sent - net1.bytes_sent) / interval / 1024

        return round(download_speed, 2), round(upload_speed, 2)

    def get_cpu_temp(self):#Get the CPU temperature; if it can't be retrieved, return 0.0
        try:
            temps = psutil.sensors_temperatures()
            if "coretemp" in temps:
                return temps["coretemp"][0].current
            elif "cpu_thermal" in temps:
                return temps["cpu_thermal"][0].current
            for entry in temps.values():
                if entry:
                    return entry[0].current
        except (AttributeError, Exception):
            return 0.0
        


    def get_gpu_temp(self):#If the graphics card temperature cannot be retrieved, set it to 0.0

        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    return f"{gpus[0].temperature}"
            except Exception:
                pass
        return 0.0


    async def run(self):
         async with aiohttp.ClientSession() as s: #We're logging in
            try:
                while True: #If the connection is lost, reconnect
                    async with s.ws_connect("ws://localhost:8563/ws") as ws: #We're connecting
                        data = {"type":"agent"} 
                        await ws.send_str(json.dumps(data)) #We are sending data indicating that it is an agent

                        try:
                            while True: 
                                
                                self.cpu_per_core = psutil.cpu_percent(interval=1, percpu=True) #Get the temperatures of the CPU cores

                                ram_info = psutil.virtual_memory() #Get RAM information
                                self.ram_usage = ram_info.percent # Get the usage from the RAM information

                                swap_info = psutil.swap_memory() # Get swap information
                                self.swap_usage = swap_info.percent # Get usage information from the swap

                                self.isc_temperatures = self.get_cpu_temp() # CPU temperature
                                self.gpu_temp = self.get_gpu_temp() # GPU temperature, if any
                                self.download_speed, self.upload_speed = await self.get_network_speed() #indirme ve yükleme hızarını al
                                
                                #Create and send data
                                data = {"type":"info","agent_name":self.agent_name,"hostname":self.computer_name,"procc_temp":self.isc_temperatures,"ram_usage":self.ram_usage,"swap_usage":self.swap_usage,"download":self.download_speed,"upload":self.upload_speed,"cpu_list":self.cpu_per_core,"gpu_temp":self.gpu_temp}
                                await ws.send_str(json.dumps(data))
                                await asyncio.sleep(4) #Wait 4 seconds

                        except Exception as e:
                            print(e)

                    await asyncio.sleep(1)
            except Exception as e:
                print(e)

                    

                
if __name__ == "__main__":
    application = app()
    asyncio.run(application.run())
    