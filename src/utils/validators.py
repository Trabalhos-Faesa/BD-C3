from typing import Any

from bson.objectid import ObjectId


def validate_object_id_str(v: ObjectId | Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if ObjectId.is_valid(v):
        return str(ObjectId(v))
    raise ValueError(f"Invalid ObjectId: '{v}'")


# def valid_digits(digits: str) -> str:
#     if not digits.isdecimal():
#         raise ValueError(f'"{digits}" deve ser composto apenas de dígitos')
#     return digits


def valid_senha(senha: str) -> str:
    MIN_CHARS = 6

    if len(senha) < MIN_CHARS:
        raise ValueError(f'A senha deve conter pelo menos {MIN_CHARS}.')
    if not any(c.isdigit() for c in senha):
        raise ValueError('A senha deve conter pelo menos um número.')
    if not any(c.isupper() for c in senha):
        raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
    if not any(c.islower() for c in senha):
        raise ValueError('A senha deve conter pelo menos uma letra minúscula.')

    return senha


def valid_cpf(cpf: str) -> str:
    cpf_digits = [int(digit) for digit in cpf if digit.isdecimal()]

    if len(cpf_digits) != 11:
        raise ValueError(f'CPF "{cpf}" inválido pois não contém 11 caracteres numéricos.')

    # # Verifica a formatação do CPF
    # if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
    #     return False
    if len(cpf_digits) != len(cpf):
        raise ValueError(f'CPF "{cpf}" inválido pois contém caracteres não numéricos.')

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(cpf_digits[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if cpf_digits[9] != expected_digit:
        raise ValueError(f'O primeiro dígito verificador do CPF "{cpf}" é inválido.')

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(cpf_digits[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if cpf_digits[10] != expected_digit:
        raise ValueError(f'O segundo dígito verificador do CPF "{cpf}" é inválido.')

    return ''.join([str(d) for d in cpf_digits])
