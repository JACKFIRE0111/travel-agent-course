# Context Engineering for Reliable LLM Apps
## EducationPals — AI Engineer Intern take-home

This submission uses a **travel-planning assistant** as the capstone for a short course on
context engineering.

The central idea is simple: a good LLM application does not rely on one giant prompt.
It preserves the user's state, detects ambiguity, asks for the missing information, and
then supplies the clarified context to the next model call.

### Repository

```text
travel-agent-course/
├── app.py
├── course.md
├── prompts.md
├── requirements.txt
├── .env.example
├── fixtures/
│   ├── first_response.txt
│   └── final_response.txt
└── output/
    ├── first_run.txt
    └── final_run.txt
```

### Run the review version — no API call

Python 3.12 is required.

```bash
python --version
pip install -r requirements.txt
python app.py --offline
```

`--offline` replays the checked-in fixtures. It does **not** require an API key and does
not make a paid API call.

### Run the live version

```bash
cp .env.example .env
# add OPENAI_API_KEY to .env
pip install -r requirements.txt
python app.py
```

The live version uses the OpenAI Responses API. The model can be changed without editing
the application:

```text
OPENAI_MODEL=gpt-5.6-luna
```

### What the capstone demonstrates

1. **State preservation** — destination, duration, and original interest are retained.
2. **Ambiguity handling** — the first call can stop and ask for one clarification.
3. **Context assembly** — the second call receives the original request plus the new
   clarification instead of relying on conversational memory outside the application.
4. **A bounded workflow** — the application has an explicit first-call / clarification /
   final-call path.
5. **Offline reproducibility** — the reviewer can execute the checked-in fixtures without
   making an API request.

### Course design

The course contains two lessons and takes about 90 minutes for a learner. Each lesson
has a build-along, and the artifacts compound into the final travel agent.

See `course.md` for the learner-facing course and `prompts.md` for the generation setup.
