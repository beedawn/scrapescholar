from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
# Make sure this key is the same key used for encryption

load_dotenv()
print("Loaded ENCRYPTION_KEY:", os.getenv("ENCRYPTION_KEY"))

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY") 


import os
print("ENCRYPTION_KEY:", os.getenv("ENCRYPTION_KEY"))
fernet = Fernet(ENCRYPTION_KEY)

encrypted_username = "gAAAAABnJkxH1Pl0YQpqbVYiJO8zPntO_CfCk7p1MR91aMQSTn-zEWAY0FXKT9uoVC-f0cEuNswXBno-Fa3Il1Jl_JUkLaFFkg=="

try:
    decrypted_username = fernet.decrypt(encrypted_username.encode()).decode()
    print("Decrypted Username:", decrypted_username)
except Exception as e:
    print("Decryption failed:", e)
