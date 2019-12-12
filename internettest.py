import asyncio
import websockets
andmed = []

connected = {}

async def handler(websocket, path):
    sõnum = await websocket.recv()
    print("recv:", sõnum)
    connected[sõnum[:6]] = {"socket":websocket}
    vastus = "Tere " +  sõnum[:6]
    await websocket.send(vastus)
    while True:
        try:
            sõnum = await websocket.recv()
            print("recv:", sõnum)
            if "Minu nimi on" in sõnum:
                connected[sõnum[:6]]["nimi"] = sõnum[21:]
            print(connected)
            
        except websockets.ConnectionClosed:
            print("Ühendus suletud")
            break

        vastus = "Tere " +  sõnum[:6]
        await websocket.send(vastus)
        


start_server = websockets.serve(handler, "127.0.0.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("Server started")
asyncio.get_event_loop().run_forever()