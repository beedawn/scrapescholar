import dotenv
import os

dotenv.load_dotenv()
host_ip = os.getenv('HOST_IP')

base_url = f"http://{host_ip}:8000"
