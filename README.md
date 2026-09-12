# niiko

The Python client for the niiko actions API. One typed method per action, three outcomes, zero dependencies.

[![pypi](https://img.shields.io/pypi/v/niiko?style=flat-square&color=0969da)](https://pypi.org/project/niiko/) [![python](https://img.shields.io/badge/python-%3E%3D3.10-2C6440?style=flat-square)](https://www.python.org) ![dependencies](https://img.shields.io/badge/dependencies-0-2C6440?style=flat-square) ![license](https://img.shields.io/badge/license-Apache--2.0-0969da?style=flat-square) [![generated](https://img.shields.io/badge/generated_from_plan-6c3240a7b22d-555?style=flat-square)](https://developers.niiko.org)

**A client that knows the actions it was written for is stale the day a new one opens.** This one is
generated from the niiko action manifest, in the same run as the TypeScript client and the reference (plan `6c3240a7b22d`),
so an action that opens on the server appears here as a typed method at once — and nothing in this repository
is edited by hand.

## Install

```bash
pip install niiko
```

Zero runtime dependencies. A client that drags an HTTP library along forces whoever installs it to resolve a
version conflict just to send a POST.

## Use

```python
import os, uuid
from niiko import Niiko, CreateLeadInput

niiko = Niiko(api_key=os.environ["NIIKO_API_KEY"])

r = niiko.create_lead(
    CreateLeadInput(
    submissionId="01890a5d-ac96-774b-bcce-b302099a8057",
    source="web_form",
    ),
    idempotency_key=str(uuid.uuid4()),  # keep it if you retry
)

if r.status == "done":
    print(r.output)
elif r.status == "refused":
    print(r.reason, (r.detail or {}).get("message"))
```

## Three outcomes, not two

| `status` | Meaning |
|---|---|
| `done` | Done. Carries the `output`. |
| `pending_approval` | **Waits for a human signature** and may complete hours later. A webhook tells you when it resolves. |
| `refused` | Not done, and `reason` says why. `detail.message`, when present, says what to do. |

A two-outcome contract forces the third one to disguise itself as another, and the disguised one is always
the one that takes longest to understand. Branch once on `status`; a refusal is a state, not an exception.

> [!NOTE]
> Send an idempotency key with every request. A timeout retry with the same key **does not execute again**: it
> answers `refused` with `reason: "duplicate"` and what happened the first time. Without one, a retry is a new
> request. The protection lasts 24 hours.

> [!IMPORTANT]
> Each action needs **two** permissions: a key with that action's scope, **and** the workspace owner having
> switched it on (Administration → Permissions). Holding the key is not enough — they are two decisions made
> by different people.

## The actions today (13)

| Action | Method | What it does |
|---|---|---|
| `miira.lead_create` | `create_lead` | Creates a new lead in the workspace CRM from its contact details. If a matching one already exists it is not duplicated: the reply is `ambiguous` with the candidates. |
| `crm.call_logged` | `logged_call` | Logs what was discussed in a call on a client's record, naming the client; optionally creates the follow-up with its date. Reads nothing and calls no one. |
| `crm.owner_assigned` | `assigned_owner` | Changes who owns a client, naming the client and the team member (by name or email). If either is ambiguous it refuses with the list. |
| `crm.stage_moved` | `moved_stage` | Moves a client's open deal to another pipeline stage, naming the client and the stage. Creates no deals: with no open deal it refuses, and with several it refuses with the list. |
| `kiipu.invoice_proposed` | `proposed_invoice` | Prepares an invoice as a DRAFT for a client named by name, with its lines and taxes. Does NOT issue it, does NOT number it and does NOT count as debt: a person reviews and issues it in Kiipu. Does not create the client if it does not exist. |
| `crm.task_created` | `created_task` | Creates a reminder (a task with date and time) on a client named by name. Does not log a call: that is crm.call_logged. Does not create the client if it does not exist. |
| `crm.deal_created` | `created_deal` | Opens a new deal in the pipeline for a client named by name, with a title, an optional value in USD, an optional stage (by name; without it, the first one) and an optional owner. Does not check for other open deals: it returns how many remain so a duplicate is visible. Does not win or lose it: that is crm.stage_moved. |
| `crm.note_added` | `added_note` | Saves a note on a client's record, naming the client: something to know next time, with no call and no date. For a call use crm.call_logged; for a dated reminder, crm.task_created. |
| `crm.contact_added` | `added_contact` | Adds a person (name, and optionally email, phone and role) to a client's record, naming the client. Does not make them the primary contact and does not create the client. If someone with that email or phone already existed, the reply says so but does not block it. |
| `miira.broadcast_quoted` | `quoted_broadcast` | Quotes sending the SAME WhatsApp message to several clients named by name (up to 50). Sends NOTHING: per client, it says whether the text goes as-is (24-hour window open, free), whether an approved template is needed and what it costs, or why that client cannot be messaged. Returns a signed quote valid for 15 minutes; to send, call miira.broadcast_sent with it. Show the quote to the person first. |
| `miira.broadcast_sent` | `sent_broadcast` | Sends the WhatsApp broadcast quoted by miira.broadcast_quoted, exactly to whom and how the quote said. If anything changed (window, consent, rate) it refuses with a new quote to confirm again. Costs money when templates are involved: do not call it without the person having seen the cost. |
| `kiipu.draft_voided` | `voided_draft` | Voids a DRAFT invoice (one created with kiipu.invoice_proposed and not yet issued), by its id or by the client's name when it is their only draft. Does not void issued invoices: that is for a person in Kiipu. |
| `kiipu.payment_reported` | `reported_payment` | Leaves in the Kiipu approval queue the notice that a client (by name) paid a given amount of an open invoice. Does NOT apply the payment and touches no balances: a person checks it against the bank and applies it. If the client has several open invoices the number must be given. |

## What this client does not do

| Not included | Why |
|---|---|
| **Validate your input** | It could — the schema is published — and that would be worse: a client that validates can disagree with the server, and the likely direction of the error is the dangerous one (approving what the server will reject). The server validates, and its refusal travels with a name. What this client gives you is the **shape**, in your editor, before sending anything. |
| **Read anything** | This API exposes verbs, not rows. There is nothing to list or paginate. |
| **Retry on its own** | A retry is a decision about your idempotency key. The client keeps it explicit. |

## Support

| | |
|---|---|
| **Versioning** | Semantic. Every visible change is in the [changelog](https://developers.niiko.org/#changelog) of the API reference. |
| **Regeneration** | This repository is generated from the niiko action manifest. When an action opens or a contract changes, a new version is published — nothing here is edited by hand. |
| **Issues** | [vorluno/niiko-sdk-python/issues](https://github.com/vorluno/niiko-sdk-python/issues) — a fault of the API itself starts at [developers.niiko.org](https://developers.niiko.org). |
| **Security** | `security@vorluno.dev` — first response within 48 hours, patch or plan within 7 days. |

## Related

- **[@vorluno/niiko-sdk](https://github.com/vorluno/niiko-sdk-typescript)** — the TypeScript client, same plan.
- **[niiko-cli](https://github.com/vorluno/niiko-cli)** — the same actions from the terminal, with the outcome in the exit code.
- **[n8n-nodes-niiko](https://github.com/vorluno/n8n-nodes-niiko)** — the same actions as an n8n node.
- **[niiko-mcp-server](https://github.com/vorluno/niiko-mcp-server)** — the same actions as MCP tools, for Claude and other AI clients.
- **[developers.niiko.org](https://developers.niiko.org)** — the API reference this is generated alongside.

<sub>Built and maintained by <a href="https://vorluno.dev">Vorluno</a>, a software studio in Panama, and generated from <a href="https://niiko.org">niiko</a>'s production action manifest — the same one the server enforces. Apache 2.0.</sub>
