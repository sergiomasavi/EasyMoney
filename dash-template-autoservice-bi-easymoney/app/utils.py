


def decode_dropdown_selection(lista_productos, dropdown_value):
    # Tonar valores del dropdown
    label_list = list()
    value_list = list()
    for i, producto in enumerate(lista_productos):
        label_list.append(f'dropdown_v{i+1}')
        value_list.append(lista_productos[i])

    dropdown_value_selection = dict(zip(label_list, value_list))

    productos_seleccionados = [dropdown_value_selection[v] for v in dropdown_value]

    return productos_seleccionados