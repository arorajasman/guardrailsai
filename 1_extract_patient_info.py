from pydantic import BaseModel, Field
from typing import List
from guardrails.hub import ValidChoices, ValidRange
import openai
from rich import print
from guardrails import Guard
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# command to run the code:
# poetry run python 1_extract_patient_info.py


class Symptom(BaseModel):
    symptom: str = Field(description="Symptom that a patient is experiencing")
    affected_area: str = Field(
        description="What part of the body the symptom is affecting",
    )


class Medication(BaseModel):
    medication: str = Field(
        description="Name of the medication the patient is taking",
    )
    response: str = Field(
        description="How the patient is responding to the medication",
    )


class PatientInfo(BaseModel):
    gender: str = Field(description="Patient's gender")
    age: int = Field(description="Patient's age in years")
    symptoms: List[Symptom] = Field(
        description="Symptoms that the patient is currently experiencing. Each symptom should be classified into a separate item in the list."  # noqa
    )
    current_meds: List[Medication] = Field(
        description="Medications the patient is currently taking and their response"  # noqa
    )


# Doctor notes
doctors_notes = """45 y/o Male with chronic macular rash to face & hair, worse in beard, eyebrows & nares.
Itchy, flaky, slightly scaly. Moderate response to OTC steroid cream."""  # noqa

# Guard prompt
prompt = """
Given the following doctor's notes about a patient, please extract a dictionary that contains the patient's information.

${doctors_notes}

${gr.complete_json_suffix_v2}
"""  # noqa

# Instantiate guard with output schema + prompt
guard = (
    Guard()
    # guard to validate the numeric data in the output
    .use(validator=ValidRange, min=0, max=100, on_fail="fix")
    # Ensures the "affected_area" in symptoms is one of "head", "neck",
    # "chest". If not, it will reask the model.
    .use(
        validator=ValidChoices,
        choices=["head", "neck", "chest"],
        on_fail="reask",
    )
    # Defines output schema and prompt for LLM.
    .from_pydantic(output_class=PatientInfo, prompt=prompt)
)


# Run OpenAI call with Guard validation
res = guard(
    openai.chat.completions.create,
    prompt_params={"doctors_notes": doctors_notes},
    max_tokens=1024,
    temperature=0.3,
)

# Print validated output tree
if guard.history.last and guard.history.last.tree:
    print(guard.history.last.tree)
else:
    print(
        "[bold red]No tree generated. Possible failure in OpenAI response or parsing.[/bold red]"  # noqa
    )
