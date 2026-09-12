"""GENERATED from the niiko action manifest — plan 6c3240a7b22d. Do not edit by hand.

Every method here exists because an action is DECLARED public. If the server answers "not_exposed", this copy
of the SDK is newer than the deployment — not that you got the name wrong.

No dependencies: urllib ships with Python. An SDK that drags an HTTP client along forces whoever installs it
to resolve a version conflict just to send a POST.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from typing import Any, Optional


class NiikoError(Exception):
    """The server answered something that cannot be read. A REFUSAL does not come through here: it is a state."""

    def __init__(self, status: int, body: Any) -> None:
        super().__init__(f"niiko: the server answered {status}")
        self.status = status
        self.body = body


@dataclass
class Result:
    """The three outcomes. Branch once on status and you know where you are.

    done              — done, with output.
    pending_approval  — waits for a human signature; may complete hours later (webhook notification).
    refused           — not done, and reason says why (detail may carry a message saying what to do).
    """

    status: str
    output: Optional[dict[str, Any]] = None
    idempotency_key: Optional[str] = None
    proposal_id: Optional[str] = None
    autonomy: Optional[str] = None
    reason: Optional[str] = None
    detail: Optional[dict[str, Any]] = None


@dataclass
class CreateLeadInput:
    submissionId: str
    source: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    fields: Optional[dict[str, Any]] = None
    consent: Optional[dict[str, Any]] = None


@dataclass
class CreateLeadOutput:
    outcome: str
    clientId: Optional[str]
    reason: Optional[str]


# The reasons miira.lead_create declares. One outside this list is a server fault, not a state.
CREATELEAD_REASONS = ("honeypot", "invalid_email", "disposable_email", "invalid_identity",)


@dataclass
class LoggedCallInput:
    client: str
    summary: str
    followUp: Optional[dict[str, Any]] = None


@dataclass
class LoggedCallOutput:
    clientId: str
    clientName: str
    activityId: str
    followUpId: Optional[str]


# The reasons crm.call_logged declares. One outside this list is a server fault, not a state.
LOGGEDCALL_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_permiso",)


@dataclass
class AssignedOwnerInput:
    client: str
    owner: str


@dataclass
class AssignedOwnerOutput:
    clientId: str
    clientName: str
    ownerUserId: str
    ownerName: str


# The reasons crm.owner_assigned declares. One outside this list is a server fault, not a state.
ASSIGNEDOWNER_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "persona_no_encontrada", "persona_ambigua", "sin_permiso",)


@dataclass
class MovedStageInput:
    client: str
    stage: str
    lostReason: Optional[str] = None


@dataclass
class MovedStageOutput:
    dealId: str
    clientId: str
    clientName: str
    stageName: str
    won: bool
    firstWon: bool


# The reasons crm.stage_moved declares. One outside this list is a server fault, not a state.
MOVEDSTAGE_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_negocio_abierto", "varios_negocios", "etapa_no_encontrada", "negocio_cerrado", "ya_en_esa_etapa", "sin_permiso",)


@dataclass
class ProposedInvoiceInput:
    client: str
    lines: list[dict[str, Any]]
    dueAt: Optional[str] = None
    series: Optional[str] = None


@dataclass
class ProposedInvoiceOutput:
    invoiceId: str
    clientId: str
    clientName: str
    status: str
    subtotalUsd: str
    taxUsd: str
    totalUsd: str
    dueAt: str
    series: str
    issueAt: str


# The reasons kiipu.invoice_proposed declares. One outside this list is a server fault, not a state.
PROPOSEDINVOICE_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_permiso",)


@dataclass
class CreatedTaskInput:
    client: str
    what: str
    dueAt: str


@dataclass
class CreatedTaskOutput:
    clientId: str
    clientName: str
    taskId: str
    dueAt: str


# The reasons crm.task_created declares. One outside this list is a server fault, not a state.
CREATEDTASK_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_permiso",)


@dataclass
class CreatedDealInput:
    client: str
    title: str
    valueUsd: Optional[str] = None
    stage: Optional[str] = None
    owner: Optional[str] = None


@dataclass
class CreatedDealOutput:
    dealId: str
    clientId: str
    clientName: str
    title: str
    valueUsd: Optional[str]
    stageName: str
    ownerName: Optional[str]
    openDeals: int


# The reasons crm.deal_created declares. One outside this list is a server fault, not a state.
CREATEDDEAL_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "etapa_no_encontrada", "etapa_cerrada", "persona_no_encontrada", "persona_ambigua", "sin_permiso",)


@dataclass
class AddedNoteInput:
    client: str
    note: str


@dataclass
class AddedNoteOutput:
    clientId: str
    clientName: str
    noteId: str


# The reasons crm.note_added declares. One outside this list is a server fault, not a state.
ADDEDNOTE_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_permiso",)


@dataclass
class AddedContactInput:
    client: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None


@dataclass
class AddedContactOutput:
    clientId: str
    clientName: str
    contactId: str
    possibleDuplicate: bool


# The reasons crm.contact_added declares. One outside this list is a server fault, not a state.
ADDEDCONTACT_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_permiso",)


@dataclass
class QuotedBroadcastInput:
    clients: list[str]
    message: str
    template: Optional[str] = None
    templateValues: Optional[list[str]] = None


@dataclass
class QuotedBroadcastOutput:
    rows: list[dict[str, Any]]
    totals: dict[str, Any]
    quote: Optional[str]
    expiresAt: Optional[str]


# The reasons miira.broadcast_quoted declares. One outside this list is a server fault, not a state.
QUOTEDBROADCAST_REASONS = ("plantilla_invalida", "tarifas_vencidas", "sin_permiso",)


@dataclass
class SentBroadcastInput:
    quote: str


@dataclass
class SentBroadcastOutput:
    queued: list[dict[str, Any]]
    costUsd: str


# The reasons miira.broadcast_sent declares. One outside this list is a server fault, not a state.
SENTBROADCAST_REASONS = ("presupuesto_invalido", "presupuesto_vencido", "presupuesto_cambiado", "plantilla_invalida", "tarifas_vencidas", "sin_permiso",)


@dataclass
class VoidedDraftInput:
    invoiceId: Optional[str] = None
    client: Optional[str] = None


@dataclass
class VoidedDraftOutput:
    invoiceId: str
    clientId: str
    clientName: str
    totalUsd: str
    status: str


# The reasons kiipu.draft_voided declares. One outside this list is a server fault, not a state.
VOIDEDDRAFT_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "borrador_no_encontrado", "varios_borradores", "no_es_borrador", "sin_permiso",)


@dataclass
class ReportedPaymentInput:
    client: str
    amountUsd: str
    invoice: Optional[str] = None


@dataclass
class ReportedPaymentOutput:
    submissionId: str
    clientId: str
    clientName: str
    invoiceId: str
    invoiceNumber: str
    outstandingUsd: str
    declaredUsd: str
    status: str
    reviewAt: str


# The reasons kiipu.payment_reported declares. One outside this list is a server fault, not a state.
REPORTEDPAYMENT_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_factura_abierta", "varias_facturas", "factura_no_encontrada", "sin_permiso",)


class Niiko:
    def __init__(self, api_key: str, base_url: str = "https://niiko.org") -> None:
        if not api_key:
            raise ValueError("niiko: api_key is required")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    def _exercise(self, action: str, body: dict[str, Any], idempotency_key: Optional[str]) -> Result:
        data = json.dumps({k: v for k, v in body.items() if v is not None}).encode()
        headers = {"authorization": f"Bearer {self._api_key}", "content-type": "application/json"}
        # Send it WHENEVER you can: a timeout retry with the same key does not execute again.
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key

        req = urllib.request.Request(
            f"{self._base_url}/api/v1/actions/{action}", data=data, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                raw = json.loads(resp.read().decode())
                status = resp.status
        except urllib.error.HTTPError as e:
            # A refusal arrives with a 4xx code and a BODY: it is not a client exception, it is a product
            # state. It is read and returned; what does raise is what cannot be read.
            try:
                raw = json.loads(e.read().decode())
            except Exception:
                raise NiikoError(e.code, None) from None
            status = e.code

        if not isinstance(raw, dict) or "status" not in raw:
            raise NiikoError(status, raw)

        return Result(
            status=raw["status"],
            output=raw.get("output"),
            idempotency_key=raw.get("idempotencyKey"),
            proposal_id=raw.get("proposalId"),
            autonomy=raw.get("autonomy"),
            reason=raw.get("reason"),
            detail=raw.get("detail"),
        )

    def create_lead(
        self, input: CreateLeadInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Creates a new lead in the workspace CRM from its contact details. If a matching one already exists it is not duplicated: the reply is `ambiguous` with the candidates.

        miira.lead_create v1 — scope miira.lead_create@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("miira.lead_create", asdict(input), idempotency_key)

    def logged_call(
        self, input: LoggedCallInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Logs what was discussed in a call on a client's record, naming the client; optionally creates the follow-up with its date. Reads nothing and calls no one.

        crm.call_logged v1 — scope crm.call_logged@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.call_logged", asdict(input), idempotency_key)

    def assigned_owner(
        self, input: AssignedOwnerInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Changes who owns a client, naming the client and the team member (by name or email). If either is ambiguous it refuses with the list.

        crm.owner_assigned v1 — scope crm.owner_assigned@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.owner_assigned", asdict(input), idempotency_key)

    def moved_stage(
        self, input: MovedStageInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Moves a client's open deal to another pipeline stage, naming the client and the stage. Creates no deals: with no open deal it refuses, and with several it refuses with the list.

        crm.stage_moved v1 — scope crm.stage_moved@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.stage_moved", asdict(input), idempotency_key)

    def proposed_invoice(
        self, input: ProposedInvoiceInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Prepares an invoice as a DRAFT for a client named by name, with its lines and taxes. Does NOT issue it, does NOT number it and does NOT count as debt: a person reviews and issues it in Kiipu. Does not create the client if it does not exist.

        kiipu.invoice_proposed v1 — scope kiipu.invoice_proposed@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("kiipu.invoice_proposed", asdict(input), idempotency_key)

    def created_task(
        self, input: CreatedTaskInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Creates a reminder (a task with date and time) on a client named by name. Does not log a call: that is crm.call_logged. Does not create the client if it does not exist.

        crm.task_created v1 — scope crm.task_created@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.task_created", asdict(input), idempotency_key)

    def created_deal(
        self, input: CreatedDealInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Opens a new deal in the pipeline for a client named by name, with a title, an optional value in USD, an optional stage (by name; without it, the first one) and an optional owner. Does not check for other open deals: it returns how many remain so a duplicate is visible. Does not win or lose it: that is crm.stage_moved.

        crm.deal_created v1 — scope crm.deal_created@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.deal_created", asdict(input), idempotency_key)

    def added_note(
        self, input: AddedNoteInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Saves a note on a client's record, naming the client: something to know next time, with no call and no date. For a call use crm.call_logged; for a dated reminder, crm.task_created.

        crm.note_added v1 — scope crm.note_added@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.note_added", asdict(input), idempotency_key)

    def added_contact(
        self, input: AddedContactInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Adds a person (name, and optionally email, phone and role) to a client's record, naming the client. Does not make them the primary contact and does not create the client. If someone with that email or phone already existed, the reply says so but does not block it.

        crm.contact_added v1 — scope crm.contact_added@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("crm.contact_added", asdict(input), idempotency_key)

    def quoted_broadcast(
        self, input: QuotedBroadcastInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Quotes sending the SAME WhatsApp message to several clients named by name (up to 50). Sends NOTHING: per client, it says whether the text goes as-is (24-hour window open, free), whether an approved template is needed and what it costs, or why that client cannot be messaged. Returns a signed quote valid for 15 minutes; to send, call miira.broadcast_sent with it. Show the quote to the person first.

        miira.broadcast_quoted v1 — scope miira.broadcast_quoted@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("miira.broadcast_quoted", asdict(input), idempotency_key)

    def sent_broadcast(
        self, input: SentBroadcastInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Sends the WhatsApp broadcast quoted by miira.broadcast_quoted, exactly to whom and how the quote said. If anything changed (window, consent, rate) it refuses with a new quote to confirm again. Costs money when templates are involved: do not call it without the person having seen the cost.

        miira.broadcast_sent v1 — scope miira.broadcast_sent@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("miira.broadcast_sent", asdict(input), idempotency_key)

    def voided_draft(
        self, input: VoidedDraftInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Voids a DRAFT invoice (one created with kiipu.invoice_proposed and not yet issued), by its id or by the client's name when it is their only draft. Does not void issued invoices: that is for a person in Kiipu.

        kiipu.draft_voided v1 — scope kiipu.draft_voided@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("kiipu.draft_voided", asdict(input), idempotency_key)

    def reported_payment(
        self, input: ReportedPaymentInput, idempotency_key: Optional[str] = None
    ) -> Result:
        """Leaves in the Kiipu approval queue the notice that a client (by name) paid a given amount of an open invoice. Does NOT apply the payment and touches no balances: a person checks it against the bank and applies it. If the client has several open invoices the number must be given.

        kiipu.payment_reported v1 — scope kiipu.payment_reported@1.

        Needs TWO permissions: a key with that scope, and the workspace having switched the action on.
        """
        return self._exercise("kiipu.payment_reported", asdict(input), idempotency_key)
