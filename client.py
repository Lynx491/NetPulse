import asyncio
import aiohttp
import json
import flet as fl
import flet_charts as flc



class veriable_manager():
    def __init__(self):
        self.veriable_table = {
        }

    def add(self,data:dict):
        result = self.veriable_table.get(data["agent_name"])
        if result:

            result["procc_temp"].append(flc.LineChartDataPoint(len(result["procc_temp"]),data["procc_temp"]))

            result["ram_usage"].append(flc.LineChartDataPoint(len(result["ram_usage"]),data["ram_usage"]))
            result["download"].append(flc.LineChartDataPoint(len(result["download"]),data["download"]))
            result["upload"].append(flc.LineChartDataPoint(len(result["upload"]),data["upload"]))
            result["swap_usage"].append(flc.LineChartDataPoint(len(result["swap_usage"]),data["swap_usage"]))
            result["gpu_temp"].append(flc.LineChartDataPoint(len(result["gpu_temp"]),data["gpu_temp"]))
            for num,i in enumerate(result["cpu_list"]):
                i.append(flc.LineChartDataPoint(len(i),data["cpu_list"][num]))


        else:
            self.veriable_table[data["agent_name"]] = {} 
            self.veriable_table[data["agent_name"]]["procc_temp"] = [] 
            self.veriable_table[data["agent_name"]]["ram_usage"] = [] 
            self.veriable_table[data["agent_name"]]["hostname"] = data["host_name"]
            self.veriable_table[data["agent_name"]]["swap_usage"] = []
            self.veriable_table[data["agent_name"]]["gpu_temp"] = []
            self.veriable_table[data["agent_name"]]["download"] = []
            self.veriable_table[data["agent_name"]]["upload"] = []
            self.veriable_table[data["agent_name"]]["cpu_list"] = []
            for i in range(len(data["cpu_list"])-1):
                self.veriable_table[data["agent_name"]]["cpu_list"].append([])


            self.add(data) 

    def adds(self,data_list:list):
        for data in data_list:
            self.add(data)
    




class Application():
    def __init__(self,page:fl.Page):
        self.page = page
        self.page.bgcolor="#000000"
        self.vm = veriable_manager()
        
        self.main = fl.Column(expand=True,scroll=fl.ScrollMode.ADAPTIVE)
        self.resp_row = fl.ResponsiveRow()
        self.main.controls.append(self.resp_row)
        self.page.add(self.main)
        self.page.update()
        asyncio.create_task(self.weboscket_listener())
        asyncio.create_task(self.regenerator())

    async def regenerator(self):
        while True:
            await asyncio.sleep(1)
            await self.Monitors_Creator()
        

    def NewComputerAdd(self,data_list:dict): 
        agent_name = data_list["agent_name"]
        hostname = data_list["hostname"]
        gpu_temp = data_list["gpu_temp"]
        cpu_temp = data_list["procc_temp"]
        cpu_list = data_list["cpu_list"]
        ram_usage = data_list["ram_usage"]
        swap_usage = data_list["swap_usage"]
        down_list = data_list["download"]
        up_list = data_list["upload"]


        container = fl.Container(
            content=fl.Column(
                controls=[
                    
                    fl.Container(bgcolor="#222222",content=fl.Column(
                        controls=[
                            fl.Row(controls=[
                                fl.Text("Agent: ",color="#FFFFFF"),
                                fl.Text(agent_name,color="#FFFFFF"),
                                fl.Text("Hostname: ",color="#FFFFFF"),
                                fl.Text(hostname,color="#FFFFFF")
                            ]),
                            fl.ResponsiveRow(
                                controls=[
                                    fl.Container(
                                        content=
                                            fl.Column(
                                                controls=[
                                                    fl.Text("Gpu And Cpu Temperature",style=fl.TextStyle(size=32),color="#FFFFFF"),
                                                    fl.Row(
                                                        controls=[
                                                            fl.Text(value="GPU color: ",color="#FFFFFF"),
                                                            fl.Button(content=fl.Text(""),bgcolor="#008800")
                                                        ]
                                                    ),
                                                    fl.Row(
                                                        controls=[
                                                            fl.Text(value="CPU color: ",color="#FFFFFF"),
                                                            fl.Button(content=fl.Text(""),bgcolor="#BB0000")
                                                        ]
                                                    ),
                                                    flc.LineChart(data_series=[gpu_temp,cpu_temp])
                                                ]
                                            ),col={"xs":6,"sm":6,"md":6,"lg":6,"xl":6},bgcolor="#444444"
                                    ),
                                    fl.Container(
                                        content=
                                            fl.Column(
                                                controls=[
                                                    fl.Text("Processor temperature per core",style=fl.TextStyle(size=32),color="#FFFFFF"),
                                                    
                                                    flc.LineChart(data_series=cpu_list)
                                                    
                                                ]
                                            ),col={"xs":6,"sm":6,"md":6,"lg":6,"xl":6},bgcolor="#444444"
                                    ), #Processor temperature per core

                                    fl.Container(
                                        content=
                                            fl.Column(
                                                controls=[
                                                    fl.Text("Ram And Swap Usage",style=fl.TextStyle(size=32),color="#FFFFFF"),
                                                    fl.Row(
                                                        controls=[
                                                            fl.Text(value="Ram color: ",color="#FFFFFF"),
                                                            fl.Button(content=fl.Text(""),bgcolor="#000000")
                                                        ]
                                                    ),
                                                    fl.Row(
                                                        controls=[
                                                            fl.Text(value="Swap color: ",color="#FFFFFF"),
                                                            fl.Button(content=fl.Text(""),bgcolor="#AA6600")
                                                        ]
                                                    ),
                                                    flc.LineChart(data_series=[ram_usage,swap_usage])
                                                    
                                                ]
                                            ),col={"xs":6,"sm":6,"md":6,"lg":6,"xl":6},bgcolor="#444444"
                                    ),
                                    fl.Container(
                                        content=
                                            fl.Column(
                                                controls=[
                                                    fl.Text("Download And Upload Speed",style=fl.TextStyle(size=32),color="#FFFFFF"),
                                                    fl.Row(
                                                        controls=[
                                                            fl.Text(value="Download color: ",color="#FFFFFF"),
                                                            fl.Button(content=fl.Text(""),bgcolor="#000988")
                                                        ]
                                                    ),
                                                    fl.Row(
                                                        controls=[
                                                            fl.Text(value="Upload color: ",color="#FFFFFF"),
                                                            fl.Button(content=fl.Text(""),bgcolor="#520088")
                                                        ]
                                                    ),
                                                    flc.LineChart(data_series=[down_list,up_list])
                                                ]
                                            ),col={"xs":6,"sm":6,"md":6,"lg":6,"xl":6},bgcolor="#444444"
                                    )
                                ]
                            )
                        ]
                    ))
                ]
            ),col={"xs":12,"sm":12,"md":12,"lg":12,"xl":12})
       
        self.resp_row.controls.append(container)

    def nth(self,num):
        if num <= 15:
            translate = {"10":"A","11":"B","12":"C","13":"D","14":"E","15":"F"}
            value = translate.get(str(num))
            if value:
                return value
            return num

    def htn(self,h):
        translate = {"A":"10","B":"11","C":"12","D":"13","E":"14","F":"15"}
        value = translate.get(h)
        if value:
            return value
        return h

    def get_cpu_list_colors(self,num=1):
        colors=[]
        defaut_cpu_color = "440000"
        color = ""
        index=0
        for i in range(num):
            for char in defaut_cpu_color:
                color += ""
                if char != "F" and index != 2:
                    index += 1
                    char = (self.nth(int(self.htn(char))+1))

                
                color += str(char)

            colors.append(color)

        return colors

            

    async def Monitors_Creator(self):
        self.resp_row.controls.clear()
        for agent_name in self.vm.veriable_table.keys():
            ram_list = self.vm.veriable_table[agent_name]["ram_usage"]
            procc_list = self.vm.veriable_table[agent_name]["procc_temp"]
            gpu_list = self.vm.veriable_table[agent_name]["gpu_temp"]#new
            cpu_list = self.vm.veriable_table[agent_name]["cpu_list"]#new
            swap_list = self.vm.veriable_table[agent_name]["swap_usage"]#new
            download_list = self.vm.veriable_table[agent_name]["download"]#new
            upload_list = self.vm.veriable_table[agent_name]["upload"]#new
            hostname = self.vm.veriable_table[agent_name]["hostname"]

            ram_data = flc.LineChartData(
                points=ram_list,
                stroke_width=3,
                color="#000000"
            )

            procc_data = flc.LineChartData(
                points=procc_list,
                stroke_width=3,
                color="#BB0000"
            )
            gpu_data = flc.LineChartData(
                points=gpu_list,
                stroke_width=3,
                color="#008800"
            )

            swap_data = flc.LineChartData(
                points=swap_list,
                stroke_width=3,
                color="#AA6600"
            )
            down_data = flc.LineChartData(
                points=download_list,
                stroke_width=3,
                color="#000988"
            )
            up_data = flc.LineChartData(
                points=upload_list,
                stroke_width=3,
                color="#520088"
            )


            cpu_usage_datas_list = []
            cpu_colors = self.get_cpu_list_colors(len(cpu_list)-1)
            for i_list,color in zip(cpu_list,cpu_colors):
                cpu_data = flc.LineChartData(
                points=i_list,
                stroke_width=3,
                color=color
                )
                cpu_usage_datas_list.append(cpu_data)

            data = {"agent_name":agent_name,"hostname":hostname,"ram_usage":ram_data,"procc_temp":procc_data,"gpu_temp":gpu_data,"swap_usage":swap_data,"download":down_data,"upload":up_data,"cpu_list":cpu_usage_datas_list}
            self.NewComputerAdd(data)

        self.page.update()


    async def weboscket_listener(self):
        async with aiohttp.ClientSession() as s: 
            async with s.ws_connect("ws://localhost:8563/ws") as ws: 

                self.data = {"type":"monitor"}  
                await ws.send_str(json.dumps(self.data))

                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        self.recv_data = json.loads(msg.data)

                        self.vm.adds(self.recv_data["data"])

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        print("errors....")
                        break
                


if __name__=="__main__":
    fl.run(Application)