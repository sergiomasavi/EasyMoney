# Librerías
import pandas as pd
import numpy as np
from tqdm import tqdm


def get_clientes_activos(filename):
    """
    Obtener dataframe de clientes activos por mes y fecha.
    Args:
        filename [{str}] -- Directorio del fichero csv

    Returns:
        clientes_activos [{pandas.DataFrame}] -- DataFrame de clientes con servicios en estado igual a 1.

    """

    try:
        clientes_activos = pd.read_csv(filename, sep=';', encoding='utf-8-sig', index_col=[0])
        clientes_activos.index = pd.to_datetime(clientes_activos.index, format='%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f'No se pudo acceder a los datos!\n{e}')
    else:
        return clientes_activos

def get_informacion_clientes_producto(filename):
    """
    Lectura del resultado "informacion_clientes_con_producto".

    Args:
        filename [{str}] -- Directorio del fichero csv

    Returns:
        df_cpi [{pandas.DataFrame}] -- DataFrame de información de clientes con servicios en estado igual a 1.
    """
    # Control de excepciones
    try:
        # Leer
        df_cpi = pd.read_csv(filename, sep=';', encoding='utf-8-sig')
        df_cpi['pk_partition'] = pd.to_datetime(df_cpi['pk_partition'], format='%Y-%m-%d')
        df_cpi.set_index('pk_partition', inplace=True)

        # Dividir el dataset en tres (clientes, productos y ratio).
        columnas_clientes = ['numero_clientes', 'nuevos_clientes', 'crecimiento_clientes']
        df_cpi_clientes = df_cpi[columnas_clientes].copy()

        columnas_productos = ['productos_contratados', 'nuevos_productos', 'crecimiento_productos']
        df_cpi_productos = df_cpi[columnas_productos].copy()

        columnas_ratios = ['producto_cliente_ratio', 'nuevos_producto_cliente_ratio']
        df_cpi_ratios = df_cpi[columnas_ratios].copy()

    except Exception as e:
        print(f'No se pudo acceder a los datos!\n{e}')

    else:
        return df_cpi_clientes, df_cpi_productos, df_cpi_ratios

def get_lista_productos(filename):
    """
    Listado de productos de Easy Money

    :param filename [{str}] -- Directorio del fichero csv
    :return lista_productos [{pandas.Series}] -- Listado de productos.
    """
    lista_productos = sorted(pd.read_csv(filename, sep=';', encoding='utf-8-sig')['productos'].to_list())
    return lista_productos

def get_nivel_permanencia(filename):
    """
    Cargar nivel de permanencia resultado del análisis para visualizar en el panel.

    Args:
        filename [{str}] -- Directorio almacenamiento del archivo con extensión csv incluida.

    Returns:
        df [{dict}] -- DataFrame del archivo.
    """

    # Control de excepciones
    try:
        # Leer
        nivel_permanencia = pd.read_csv(filename, sep=';', encoding='utf-8-sig')
        df_bar = pd.DataFrame(nivel_permanencia['region_permanencia'].value_counts(normalize=True))
        df_bar = df_bar.reset_index().rename({'region_permanencia': 'total', 'index': 'region_permanencia'}, axis=1)
        df_bar.sort_values('total', ascending=False, inplace=True)
        # Añadir columna de región
        region = {
            'baja': '[1-6]',
            'media': '[7-10]',
            'alta': '[11-15]',
            'completa': '[16-17]'
        }
        df_bar['region'] = df_bar['region_permanencia'].map(region)
    except Exception as e:
        print(f'No se pudo acceder a los datos!\n{e}')

    else:
        return df_bar

def get_products_df(filename_dir):
    """
    Carga el fichero products_df.csv y se encarga de aplicar el formato 
    adecuado a las columnas que lo componen.
    
    Args:
    -----
    filename_dir [{str}] -- Directorio de almacenamiento incluyendo el nombre 
                            fichero.
    
    Returns:
    ------
    df_prod [{pandas.DataFrame}] -- Fichero csv cargado en formato DataFrame
    """

    # Cargar datos
    df_prod = pd.read_csv(filename_dir, sep=',', encoding='utf-8-sig', header=0)
    df_prod.drop('Unnamed: 0', axis=1, inplace=True)

    # Añadir formato adeacuado a las columnas
    df_prod['pk_partition'] = pd.to_datetime(df_prod['pk_partition'], format='%Y-%m-%d')
    df_prod['pk_cid'] = df_prod['pk_cid'].apply(str)


    # Rename
    df_prod.rename({'em_acount':'em_account'}, axis=1,inplace=True)

    return df_prod

def resume_products_df(df_prod):
    """
    Imprime por pantalla un resumen sobre las características principales del dataset "products_df.csv"
    
    Args:
    df [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df"
    -----
    """
    
    # Mostrar características principales del dataset
    print('Tamaño del dataset')
    print(f'\tSamples: {df_prod.shape[0]}')
    print(f'\tFeatures: {df_prod.shape[1]}')
    print(2*'\n')
    
    # Número total de particiones en el dataframe
    n_particiones = df_prod.pk_partition.value_counts().shape[0]
    print(f'Número de particiones del histórico: {n_particiones}')
    
    # Número de clientes únicos
    clients_id = list(df_prod.pk_cid.unique())
    print(f'Número de clientes únicos: {len(clients_id)}')
    print(2*'\n')
    
    # Información del dataframe
    print('Información del DataFrame')
    print(df_prod.info())
    print(2*'\n')
    
    # Descripción del dataframe
    print('Descripción del dataset')
    print(df_prod.describe().T)
    print(2*'\n')
    
    # Valores nulos
    print('Valores nulos', df_prod.isna().sum(), sep=2*'\n')
      
def listar_productos(df_prod):
    """
    Listar productos disponibles del fichero products_df.csv

    Args:
    -----
    df [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df"
    """
    
    no_products_cols = ['pk_cid', 'pk_partition']
    productos = df_prod.drop(no_products_cols, axis=1).columns.to_list()
    
    lista_productos = []
    print(f"Productos disponibles: {len(productos)}",end=2*'\n')
    for p in sorted(productos):
        print(f'\t{p}')
        lista_productos.append(p)
        
    return lista_productos
        
def nulos_productos(df_prod):
    """
    Establece a 0 los valores nulos encontrados en los productos "payroll" y "pension_plan" del dataset de products_df.csv
    Dado que se trata de un dataset de clientes, se entiendo que los valores nulos indican que dicho cliente no tiene activado 
    ("dado de alta") dicho producto en el momento temporal correspondiente. 
    
    Dicho de otra forma, un valor nulo conlleva:
        - Continúa siendo cliente dado que aparece en el registro.
        - No tiene activado el producto y se establece el valor nulo a 0.
        
        
    Args:
    -----
    df [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" con columnas de valores nulos.
    
    Returns:
    -----
    df_prod [{pandas.DataFrame}] -- DataFrame sin valores nulos.
    """
    
    # Asignar valores nulos a 0 (cliente no activo)
    for col_name in df_prod.columns:
        df_prod.loc[(df_prod[col_name].isna()), col_name] = 0

    print(f'Total de valores nulos:', df_prod.isna().sum(), sep=2*'\n')
    
    return df_prod

def registro_clientes(df_prod):
    """
    Función que calcula si el cliente aparece o no en la bbdd para cada fecha de ingesta de datos.
    
    El resultado se obtiene situando en las filas los pk_cid de cada uno de los clientes y en 
    las columnas la fecha de ingesta. Si el cliente aparece en dicha fecha, se completa con un 1, si
    no aparece, se completará con un 0.
    
    Args:
    ------
    df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" con columnas de valores nulos.

    
    Returns:
    ------
    registro_clientes [{pandas.DataFrame}] -- Registro de clientes mes a mes
    """
    
    # Clientes y particiones únicas
    clientes = df_prod['pk_cid'].unique()
    particiones = df_prod['pk_partition'].unique()

    # Inicialización del dataframe (todos los valores están establecidos en NaN)
    registro_clientes = pd.DataFrame(
        columns = particiones, 
        index = clientes,
        dtype=int
    )
    
    # Bucle iterativo
    for fecha_ingesta in particiones:
        # Seleccionar fecha_ingesta
        prod_fi = df_prod.loc[df_prod['pk_partition'] == fecha_ingesta]

        # Obtener todos los pk_cid de la fecha de ingesta
        clientes_fi = prod_fi['pk_cid']

        # Indicar con el valor 1 los clientes que se encuentran en esa fecha y 0 en cc.
        clientes_encontrados = registro_clientes.index.isin(clientes_fi)
        clientes_no_encontrados = ~registro_clientes.index.isin(clientes_fi)

        # Asignar el valor
        registro_clientes.loc[clientes_encontrados, fecha_ingesta] = 1
        registro_clientes.loc[clientes_no_encontrados, fecha_ingesta] = 0
        
    return registro_clientes

def contratacion_general(df_prod):
    """
    Calcula el "nivel de contratación" de un producto como su tasa de éxito (número de clientes con el servicio activo)
    activado.
    
    Args:
    ------
    df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" con columnas de valores nulos.

    
    Returns:
    ------
    contratacion_gen [{pandas.DataFrame}] -- Indice de contratacion.
    """
    
    columnas_ordenadas = [
        'pk_cid','pk_partition','short_term_deposit', 'loans', 
        'mortgage', 'funds', 'securities', 'long_term_deposit', 
        'em_account_pp', 'credit_card', 'payroll', 'pension_plan', 
        'payroll_account', 'emc_account', 'debit_card', 'em_account_p', 'em_account', 
    ]

    contratacion_gen = df_prod.copy()
    contratacion_gen = contratacion_gen[columnas_ordenadas].set_index(['pk_cid', 'pk_partition'])

    contratacion_gen = contratacion_gen.describe().T.sort_values('mean', ascending=False)[['mean']]
    contratacion_gen.rename(
    {
        'mean': 'total',
    }, axis=1, inplace=True)
    
    return contratacion_gen

def contratacion_anual(df_prod):
    """
    Calcula el "indice de contratación" de un producto como su tasa de éxito (número de clientes con el servicio activo)
    activado por año
    
    Args:
    ------
    df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" con columnas de valores nulos.

    
    Returns:
    ------
    contratacion_anual [{pandas.DataFrame}] -- Indice de contratacion anual
    """
    
    columnas_ordenadas = [
        'year', 'short_term_deposit', 'loans', 
        'mortgage', 'funds', 'securities', 'long_term_deposit', 
        'em_account_pp', 'credit_card', 'payroll', 'pension_plan', 
        'payroll_account', 'emc_account', 'debit_card', 'em_account_p', 'em_account', 
    ]

    # Indice contratación anual
    contratacion_anual = df_prod.copy()
    contratacion_anual['year'] = contratacion_anual['pk_partition'].dt.year
    contratacion_anual.set_index(['pk_cid', 'pk_partition'], inplace=True)
    contratacion_anual = contratacion_anual[columnas_ordenadas]

    # Pivot table
    contratacion_anual=contratacion_anual.pivot_table(index='year',
                                                    aggfunc=np.mean).T
    
    return contratacion_anual

def contratacion_mensual(df_prod):
    """
    Calcula el "indice de contratación" de un producto como su tasa de éxito (número de clientes con el servicio activo)
    activado por mes
    
    Args:
    ------
    df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" con columnas de valores nulos.

    
    Returns:
    ------
    contratacion mensual [{pandas.DataFrame}] -- Indice de contratacion mensual
    """
    lista_productos =[
        'short_term_deposit', 'loans', 
        'mortgage', 'funds', 'securities', 'long_term_deposit', 
        'em_account_pp', 'credit_card', 'payroll', 'pension_plan', 
        'payroll_account', 'emc_account', 'debit_card', 'em_account_p', 'em_account', 
    ]

    df_prod = df_prod.copy()
    partitions = df_prod['pk_partition'].unique()

    contratacion_mensual = pd.DataFrame(index=lista_productos, columns=partitions)

    for fecha_ingesta in partitions:
        contratacion_mensual[fecha_ingesta] = df_prod.loc[df_prod['pk_partition']==fecha_ingesta].set_index(['pk_cid', 'pk_partition']).mean()    

    return contratacion_mensual
    
def indice_contratacion(df_prod):
    """
    Cálcula el índice de contratación general, anual y mensual.
    
    Args:
    ------
    df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" con columnas de valores nulos.

    
    Returns:
    ------
    nivel_contratacion [{pandas.DataFrame}] -- Indice de contratacion general, anual y mensual.
    """
    cont_gen = contratacion_general(df_prod = df_prod)
    cont_ann = contratacion_anual(df_prod = df_prod)
    cont_men = contratacion_mensual(df_prod = df_prod)
    cont_men.columns = cont_men.columns.strftime('%Y-%m') 
    
    # Unir resultados
    contratacion = pd.DataFrame(index=cont_gen.index)
    contratacion = contratacion.join([cont_gen, cont_ann, cont_men])
    
    return contratacion    

def clientes_producto(df_prod):
    """
    Calcula el número de clientes activos (1) y no activos (0) por cada producto y mes de ingesta.
    
    Args:
    ------
    df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" sin columnas de valores nulos.

    
    Returns:
    ------
    df_informacion [{pandas.DataFrame}] -- Información de clientes y productos.
    df_productos [{pandas.DataFrame}] -- Número de clientes con valor 1 por mes para cada producto.

    """
    # Listado de productos
    lista_productos = [
        'short_term_deposit', 'loans', 'mortgage', 'funds', 'securities',
        'long_term_deposit', 'em_account_pp', 'credit_card', 'payroll', 
        'pension_plan', 'payroll_account', 'emc_account', 'debit_card', 
        'em_account_p', 'em_account'
    ]

    #Lista de fechas de ingesta
    partitions = df_prod['pk_partition'].unique()

    # Inicialización de salida
    clientes_activos = pd.DataFrame(index=partitions, columns=lista_productos)
    clientes_no_activos = clientes_activos.copy()

    # Cálculo
    for p in lista_productos:
        for fecha_ingesta in partitions:
            clientes_activos.loc[fecha_ingesta][p] = df_prod.loc[df_prod['pk_partition']==fecha_ingesta][p].sum()
            clientes_no_activos.loc[fecha_ingesta][p] = df_prod.loc[df_prod['pk_partition']==fecha_ingesta][p].count() - clientes_activos.loc[fecha_ingesta][p]

    return clientes_activos, clientes_no_activos

def analizar_productos_clientes(df_prod, ca):
    """
    Añade información al dataset de clientes (activos) de releveancia:

        - numero_clientes. Número de clientes con el servicio activado (estado igual a 1).

        - nuevos_clientes.	Diferencia de número de clientes del mes actual y del mes anterior.

        - productos_contratados. Número de productos contratados contabilizando todos los productos.

        - nuevos_productos.	Diferencia del número de productos contratados del mes actual respecto al mes anterior.

        - producto_cliente_ratio. Relación entre el número de productos contratados y el número de clientes.
                - >1. Clientes con más de un producto.
                - <1. Clientes con menos de 1 producto.

        - crecimiento_clientes. Relación entre el número de nuevos clientes del mes actual y el número de clientes del mes anterior.

        - crecimiento_productos. Relación entre el número de nuevos productos del mes actual y el número de productos del mes anterior.

        - nuevos_producto_cliente_ratio. Relación entre el número de productos contratados nuevos y el número de clientes nuevos.

    Args:
    ------
        df_prod [{pandas.DataFrame}] -- DataFrame obtenido con la función "get_products_df" sin columnas de valores nulos.
        df_ca [{pandas.DataFrame}] --

    Returns:
        df_informacion [{pandas.DataFrame}] -- Información de clientes y productos.
    """
    df = df_prod.copy()
    df_ca = ca.copy()

    # Clientes totales por fecha.
    registro = registro_clientes(df)
    clientes_totales = clientes_fecha(registro=registro, show_msg=False)

    # Calcular número de clientes.
    df_ca['numero_clientes'] = clientes_totales.values

    # Productos activos por fecha.
    df_ca['productos_contratados'] = df_ca.sum(axis=1) - df_ca['numero_clientes']

    # Ratio de productos respecto a numero de clientes
    df_ca['producto_cliente_ratio'] = df_ca['productos_contratados']/df_ca['numero_clientes']

    # Clientes nuevos.
    df_ca['nuevos_clientes'] = (df_ca['numero_clientes'] - df_ca['numero_clientes'].shift(1)).fillna(0)

    # Productos nuevos contratados.
    df_ca['nuevos_productos'] = (df_ca['productos_contratados'] - df_ca['productos_contratados'].shift(1)).fillna(0)

    # Crecimiento de clientes.
    df_ca['crecimiento_clientes'] = (df_ca['nuevos_clientes']/df_ca['numero_clientes'].shift(1)).fillna(0)

    # Crecimiento de productos.
    df_ca['crecimiento_productos'] = (df_ca['nuevos_productos']/df_ca['productos_contratados'].shift(1)).fillna(0)

    # Ratio de nuevos productos respecto a nuevo número de clientes
    df_ca['nuevos_producto_cliente_ratio'] = (df_ca['nuevos_productos']/df_ca['nuevos_clientes']).fillna(0)

    # Ordenar columnas del dataframe.
    columnas_informacion = [
        'numero_clientes', 'nuevos_clientes',  'productos_contratados', 'nuevos_productos',
        'producto_cliente_ratio', 'crecimiento_clientes', 'crecimiento_productos','nuevos_producto_cliente_ratio'
    ]

    # Salida
    df_informacion = df_ca[columnas_informacion].copy()
    df_informacion.index.name = 'pk_partition' # Establecer nombre del índice.

    return df_informacion

def clientes_fecha(registro, show_msg=True):
    """
    Aplica un sumatorio a cada fecha para conocer el número de clientes
    cada mes.
    
    Arguments:
    ----------
    registro {[dataframe]} -- Registro de clientes.
    
    Returns:
    ----------
    clientes_totales {[dataframe]} -- DataFrame con el número de clientes por 
                                      fecha.
    """
    
    clientes = pd.DataFrame(index=registro.columns.to_list())
    clientes['total'] = np.nan

    partitions = registro.columns.to_list()

    for fecha_ingesta in partitions:
        num_clientes = registro[fecha_ingesta].sum()
        if show_msg:
            print(f'{fecha_ingesta} -> {num_clientes} clientes')
        clientes.loc[fecha_ingesta] = num_clientes

    if not show_msg:
        return clientes

def promedio_permanencia(nivel_permanencia):
    """
    Calcula la media de permanencia por número de meses.
    Args:
        nivel_permanencia [{pandas.Series}]:

    Returns:

    """
    prom_perm = pd.DataFrame(nivel_permanencia.value_counts(normalize=True)).reset_index()
    prom_perm.rename({'numero_meses': 'score', 'index': 'numero_meses'}, axis=1, inplace=True)

    return prom_perm

def nivel_permanencia(registro, periodo):
    """
    Calcula el nivel de permanencia (np) del cliente (c) es:

            nvp = (mc)/t

    siendo:
        - nvp. Nivel de permanencia del cliente.
        - mc. Número de meses que aparece como cliente.
        - t. Período de tiempo total.

    Args:
    -----
    registro {[dataframe]} -- Registro de clientes (el indice corresponde con el pk_cid del cliente).
    periodo {[float]} -- Período de tiempo total sobre el que evaluar.


    Returns:
    nvp {[pandas.DataFrame]} -- Nivel de permanencia de los clientes
    """
    # Período de tiempo
    nivel_perm = pd.DataFrame(columns=['pk_cid', 'numero_meses', 'score'])
    nivel_perm['pk_cid'] = registro.index  #  El indice del registro corresponde con el pk_cid del cliente.

    # Formula
    mc = registro.sum(axis=1)
    nvp = mc / periodo

    #  Almacenamiento
    nivel_perm['numero_meses'] = mc.values
    nivel_perm['score'] = nvp.values

    return nivel_perm.reset_index(drop=True)

def region_permanencia(nivel_permanencia):
    """
    Calcula la región del nivel de permanencia de los clientes.

        - (1) Fidelización baja. Aquellos clientes que permanencen en el registro entre 0 y 6 meses.
        - (2) Fidelización media. Aquellos clientes que permanecen en el registro entre 7 y 10 meses.
        - (3) Fidelización alta. Aquellos clientes que permanecen en el registro entre 11 y 15 meses.
        - (4) Fidelización completa. Aquellos clientes que permanencen en el registro entre 16 y 17 meses.

    Args:
    ------
    nivel_permanencia {[pandas.DataFrame]} -- Nivel de permanencia de los clientes


    Returns:
    --------
    region_permanencia {[pandas.Series]} -- Región de permanencia
    """
    # Inicialización de la serie
    nivel_permanencia['region_permanencia'] = np.nan

    # Filtros
    fidelizacion_baja = (nivel_permanencia['numero_meses'] >= 1) & (nivel_permanencia['numero_meses'] <= 6)
    fidelizacion_media = (nivel_permanencia['numero_meses'] >= 7) & (nivel_permanencia['numero_meses'] <= 10)
    fidelizacion_alta = (nivel_permanencia['numero_meses'] >= 11) & (nivel_permanencia['numero_meses'] <= 15)
    fidelizacion_completa = (nivel_permanencia['numero_meses'] >= 16) & (nivel_permanencia['numero_meses'] <= 17)


    # Aplicar máscaras/filtros
    nivel_permanencia.loc[fidelizacion_baja, 'region_permanencia'] = 'baja'
    nivel_permanencia.loc[fidelizacion_media, 'region_permanencia'] = 'media'
    nivel_permanencia.loc[fidelizacion_alta, 'region_permanencia'] = 'alta'
    nivel_permanencia.loc[fidelizacion_completa, 'region_permanencia'] = 'completa'

    return nivel_permanencia['region_permanencia'].values

def valorar_productos_clientes(df, lista_productos):
    """
    
    Función que permite valorar a los clientes en función de la relación que han mantenido con EasyMoney. A continuación, se 
    describen las columnas de salida de "prod_client_val".
   
        - 'pk_cid'. Identificador de cliente
        
        - 'product'. Producto analizado
        
        - 'num_months'. Número de meses que aparece en el registro.
        
        - 'max_permanence'. Máxima permanencia como cliente activo. Se define como la relación entre la longitud del número 
                            máximo de veces que permanece con un estado igual a 1 sin tener ningún estado igual a 0 y el número
                            de meses que permanece en el registro.
        
        - 'permanence_ratio'. Ratio de permanencia. Se define como la relación entre el número de veces su estado es 1 y el 
                              número de meses que aparece en el registro.                            
                            
        - 'losses_ratio'. Ratio de perdida. Se define como el número de veces cuyo estado es 0 y el número de meses que aparece
                          en el registro (equivalente a 1-permanence_ratio)
        
    Args:
    -----
    df [{pandas.DataFrame}] -- Dataset de productos.
    producto [{str}] -- Producto a analizar (debe estar en la lista de productos).
    lista_productos [{list}] -- Listado de productos.
    
    
    Returns:
    ------
    resultado [{dict}] -- Diccionario con dos elementos:
                            - p [{pandas.DataFrame}]. Dataset de productos almacenado con información adicional.
                            
                            - v [{list}]. Conjunto de valoraciones para cada producto (cada valoración por cada producto se 
                                          representa con un pandas.DataFrame.
    """
    print('Valoración de clientes. Este proceso puede tomar un tiempo de espera largo...')

    # Añadir información al dataset
    products = df.copy() 
    products['year'] = products['pk_partition'].dt.year # año de cada muestra
        
    # Cada fecha de ingesta tiene un valor asociado (0,16)
    # Empaquetar valor de cada mes en un diccionario
    k = pd.Series(products['pk_partition'].unique()).values
    v = [x for x in range(0, len(k))]
    d_values = dict(zip(k, v)) # Valor de los días
    products['id_partition'] = products['pk_partition'].map(d_values)

    # Inicialización de la variable de retorno.
    resultado = {
        'p': products, # Dataset con información adicional.
        'v': list()
    }

    # Calcular valoración de los clientes
    # Inicialización dataframe resultado
    val_clients = pd.DataFrame(
        columns=[
            'pk_cid','product', 'num_months', 'max_permanence', 'permanence_ratio', 'losses_ratio'
        ]
    )

    # Calcular la valoración del cliente utilizando progress_apply para visualizar el progreso.
    drop_columns = ['pk_partition','year','id_partition']
    df = resultado['p'].drop(drop_columns, axis=1)
    df_result = df.groupby('pk_cid').progress_apply(val_c, lista_productos=lista_productos)

    df_result.reset_index(drop=True, inplace=True)
    df_result.set_index(['pk_cid', 'product'])

    return df_result

def val_c(historial_cliente, lista_productos):

    def tuplify(s, k):
        return list(zip(*[s.values[i:].tolist() for i in range(k)]))

    # Identificar cliente
    pk_cid = historial_cliente['pk_cid'].unique()[0]
    t = historial_cliente.shape[0]  # Periodo. t = 17 meses

    # Añadir cliente al resultado
    val_cl = pd.DataFrame(
        {
            'pk_cid': np.repeat(pk_cid, len(lista_productos)),
            'product': np.repeat(str, len(lista_productos)),
            'num_months': np.repeat(np.nan, len(lista_productos)),
            'num_months_up': np.repeat(np.nan, len(lista_productos)),
            'max_permanence_ratio': np.repeat(np.nan, len(lista_productos)),
            'permanence_ratio': np.repeat(np.nan, len(lista_productos)),
            'losses_ratio': np.repeat(np.nan, len(lista_productos)),
        }
    )

    # Analizar al cliente
    for i,p in enumerate(lista_productos):
        # Almacenar producto
        val_cl.at[i, 'product'] = p
        historial_producto_cliente = historial_cliente[p]

        if (historial_producto_cliente==1).all():
            val_cl.at[i, 'num_months_up'] = t
            val_cl.at[i, 'num_months'] = t
            val_cl.at[i, 'max_permanence_ratio'] = 1
            val_cl.at[i, 'losses_ratio'] = 0
            val_cl.at[i, 'permanence_ratio'] = 1

            continue

        elif (historial_producto_cliente==0).all():
            val_cl.at[i, 'num_months'] = t
            val_cl.at[i, 'num_months_up'] = 0
            val_cl.at[i, 'max_permanence_ratio'] = 0
            val_cl.at[i, 'losses_ratio'] = 0
            val_cl.at[i, 'permanence_ratio'] = 0
            continue

        else:
            resultados = dict()
            for k in range(1, t - 1):
                resultados[k] = pd.value_counts(tuplify(historial_producto_cliente, k))
                # Comprobar si existe la secuencia más favorable (todos unos)
                if not tuple(np.repeat(1, k)) in resultados[k].index.to_list():
                    # Si no existe la máxima pertenencia que ha tenido es k y se normaliza
                    # con el número total de periodos que ha disfrutado
                    val_cl.at[i, 'num_months'] = t
                    val_cl.at[i, 'num_months_up'] = historial_producto_cliente[historial_producto_cliente==1].shape[0]
                    val_cl.at[i, 'max_permanence_ratio'] = (k-1) / t
                    val_cl.at[i, 'losses_ratio'] = historial_producto_cliente[historial_producto_cliente==0].shape[0]/t
                    val_cl.at[i, 'permanence_ratio'] = 1-val_cl.iloc[i]['losses_ratio']

                    break

    return val_cl

def get_valoracion_clientes(filename):
    """
    Realiza la lectura del dataset de valoraciones de los clientes.


    Args:
    -----
    filename [{str}] -- Directorio y nombre del fichero csv de almacenamiento.


    Returns:
    -----
    valoracion_clientes {[pandas.DataFrame]} -- Dataset de valoración.
    """
    valoracion_clientes = pd.read_csv(filename, sep=';', encoding='utf-8-sig')
    valoracion_clientes['pk_cid'] = valoracion_clientes['pk_cid'].apply(str)

    return valoracion_clientes

def tipos_clientes(valoracion_clientes):
    """
    Se distinguen dos tipos de clientes:

        - Clientes con producto contratado en algún mes que producen una facturación en EasyMoney.
        - Clientes sin producto contratado ningún mes que no producen una facturación (captados pero no facturan).

    Args:
    -----
        valoracion_clientes [{pandas.DataFrame}] -- Valoración de clientes por producto.

    Returns:
        productos_contratados [{pandas.DataFrame}] -- Clientes con productos contratados dentro del dataset de valoración.
        productos_no_contratados [{pandas.DataFrame}] -- Clientes sin productos contratados dentro del dataset de valoración.
    """
    productos_contratados = valoracion_clientes[valoracion_clientes['num_months_up'] >= 1]
    productos_no_contratados = valoracion_clientes[valoracion_clientes['num_months_up'] == 0]

    num_clientes_con_producto = len(productos_contratados['pk_cid'].unique())
    num_productos_contratados = productos_contratados.shape[0]

    print(f'Número de clientes con servicios contratados: {num_clientes_con_producto}')
    print(f'Número de productos contratados totales: {num_productos_contratados}')

    return productos_contratados, productos_no_contratados