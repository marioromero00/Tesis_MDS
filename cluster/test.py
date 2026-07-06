import ray
import socket

ray.init("ray://localhost:10001")

@ray.remote
def donde_estoy():
    return {
        "hostname": socket.gethostname(),
    }

print(ray.get(donde_estoy.remote()))