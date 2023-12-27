
# <center><small>***Proyecto Machine Learning Operations - Steam***</small></center>  

Para el presente proyecto se entrego un archivo markdown llamado **`Solicitud`** el cual contiene los lineamientos generales de trabajo solicitados, el link para el dataset asi como su diccionario lo encontraremos al final de este archivo.

El dataset contiene los siguientes archivos: 

1. steam_games.json.gz
2. user_reviews.json.gz
3. users_items.json.gz  

Para empezar nos socilitan hacer las transformaciones necesarias al dataset asi tambien como una ingeniería de características. Todo esto se realizo en el archivo **`01_ETL.ipynb`**.<br>
Como puntos importantes en esta parte tenemos:
+ Algunos de los archivos proporcionados no eran objetos validos **json** por lo que se utilizo la `biblioteca ast` para poder leerlos facilitando su lectura y ahorrando tiempo al ya no necesitar transformar los **json** no validos en validos de forma manual.
+ Dos archivos tenian la presencia de de columnas anidadas por lo que estas fueron tratadas de tal forma que para desanidarlas se crearon 2 archivos adicionales para luego tener un total de 5 archivos que podemos utilizar.
+ Se prosiguio con normalidad en el tratameinto de estos archivos eliminando filas vacias y duplicadas, tambien se trataron aquellas filas que tenian valores nulos.
+ En cuanto a la ingenieria de caracteristicas se destaca la transformación de la columna review del dataframe user_reviews puesto que se uso SentimentIntensityAnalyzer de la `biblioteca nltk`, para ello se el `modelo VADER` puesto que el texto de la columna review usaba lenguaje con emoticonos y mas informal por lo que este modelo era el mas adecuado.
+ Tambien podemos mencionar la extraccion de información de las columnas para una mejor pulcritud de los dataframes, como ejemplos tenemos la extraccion de los años en fechas o la estandarizacion de la columna que contiene precios del dataframe steam_games
+ Otro punto a destacar es la disminución de los generos del dataframe steam_games_genres puesto que luego se usaran estos datos para el sistema de recomendación por lo que es importante la reduccion de estas dimensiones para que dicho sistema de no sea demasiado pesado. 

Luego nos socilicitan hacer una EDA en general para ver la presencia de outliers y ver si es necesario que sean borrados. Este paso lo podemos encontrar en **`02_ETL_EDA.ipynb`**.<br>
Como puntos importantes en esta parte tenemos:
+ Se establecen las relaciones de los archivos que se ven en el siguiente cuadro:

|steam_games|steam_games_genres|user_items|user_items_list|user_reviews|
|-|-|-|-|-|
| | |***steam_id***|***steam_id***|***steam_id***|
|***item_id***|***item_id***||***item_id***|***item_id***|
|item_name|genres|user_id|playtime_forever|posted|
|developer||items_count| |recommend|
|release_year| | | |sentiment_analysis|
|price| | | |review|
+ Se encuentran outliers en steam_games en la columna Year que es tratada
+ Tambien encontramos que la columna price tiene demasiados elementos que se consideran outliers por lo que buscaremos que la distribución de esta columna se asemeje a una distribución normal mediante el `método boxcox`, luego obtenemos los outliers resultantes despues de la transformación. Una vez realizado este procedimiento se coteja  que los outliers no son producto de data errada por lo que no se realiza un cambio posterior, este paso tambien se realiza con la columna items_count de user_items y arroja el mismo resultado.

Tambien nos solicitan el desarrollo de una api con FastAPI, asi tambien como el desarrollo de 5 funciones que deben poder ser consumidas por esta api, para ello primero se dasarrollaron las funciones por separado y las podemos encontrar asi en el archivo **`03_Funciones.ipynb`**. Luego se junta todo en el archivo **`main.py`** y en este mismo archivo es donde se arma la API y se despliega de forma local con Uvicorn.

Luego para el despliegue de esta api se usa el servicio de **`render.com`**.
Para este punto es importante tener en cuenta que el servicio solo ofrece un espacio limitado a 512 mb en su versión gratuita por lo que en las funciones del archivo **`main.py`** se usa lazy charge en las funciones para que de esa forma solo se cargue lo necesario para cada solicitud y asi no se sobrecargue el sistema.

Para el sistema de recomendacion item-item se uso `similitud coseno` y se usaron como base los generos del videojuego. El desarrollo de este paso lo podemos encontrar en el archivo **`04_ML.ipynb`**

El archivo **`final_main.py`** contiene no solo las funciones del archivo **`main.py`** sino tambien el sistema de recomendación item-item, la razon para tener dos archivos main es debido a que, como ya se menciono, solo se cuenta con un espacio de 512 mb por lo que entrenar el modelo con esas limitaciones no es posible, por lo que el archivo con el sistema de recomendacion necesita una mayor cantidad de espacio.

Para la demostración correspondiente podemos dirigirnos al siguiente [link](https://drive.google.com/file/d/1pwKceWnqWMxy79boBnTeCNiYiUh3dA0c/view)
  

<div style="text-align: right;">
  
Contacto:  
Erwin Alain Felix Tayro Mosqueira  
erwin.aftm@gmail.com<br>
[Linkedin](https://www.linkedin.com/in/alain-tayro/)
</div>
