from simple_websocket_server import WebSocket

class ConnectionManager:
    clients : dict[WebSocket, str] = {}
    discClients : list[str] = []

    def addClient(self,client : WebSocket):
        print(client.address, 'connected')
        self.clients[client] = ""

    def setClientName(self,client : WebSocket, name : str):
        self.clients[client] = name

    def removeClient(self,client : WebSocket):
        print(client.address, 'closed')
        print(self.clients[client], " disconnected")
        self.discClients.append(self.clients[client])
        self.clients.pop(client)
