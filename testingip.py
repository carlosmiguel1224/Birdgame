import socket

def get_local_ip():
    try:
        # Create a temporary socket connection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Connect to an arbitrary address (not important)
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]  # This gives the local IP address
    except Exception as e:
        local_ip = '127.0.0.1'  # Default to loopback address if error occurs
    finally:
        s.close()
    return local_ip

# Get the local IP address
local_ip = get_local_ip()
print(f"Local IP address: {local_ip}")

#This is the real local ip for the game 192.168.1.119