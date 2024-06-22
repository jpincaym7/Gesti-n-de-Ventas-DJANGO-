def get_card_type(card_number):
    # Eliminar espacios en blanco y guiones del número de la tarjeta
    card_number = card_number.replace(' ', '').replace('-', '')

    # Comprobar la longitud del número de tarjeta para determinar el tipo
    if len(card_number) == 15 and card_number.isdigit() and (card_number.startswith('34') or card_number.startswith('37')):
        return 'amex'
    elif len(card_number) == 16 and card_number.isdigit():
        if card_number.startswith('4'):
            return 'visa'
        elif card_number.startswith(('51', '52', '53', '54', '55')):
            return 'mastercard'
        elif 2221 <= int(card_number[:4]) <= 2720:
            return 'mastercard'
        elif 622126 <= int(card_number[:6]) <= 622925:
            return 'discover'
    
    # Si no coincide con ninguno de los patrones anteriores, se devuelve None
    return None

