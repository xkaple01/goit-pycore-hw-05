import mesop as me
from backend.task_2 import generator_numbers, sum_profit


@me.stateclass
class State:
    is_input_provided: bool = False
    text: str = ''
    is_output_computed: bool = False
    total_profit: float = 0.0


def on_input_textarea(e: me.InputEvent) -> None:
    state: State = me.state(state=State)

    input_text: str = e.value
    state.is_input_provided = False
    state.is_output_computed = False

    if len(input_text) > 0 and len(input_text) <= 1000:
        state.text = input_text
        state.is_input_provided = True
    else:
        state.is_input_provided = False


def on_click_compute(e: me.ClickEvent) -> None:
    state: State = me.state(state=State)
    try:
        state.total_profit = sum_profit(text=state.text, func=generator_numbers)
        state.is_output_computed = True
    except:
        state.is_output_computed = False


def body_2() -> None:
    state: State = me.state(state=State)

    with me.box(
        style=me.Style(
            height='512px',
            display='grid',
            grid_template_rows='96px 1fr 1fr 1fr',
            margin=me.Margin(left='16px', right='16px'),
            align_items='center',
            text_align='center',
        )
    ):
        me.text(
            text='Analyze text to compute the total income.',
            style=me.Style(text_align='left'),
        )
        me.textarea(
            hint_label='Enter text',
            on_input=on_input_textarea,
            rows=7,
            appearance='outline',
            style=me.Style(width='100%', height='100%'),
        )
        me.button(
            label='Compute',
            on_click=on_click_compute,
            type='flat',
            disabled=(not state.is_input_provided),
        )
        me.textarea(
            hint_label=f'Total income',
            readonly=True,
            disabled=(not state.is_output_computed),
            value=str(state.total_profit) if state.is_output_computed else '',
            rows=1,
            appearance='outline',
            style=me.Style(width='100%'),
        )
