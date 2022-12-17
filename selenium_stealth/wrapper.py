from selenium.webdriver import Chrome as Driver
from typing import Any
import json
from selenium_stealth.remote import send


def evaluationString(fun: str, *args: Any) -> str:
    """Convert function and arguments to str."""
    _args = ', '.join([
        json.dumps('undefined' if arg is None else arg) for arg in args
    ])
    expr = '(' + fun + ')(' + _args + ')'
    return expr


def evaluateOnNewDocument(driver: Driver, pagefunction: str, *args: str) -> None:

    js_code = evaluationString(pagefunction, *args)

    send(driver, "Page.addScriptToEvaluateOnNewDocument", {
        "source": js_code,
    })



