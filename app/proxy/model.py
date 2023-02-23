
from typing import Optional
from pydantic import BaseModel, Field


class CreateProxy(BaseModel):
    proxy_name: str 
    ip_address: str
    port: str
    note: str
    
    class config: 
        orm_mode = True
        
class UpdateProxy(BaseModel):
    proxy_name: Optional[str]
    ip_address: Optional[str]
    port: Optional[str]
    note: Optional[str]
    
    class config: 
        orm_mode = True
