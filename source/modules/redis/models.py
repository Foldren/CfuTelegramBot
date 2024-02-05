from aredis_om import Field, JsonModel


class User(JsonModel):
    chat_id: int = Field(index=True)
    accessToken: str
    cookies: dict

