import asyncio
import websockets

async def test_ws():
    uri = "ws://127.0.0.1:8000/ws/telemetry"
    try:
        async with websockets.connect(uri) as websocket:
            print("[*] Connected to WS")
            msg = await websocket.recv()
            print(f"[*] Received: {msg}")
    except Exception as e:
        print(f"[!] WS Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
