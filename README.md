# Guardrails AI

## Description

This repository contains examples of Guardrails AI. 

## Installation

To install the required dependencies, you can use Poetry. First, make sure you have Poetry installed on your system. Then, navigate to the root directory of this project and run:

```bash
poetry install
```

This will install all the required dependencies specified in the `pyproject.toml` file.

## Dependencies

- **Python**: >=3.8.1,<4.0
- **NLTK**: *
- **Spacy-Transformers**: ^1.3.4 (optional)
- **Guardrails-AI**: ^0.4.0
- **Transformers**: ^4.18.0 
- **Pydantic**: *

## OpenAI Configuration Steps

To configure OpenAI's GPT, follow these steps:

1. **Sign Up for OpenAI**: If you haven't already, sign up for an account on the OpenAI platform.
2. **Get API Key**: Once you have an account, navigate to the API section and generate an API key.
3. **Configure Environment Variable**: Set up an environment variable to store your API key. In your terminal, run:

    ```bash
    export OPENAI_API_KEY=your-api-key
    ```

    Replace `your-api-key` with the API key you obtained from OpenAI.


## Running Programs

To run the programs, navigate to the root directory of this project and run following commands:

```bash
poetry run python <python file name>
poetry run python .\1_extract_patient_info.py 
poetry run python .\2_competitor_checks.py 
poetry run python .\3_chaining_validators.py 
poetry run python .\4_custom_validator.py 
```
