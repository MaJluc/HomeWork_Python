from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=20)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=12)
    category_id: int


class QuestionResponse(BaseModel):
    id: int
    text: str
    category: CategoryBase | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class MessageResponse(BaseModel):
    message: str