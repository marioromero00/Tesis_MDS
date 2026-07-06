import ray
import socket

ray.init("ray://localhost:10001")
@ray.remote
def pip_list():
    import subprocess
    import socket

    out = subprocess.check_output(
        ["python", "-m", "pip", "list"],
        text=True
    )

    return socket.gethostname(), out

host, paquetes = ray.get(pip_list.remote())

print(host)
print(paquetes)