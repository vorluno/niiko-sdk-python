"""GENERADO desde el manifiesto de acciones de niiko — plan 9a8b80d285ff. No editar a mano.

Cada metodo de aqui existe porque una accion esta DECLARADA como publica. Si el servidor contesta
"not_exposed", es que esta copia del SDK es mas nueva que el despliegue — no que te equivocaste de nombre.

Sin dependencias: urllib viene con Python. Un SDK que arrastra un cliente HTTP obliga a quien lo instala a
resolver un conflicto de versiones para mandar un POST.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from typing import Any, Optional


class NiikoError(Exception):
    """El servidor contesto algo que no se puede leer. Una NEGATIVA no llega por aqui: es un estado."""

    def __init__(self, status: int, cuerpo: Any) -> None:
        super().__init__(f"niiko: el servidor contesto {status}")
        self.status = status
        self.cuerpo = cuerpo


@dataclass
class Resultado:
    """Los tres desenlaces. Se ramifica una vez por status y ya sabes donde estas.

    done              — hecho, con output.
    pending_approval  — espera una firma humana; puede terminar horas despues (aviso por webhook).
    refused           — no se hizo, y reason dice por que.
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


# Los motivos que miira.lead_create declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.call_logged declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.owner_assigned declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.stage_moved declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que kiipu.invoice_proposed declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.task_created declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.deal_created declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.note_added declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que crm.contact_added declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que miira.broadcast_quoted declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
QUOTEDBROADCAST_REASONS = ("plantilla_invalida", "tarifas_vencidas", "sin_permiso",)


@dataclass
class SentBroadcastInput:
    quote: str


@dataclass
class SentBroadcastOutput:
    queued: list[dict[str, Any]]
    costUsd: str


# Los motivos que miira.broadcast_sent declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que kiipu.draft_voided declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
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


# Los motivos que kiipu.payment_reported declara. Uno fuera de esta lista es un fallo del servidor, no un estado.
REPORTEDPAYMENT_REASONS = ("cliente_no_encontrado", "cliente_ambiguo", "demasiados_clientes", "sin_factura_abierta", "varias_facturas", "factura_no_encontrada", "sin_permiso",)


class Niiko:
    def __init__(self, api_key: str, base_url: str = "https://niiko.org") -> None:
        if not api_key:
            raise ValueError("niiko: falta api_key")
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    def _ejercer(self, accion: str, cuerpo: dict[str, Any], idempotency_key: Optional[str]) -> Resultado:
        datos = json.dumps({k: v for k, v in cuerpo.items() if v is not None}).encode()
        cabeceras = {"authorization": f"Bearer {self._api_key}", "content-type": "application/json"}
        # Mandala SIEMPRE que puedas: un reintento por timeout con la misma clave no vuelve a ejecutar.
        if idempotency_key:
            cabeceras["idempotency-key"] = idempotency_key

        req = urllib.request.Request(
            f"{self._base_url}/api/v1/actions/{accion}", data=datos, headers=cabeceras, method="POST"
        )
        try:
            with urllib.request.urlopen(req) as resp:
                crudo = json.loads(resp.read().decode())
                estado = resp.status
        except urllib.error.HTTPError as e:
            # Una negativa llega con codigo 4xx y CUERPO: no es una excepcion del cliente, es un estado del
            # producto. Se lee y se devuelve; lo que si revienta es lo que no se puede leer.
            try:
                crudo = json.loads(e.read().decode())
            except Exception:
                raise NiikoError(e.code, None) from None
            estado = e.code

        if not isinstance(crudo, dict) or "status" not in crudo:
            raise NiikoError(estado, crudo)

        return Resultado(
            status=crudo["status"],
            output=crudo.get("output"),
            idempotency_key=crudo.get("idempotencyKey"),
            proposal_id=crudo.get("proposalId"),
            autonomy=crudo.get("autonomy"),
            reason=crudo.get("reason"),
            detail=crudo.get("detail"),
        )

    def create_lead(
        self, entrada: CreateLeadInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Crea un lead nuevo en el CRM del workspace a partir de sus datos de contacto. Si ya existe uno que encaja, no lo duplica: contesta `ambiguous` con los candidatos.

        miira.lead_create v1 — alcance miira.lead_create@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("miira.lead_create", asdict(entrada), idempotency_key)

    def logged_call(
        self, entrada: LoggedCallInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Anota en la ficha de un cliente, dicho por su nombre, lo que se habló en una llamada; opcionalmente deja creado el seguimiento con su fecha. No lee nada ni llama a nadie.

        crm.call_logged v1 — alcance crm.call_logged@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.call_logged", asdict(entrada), idempotency_key)

    def assigned_owner(
        self, entrada: AssignedOwnerInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Cambia de quién es un cliente, diciendo el nombre del cliente y el nombre (o correo) del miembro del equipo. Si alguno de los dos es ambiguo, se niega con la lista.

        crm.owner_assigned v1 — alcance crm.owner_assigned@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.owner_assigned", asdict(entrada), idempotency_key)

    def moved_stage(
        self, entrada: MovedStageInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Mueve el negocio abierto de un cliente a otra etapa del pipeline, diciendo el nombre del cliente y el de la etapa. No crea negocios: sin uno abierto se niega, y con varios se niega con la lista.

        crm.stage_moved v1 — alcance crm.stage_moved@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.stage_moved", asdict(entrada), idempotency_key)

    def proposed_invoice(
        self, entrada: ProposedInvoiceInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Deja preparada una factura como BORRADOR para un cliente dicho por su nombre, con sus líneas e impuestos. NO la emite, NO la numera y NO cuenta como deuda: una persona la revisa y la emite en Kiipu. No crea el cliente si no existe.

        kiipu.invoice_proposed v1 — alcance kiipu.invoice_proposed@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("kiipu.invoice_proposed", asdict(entrada), idempotency_key)

    def created_task(
        self, entrada: CreatedTaskInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Crea un recordatorio (tarea con fecha y hora) sobre un cliente dicho por su nombre. No anota una llamada: para eso está crm.call_logged. No crea el cliente si no existe.

        crm.task_created v1 — alcance crm.task_created@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.task_created", asdict(entrada), idempotency_key)

    def created_deal(
        self, entrada: CreatedDealInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Abre un negocio nuevo en el pipeline para un cliente dicho por su nombre, con título, valor opcional en USD, etapa opcional (por nombre; sin ella, la primera) y responsable opcional. No comprueba si ya tiene otros abiertos: devuelve cuántos quedan para que se vea un duplicado. No lo gana ni lo pierde: eso es crm.stage_moved.

        crm.deal_created v1 — alcance crm.deal_created@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.deal_created", asdict(entrada), idempotency_key)

    def added_note(
        self, entrada: AddedNoteInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Guarda una nota en la ficha de un cliente dicho por su nombre: algo que hay que saber la próxima vez, sin llamada ni fecha. Para una llamada está crm.call_logged; para un recordatorio con fecha, crm.task_created.

        crm.note_added v1 — alcance crm.note_added@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.note_added", asdict(entrada), idempotency_key)

    def added_contact(
        self, entrada: AddedContactInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Añade una persona (nombre, y opcionalmente correo, teléfono y cargo) a la ficha de un cliente dicho por su nombre. No la hace contacto principal ni crea el cliente. Si ya había alguien con ese correo o teléfono, lo dice en la respuesta pero no lo impide.

        crm.contact_added v1 — alcance crm.contact_added@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("crm.contact_added", asdict(entrada), idempotency_key)

    def quoted_broadcast(
        self, entrada: QuotedBroadcastInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Presupuesta mandar el MISMO mensaje de WhatsApp a varios clientes dichos por su nombre (hasta 50). NO envía nada: dice, por cliente, si le llega el texto tal cual (ventana de 24 h abierta, gratis), si hace falta una plantilla aprobada y cuánto cuesta, o por qué no se le puede escribir. Devuelve un presupuesto firmado que vale 15 minutos; para enviar, llama a miira.broadcast_sent con él. Enséñale el presupuesto a la persona antes.

        miira.broadcast_quoted v1 — alcance miira.broadcast_quoted@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("miira.broadcast_quoted", asdict(entrada), idempotency_key)

    def sent_broadcast(
        self, entrada: SentBroadcastInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Envía la difusión de WhatsApp presupuestada por miira.broadcast_quoted, exactamente a quienes y como dijo el presupuesto. Si algo cambió (ventana, consentimiento, tarifa) se niega con el presupuesto nuevo para confirmarlo otra vez. Cuesta dinero cuando hay plantillas: no lo llames sin que la persona haya visto el coste.

        miira.broadcast_sent v1 — alcance miira.broadcast_sent@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("miira.broadcast_sent", asdict(entrada), idempotency_key)

    def voided_draft(
        self, entrada: VoidedDraftInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Anula un BORRADOR de factura (uno creado con kiipu.invoice_proposed y todavía no emitido), por su id o por el nombre del cliente si es su único borrador. No anula facturas emitidas: eso es de una persona en Kiipu.

        kiipu.draft_voided v1 — alcance kiipu.draft_voided@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("kiipu.draft_voided", asdict(entrada), idempotency_key)

    def reported_payment(
        self, entrada: ReportedPaymentInput, idempotency_key: Optional[str] = None
    ) -> Resultado:
        """Deja en la cola de aprobación de Kiipu el aviso de que un cliente (por su nombre) pagó cierto monto de una factura abierta. NO aplica el pago ni toca saldos: una persona lo revisa contra el banco y lo aplica. Si el cliente tiene varias facturas abiertas hay que decir el número.

        kiipu.payment_reported v1 — alcance kiipu.payment_reported@1.

        Necesita DOS permisos: una clave con ese alcance, y que el workspace haya encendido la accion.
        """
        return self._ejercer("kiipu.payment_reported", asdict(entrada), idempotency_key)
