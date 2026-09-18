from django.http import HttpRequest
from ninja import NinjaAPI

api = NinjaAPI(title="Time Grinder API")


@api.get("/health", response=dict[str, str])
def health(request: HttpRequest):
    return {"status": "ok"}
