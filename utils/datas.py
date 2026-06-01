def formatar_data_br(data):

    if not data:
        return "-"

    return data.strftime("%d/%m/%Y")