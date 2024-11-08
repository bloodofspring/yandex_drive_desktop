from app_windows.dialog_samples import EmptyDialog


class WrongRegDataDialog(EmptyDialog):
    INFO = "Указан неверный логин или пароль!"


class LoginIsTakenDialog(EmptyDialog):
    INFO = "Этот логин уже занят!"
