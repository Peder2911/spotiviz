import os

PRODUCTION = bool(os.getenv("PRODUCTION",False))
FRONTEND_DEV_SERVER = os.getenv("FRONTEND_DEV_SERVER","http://localhost:1234")

