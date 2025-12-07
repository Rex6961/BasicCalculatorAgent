from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class OperationType(str, Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculatorInput(BaseModel):
    a: float = Field(..., description="The first number")
    b: float = Field(..., description="The second number")
    operation: OperationType = Field(..., description="Arithmetic operation to perform")


class CalculatorOutput(BaseModel):
    result: Optional[float] = Field(None, description="The mathematical result if successful")
    error: Optional[str] = Field(None, description="Error message if calculation failed")
    success: bool = Field(..., description="True if calculation was successful")


def basic_calculator(input_data: CalculatorInput) -> CalculatorOutput:
    """Performs basic arithmetic operations with strict validation.

    Args:
        input_data (CalculatorInput): Input data

    Returns:
        CalculatorOutput: Output data
    """
    match input_data.operation:
        case OperationType.ADD:
            return CalculatorOutput(result=input_data.a + input_data.b, success=True)
        case OperationType.SUBTRACT:
            return CalculatorOutput(result=input_data.a - input_data.b, success=True)
        case OperationType.MULTIPLY:
            return CalculatorOutput(result=input_data.a * input_data.b, success=True)
        case OperationType.DIVIDE:
            if input_data.b == 0:
                return CalculatorOutput(error="Cannot divide by zero", success=False)
            return CalculatorOutput(result=input_data.a / input_data.b, success=True)


if __name__=="__main__":
    try:
        raw_data_from_agent = {"a": 15, "b": 4, "operation": "divide"}

        validation_input = CalculatorInput(**raw_data_from_agent)

        output = basic_calculator(validation_input)

        print(output.model_dump(exclude_none=True))

    except ValidationError as e:
        print(f"Agent Hallucination detected: {e}.")
