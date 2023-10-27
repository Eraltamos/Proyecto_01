from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# Cargar los datos desde el archivo CSV (suponiendo que ya los tienes en un DataFrame)
steam_games_df = pd.read_csv("steam_games.csv")

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Modelo Pydantic para recibir el desarrollador en la solicitud
class DeveloperRequest(BaseModel):
    developer: str

# Función para obtener la cantidad de items y porcentaje de contenido gratuito por año
@app.post('/developer/')
def developer(request: DeveloperRequest):
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