import machine, neopixel, time
from machine import Timer

neo_di = machine.Pin(28)
np = neopixel.NeoPixel(neo_di, 12)

print(np.n)


# print("freq MHz", machine.freq()/1000000)

# TIMEOUT_MS = 60*1000 # use with await hat_characteristic_write.written(timeout_ms=TIMEOUT_MS)


import bluetooth, aioble
import asyncio

# Test using https://googlechrome.github.io/samples/web-bluetooth/discover-services-and-characteristics.html
HAT_SERVICE_UUID = bluetooth.UUID("8d8bbe55-f9c9-4436-8541-c26ea243dbae")
HAT_CHAR_UUID_WRITE = bluetooth.UUID("05839cfc-5d02-4daa-80d9-82303b98f7fc")
# HAT_CHAR_UUID_READ = bluetooth.UUID("aa54674c-afa6-447e-b92b-ff60301fbfd0")

hat_service = aioble.Service(HAT_SERVICE_UUID)
# Should this be a aioble.BufferedCharacteristic?
hat_characteristic_write = aioble.Characteristic(
    hat_service, HAT_CHAR_UUID_WRITE, write=True, read=True, notify=True, capture=True
)
#hat_characteristic_read = aioble.Characteristic(
#    hat_service, HAT_CHAR_UUID_READ, read=True, notify=True
#)
aioble.register_services(hat_service)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 2_000
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_DISPLAY = const(320)

# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    print("starting peripheral_task")
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="sound-hat",
            services=[HAT_SERVICE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_DISPLAY,
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected(timeout_ms=5*60*1_000)
            all_off()
            
def all_on():
    np.fill((150,150,150))
    np.write()

def all_off():
    np.fill((0,0,0))
    np.write()   

# https://stackoverflow.com/questions/76728708/micropython-aioble-how-to-receive-data-as-a-server
async def recv_actor():
    print('READING', hat_characteristic_write)
    while True:
        # capture enabled returns "data"
        connection, data = await hat_characteristic_write.written()
        print("Got something from written", data)
        message = data.decode('utf-8')
        messageType, messageState = message.split(':', 1)
        if messageType == "l" and messageState.lower() == 'on':
            print("turning light on")
            all_on()
        elif messageType == "l" and messageState.lower() == 'off':
            print("turning light off")
            all_off()
        else:
            print("Unknown messageType and Message:", message, messageType, messageState)
        # await asyncio.sleep(1)

#async def subscribe_actor():
#    await hat_characteristic_write.subscribe(notify=True)
#    while True:
#        data = await hat_characteristic_write.notified()
#        print("Got something from subscribe!", data)

# Run both tasks.
async def main():
    print("starting main")
#    t1 = asyncio.create_task(heartbeat_task())
    t2 = asyncio.create_task(peripheral_task())
    t3 = asyncio.create_task(recv_actor())
    await asyncio.gather(t2, t3)
    print("finished main")


asyncio.run(main())

print("finished running script")

# TODO def instance0():
#    try:
#        asyncio.run(instance0_task())
#    finally:
#        aioble.stop()
