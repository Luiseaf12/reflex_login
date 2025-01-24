import reflex as rx
import re
import asyncio
import bcrypt as bc
from sqlmodel import select
from typing import List
from ..models import User

class SessionState(rx.State):
    username: str = 'usuario1@test.com'
    password: str = ""
    loader: bool = False
    error_create_user: str = ''

    @rx.event(background=True)
    async def auth_user(self, data: dict):
        print(data)
        async with self:
            self.loader = True
            try:
                resp = self.user_validate(data['username'], data['password'])
                print(resp)
                self.loader = False
                if resp:
                    print ("redireccionando")
                    return rx.redirect('/')
            except BaseException as be:
                self.error_create_user = str(be.args[0])
                self.loader = False
        await self.handleNotify()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(2)
            self.error_create_user = ''

    @rx.var(cache=False)
    def user_invalid(self) -> bool:
        return not (re.match(r"[^@]+@[^@]+.[^@]+", self.username) and self.username != "example@mail.com")
    
    @rx.var(cache=False)
    def user_empty(self) -> bool:
        return not self.username.strip()

    @rx.var(cache=False)
    def password_empty(self) -> bool:
        return not self.password.strip()

    @rx.var(cache=False)
    def validate_fields(self) -> bool:
        return (
            self.user_empty
            or self.user_invalid
            or self.password_empty
        )


    def user_validate(self, email: str, password: str):
        #buscar usuario
        user = self.select_userb_by_email(email)
        if(user == None):
            raise BaseException('El usuario no existe')
        if(not self.validate_password(password, user.password)):
            raise BaseException('Credenciales incorrectas')
        rx.LocalStorage("pruebatoken", name="TOKEN")
        rx.Cookie(name="pruebatoken", max_age=3600)
        return True

    def validate_password(self, password: str, password_db:str):
        #hashed = bc.hashpw(password.encode('utf-8'), bc.gensalt())
        return bc.checkpw(password.encode('utf-8'), password_db.encode('utf-8'))
        
    
    def select_userb_by_email(self, email: str):
        with rx.session() as session:
            query = select(User).where(User.username == email)
            return session.exec(query).one_or_none()

class UsersState(rx.State):
    """Estado para manejar los usuarios."""
    
    users: List[User] = []
    search_term: str = ""
    
    @rx.var(cache=False)
    async def get_users(self):
        """Obtiene todos los usuarios de la base de datos."""
        async with get_async_session() as session:
            query = select(User)
            result = await session.execute(query)
            self.users = result.scalars().all()
    
    async def on_mount(self):
        """Se ejecuta cuando el componente se monta"""
        await self.get_users()
    
    @rx.var(cache=False)
    def filtered_users(self) -> List[User]:
        if not self.search_term:
            return self.users
        
        search = self.search_term.lower()
        return [
            item for item in self.users
            if search in item.username.lower() 
            or (item.descripcion and search in item.descripcion.lower())
        ]