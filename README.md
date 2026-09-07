# VIP Registration Desk

A FastAPI code quiz solution: two endpoints demonstrating header/cookie
parameter models, response model filtering, and status codes.

## Endpoints

### `POST /staff` — register a VIP staff member

**Headers** (required together, declared as one model):
| Header | Required | Default |
|---|---|---|
| `X-Union-Pass` | yes | — |
| `X-Client-Version` | no | `"1.0"` |

**Body:**
```json
{
  "username": "amaka.eze",
  "full_name": "Amaka Eze",
  "password": "unionpass2026",
  "station": "VIP Front Desk"
}
```

**Behavior:**
- Missing `X-Union-Pass` → `422`
- `X-Union-Pass` present but wrong → `401`, `{"detail": "Wrong pass."}`
- `password` under 8 characters → `422`
- Valid request → `201`, staff member returned **without** `password`

### `GET /desk/greeting` — greet a returning visitor

**Cookies** (declared as one model):
| Cookie | Required | Default |
|---|---|---|
| `session_id` | yes | — |
| `language` | no | `"en"` |

**Behavior:**
- Missing `session_id` cookie → `422`
- `language=en` → `"Welcome back!"`
- `language=pidgin` → `"How far, you don come again!"`
- anything else → `"Welcome!"`

## Setup

```bash
uv add --dev fastapi pydantic "uvicorn[standard]" pytest httpx
uv run fastapi dev
```

Interactive docs: http://127.0.0.1:8000/docs

## Testing

```bash
uv run pytest test_main.py -v
```

Or by hand from a terminal (Swagger can't set cookies for you):
```bash
curl -b "session_id=abc123; language=pidgin" http://127.0.0.1:8000/desk/greeting
curl http://127.0.0.1:8000/desk/greeting   # refused, no session_id
```

## Reference

Built from these FastAPI docs chapters:
[Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/) ·
[Cookie Parameters](https://fastapi.tiangolo.com/tutorial/cookie-params/) ·
[Header Parameter Models](https://fastapi.tiangolo.com/tutorial/header-param-models/) ·
[Cookie Parameter Models](https://fastapi.tiangolo.com/tutorial/cookie-param-models/) ·
[Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) ·
[Extra Models](https://fastapi.tiangolo.com/tutorial/extra-models/) ·
[Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/) ·
[Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/)
