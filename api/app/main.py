from fastapi import FastAPI

app = FastAPI(
    title="Cardfolio 2.0 API",
    description="Card collecting platform with price tracking and portfolio management",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
