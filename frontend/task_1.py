import mesop as me
from backend.task_1 import fibonacci


@me.stateclass
class State:
    fib_idx: int = 0
    is_input_valid: bool = False
    is_output_computed: bool = False
    fib_value: int = 0


def on_input_idx(e: me.InputEvent) -> None:
    state: State = me.state(state=State)
    state.is_output_computed = False
    try:
        state.fib_idx = int(e.value)
        state.is_input_valid = True
    except:
        state.is_input_valid = False
    else:
        if state.fib_idx < 0 or state.fib_idx > 100:
            state.is_input_valid = False


def on_click_compute(e: me.ClickEvent) -> None:
    state: State = me.state(state=State)
    try:
        state.fib_value = fibonacci(state.fib_idx)
        state.is_output_computed = True
    except:
        state.is_output_computed = False


def body_1() -> None:
    state: State = me.state(state=State)
    with me.box(
        style=me.Style(
            height='324px',
            margin=me.Margin(left='16px', right='16px'),
            display='grid',
            grid_template_rows='96px 1fr 1fr 1fr',
            align_items='center',
            text_align='center',
        )
    ):
        me.text(
            text='Compute Fibonacci numbers with caching.',
            style=me.Style(text_align='left'),
        )
        me.input(
            hint_label='Enter integer from 0 to 100',
            on_input=on_input_idx,
            appearance='outline',
            style=me.Style(width='100%'),
        )
        me.button(
            label='Compute',
            on_click=on_click_compute,
            disabled=(not state.is_input_valid),
            type='flat',
        )
        me.textarea(
            hint_label='Computed Fibonacci Number',
            readonly=True,
            disabled=(not state.is_output_computed),
            value=str(state.fib_value) if state.is_output_computed else '',
            rows=1,
            appearance='outline',
            style=me.Style(width='100%'),
        )
