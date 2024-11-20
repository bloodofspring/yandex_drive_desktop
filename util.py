from app_windows.dialog_samples import EmptyDialog
from database.models import Session


class AuthFailed(EmptyDialog):
    INFO = "Ошибка авторизации! Пожалуйста, перезайдите в аккаунт."


def get_last_session() -> Session | None:
    try:
        return Session.select().order_by(Session.created_at.desc())[0]
    except IndexError:
        AuthFailed().exec()

        return None
