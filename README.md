# Insurance Claim Analyzer

An experimental, agent-based insurance claim review pipeline. The application collects claim data and evidence, analyzes submitted images, and performs a secondary review that produces an approval decision.

## Pipeline

The executable flow in `main.py` is:

1. **DataAgent** uses a Groq model and LangChain tools to collect:
	- evidence requirements from `data/evidence_requirements.csv`
	- user history from `data/user_history.csv`
	- image paths from `data/images/<user_id>/`
2. **AnalysisAgent** uploads the images to Google Gemini and returns structured image-analysis data.
3. **ReviewAgent** sends the claim analysis to a second Groq model and returns a structured decision:
	- `Approved`
	- `Rejected`
	- `Human Intervention`

The current example uses `user_001` and a hard-coded car-damage claim in `main.py`.

## Requirements

- Python 3.14 or newer, as specified in `pyproject.toml`
- A Groq API key
- A Google Generative AI API key
- An NVIDIA API key (required by the current settings model, although the sample flow does not use the NVIDIA model)

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Alternatively, install the project using the `pyproject.toml` dependency list:

```powershell
pip install -e .
```

Create a `.env` file in the project root:

```dotenv
GROQ_API_KEY=your_groq_api_key
GL_GEN_AI_API_KEY=your_google_generative_ai_api_key
NV_KIMI_K3_API_KEY=your_nvidia_api_key
```

The settings loader reads this file from the current working directory and exports the keys as `GROQ_API_KEY`, `GOOGLE_API_KEY`, and `NVIDIA_API_KEY` for the model clients.

## Run

Run the sample claim from the project root:

```powershell
python main.py
```

The program prints the collected user data, the analyzer output, and the final review result.

## Project Layout

```text
.
|-- main.py                         # Sample pipeline entry point
|-- pyproject.toml                  # Project metadata and dependencies
|-- requirements.txt                # Pip dependency list
|-- data/
|   |-- evidence_requirements.csv   # Evidence rules by claim type
|   |-- user_history.csv            # Historical claim records
|   `-- images/<user_id>/           # Claim images for each user
`-- src/
	 |-- agents/                     # Data, analysis, and review agents
	 |-- config/                     # Environment-backed settings
	 |-- models/                     # Pydantic structured-output models
	 |-- prompts/                    # Agent system prompts
	 `-- tools/                      # CSV and image lookup tools
```

## Data Conventions

Each image directory must be named with the corresponding `user_id`, for example:

```text
data/images/user_001/claim-front.jpg
data/images/user_001/claim-rear.png
```

The image lookup tool scans the user directory and returns the discovered paths. Supported review image extensions are `.png`, `.jpg`, `.jpeg`, and `.webp`.

## Structured Models

The Pydantic models in `src/models/models.py` define the main contracts:

- `UserData`: collected claim, history, evidence requirements, and image paths
- `AnalysisData`: image validity, damage classification, evidence sufficiency, risk flags, and claim status
- `ReviewData`: discrepancies, final decision, and review reason

## Notes

- `AnalysisAgent` uses `gemini-2.5-flash` by default.
- `DataAgent` uses `openai/gpt-oss-120b` through Groq by default.
- `ReviewAgent` uses `qwen/qwen3.8-27b` through Groq by default.
- Review image data URLs must use standard Base64 encoding (`base64.b64encode`), not Base85.
- The project is a prototype and does not expose an HTTP API or persist decisions to a database.
