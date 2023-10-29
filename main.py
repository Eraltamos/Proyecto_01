from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Modelo Pydantic para recibir el desarrollador en la solicitud
class DeveloperRequest(BaseModel):
    developer: str

# Modelo Pydantic para recibir el género en la solicitud
class GenreRequest(BaseModel):
    genero: str

# Modelo Pydantic para recibir el id en la solicitud
class UserRequest(BaseModel):
    user_id: str

# Modelo Pydantic para recibir el año en la solicitud
class YearRequest(BaseModel):
    año: int

# Función para obtener la cantidad de items y porcentaje de contenido gratuito por año
@app.post('/developer/')
def developer(request: DeveloperRequest):

    # Cargar los archivos Parquet
    steam_games_df = pd.read_parquet("dataset/steam_games.parquet")

    developer_name = request.developer
    
    # Filtrar las filas que coinciden con el desarrollador
    developer_df = steam_games_df[steam_games_df['developer'] == developer_name]
    
    # Convertir años a tipos de datos nativos de Python
    developer_df['release_year'] = developer_df['release_year'].astype(int)

    # Calcular la cantidad de items y el porcentaje de contenido gratuito por año
    result = []
    for year in sorted(developer_df['release_year'].unique(), reverse=False):
        year_items = len(developer_df[developer_df['release_year'] == year])
        year_free_items = len(developer_df[(developer_df['release_year'] == year) & (developer_df['price'] == 0)])
        year_percentage_free = (year_free_items / year_items) * 100 if year_items > 0 else 0
        
        result.append({
            "Año": int(year),
            "Cantidad de Items": int(year_items),
            "Contenido Free": f"{int(year_percentage_free):.2f}%"
        })

    return result

@app.post('/userforgenre/')
def UserForGenre(request: GenreRequest):
    genero = request.genero

    # Cargar los archivos Parquet
    steam_games_df = pd.read_parquet("dataset/steam_games.parquet")
    steam_games_genre_df = pd.read_parquet("dataset/steam_games_genre.parquet")
    user_items_df = pd.read_parquet("dataset/user_items.parquet")
    user_items_list_df = pd.read_parquet("dataset/user_items_list.parquet")

    # Filtrar los juegos que pertenecen al género especificado
    games_in_genre = steam_games_genre_df[steam_games_genre_df['genres'].str.contains(genero, case=False)]

    if games_in_genre.empty:
        return {"error": "Género no encontrado"}

    # Obtener una lista de los item_id de los juegos en el género
    item_ids_in_genre = games_in_genre['item_id'].tolist()

    # Filtrar los registros de user_items_list para obtener las horas jugadas de los juegos en el género
    genre_playtime = user_items_list_df[user_items_list_df['item_id'].isin(item_ids_in_genre)]

    if genre_playtime.empty:
        return {"error": "No hay datos de horas jugadas para este género"}

    # Utilizar merge para combinar genre_playtime con steam_games_df
    merged_df = genre_playtime.merge(steam_games_df[['item_id', 'release_year']], on='item_id', how='inner')

    # Fusionar merged_df con user_items_df para obtener el user_id
    merged_df = merged_df.merge(user_items_df[['steam_id', 'user_id']], left_on='steam_id', right_on='steam_id', how='inner')

    # Calcular las horas jugadas por usuario y año
    user_playtime_by_year = (merged_df.groupby(['user_id', 'release_year'])['playtime_forever'].sum()
                            .reset_index()
                            .rename(columns={'user_id': 'Usuario', 'release_year': 'Año', 'playtime_forever': 'Horas'})
                            )

    # Encontrar el usuario con más horas jugadas para el género
    user_with_most_playtime = user_playtime_by_year.groupby('Usuario')['Horas'].sum().idxmax()

    # Filtrar las horas jugadas por usuario
    user_hours = user_playtime_by_year[user_playtime_by_year['Usuario'] == user_with_most_playtime]

    # Eliminar usuario de la tabla para que no se repita
    user_hours = user_hours.drop(['Usuario'], axis=1)

    # Crear el resultado final
    result = {
        "Usuario con más horas jugadas para Género " + genero: user_with_most_playtime,
        "Horas jugadas": user_hours.to_dict(orient='records')
    }

    return result

@app.post("/userdata")
def get_user_data(request: UserRequest):

    user_id = request.user_id

    # Cargar los archivos Parquet
    steam_games_df = pd.read_parquet("dataset/steam_games.parquet")
    user_items_df = pd.read_parquet("dataset/user_items.parquet")
    user_items_list_df = pd.read_parquet("dataset/user_items_list.parquet")
    user_reviews_df = pd.read_parquet("dataset/user_reviews.parquet")

    # Filtrar la fila correspondiente al user_id en user_items_df
    user_row = user_items_df[user_items_df['user_id'] == user_id]

    if user_row.empty:
        return {"error": "Usuario no encontrado"}

    # Obtener la cantidad de items del usuario
    items_count = int(user_row['items_count'].values[0])

    # Obtener el steam_id del usuario
    steam_id = user_row['steam_id'].values[0]

    # Filtrar las filas correspondientes a este steam_id en user_items_list_df
    user_item_rows = user_items_list_df[user_items_list_df['steam_id'] == steam_id]

    # Encontrar los item_id correspondientes
    item_ids = user_item_rows['item_id'].tolist()

    # Filtrar las filas correspondientes en steam_games_df y obtener los precios
    prices = steam_games_df[steam_games_df['item_id'].isin(item_ids)]['price']

    # Calcular el dinero gastado por el usuario
    money_spent = prices.sum()

    # Filtrar las reviews correspondientes a este steam_id
    user_reviews = user_reviews_df[user_reviews_df['steam_id'] == steam_id]

    # Contar las reviews recomendadas
    recommended_reviews = user_reviews[user_reviews['recommend'] == 1]
    total_reviews = len(user_reviews)

    # Calcular el porcentaje de recomendación
    if total_reviews > 0:
        recommendation_percentage = (len(recommended_reviews) / total_reviews) * 100
    else:
        recommendation_percentage = 0

    # Crear el resultado final
    result = {
        "Usuario X": user_id,
        "Dinero gastado": f"{money_spent:.2f} USD",
        "% de recomendación": f"{recommendation_percentage:.2f}%",
        "cantidad de items": items_count
    }

    return result



@app.post("/best_developer_year")
def get_best_developers(request: YearRequest):

    año = request.año

    # Cargar los archivos Parquet
    steam_games_df = pd.read_parquet("dataset/steam_games.parquet")
    user_reviews_df = pd.read_parquet("dataset/user_reviews.parquet")

        # Paso 1: Filtrar el DataFrame de steam_games para obtener los juegos del año dado
    games_of_year = steam_games_df[steam_games_df['release_year'] == año][['item_id', 'developer']]

    # Paso 2: Filtrar el DataFrame de user_reviews para obtener las reviews recomendadas y positivas
    positive_reviews = user_reviews_df[(user_reviews_df['recommend'] == 1) & (user_reviews_df['sentiment_analysis'] == 2)][['item_id']]

    # Paso 3: Contar las reviews recomendadas y positivas por juego
    recommendations_per_game = positive_reviews['item_id'].value_counts().reset_index()
    recommendations_per_game.columns = ['item_id', 'recommendation_per_game']

    # Paso 4: Fusionar los DataFrames de juegos y recomendaciones
    merged_df = games_of_year.merge(recommendations_per_game, on='item_id', how='inner')

    # Paso 5: Calcular la suma de recomendaciones por desarrollador
    developer_recommendations = merged_df.groupby('developer')['recommendation_per_game'].sum().reset_index()

    # Paso 6: Ordenar los desarrolladores por recomendaciones en orden descendente
    top_developers = developer_recommendations.sort_values(by='recommendation_per_game', ascending=False).head(3)

    # Paso 7: Formatear el resultado en el formato deseado
    result = [{"Puesto " + str(i+1): developer} for i, developer in enumerate(top_developers['developer'])]

    return result

@app.post("/developer_reviews_analysis")
def get_developer_reviews_analysis(request: DeveloperRequest):
    developer = request.developer

    # Cargar los archivos Parquet
    steam_games_df = pd.read_parquet("dataset/steam_games.parquet")
    user_reviews_df = pd.read_parquet("dataset/user_reviews.parquet")

    # Paso 1: Filtrar el DataFrame de steam_games para obtener los juegos del desarrollador
    games_of_developer = steam_games_df[steam_games_df['developer'] == developer][['item_id']]

    # Paso 2: Filtrar el DataFrame de user_reviews para obtener las reviews relacionadas a estos juegos
    reviews_of_developer = user_reviews_df[user_reviews_df['item_id'].isin(games_of_developer['item_id'])]

    # Paso 3: Filtrar las reviews con sentiment_analysis igual a 2 (positivo) y 0 (negativo)
    positive_reviews = reviews_of_developer[reviews_of_developer['sentiment_analysis'] == 2]
    negative_reviews = reviews_of_developer[reviews_of_developer['sentiment_analysis'] == 0]

    # Paso 4: Contar la cantidad de reseñas positivas y negativas
    positive_count = len(positive_reviews)
    negative_count = len(negative_reviews)

    # Paso 5: Crear el diccionario de resultado
    result = {developer: {"Negative": negative_count, "Positive": positive_count}}

    return result
