"""
Script para descargar los 100 libros más descargados de Project Gutenberg
Ejecutar: python src/download_books.py
"""

import requests
import time
import os
from pathlib import Path

# Top 100 libros más descargados de Project Gutenberg (actualizado 2024)
# Fuente: https://www.gutenberg.org/browse/scores/top
TOP_100_BOOKS = [
    1342, 11, 84, 1661, 2701, 1952, 174, 98, 5200, 345,
    43, 1080, 76, 1260, 46, 2542, 74, 1497, 16, 219,
    1232, 100, 1399, 2600, 209, 1184, 205, 844, 1322, 36,
    2591, 1400, 2554, 4300, 158, 1250, 244, 1998, 730, 1727,
    768, 2814, 161, 41, 1259, 58, 996, 5740, 514, 2148,
    1251, 3296, 120, 45, 23, 37106, 1112, 3825, 2000, 1404,
    135, 105, 375, 64317, 6130, 19033, 25344, 28054, 215, 4363,
    1998, 7849, 8492, 3207, 30254, 2500, 160, 2265, 829, 103,
    4085, 132, 1695, 203, 113, 17135, 408, 1400, 1155, 2852,
    3600, 599, 55, 14838, 61, 2097, 15399, 67979, 1257, 15695
]

def download_book(book_id, save_dir="data"):
    """
    Descarga un libro de Project Gutenberg por su ID.
    
    Args:
        book_id: ID del libro en Project Gutenberg
        save_dir: Directorio donde guardar el archivo
    
    Returns:
        True si se descargó exitosamente, False en caso contrario
    """
    # Crear directorio si no existe
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    # URL del libro (formato UTF-8 plain text)
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
    # URL alternativa (formato ASCII)
    url_alt = f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt"
    
    filepath = os.path.join(save_dir, f"{book_id}.txt")
    
    # Si ya existe, saltar
    if os.path.exists(filepath):
        print(f"  ✓ {book_id}.txt ya existe")
        return True
    
    # Intentar descargar
    for attempt_url in [url, url_alt]:
        try:
            response = requests.get(attempt_url, timeout=30)
            
            if response.status_code == 200:
                # Guardar archivo
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"  ✓ Descargado: {book_id}.txt")
                return True
            
        except Exception as e:
            continue
    
    print(f"  ✗ Error descargando {book_id}: No se pudo acceder")
    return False


def download_all_books(book_ids=TOP_100_BOOKS, save_dir="data", delay=2):
    """
    Descarga múltiples libros con delay entre peticiones.
    
    Args:
        book_ids: Lista de IDs de libros
        save_dir: Directorio de destino
        delay: Segundos de espera entre descargas (para no sobrecargar servidor)
    """
    print("="*60)
    print("📚 DESCARGADOR DE PROJECT GUTENBERG")
    print("="*60)
    print(f"\nDescargando {len(book_ids)} libros...")
    print(f"Directorio: {save_dir}/\n")
    
    successful = 0
    failed = 0
    
    for i, book_id in enumerate(book_ids, 1):
        print(f"[{i}/{len(book_ids)}] Libro {book_id}:")
        
        if download_book(book_id, save_dir):
            successful += 1
        else:
            failed += 1
        
        # Delay para no sobrecargar el servidor
        if i < len(book_ids):
            time.sleep(delay)
    
    print("\n" + "="*60)
    print(f"✅ Descarga completada:")
    print(f"   Exitosos: {successful}")
    print(f"   Fallidos: {failed}")
    print("="*60)


if __name__ == "__main__":
    # Ejecutar descarga
    download_all_books(
        book_ids=TOP_100_BOOKS,
        save_dir="data",
        delay=1  # 1 segundo entre descargas
    )