"""
Funciones de utilidad para procesamiento de libros
"""

import re
import os
from typing import List, Tuple


def read_txt(filepath: str) -> str:
    """
    Lee un archivo de texto probando múltiples encodings.
    
    Args:
        filepath: Ruta al archivo
    
    Returns:
        Contenido del archivo como string
    """
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    
    raise ValueError(f"No se pudo leer {filepath} con ningún encoding conocido")


def strip_gutenberg_headers(text: str) -> str:
    """
    Elimina los headers y footers de Project Gutenberg.
    
    Project Gutenberg añade información al principio y final de cada libro:
    - Header: Licencia, información del proyecto
    - Footer: Más información de licencia
    
    Args:
        text: Texto completo del libro
    
    Returns:
        Texto limpio sin headers/footers
    """
    # Patrones comunes de inicio
    start_patterns = [
        r'\*\*\*\s*START OF (THIS|THE) PROJECT GUTENBERG.*?\*\*\*',
        r'\*\*\*START OF (THIS|THE) PROJECT GUTENBERG.*?\*\*\*',
        r'START OF (THIS|THE) PROJECT GUTENBERG',
    ]
    
    # Patrones comunes de fin
    end_patterns = [
        r'\*\*\*\s*END OF (THIS|THE) PROJECT GUTENBERG.*?\*\*\*',
        r'\*\*\*END OF (THIS|THE) PROJECT GUTENBERG.*?\*\*\*',
        r'END OF (THIS|THE) PROJECT GUTENBERG',
    ]
    
    # Buscar inicio (tomar texto después del marker)
    start_idx = 0
    for pattern in start_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            start_idx = match.end()
            break
    
    # Buscar fin (tomar texto antes del marker)
    end_idx = len(text)
    for pattern in end_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            end_idx = match.start()
            break
    
    # Extraer texto limpio
    clean_text = text[start_idx:end_idx].strip()
    
    return clean_text


def preprocess_text(text: str, language='english') -> List[str]:
    """
    Preprocesa el texto aplicando los 4 filtros:
    1. Minúsculas
    2. Tokenización (con NLTK)
    3. Eliminación de signos especiales/puntuación
    4. Stopwords (con NLTK)
    
    Args:
        text: Texto a procesar
        language: Idioma del texto ('english', 'spanish', etc.)
    
    Returns:
        Lista de tokens limpios
    """
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    
    # 1. Convertir a minúsculas
    text = text.lower()
    
    # 2. Tokenización con NLTK
    tokens = word_tokenize(text)
    
    # 3. Eliminar puntuación, números y signos especiales
    # Mantener solo palabras alfabéticas de 2+ caracteres
    tokens = [token for token in tokens if token.isalpha() and len(token) >= 2]
    
    # 4. Eliminar stopwords con NLTK
    stop_words = set(stopwords.words(language))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens


def load_all_books(data_dir: str, max_books: int = None) -> List[Tuple]:
    """
    Carga todos los libros de un directorio.
    
    Args:
        data_dir: Directorio con archivos .txt
        max_books: Máximo número de libros a cargar (None = todos)
    
    Returns:
        Lista de tuplas (book_id, filename, text, tokens)
    """
    books = []
    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.txt')])
    
    if max_books:
        files = files[:max_books]
    
    print(f"📚 Cargando {len(files)} libros desde {data_dir}/")
    
    for i, fname in enumerate(files, 1):
        try:
            # Extraer ID del libro
            book_id = os.path.splitext(fname)[0]
            filepath = os.path.join(data_dir, fname)
            
            # Leer archivo
            raw_text = read_txt(filepath)
            
            # Limpiar headers de Gutenberg
            clean_text = strip_gutenberg_headers(raw_text)
            
            # Preprocesar
            tokens = preprocess_text(clean_text)
            
            # Filtrar libros muy cortos
            if len(tokens) < 50:
                print(f"  ⚠️  Saltando {fname} (muy corto: {len(tokens)} tokens)")
                continue
            
            books.append((book_id, fname, clean_text, tokens))
            
            # Mostrar progreso cada 10 libros
            if i % 10 == 0:
                print(f"  ✓ Procesados {i}/{len(files)} libros")
        
        except Exception as e:
            print(f"  ✗ Error procesando {fname}: {e}")
            continue
    
    print(f"✅ Total de libros cargados exitosamente: {len(books)}\n")
    return books


def get_book_title_from_text(text: str, max_chars: int = 100) -> str:
    """
    Intenta extraer el título del libro del texto.
    
    Args:
        text: Texto del libro
        max_chars: Máximo de caracteres a considerar
    
    Returns:
        Primera línea no vacía (posible título)
    """
    lines = text.split('\n')
    for line in lines[:10]:  # Buscar en primeras 10 líneas
        line = line.strip()
        if line and len(line) <= max_chars:
            return line
    return "Unknown Title"