from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BranchBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    address: str | None = Field(default=None, max_length=255)


class BranchCreate(BranchBase):
    pass


class BranchUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    address: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class BranchResponse(BranchBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=8, max_length=128)
    role: UserRole
    branch_id: int | None = None

    @model_validator(mode="after")
    def validate_branch(self):
        if self.role == UserRole.COMMON and self.branch_id is None:
            raise ValueError("A common user must be assigned to a branch")
        return self


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=80)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None
    branch_id: int | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole
    branch_id: int | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class StockChange(BaseModel):
    product_id: str = Field(min_length=1, max_length=80)
    quantity: int = Field(gt=0)


class StockResponse(BaseModel):
    id: int
    branch_id: int
    product_id: str
    quantity: int
    branch_name: str | None = None

    model_config = ConfigDict(from_attributes=True)



class MessageResponse(BaseModel):
    message: str
