import asyncio
from bleak import BleakClient

address = "25d8f817-f7dc-4fa5-b034-c6b94a4810e2"
temp_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        temp = await client.read_gatt_char(temp_UUID)
        print("The current temp is: {0}".format("".join(map(chr, temp))))
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop))
except:
    raise
