import os
import re

# Diccionario con ID -> Nombre del libro (limpio para nombres de archivo)
libros = {
    84: "Frankenstein - Mary Wollstonecraft Shelley",
    2701: "Moby Dick - Herman Melville",
    1342: "Pride and Prejudice - Jane Austen",
    1513: "Romeo and Juliet - William Shakespeare",
    46: "A Christmas Carol - Charles Dickens",
    43: "Dr Jekyll and Mr Hyde - Robert Louis Stevenson",
    100: "Complete Works of Shakespeare",
    145: "Middlemarch - George Eliot",
    11: "Alice's Adventures in Wonderland - Lewis Carroll",
    2641: "A Room with a View - E M Forster",
    8492: "The King in Yellow - Robert W Chambers",
    37106: "Little Women - Louisa May Alcott",
    67979: "The Blue Castle - L M Montgomery",
    33944: "How to Observe Morals and Manners - Harriet Martineau",
    2554: "Crime and Punishment - Fyodor Dostoyevsky",
    16389: "The Enchanted April - Elizabeth Von Arnim",
    394: "Cranford - Elizabeth Cleghorn Gaskell",
    6761: "The Adventures of Ferdinand Count Fathom - T Smollett",
    2160: "The Expedition of Humphry Clinker - T Smollett",
    4085: "The Adventures of Roderick Random - T Smollett",
    16328: "Beowulf - An Anglo-Saxon Epic Poem",
    6593: "History of Tom Jones - Henry Fielding",
    1259: "Twenty Years After - Alexandre Dumas",
    5197: "My Life Vol 1 - Richard Wagner",
    1260: "Jane Eyre - Charlotte Bronte",
    174: "The Picture of Dorian Gray - Oscar Wilde",
    345: "Dracula - Bram Stoker",
    76: "Adventures of Huckleberry Finn - Mark Twain",
    1661: "The Adventures of Sherlock Holmes - Arthur Conan Doyle",
    98: "A Tale of Two Cities - Charles Dickens",
    1998: "Thus Spake Zarathustra - Friedrich Nietzsche",
    844: "The Importance of Being Earnest - Oscar Wilde",
    768: "Wuthering Heights - Emily Bronte",
    1184: "The Count of Monte Cristo - Alexandre Dumas",
    17135: "Twas the Night before Christmas - Clement Clarke Moore",
    28054: "The Brothers Karamazov - Fyodor Dostoyevsky",
    2542: "A Doll's House - Henrik Ibsen",
    4300: "Ulysses - James Joyce",
    64317: "The Great Gatsby - F Scott Fitzgerald",
    3207: "Leviathan - Thomas Hobbes",
    25162: "Chi Pei Ou Than - Shizhen Wang",
    5200: "Metamorphosis - Franz Kafka",
    1232: "The Prince - Niccolo Machiavelli",
    25344: "The Scarlet Letter - Nathaniel Hawthorne",
    36034: "White Nights and Other Stories - Fyodor Dostoyevsky",
    8800: "The Divine Comedy - Dante Alighieri",
    74: "The Adventures of Tom Sawyer - Mark Twain",
    4363: "Beyond Good and Evil - Friedrich Nietzsche",
    1080: "A Modest Proposal - Jonathan Swift",
    7370: "Second Treatise of Government - John Locke",
    10554: "Right Ho Jeeves - P G Wodehouse",
    205: "Walden and Civil Disobedience - Henry David Thoreau",
    2600: "War and Peace - Leo Tolstoy",
    2591: "Grimms' Fairy Tales - Jacob and Wilhelm Grimm",
    4200: "The Diary of Samuel Pepys - Samuel Pepys",
    3296: "The Confessions of St Augustine",
    17199: "Golden Days for Boys and Girls Vol XII",
    45: "Anne of Green Gables - L M Montgomery",
    77410: "A Dictionary of the Art of Printing - William Savage",
    6130: "The Iliad - Homer",
    1400: "Great Expectations - Charles Dickens",
    55: "The Wonderful Wizard of Oz - L Frank Baum",
    3206: "Moby Multiple Language Lists of Common Words - Grady Ward",
    1023: "Bleak House - Charles Dickens",
    18035: "Marjorie at Seacote - Carolyn Wells",
    5740: "Tractatus Logico-Philosophicus - Ludwig Wittgenstein",
    49266: "The Wars of Religion in France 1559-1576 - James Westfall Thompson",
    72679: "The Lesser Key of Solomon - Goetia",
    408: "The Souls of Black Folk - W E B Du Bois",
    120: "Treasure Island - Robert Louis Stevenson",
    1399: "Anna Karenina - Leo Tolstoy",
    41835: "Puvis de Chavannes - Francois Crastre",
    34901: "On Liberty - John Stuart Mill",
    30254: "The Romance of Lust - Anonymous",
    1497: "The Republic - Plato",
    829: "Gulliver's Travels - Jonathan Swift",
    77411: "The Country Seats of the United States - William Birch",
    52621: "Society in America Vol 1 - Harriet Martineau",
    1727: "The Odyssey - Homer",
    17450: "The Part Borne by the Dutch in the Discovery of Australia - J E Heeres",
    1952: "The Yellow Wallpaper - Charlotte Perkins Gilman",
    40957: "Leibniz's New Essays Concerning Human Understanding - John Dewey",
    244: "A Study in Scarlet - Arthur Conan Doyle",
    26: "Paradise Lost - John Milton",
    996: "Don Quixote - Miguel de Cervantes",
    77405: "Romantic Castles and Palaces",
    2680: "Meditations - Marcus Aurelius",
    77408: "Blue Trousers - Murasaki Shikibu",
    730: "Oliver Twist - Charles Dickens",
    27827: "The Kama Sutra of Vatsyayana",
    514: "Little Women - Louisa May Alcott",
    161: "Sense and Sensibility - Jane Austen",
    135: "Les Miserables - Victor Hugo",
    56517: "The Philosophy of Auguste Comte - Lucien Levy-Bruhl",
    26315: "Shakespeare's Family - C C Stopes",
    110: "Tess of the d'Urbervilles - Thomas Hardy",
    24029: "Leng Yan Guan - Junqing Wang",
    36965: "Harriet Martineau - Florence Fenwick Miller",
    16119: "Doctrina Christiana",
    779: "The Tragical History of Doctor Faustus - Christopher Marlowe"
}

def limpiar_nombre(nombre):
    """Limpia el nombre para que sea válido como nombre de archivo"""
    # Reemplazar caracteres problemáticos
    nombre = nombre.replace(':', ' -')
    nombre = nombre.replace('/', '-')
    nombre = nombre.replace('\\', '-')
    nombre = nombre.replace('|', '-')
    nombre = nombre.replace('?', '')
    nombre = nombre.replace('*', '')
    nombre = nombre.replace('<', '')
    nombre = nombre.replace('>', '')
    nombre = nombre.replace('"', '')
    # Eliminar espacios múltiples
    nombre = re.sub(r'\s+', ' ', nombre)
    return nombre.strip()

def renombrar_archivos(directorio='.', modo_prueba=True):
    """
    Renombra archivos basándose en sus IDs del Proyecto Gutenberg
    
    Args:
        directorio: Carpeta donde están los archivos (por defecto: carpeta actual)
        modo_prueba: Si es True, solo muestra qué cambios haría sin ejecutarlos
    """
    archivos_renombrados = 0
    archivos_no_encontrados = []
    
    print(f"{'='*80}")
    print(f"MODO: {'PRUEBA (no se renombrará nada)' if modo_prueba else 'EJECUCIÓN REAL'}")
    print(f"Directorio: {os.path.abspath(directorio)}")
    print(f"{'='*80}\n")
    
    # Obtener todos los archivos en el directorio
    archivos = [f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))]
    
    for archivo in archivos:
        # Extraer el ID del nombre del archivo (busca números)
        match = re.search(r'\b(\d+)\b', archivo)
        
        if match:
            id_libro = int(match.group(1))
            
            if id_libro in libros:
                # Obtener la extensión original
                _, extension = os.path.splitext(archivo)
                
                # Crear nuevo nombre
                nuevo_nombre = limpiar_nombre(libros[id_libro]) + extension
                
                ruta_antigua = os.path.join(directorio, archivo)
                ruta_nueva = os.path.join(directorio, nuevo_nombre)
                
                print(f"✓ {archivo}")
                print(f"  → {nuevo_nombre}\n")
                
                if not modo_prueba:
                    try:
                        os.rename(ruta_antigua, ruta_nueva)
                        archivos_renombrados += 1
                    except Exception as e:
                        print(f"  ⚠ ERROR: {e}\n")
                else:
                    archivos_renombrados += 1
            else:
                archivos_no_encontrados.append(f"{archivo} (ID: {id_libro})")
    
    # Resumen
    print(f"\n{'='*80}")
    print(f"RESUMEN:")
    print(f"  - Archivos {'que se renombrarían' if modo_prueba else 'renombrados'}: {archivos_renombrados}")
    print(f"  - Archivos sin coincidencia: {len(archivos_no_encontrados)}")
    
    if archivos_no_encontrados:
        print(f"\nArchivos sin coincidencia:")
        for archivo in archivos_no_encontrados:
            print(f"  • {archivo}")
    
    print(f"{'='*80}")

if __name__ == "__main__":
    # PASO 1: Ejecutar primero en MODO PRUEBA para ver qué cambios se harían
    print("\n🔍 EJECUTANDO EN MODO PRUEBA...\n")
    renombrar_archivos(directorio='.', modo_prueba=True)
    
    # PASO 2: Descomentar la siguiente línea para ejecutar el renombrado real
    # print("\n⚠️  EJECUTANDO RENOMBRADO REAL...\n")
    # renombrar_archivos(directorio='.', modo_prueba=False)