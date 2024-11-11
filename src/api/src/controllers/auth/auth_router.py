from fastapi import APIRouter, FastAPI, HTTPException, Depends
from pydantic import BaseModel
from utils.supabase_client import SupabaseClient
from middlewares.auth_middleware import get_current_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Ingest route not found"}}
)

# Modelo de dados para login
class LoginRequest(BaseModel):
    email: str
    password: str

sb = SupabaseClient();

# Endpoint de autenticação
@auth_router.post("/login")
async def login(request: LoginRequest):

    print(request.email)

    try:
        # Faz login no Supabase
        response = sb.supabase.auth.sign_in_with_password({
            'email': request.email,
            'password': request.password
        })

        # # Verifica se houve um erro na resposta
        # if response.error:
        #     raise HTTPException(status_code=400, detail=response.error.message)
        
        # Extrai o token de acesso JWT e as informações do usuário
        access_token = response.session.access_token  # Acessa o token diretamente da sessão
        user_info = response.user  # Acessa informações do usuário diretamente

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user_info.id,
                "email": user_info.email,
                "role": user_info.role
            }
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Falha na autenticação.")

# Endpoint protegido que requer autenticação
@auth_router.get("/secure-data")
async def secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "Você está autenticado", "user": current_user}

# Endpoint público que não requer autenticação
@auth_router.get("/public-data")
async def public_data():
    return {"message": "Este é um endpoint público. Não é necessária autenticação."}
