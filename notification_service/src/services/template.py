from os import PathLike

from jinja2 import Environment, FileSystemLoader, Template
from src.core.constants import ChannelEnum, EventsEnum


class TemplateService:
    def __init__(self, template_path: str | PathLike[str]) -> None:
        self.loader = FileSystemLoader(template_path)
        self.env = Environment(loader=self.loader)

    def get_template(self, event_type: EventsEnum, channel: ChannelEnum) -> Template:
        return self.env.get_template(f"{event_type}__{channel}.jinja")

    def render_template(self, template: Template, context: dict) -> str:
        return template.render(context)
