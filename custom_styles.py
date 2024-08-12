# custom_styles.py

import json

# Paletas padrão
default_palettes = {
    'NES': [
        0, 0, 0,        # Preto
        29, 43, 83,     # Azul Escuro
        126, 37, 83,    # Roxo Escuro
        0, 135, 81,     # Verde Escuro
        171, 82, 54,    # Marrom
        95, 87, 79,     # Cinza Escuro
        194, 195, 199,  # Cinza Claro
        255, 241, 232,  # Branco
        255, 0, 77,     # Vermelho Vivo
        255, 163, 0,    # Laranja
        255, 236, 39,   # Amarelo
        0, 228, 54,     # Verde
        41, 173, 255,   # Azul Claro
        131, 118, 156,  # Roxo Claro
        255, 119, 168,  # Rosa
        255, 204, 170   # Pêssego
    ],
    'Atari 2600': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        255, 0, 0,      # Vermelho
        0, 255, 0,      # Verde
        0, 0, 255,      # Azul
        255, 255, 0,    # Amarelo
        255, 0, 255,    # Magenta
        0, 255, 255,    # Ciano
    ],
    'Windows XP': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        0, 0, 255,      # Azul
        255, 0, 0,      # Vermelho
        0, 255, 0,      # Verde
        255, 255, 0,    # Amarelo
        255, 0, 255,    # Magenta
        0, 255, 255,    # Ciano
    ],
    'Windows 95': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        0, 0, 128,      # Azul Escuro
        128, 128, 128,  # Cinza
        0, 128, 0,      # Verde
        128, 0, 0,      # Vermelho
        128, 0, 128,    # Magenta
        0, 128, 128,    # Ciano
    ],
    'Computador dos Anos 70': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        128, 128, 0,    # Oliva
        0, 128, 128,    # Ciano
        128, 0, 0,      # Vermelho Escuro
        0, 128, 0,      # Verde Escuro
        128, 128, 128,  # Cinza
        192, 192, 192,  # Cinza Claro
    ],
    'VHS': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        128, 128, 128,  # Cinza
        255, 0, 0,      # Vermelho
        0, 255, 0,      # Verde
        0, 0, 255,      # Azul
        255, 255, 0,    # Amarelo
        255, 0, 255,    # Magenta
    ],
    'Super Nintendo': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        139, 0, 0,      # Vermelho Escuro
        0, 139, 0,      # Verde Escuro
        0, 0, 139,      # Azul Escuro
        255, 255, 0,    # Amarelo
        255, 20, 147,   # Rosa
        0, 255, 255,    # Ciano
    ],
    'Sega Genesis': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        128, 128, 128,  # Cinza
        255, 0, 0,      # Vermelho
        0, 255, 0,      # Verde
        0, 0, 255,      # Azul
        255, 255, 0,    # Amarelo
        255, 0, 255,    # Magenta
    ],
    'Nintendo 64': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        0, 0, 255,      # Azul
        255, 0, 0,      # Vermelho
        0, 255, 0,      # Verde
        255, 255, 0,    # Amarelo
        255, 0, 255,    # Magenta
        0, 255, 255,    # Ciano
    ],
    'Playstation 2': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        0, 0, 128,      # Azul Escuro
        128, 0, 0,      # Vermelho Escuro
        0, 128, 0,      # Verde Escuro
        128, 128, 0,    # Oliva
        128, 0, 128,    # Magenta
        0, 128, 128,    # Ciano
    ],
    'Cinema Antigo': [
        0, 0, 0,        # Preto
        255, 255, 255,  # Branco
        128, 128, 128,  # Cinza
        192, 192, 192,  # Cinza Claro
        0, 0, 128,      # Azul Escuro
        128, 0, 0,      # Vermelho Escuro
        0, 128, 0,      # Verde Escuro
        128, 128, 0,    # Oliva
    ],
    'Sem Paleta': None  # Para a opção sem paleta específica
}


# Armazena as paletas personalizadas carregadas
custom_palettes = {}

def load_custom_palette(jrc_file_path):
    """Load a custom palette from a .jrc file."""
    try:
        with open(jrc_file_path, 'r') as f:
            data = json.load(f)
            name = data.get('name', 'Custom Style')
            palette = data.get('palette', [])
            if len(palette) % 3 != 0:
                raise ValueError("The palette must have a number of colors that is a multiple of 3.")
            return name, palette
    except Exception as e:
        raise ValueError(f"Failed to load .jrc file: {e}")

def add_custom_palette(name, palette):
    """Add a custom palette to the collection."""
    if name in custom_palettes:
        raise ValueError(f"Palette '{name}' already exists.")
    custom_palettes[name] = palette

def get_palette(name):
    """Retrieve a palette by name, either custom or default."""
    return custom_palettes.get(name) or default_palettes.get(name)

def load_palette_from_file(file_path):
    """Load a palette from a .jrc file and add it to the collection."""
    name, palette = load_custom_palette(file_path)
    add_custom_palette(name, palette)
