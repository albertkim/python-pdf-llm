# Python PDF LLM Analyzer

I'm perpetually on the lookout for the best ways to mass parse PDFs. After playing with various non-vision based PDF parsers, I've determined that they are not good enough if you are dealing PDFs of various formats - photos, scans, text-based, and more.

This repository is a Python tool that I use to evaluate LLM performance.

### .env setup

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
XAI_API_KEY=
DEEPSEEK_API_KEY=
```

### How it works

- Uses the OpenAI SDK as the main SDK to connect to other services
- Stores pdf/image files in the `/data` directory
- All functions are written to be async-first

### Using Poetry

If you are new to poetry (like I am), these are the key commands you need to know.

1. Download and install Poetry
2. `poetry install` will install dependencies in `pyproject.toml` (not `requirements.txt`)
3. `poetry add {dependency}` to install a new dependency

Note that the dependencies are tracked in `pyproject.toml`, not a `requirements.txt`.

BONUS: If you are starting a new project and you want to initialize Poetry in your project, `cd` into it and run `poetry init` (of course, assuming have Poetry installed)
