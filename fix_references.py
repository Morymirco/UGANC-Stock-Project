import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remplacer FONTS par self.FONTS
    content = re.sub(r'(?<!self\.)FONTS\[', 'self.FONTS[', content)
    
    # Remplacer COLORS par self.COLORS
    content = re.sub(r'(?<!self\.)COLORS\[', 'self.COLORS[', content)
    
    # Remplacer SIZES par self.SIZES
    content = re.sub(r'(?<!self\.)SIZES\[', 'self.SIZES[', content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

if __name__ == "__main__":
    file_path = r"c:\Users\HP\Documents\University Projects\UGANC-Stock-Project\ui\screens\article_manager.py"
    fix_file(file_path)
    print("Les références ont été corrigées avec succès !")
