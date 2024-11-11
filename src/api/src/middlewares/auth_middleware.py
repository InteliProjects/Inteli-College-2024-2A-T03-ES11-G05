from fastapi import Request, HTTPException, Depends
from utils.supabase_client import SupabaseClient
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Usando FastAPI Security para obter o token do cabeçalho Authorization
security = HTTPBearer()

sb = SupabaseClient();

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials  # Extrai o token JWT do cabeçalho Authorization
    
    try:
        # Valida o token JWT usando o Supabase
        user = sb.supabase.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

# Dependência para obter o usuário atual
async def get_current_user(user: dict = Depends(verify_token)):
    return user
