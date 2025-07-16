# Import Guard and Validator
from pydantic import BaseModel, Field
from guardrails.hub import CompetitorCheck
from guardrails import Guard
from rich import print


# Create Pydantic BaseModel
class Product(BaseModel):
    product_name: str
    product_description: str = Field(
        description="Description about the product",
    )


# Create a Guard to check for valid Pydantic output
guard = (
    Guard()
    .use(
        validator=CompetitorCheck,
        on_fail="fix/exception",
        competitors=["Burger Haven", "Sub Wraps"],
    )
    .from_pydantic(
        output_class=Product,
    )
)

product_details = """
        {
            "product_name": "Veggie Delight Sandwich",
            "product_description": "A delicious sandwich filled with fresh veggies, a healthier alternative to fast food; inspired by the flavors of Sub Wraps."
        }
        """  # noqa
# Run LLM output generating JSON through guard
try:
    output = guard.validate(llm_output=product_details)
    print(guard.history.last.tree)
except Exception as e:
    print(e)
