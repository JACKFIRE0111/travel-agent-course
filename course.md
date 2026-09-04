# Context Engineering for Reliable LLM Apps

**Format:** 2 lessons · ~90 minutes total · text only  
**Capstone:** a travel-planning assistant that handles ambiguous requests through a
controlled two-step context pipeline.

## Course goal

By the end of this course, the learner can design an LLM workflow that preserves the
important parts of a user request, detects missing information, asks for clarification,
and explicitly assembles the context for a final generation step.

The learner is not trying to write a clever prompt. The goal is to make the application's
**context flow observable and reliable**.

---

# Lesson 1 — Find the missing context

## Section 1 — Why a plausible answer can still be wrong

A model can produce a fluent answer from an underspecified request. That is exactly the
problem: fluency hides missing information.

Consider:

> "Plan three days in Tokyo. I like food and culture."

"Food and culture" could mean street food, fine dining, traditional cuisine, museums,
temples, architecture, nightlife, or several combinations. A useful system should not
silently choose one interpretation when the choice changes the itinerary.

**Checkpoint:** Given an underspecified request, identify the information that would
materially change the answer.

## Section 2 — Breakpoints in the workflow

There are three common breakpoints:

1. **Ambiguous intent** — the system does not know which interpretation the user means.
2. **Lost state** — the second step forgets information supplied in the first step.
3. **Unbounded context** — irrelevant history is passed along, making the next step harder
   to control.

The practical move is to name the breakpoint before writing the prompt.

**Checkpoint:** For a travel assistant, name at least three pieces of context that must
survive from the first interaction to the final itinerary.

## Section 3 — Turn breakpoints into checkpoints

A checkpoint is observable. "Understand context better" is not a checkpoint.

A useful checkpoint is:

> "Given an ambiguous interest, the application asks one clarification question and
> offers two or three interpretations."

That is testable. You can run the application and see whether it happened.

**Checkpoint:** Write one observable success condition for ambiguity handling.

## Section 4 — Build-along: a controlled clarification step

Start with a minimal Python application that collects destination, number of days, and
interests. Send those fields to the model.

Then add one rule:

- If the request is ambiguous, ask one concise clarification question.
- Do not generate the final itinerary yet.

The application should preserve the original values in variables. Do not ask the model
to remember them implicitly.

### Build-along 1 artifact

A first-response travel agent that either produces a plan or stops for clarification.

**Time target:** 15–20 minutes.

---

# Lesson 2 — Assemble context for the final call

## Section 1 — The second call is a new context boundary

After clarification, the application has two sources of information:

- the original request;
- the user's clarification.

Treat them as explicit inputs to the final model call.

This is safer than relying on the model to reconstruct the conversation from an
unstructured transcript.

**Checkpoint:** List the exact fields the final call needs.

## Section 2 — Preserve signal, not everything

More context is not automatically better context.

For this capstone, the final call needs:

- destination;
- number of days;
- original interest;
- clarification.

It does not need unrelated terminal output, implementation details, or every previous
sentence.

**Checkpoint:** Given a conversation history, remove three pieces of information that do
not belong in the final planning context.

## Section 3 — Make the workflow explicit

The application now has a simple state machine:

```text
USER INPUT
    |
    v
FIRST MODEL CALL
    |
    +---- clear ----> FINAL PLAN
    |
    +---- ambiguous -> CLARIFICATION
                         |
                         v
                  CONTEXT ASSEMBLY
                         |
                         v
                  SECOND MODEL CALL
                         |
                         v
                     FINAL PLAN
```

The important engineering property is not the diagram itself. It is that each transition
has a defined input and output.

**Checkpoint:** Explain what data crosses the clarification boundary and why.

## Section 4 — Build-along: the final context pipeline

Extend the first build-along with a second model call.

The second prompt should contain the original request and the clarification as explicit
fields. Ask for:

1. a day-by-day itinerary;
2. main attractions;
3. food recommendations;
4. practical travel tips.

Keep the final output concise and realistic.

### Build-along 2 artifact

A working two-step travel agent whose final answer is produced only after the required
context is available.

**Time target:** 15–20 minutes.

---

# Capstone — Test the context boundary

Run at least two cases.

### Case A: ambiguous

Input:

- Destination: Tokyo
- Days: 3
- Interests: food and culture

The first response should ask for clarification rather than immediately committing to one
interpretation.

Then answer the clarification and inspect the final itinerary.

### Case B: clear

Input:

- Destination: Chicago
- Days: 2
- Interests: architecture, steak, and museums

The application should be able to proceed directly.

## Capstone success criteria

A submission passes when:

- the original request is preserved;
- ambiguous intent triggers a clarification step;
- the clarification is explicitly included in the final context;
- the final answer follows the requested structure;
- the workflow is understandable without hidden state.

The lesson is deliberately small. The learner leaves with a reusable pattern:

**detect missing context → ask for it → assemble only the needed context → generate.**
