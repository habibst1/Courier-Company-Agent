"""Run the API server:  python -m app [--host 127.0.0.1] [--port 8000] [--reload]"""

import argparse

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the CourierTrack API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="restart on code changes")
    args = parser.parse_args()
    uvicorn.run(
        "app.main:create_app",
        factory=True,
        host=args.host,
        port=args.port,
        reload=args.reload,
        # psycopg's async mode needs a selector event loop; Windows defaults to Proactor.
        loop="asyncio:SelectorEventLoop",
    )


if __name__ == "__main__":
    main()
