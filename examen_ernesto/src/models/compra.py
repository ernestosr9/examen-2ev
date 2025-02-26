from sqlmodel import Field, SQLModel

class Compra(SQLModel, table=True):
    producto: str | None = Field(default=None, primary_key=True)
    tipo: str = Field(index=True, max_length=50)
    precio: int = Field(gt=0)

