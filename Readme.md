  
  
# <center>Proyecto individual Nro 1</center>  

# <center><small>***Machine Learning Operations***</small></center>  

Para el presente proyecto se entrego un dataset con los siguientes archivos:
1. steam_games.json.gz
2. user_reviews.json.gz
3. users_items.json.gz  

Con el objetivo de desplegar una api con fastAPI en el servicio render.com, el cual solo te da un espacio limitado de 512mb. Esta api debe disponibilizar los datos a 5 consultas proporcionadas, ademas de que posteriormente tambien se propone realizar un sistema de recomendacion usando similitud coseno.  

A continuación se explicara como se desarrollo el presente proyecto:

## ETL del dataset

- Para empezar se hizo un proceso de ETL a los archivos proporcionados. En primer lugar se hizo la descompresión del formato json.gz a json. Si bien es posible trabajar el formato directamente con json.gz es importantes destacar que esto se realizar cuando los archivos tienen el formato json valido, caso que no es cumplido en el presente situación por lo que se abordo en este enfoque.  
- Posteriormente se hizo la transformacion a csv de los archivos json resultantes del anterior proceso, es importante destacar que los archivos eran json anidados por lo que en el caso de steam_games.json y user_items.json resulto en que cada uno de estos dio 2 csv, para un total de 5 archivos tipo csv. 
- Para informacion mas detallada tenemos el archivo ***"01 ETL_Dataset.ipynb"***.

## EDA del dataset   

- Para este paso se termino de limpiar las tablas tratando con los valores nulos y duplicados, los dataframes resultantes de esta fase fueron guardados en formato .parquet  
- Para informacion mas detallada tenemos el archivo ***"02 EDA_Parte 1.ipynb"***.  

## Analisis  

Gracias al anterior tratamiento a continuacion podemos observar como se relacionan los archivos:  
|steam_games.parquet|steam_games_genre.parquet|user_items.parquet|user_items_list.parquet|user_reviews.parquet|
|-|-|-|-|-|
| | |***steam_id***|***steam_id***|***steam_id***|
|***item_id***|***item_id***||***item_id***|***item_id***|
|item_name|genres|user_id|playtime_forever|posted|
|developer|user_counts|items_count| |recommend|
|release_year| | | |sentiment_analysis|
|price| | | | |  

Como podemos observar en el cuadro las tablas se relacionan principalmente por 2 columnas que son item_id y steam_id que seran las columnas predeterminadas por donde se haran las relaciones para resolver las distintas solicitudes que pueda haber.  

## Resolución de solicitudes  

Para empezar a resolver las solicitudes es importante tener en cuenta la limitada memoria que disponemos en el servicio 'render.com'. Bajo esa premisa es importante que el codigo proporcionado no solo ester ordenado, sino tambien sea los mas eficiente posible para asi evitar sobrecargar el servicio.

Es por ello que en el presente repositorio encontraremos 2 archivos principales que se pueden desplegar:

- ***"main.py"***: Este archivo es el que se uso para ser desplegado en 'render.com' y contiene los 5 endpoints solicitados. Se requieren tres aclaraciones en este punto:

    - Primero: que la solicitud /userforgenre tumba el servidor por lo que no es funcional si consideramos las limitaciones de memoria

    - Segundo: La solicitud de Machine Learning no se incluyo en este archivo tambien por la limitación de la memoria

    - Tercero: para la elaboración de este archivo se uso un enfoque de lazy load o carga diferida para cargar solo necesario cuando se solicite y asi en la medida de lo posible no tumbar el servidor

- ***"final_main.py"***: En este archivo encontraremos los 5 endpoints solicitados y tambien el endpoint del sistema de recomendación item-item, en este archivo ya no encontraremos el codigo tomando en cuenta la carga diferida por lo que se puede tomar en general este archivo como el caso en donde no haya limitaciones de memoria

Para la demostración correspondiente podemos dirigirnos al siguiente [link](https://drive.google.com/file/d/1RUO4YM6KfashwXnWBRq074qTg-qqA7Kz/view?usp=drive_link)
  

<div style="text-align: right;">
  
Contacto:  
Erwin Alain Felix Tayro Mosqueira  
erwin.aftm@gmail.com
</div>
