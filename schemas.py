from pydantic import BaseModel


class AuthDetails(BaseModel):
    username: str
    password: str

class DataDetails(BaseModel):
    data_device_id: str
    data_smoke: str
    data_vibration: str
    data_mic: str
    data_motion: str
    data_key: str