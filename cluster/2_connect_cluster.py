import ray
import os
import pandas as pd
from datetime import datetime

# 1. Enable the Mac/Linux hybrid cluster flag
#os.environ["RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER"] = "1"

# --- CONFIGURATION ---
# This connects to the LOCAL end of your Cloudflare bridge
CLUSTER_ADDRESS = "ray://localhost:10001"
# ---------------------

try:
    print(f"🔌 Connecting to Ray Cluster via {CLUSTER_ADDRESS}...")
    # Connect in 'Client Mode'
    ray.init(address=CLUSTER_ADDRESS)

    print("\n✅ SUCCESS! Connected to the Cluster.")
    print("-" * 50)

    # 2. Get Cluster Resources
    resources = ray.cluster_resources()
    nodes = ray.nodes()

    # 3. Format and Print Configuration
    print(f"📊 CLUSTER SUMMARY ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"  • Total Nodes:     {len(nodes)}")
    print(f"  • Total CPUs:      {resources.get('CPU', 0)}")
    print(f"  • Total GPUs:      {resources.get('GPU', 0)}")
    print(f"  • Total RAM:       {resources.get('memory', 0) / 1e9:.2f} GB")
    print(f"  • Object Store:    {resources.get('object_store_memory', 0) / 1e9:.2f} GB")

    print("\n🖥️  NODE DETAILS:")
    node_data = []
    for node in nodes:
        node_data.append({
            "NodeID": node['NodeID'][:8],
            "IP": node['NodeManagerAddress'],
            "Status": "ALIVE" if node['Alive'] else "DEAD",
            "Resources": node['Resources']
        })

    # Display as a clean table (requires pandas)
    df = pd.DataFrame(node_data)
    print(df.to_string(index=False))


    # 4. Quick Execution Test (Ping all nodes)
    @ray.remote
    def get_info():
        import socket
        import sys
        return f"Node: {socket.gethostname()} | Python: {sys.version.split()[0]}"


    print("\n📡 RUNNING DISTRIBUTED TEST...")
    # Run a task for each node to ensure they are all responding
    results = ray.get([get_info.remote() for _ in range(len(nodes))])
    for r in set(results):
        print(f"  • {r}")

except Exception as e:
    print(f"\n❌ CONNECTION FAILED")
    print(f"Error: {e}")
    print("\nQuick Checklist:")
    print("1. Is your 'cloudflared' tunnel still running in the other terminal?")
    print("2. Did you set 'RAY_ENABLE_WINDOWS_OR_OSX_CLUSTER=1' on the Mac Head Node?")
    print("3. Check the Mac: Run 'ray status' to ensure the GCS is alive.")

finally:
    # We keep the connection open for now, but you can call ray.shutdown() if needed.
    pass