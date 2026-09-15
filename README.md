# ZLSS AI Operating System (ZAIOS)

**ZAIOS** is the ZLSS operating standard for reliable AI-assisted work across research, business, document production, software development, multi-agent collaboration, data governance, verification, and delivery.

> **Current version:** v1.0.1  
> **Status:** Public Working Standard  
> **Primary language:** Traditional Chinese, with key control terms retained in English

## Purpose

ZAIOS is designed to move AI from a conversational tool to an operating system for work that is **executable, verifiable, recoverable, auditable, and transferable**.

Its core operating loop is:

```text
CAPTURE
→ GROUND
→ ROUTE
→ PLAN (when needed)
→ EXECUTE
→ RECORD
→ VERIFY
→ CROSS-CHECK (when needed)
→ DELIVER
→ SYNC / PUBLISH
→ CLOSE
```

## Non-negotiable principles

1. **No fake completion.** If it was not actually done, it must not be reported as done.
2. **Do first.** Clear, executable, authorized work should be performed before optional advice is added.
3. **Minimal change.** Only modify the requested scope; do not expand the work without authorization.
4. **Evidence and traceability.** Important conclusions must be traceable; unknowns must remain explicit.
5. **Delivery is part of completion.** The correct destination, verification, and sync/publish gate must pass.
6. **Research requires three deliverables:** research report, reference materials, and research method.
7. **Google Drive Gate.** When Drive archiving is required, research is not complete until Drive synchronization is verified.

## Research operating standard

Every formal research project must contain at least:

```text
01_研究報告/
02_參考資料/
03_研究方法/
```

The three folders are mandatory when the project uses the ZAIOS Research Operating Standard. If Google Drive is specified as the archival location, Drive synchronization must be verified before the project can be marked complete.

## Core document

The complete current standard is maintained in:

[`ZLSS_AI_Operating_System_v1.0.1.md`](./ZLSS_AI_Operating_System_v1.0.1.md)

## Design coverage score

**ZAIOS v1.0.1 Design Coverage Score: 96/100 (9.6/10)**

This score uses the same 10-category, 100-point design-coverage rubric across the compared workflows. It is a **design-coverage assessment**, not an independent performance benchmark or third-party certification.

## Scope

ZAIOS covers:

- task routing and right-sized process;
- source-of-truth governance;
- planning and specification;
- durable state and recovery;
- multi-agent orchestration;
- verification and evidence;
- human-in-the-loop and risk gates;
- research and source governance;
- artifact lifecycle and handoff;
- GitHub / Google Drive / external synchronization gates;
- versioning and definition of done.

## Versioning

ZAIOS uses semantic-style versioning:

```text
MAJOR.MINOR.PATCH
```

- **MAJOR** — incompatible governance changes
- **MINOR** — backward-compatible capability additions
- **PATCH** — wording, clarification, and minor corrections

## Final principle

> AI creates value not by producing more answers, but by reliably completing authorized work, leaving evidence, and enabling the next person or agent to continue without loss of context.

---

**Repository:** `zlss20240168-ESG/ZLSS-AI-Operating-System`  
**Current release document:** `ZLSS_AI_Operating_System_v1.0.1.md`
