import logging
from assistant_core.config import Settings
from assistant_core.errors import ProviderError, InvalidRequest
from assistant_core.knowledge import OfficeDirectory, Handbook
from assistant_core.models import Message, Response, Intent, Source
from assistant_core.responder import Responder, TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger("assistant_core")

class AssistantService:
    def __init__(
        self,
        settings: Settings,
        offices: OfficeDirectory,
        handbook: Handbook,
        responder: Responder,
    ):
        self.settings = settings
        self.offices = offices
        self.handbook = handbook
        self.responder = responder
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        intent = route(msg.text, self.offices.names)
        if intent is Intent.GREETING:
            return Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
            )
        if intent is Intent.FEE:
            return self._fee(msg.text)
        if intent is Intent.OFFICE:
            o = self.offices.find(msg.text)
            if o:
                return Response(
                    answer=f"{o.name}: room {o.room}, open {o.hours}.",
                    intent=intent,
                )
            return Response(answer="Office not found.", intent=Intent.UNKNOWN)
        return self._rule(msg.text)

    def _fee(self, text: str) -> Response:
        try:
            credits_num, retake_num = parse_credits(text)
            total = tuition(
                credits_num,
                retake_num,
                self.settings.credit_rate_vnd,
                self.settings.retake_multiplier,
                self.settings.max_credits,
            )
            return Response(
                answer=f"Your tuition is {total:,} VND",
                intent=Intent.FEE,
            )
        except InvalidRequest as e:
            return Response(answer=str(e), intent=Intent.FEE)

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if rule is None:
            return Response(
                answer="Sorry, I don't know that yet.", intent=Intent.UNKNOWN
            )
        sources = [Source(id=rule.id, title=rule.title)]
        try:
            answer = self.responder.explain(text, rule)
            return Response(answer=answer, intent=Intent.RULE, sources=sources)
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
                degraded=True,
            )
