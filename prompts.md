# AI generation setup

The take-home asks for the course and build-alongs to be generated with AI. These are the
prompts used to generate the learner-facing material.

## Course-generation prompt

```text
You are an instructional designer and AI engineer.

Create a two-lesson, approximately 90-minute, text-only course on context engineering
for reliable LLM applications.

Capstone: a Python travel-planning assistant.

Requirements:
- Work backward from the capstone.
- Before writing lesson prose, identify at least three real learner breakpoints.
- Turn each breakpoint into an observable checkpoint.
- Use two lessons.
- Each lesson has no more than five sections.
- Each section is designed for roughly 2–3 minutes / 300–500 words.
- Include exactly one build-along at the end of each lesson.
- Each build-along should produce a small artifact under 20 minutes.
- Lesson 1's artifact must become Lesson 2's input.
- Lesson 2's artifact must complete the capstone.
- Prioritize practical context flow over prompt-writing tricks.
- Use text only.
- Include a compact state-flow diagram using plain text.
- Avoid video/audio requirements.
```

## Build-along generation prompt

```text
Generate a small Python build-along for the course capstone.

The artifact must:
- collect destination, duration, and interests;
- call an LLM;
- stop for clarification when interests are ambiguous;
- preserve the original user state;
- use a second call after clarification;
- explicitly assemble the final context;
- produce a concise travel plan.

Keep the implementation small enough to build in under 20 minutes.
Do not introduce a web framework, database, vector database, or unnecessary dependency.
```

## Quality-review prompt

```text
Review this course as if you were hiring an AI engineer.

Reject it if:
- the lessons are generic LLM explanations;
- checkpoints are not observable;
- build-alongs do not compound;
- the capstone does not test the lesson's core concept;
- the second model call relies on hidden conversation state;
- the learner cannot complete the course in about 90 minutes.

Suggest only changes that improve those criteria.
```

## Orchestration

The generation process is intentionally staged:

1. identify breakpoints;
2. define observable checkpoints;
3. design the capstone backward;
4. generate lesson containers around the checkpoints;
5. generate the build-alongs;
6. review for time, compounding, and testability;
7. freeze the learner-facing course in `course.md`.

The checked-in prompts make the generation process inspectable rather than presenting only
the polished output.
