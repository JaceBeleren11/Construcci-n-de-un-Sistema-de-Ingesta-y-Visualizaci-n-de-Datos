import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv

# Obtener la ruta del directorio donde está este script (server.py)
basedir = os.path.abspath(os.path.dirname(__file__))
# Unir esa ruta con el nombre de tu archivo de credenciales
ruta_env = os.path.join(basedir, "Credenciales.env")

# Cargar el archivo usando la ruta completa
load_dotenv(ruta_env)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Permitir peticiones desde cualquier frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API de Data Warehouse"}

@app.get("/api/datos")
def get_datos():
    try:
        # Obtenemos los últimos 50 registros de la base de datos
        response = supabase.table("datos_central").select("*").order("id", desc=True).limit(50).execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 