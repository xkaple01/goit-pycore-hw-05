import mesop as me
import mesop.labs as mel
from backend.task_4 import transform


def body_4() -> None:
    with me.box(
        style=me.Style(
            height='600px',
            border_radius='16px',
            margin=me.Margin(top='16px', left='16px', right='16px'),
        )
    ):
        mel.chat(transform=transform, title='Virtual Assistant', bot_user='Bot')