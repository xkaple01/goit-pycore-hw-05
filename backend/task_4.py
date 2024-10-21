import re
import mesop.labs as mel
from collections.abc import Generator, Callable


contacts: dict[str, str] = {}


def input_error(func: Callable) -> str:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            return str(ex)

    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split()
    cmd: str = cmd.strip().lower()
    return cmd, args


def check_name_valid(name: str) -> bool:
    return re.fullmatch(pattern='[A-Za-z]{2,32}', string=name) is not None


def check_phone_valid(phone: str) -> bool:
    return re.fullmatch(pattern='[+0-9]{2,20}', string=phone) is not None


def show_hello() -> Generator[str]:
    yield (
        'Hi. How can i help you? \n\n'
        'Type "help" to get the list of available commands.'
    )


def show_help() -> Generator[str]:
    messages: list[str] = [
        'Available commands:',
        'add [name] [phone]',
        'change [name] [new_phone]',
        'phone [name]',
        'all',
        'help',
    ]

    for m in messages:
        yield m + '\n\n'


@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError(
            f'add: accepts 2 input arguments, but {len(args)} were provided.'
        )

    name, phone = args

    if not check_name_valid(name=name):
        raise ValueError('Name can contain only letters A-Z, a-z')

    if not check_phone_valid(phone=phone):
        raise ValueError('Phone number can contain only characters: + 0-9')

    if name in contacts:
        raise ValueError(
            f'Contact with name {name} is already present. Please, use "change" command to update the phone number.'
        )

    contacts[name] = phone

    return 'Contact added.'


@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 2:
        raise ValueError(
            f'change: accepts 2 input arguments, but {len(args)} were provided.'
        )

    name, new_phone = args

    if name not in contacts:
        raise ValueError(
            f'There is no contact with name {name}. Please, add this contact first.'
        )

    contacts[name] = new_phone

    return 'Contact updated.'


@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) != 1:
        raise ValueError(
            f'phone: accepts 1 input argument, but {len(args)} were provided.'
        )

    name: str = args[0]

    if name not in contacts:
        raise ValueError(f'Contact with name {name} is absent.')

    return f'{name} : {contacts[name]}'


@input_error
def show_all(args: list[str], contacts: dict[str, str]) -> Generator[str]:
    if len(args) != 0:
        raise ValueError(
            f'show: accepts 0 input arguments, but {len(args)} were provided.'
        )

    if len(contacts.items()) > 0:
        for name, phone in contacts.items():
            yield f'{name} : {phone} \n\n'
    else:
        yield 'There are no contacts in address book yet.'


def show_goodbye() -> str:
    return 'Good bye!'


def transform(input: str, history: list[mel.ChatMessage]) -> str | Generator[str]:
    try:
        cmd, args = parse_input(user_input=input)

        match cmd:
            case 'hello' | 'hi':
                return show_hello()
            case 'add':
                return add_contact(args=args, contacts=contacts)
            case 'change':
                return change_contact(args=args, contacts=contacts)
            case 'phone':
                return show_phone(args=args, contacts=contacts)
            case 'all':
                return show_all(args=args, contacts=contacts)
            case 'close' | 'exit':
                return show_goodbye()
            case 'help' | '"help"' | _:
                return show_help()
    except:
        return show_help()
