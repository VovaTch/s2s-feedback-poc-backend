from typing import Self

from pydantic import BaseModel, Field, ValidationError, model_validator


class Query(BaseModel):
    lang_id: str
    eng_sentence: str
    lang_sentence: str


class FeedbackError(BaseModel):
    message: str
    rating_deducted: int = Field(..., ge=1, le=10)


class FeedbackResponse(BaseModel):
    thoughts: list[str]
    total_rating: int = Field(..., ge=1, le=10)
    errors: list[FeedbackError]
    correct_translations: list[str]

    @model_validator(mode="after")
    def check_rating(self) -> Self:
        rating_deducted_sum = sum(error.rating_deducted for error in self.errors)
        if 10 - self.total_rating != rating_deducted_sum:
            raise ValidationError(
                "The sum of rating deducted must be equal to 10 - total_rating"
            )
        return self
