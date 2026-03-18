import subprocess
import time
import ray

REMOTE_HOSTNAME = "ray-client.monaka.cl"
LOCAL_PORT = "10001"

CF_CLIENT_ID = "TU_CLIENT_ID"
CF_CLIENT_SECRET = "TU_CLIENT_SECRET"

print(f"🌉 Opening bridge to {REMOTE_HOSTNAME}...")

conf_bridge = subprocess.Popen(
    [
        "./cloudflared", "access", "tcp",
        "--hostname", REMOTE_HOSTNAME,
        "--url", f"localhost:{LOCAL_PORT}",
        "--header", f"CF-Access-Client-Id={CF_CLIENT_ID}",
        "--header", f"CF-Access-Client-Secret={CF_CLIENT_SECRET}",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

time.sleep(5)

try:
    print("📡 Connecting to Ray cluster...")
    ray.init(address=f"ray://localhost:{LOCAL_PORT}")
    print("✅ SUCCESS! Connected to the Ray Cluster.")
    print(f"Nodes in Cluster: {len(ray.nodes())}")
except Exception as e:
    print(f"❌ FAILED: {e}")
finally:
    conf_bridge.terminate()