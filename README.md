# Django Unchained — Bounty Board

A REST API for a frontier town's bounty office. Outlaws get put on the board with a reward, and the office tracks whether they're `wanted` or `captured`.

## Frontier Concept
**Bounty Board** — the town's bounty office. Users create bounty listings for outlaws with a reward amount and status.

## Tech Stack
- Django + Django REST Framework
- djangorestframework-simplejwt for JWT auth
- SQLite (default)
- Django's built-in LocMemCache for caching

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Method | Path | Auth Required |
|---|---|---|
| POST | /api/auth/register/ | No |
| POST | /api/auth/login/ | No |
| POST | /api/auth/refresh/ | No |
| GET | /api/bounties/ | Yes |
| POST | /api/bounties/ | Yes |
| GET | /api/bounties/<id>/ | Yes + ownership |
| PUT/PATCH | /api/bounties/<id>/ | Yes + ownership |
| DELETE | /api/bounties/<id>/ | Yes + ownership |

## Bonus Features Implemented

### Rate Limiting
Using DRF's built-in throttle classes (`UserRateThrottle`, `AnonRateThrottle`), configured in `settings.py`:
- Authenticated users: 60 requests/minute
- Anonymous users: 10 requests/minute

### Caching
The bounty list endpoint (`GET /api/bounties/`) is cached per-user using Django's `LocMemCache`, with a 60-second timeout. The cache key is scoped to the requesting user's ID, so users never see each other's cached data.

**Cache invalidation:** any create, update, or delete on a bounty deletes that user's cache key, so the next GET request fetches fresh data from the database instead of serving stale results.

## Security Notes

- `owner` is never accepted from client input — it's always set server-side from the authenticated request user, preventing a user from creating or reassigning a bounty to someone else.
- Ownership is enforced at the queryset level: `get_queryset()` filters every list/retrieve/update/delete operation to `owner=request.user`. A user requesting another user's bounty by ID gets a 404, not a 403 — this avoids confirming the resource even exists.