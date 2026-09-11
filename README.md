# niiko — SDK de Python

> Cliente **generado** de la API de acciones de niiko. No se edita a mano: sale del manifiesto de acciones, en
> la misma corrida que el otro cliente y que la referencia. Plan `9a8b80d285ff`.

```bash
pip install niiko
```

```python
import os, uuid
from niiko import Niiko, CreateLeadInput

niiko = Niiko(api_key=os.environ["NIIKO_API_KEY"])

r = niiko.create_lead(
    CreateLeadInput(
    submissionId="01890a5d-ac96-774b-bcce-b302099a8057",
    source="web_form",
    ),
    idempotency_key=str(uuid.uuid4()),
)

if r.status == "done":
    print(r.output)
elif r.status == "refused":
    print(r.reason)
```

## Lo que este cliente **no** hace

**No valida tu input.** Podría —el esquema está publicado— y sería peor: un cliente que valida es un cliente
que puede discrepar del servidor, y la dirección probable del error es la peligrosa (aprueba lo que el servidor
va a rechazar). El servidor valida, y su negativa viaja con nombre. Lo que este cliente aporta es la **forma**:
qué campos hay, cuáles son obligatorios y qué te puede contestar, en tu editor, antes de mandar nada.

## Tres desenlaces, no dos

| `status` | qué significa |
|---|---|
| `done` | Hecho. Trae el `output`. |
| `pending_approval` | **Queda esperando una firma humana** y puede terminar horas después. Te avisamos por webhook. |
| `refused` | No se hizo, y `reason` dice por qué. |

Un contrato de dos desenlaces obliga a que el tercero se disfrace de otro, y el que se disfraza siempre es el
que más se tarda en entender.

## Idempotencia

Manda una clave de idempotencia con cada encargo. Un reintento por timeout con la misma clave **no vuelve a
ejecutar**: contesta `refused` con `reason: "duplicate"` y lo que pasó la primera vez. Sin ella, un reintento
es un encargo nuevo. La protección dura 24 horas.

## Dos permisos, no uno

Una clave con el alcance de la acción, **y** que el dueño del workspace la haya encendido. Tener la clave no
basta: son dos decisiones distintas y las toma gente distinta.

## Referencia

**[developers.niiko.org](https://developers.niiko.org)** — la referencia completa, generada en la misma corrida
que este cliente.

## Licencia

Apache-2.0.

---

Hecho por **[Vorluno](https://vorluno.dev)** — un estudio de software de Panamá.
