import mesop as me
from backend.task_3 import LogLevel, count_messages_in_logfile


@me.stateclass
class State:
    is_input_provided: bool = False
    text: str = ''
    radio_value: str = ''
    is_output_computed: bool = False
    n_messages: int = 0
    hint: str = ''


def on_input_textarea(e: me.InputEvent) -> None:
    state: State = me.state(state=State)

    input_text: str = e.value
    state.radio_value = ''
    state.is_input_provided = False
    state.is_output_computed = False

    if len(input_text) > 0 and len(input_text) < 4096:
        state.is_input_provided = True
        state.text = input_text


def on_change_radio(e: me.RadioChangeEvent) -> None:
    state: State = me.state(state=State)
    state.radio_value = e.value
    try:
        state.n_messages = count_messages_in_logfile(
            input_text=state.text, input_level=LogLevel(state.radio_value)
        )
        state.is_output_computed = True
        state.hint = ''
    except:
        state.is_output_computed = False
        state.hint = 'Please, provide correctly formatted log file.'


def body_3() -> None:
    state: State = me.state(state=State)
    with me.box(
        style=me.Style(
            height='600px',
            display='grid',
            grid_template_rows='96px 1fr 1fr 1fr',
            margin=me.Margin(left='16px', right='16px'),
            align_items='center',
            text_align='center',
        )
    ):

        me.text(text='Count messages in log file.', style=me.Style(text_align='left'))

        me.textarea(
            label='Insert text of log file',
            on_input=on_input_textarea,
            hint_label=state.hint,
            rows=10,
            appearance='outline',
            style=me.Style(width='100%', height='100%'),
        )

        me.radio(
            options=[
                me.RadioOption(label='INFO', value=LogLevel.INFO.name),
                me.RadioOption(label='DEBUG', value=LogLevel.DEBUG.name),
                me.RadioOption(label='ERROR', value=LogLevel.ERROR.name),
                me.RadioOption(label='WARNING', value=LogLevel.WARNING.name),
            ],
            on_change=on_change_radio,
            disabled=(not state.is_input_provided),
            value=state.radio_value,
        )

        me.textarea(
            hint_label='Number of messages',
            value=str(state.n_messages) if state.is_output_computed else '',
            readonly=True,
            disabled=(not state.is_output_computed),
            rows=1,
            appearance='outline',
            style=me.Style(width='100%'),
        )
