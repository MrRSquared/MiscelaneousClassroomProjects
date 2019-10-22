import socket, time, asyncio
from bleak import BleakClient

address = "D8:A0:1D:54:C7:1A"
color_UUID = "4ac8a682-9736-4e5d-932b-e9b31405049c"

async def run(address, loop, color):
    b = bytearray()
    b.extend(map(ord, color))
    async with BleakClient(address, loop=loop) as client:
        model_number = await client.write_gatt_char(color_UUID, b)
        print("Sent color... " +color +"as.." +str(b))


# Define color dictionary
cheerMap = {
    "FF0000" : "red",
    "008000" : "green",
    "0000FF" : "blue",
    "00FFFF" : "cyan",
    "FFFFFF" : "white",
    "FDF5E6" : "oldlace",
    "800080" : "purple",
    "FF00FF" : "magenta",
    "FFFF00" : "yellow",
    "FFA500" : "orange",
    "FFC0CB" : "pink",}
#Define the color variable (we use that to grab the color from the Cheerlights server.)
color = ''
# Connect to the cheerlights server


url = 'http://api.thingspeak.com/channels/1417/field/2/last.txt'
_, _, host, path = url.split('/', 3)
ai = socket.getaddrinfo(host, 80)
print('Address infos:', ai)
addr = ai[0][-1]
print('Connect address:', addr)

while True:
    try:
        x = 0
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while (x is not 1 ):
            # s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
            data = s.recv(100)
            print(data)
            if data:
                    chunk = str(data, 'utf8')
                    # print(chunk, end='')s
                    hash_index = chunk.find('#')
                    if hash_index >= 0:
                        color = chunk[hash_index + 1: hash_index + 7]
                        led_color = cheerMap.get(color)
                        loop = asyncio.get_event_loop()
                        loop.run_until_complete(run(address, loop, led_color))
                        # dotstar[0] = led_color
                        print(led_color)
                        x=1
        time.sleep(5)
        s.close()
    except (KeyboardInterrupt, SystemExit):
        break
    except Exception as inst:
        print('')
        print('-------------------------------------------------------------')
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly,
        print('-------------------------------------------------------------')
        print('')
    # but may be overridden in exception subclasses
