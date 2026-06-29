import socket


def check_bridge(port=10001):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        # Try to connect to the local end of your tunnel
        s.connect(("localhost", port))
        print(f"✅ SUCCESS: Local port {port} is open and accepting connections.")

        # Try to read a tiny bit of data (Ray usually sends a handshake)
        # Note: This might timeout if Ray is idle, but the connect() above is the real test.
        print("📡 Tunnel is active. Ready for ray.init()")
    except Exception as e:
        print(f"❌ FAILURE: Could not connect to localhost:{port}. Is cloudflared running?")
        print(f"Error: {e}")
    finally:
        s.close()


if __name__ == "__main__":
    check_bridge()