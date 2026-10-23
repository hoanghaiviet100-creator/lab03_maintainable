import sys
import time
import logging
from pathlib import Path
from assistant_core.config import load_settings
from assistant_core.knowledge import OfficeDirectory, Handbook
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService
from assistant_core.logging_setup import setup_logging

def main():
    settings = load_settings()
    setup_logging(settings.log_level)
    log = logging.getLogger("assistant_core")

    data_dir = settings.data_dir
    if not data_dir.is_absolute():
        data_dir = Path.cwd() / data_dir

    offices = OfficeDirectory.from_csv(data_dir / "offices.csv")
    handbook = Handbook.from_json(data_dir / "handbook.json")
    responder = StubLLMResponder()
    service = AssistantService(settings, offices, handbook, responder)

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        start = time.time()
        res = service.handle(Message(text=query))
        latency = round((time.time() - start) * 1000, 2)
        log.info(
            "handled",
            extra={
                "intent": res.intent.value,
                "latency_ms": latency,
                "session": "local",
                "degraded": res.degraded,
            },
        )
        print(res.answer)
        return

    print("Assistant ready")
    while True:
        try:
            q = input("> ")
        except (KeyboardInterrupt, EOFError):
            break
        if q.strip().lower() == "quit":
            break
        res = service.handle(Message(text=q))
        print(res.answer)

if __name__ == "__main__":
    main()
