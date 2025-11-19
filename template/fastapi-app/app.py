from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {
        "message": "FastAPI App Demo",
        "info": "This is a simple FastAPI application running in Docker.",
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
