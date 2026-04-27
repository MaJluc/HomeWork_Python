from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator


class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)

class User(BaseModel):
    name: str = Field(pattern=r"^[A-Za-z ]{2,}$")
    age: int = Field(..., gt=0, le=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode="after")
    def check_employment(self):
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError("Возраст должен быть 18-65 для работающего")
        return self

def registration(json_input: str):
    try:
        user = User.model_validate_json(json_input, strict=True)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return e.json(indent=4)
    
# ТЕСТОВЫЕ ДАННЫЕ:    

# ✅ УСПЕШНЫЙ КЕЙС
valid_json = """{
    "name": "John Doe",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}"""

# ❌ ОШИБКА: возраст не подходит для работающего
invalid_age_json = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}"""

# ❌ ОШИБКА: неверный email
invalid_email_json = """{
    "name": "John Doe",
    "age": 25,
    "email": "wrong_email",
    "is_employed": false,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}"""

# ❌ ОШИБКА: некорректные данные адреса
invalid_address_json = """{
    "name": "John Doe",
    "age": 25,
    "email": "john@example.com",
    "is_employed": false,
    "address": {
        "city": "B",
        "street": "St",
        "house_number": -5
    }
}"""


if __name__ == "__main__":
    print("✅ VALID:")
    print(registration(valid_json))

    print("\n❌ INVALID AGE:")
    print(registration(invalid_age_json))

    print("\n❌ INVALID EMAIL:")
    print(registration(invalid_email_json))

    print("\n❌ INVALID ADDRESS:")
    print(registration(invalid_address_json))