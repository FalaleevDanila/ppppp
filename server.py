import asyncio

class ClientServerProtocol(asyncio.Protocol):

    storage = dict()

    def __init__(self):
        super().__init__()

    def process_data(self, data):

        command = data.split(' ')
        ans = 'ok\n'
        if command[0] == 'get' and len(command) == 2:
            res = {}
            if command[1] == '*\n':
                res = self.storage
            else:
                if command[1] in self.storage:
                    res = self.storage[command[1]]
            data = res
            for key, timestamp in data.items():
                res[key] = sorted(timestamp.items())

            for i in res:
                if not i:
                    continue
                for key, value in i.items():
                    #for value, timestamp in values:
                    ans = ans + key + ' ' + value + '\n'
                '''
                if command[1] == '*\n':
                    for key, values in self.storage.items():
                        for value in values:
                            ans = ans + key + ' ' + value[1] + ' ' + value[0] + '\n'
                else:
                    if command[1] in self.storage:
                        for value in self.storage[command[1]]:
                            ans = ans + command[1] + ' ' + value[1] + ' ' + value[0] + '\n' 
                '''
            return ans + "\n"

        elif command[0] == 'put':
            if command[1] not in self.storage:
                self.storage[command[1]] = {}

            self.storage[command[1]][command[3]] = command[2]
            return ans + "\n"
        else:
            return 'error\nwrong command\n\n'

#ok
    def connection_made(self, transport):
        self.transport = transport


    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())



def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()



run_server('127.0.0.1', 8888)