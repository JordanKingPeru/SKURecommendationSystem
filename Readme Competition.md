# Drop the bit

## Descripción

Hola ChatGPT, vamos a participar de un concurso de analítica avanzada. Te voy a compartir una capeta comprimida "data_sample.zip", el cual tiene 3 archivos parquet: df_rentabilidad.csv, df_submit.csv, df_train.csv estos son los inputs del concurso. Se requiere construir el proceso para conseguir el objetivo del concurso. Te paso todo el detalle que necesitas saber sobre el concurso y la data, primero propón los pasos lógicos que debemos de seguir para conseguir el objetivo y luego vamos ejecutanto la propuesta.

Ejecuta la primera etapa de extracción y exploración de los datos.

# Datathion Alicorp 2023

Modelo de Sistema de Recomendacion de SKU's y optimización

## Concurso

El reto consiste en crear un algoritmo de recomendación de skus para nuestros clientes que cuentan con un canal de atención digital, estos clientes pueden ser atendidos de manera análoga como digital (Bodegas, Panaderías y Restaurantes). El objetivo es que los participantes puedan enviarnos un listado de clientes con skus priorizados (máximo 30) de mayor a menor prioridad, es decir el primer sku de un cliente es el de mayor probabilidad de compra en la siguiente semana de venta.

Dataset de entrenamiento:

Data Entrenamiento: Información de ventas extraída de los sistemas de información digital y análoga, desde Febrero 2022 hasta Enero 2023.

Data Producto : Maestro de productos con información de las características propias de cada sku.

Submisison : Dataset que contiene el formato de entregable, cada cliente debe tener como máximo 50 skus.

## Evaluación

Se está considerando como data de entrenamiento del algoritmo a los datos de 12 meses pasados (desde el 30 de enero 2022 hasta el 05 de febrero 2023), para el cáculo de la métrica en el leader board se utiliza las ventas de la primera semana de febrero desde el 06 de febrero hasta el 12 de febrero.

Dentro del proceso de venta semanal que se realiza las recomendaciones que toma el sistema son máximo 50 pero se está acotando a solamente 30 SKUs, debido a que son los SKUs que presentan mayor distribución de venta en historia.

Sea el Recall por cliente obtenido:

$ Recall_{Cliente} = \frac{\lvert Recomendados \bigcap  Comprados \rvert}{\lvert Comprados \rvert} $

La evaluación se hará mediante la siguiente métrica:

$ Recall_{Promedio} = \frac{\sum \limits_{i=1} ^{n} Recall_{Cliente-i}}{N} $

Donde:

* Recomendados: Cantidad de productos de recomendados (máximo 50).
* Comprados: Cantidad de productos relevantes; es decir, que fueron recomendados y comprados.
* N: Cantidad de Clientes

Observación: solamente se permitirá la evaluación de SKUs distintos para cada cliente.

La forma de evaluar será mediante un Recall Promedio el cual consiste en contrastar estos 50 SKUs con la venta y ver cuánto de los SKUs vendidos forman parte de la lista de SKUs recomendados, para luego obtener el promedio de todos los Recall obtenidos por cada cliente.

### Submission File

Por cada customer_id, tendran que recomendar una lista de 50 productos. El archivo deberá contener las columnas y el formato de la siguiente forma:

```python
customer_id,product_id
1,120 987 203 ... (etc.)
2,80 2 10 ... (etc.)
3,40 25 11 ... (etc.) 
```

## Descripción de los datos

### Data Entrenamiento [df_train.parquet]

Diccionario de datos:

* **fecha_compra** Dia donde un cliente hizo una compra.
* **customer_id** Codigo de cliente
* **product_id** Codigo de producto
* **type_id** Tipo de negocio (GA: Gastronomia, PA: Panificacion, BO: Bodegas)
* **business_id** Codigo tipo de producto (a que negocio pertenece el producto)
* **channel_id** Canal de venta (A: Diadia, B: Insuma, V: Tradicional)
* **cantidad_venta** Cantidad de producto comprado
* **monto_venta_transf** Monto de compra
* **peso_venta_transf** Volumen de compra

```python
df_train = pd.read_csv('../01data/01origin/train.csv',
                        sep='|',
                        encoding='utf-8',
                        dtype={'fecha_compra':'str',
                                'customer_id':'str',
                                'product_id':'str',
                                'type_id':'str',
                                'business_id':'str',
                                'channel_id':'str',
                                'cantidad_venta':np.float64,
                                'monto_venta_transf':np.float64,
                                'peso_venta_transf':np.float64,})
```

### Data Producto [df_rentabilidad.parquet]

Diccionario de datos:

* **product_id** Codigo de producto
* **family_id** Codigo de familia (Marca a la que pertenece)
* **negocio_id** Codigo tipo de producto (a que negocio pertenece el producto)
* **category_id** Codigo de categoria de producto
* **tier_id** Codigo de tier, indica jerarquia de un producto ( 1 = premiun, 2 = mainstream, 3=economy, 4=super economy)
* **utilidad_bruta_transf** Utilidad bruta del producto

```python
df_rentabilidad = pd.read_csv('../01data/01origin/RentabilidadProduct.csv',
                                sep='|',
                                encoding='utf-8',
                                dtype={'product_id': 'str',
                                        'family_id': 'str',
                                        'negocio_id': 'str',
                                        'category_id': 'str',
                                        'tier_id': 'str',
                                        'utilidad_bruta_transf': np.float64,})
```

### Submission [df_submit.parquet]

Diccionario de datos:

* **customer_id** Codigo de cliente
* **product_id** Codigo de los 50 productos recomendados (Debe estar ordenado de acuerdo al resultado de su rank)
