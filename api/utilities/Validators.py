import re
from itertools import cycle

class Validators():
    def __init__(self):
        pass

    def full(self, value):
        msg_error = "O campo <<field>> não pode estar vazio."
        return {'res': True} if value else {'res': False, 'error': {'msg': msg_error, 'status_code': 400}}

    def gt3(self, value):
        msg_error = "O campo <<field>> deve ter mais de 3 caracteres."
        return {'res': True} if len(value) > 3 else {'res': False, 'error': {'msg': msg_error, 'status_code': 400}}

    def phone(self, value):
        pattern = r"^\+\d{1,3}\s?\d{1,4}[-\s]?\d{4,5}[-\s]?\d{4}$"
        if re.match(pattern, value):
            return {'res': True}
        msg_error = "O campo <<field>> deve ser um número de telefone válido. Ex: +55 35 12345-6789."
        return {'res': False, 'error': {'msg': msg_error, 'status_code': 400}}

    def email(self, value):
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(regex, value):
            return {'res': True}
        msg_error = "O campo <<field>> deve ser um email válido. Ex: exemplo@dominio.com."
        return {'res': False, 'error': {'msg': msg_error, 'status_code': 400}}

    def password(self, password):
        errors = []
        if len(password) < 8:
            errors.append("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"\d", password):
            errors.append("A senha deve conter pelo menos um dígito numérico.")
        if not re.search(r"[A-Z]", password):
            errors.append("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r"[a-z]", password):
            errors.append("A senha deve conter pelo menos uma letra minúscula.")
        if not re.search(r"[ @!#$?%&'()*+,-./[\\\]^_`{|}~\"]", password):
            errors.append("A senha deve conter pelo menos um caractere especial.")

        count_password_strenght = 10 - (len(errors)*2)

        if errors:
            msg_error = "\n".join(errors)
            print(msg_error)
            return {'res': False, 'error': {'msg': msg_error, 'status_code': 400, 'password_strength':  count_password_strenght}}

        return {'res': True}

    def url(self, value, values):
        pattern = (r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
        if re.match(pattern, value):
            return {'res': True}
        msg_error = "O campo <<field>> deve ser uma URL válida. Ex: https://www.exemplo.com"
        return {'res': False, 'error': {'msg': msg_error, 'status_code': 400}}
