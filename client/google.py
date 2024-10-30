from dataclasses import dataclass

import httpx

from schema import GoogleUserData
from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient


    async def get_user_info(self, code: str) -> GoogleUserData:
        """
        Мы должны верифицировать себя как приложение, что бы
        гугл понял что это именно то приложение куда он отправляет код,
        поэтому пишем свои креды.
        """
        access_token = await self._get_access_token(code=code)
        async with self.async_client as client:
            print("перед отправкой все нормально")
            user_info = await client.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
        print("выполнили отправку токена в гугл")
        return GoogleUserData(**user_info.json(), access_token=access_token)

    async def _get_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        async with self.async_client as client:
            response = await client.post(self.settings.GOOGLE_TOKEN_URL, data=data)

        print("выполняем получение токена")
        return response.json()["access_token"]  # по этому токену мы сново идем в гугул что бы получить user info
