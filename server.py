import asyncio

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False



class ClientServerProtocol(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        self.storage = {}

    def get(self, key):
        res = {}
        if key == '*':
            res = self.storage
        else:
            if key in self.storage:
                res = {key: {self.storage[key]}}

        data = res
        if data != {}:
            for key, timestamp in data.items():
                res[key] = sorted(timestamp.items())
        return res

    def put(self, key, value, timestamp):
        if key not in self.storage:
            self.storage[key] = {}
        self.storage[key][timestamp] = value
        #self.storage[key].append((int(timestamp), float(value)))
        #self.storage[key].sort(key=lambda tup: tup[0])

    def form_answer(self, data):
        ans = []
        for key, values in data.items():
            if not key:
                continue
            for timestamp, value in values:
                ans.append(f"{key} {value} {timestamp}")

        res = ''
        if ans:
            for j in ans:
                res += j + '\n'

        return res

    def process_data(self, data):

        command = data.split(' ')

        ans = 'ok\n'
        if command[0] == 'get' and len(command) == 2:
            command[1] = command[1].replace('\n', '')
            ans_c = self.get(command[1])
            if ans_c:
                ans += self.form_answer(ans_c)
            return ans + "\n"

        elif command[0] == 'put' and len(command) == 4 and is_digit(command[2]) and is_digit(command[3]):
            command[3] = command[3].replace('\n', '')
            self.put(command[1], float(command[2]), int(command[3]))
            return ans + "\n"
        else:
            return 'error\nwrong command\n\n'

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
