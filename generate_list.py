import os
import json
import urllib.parse

def generate_json():
    pdf_dir = 'pdf'
    songs = []
    
    if not os.path.exists(pdf_dir):
        print(f"Chyba: Složka '{pdf_dir}' neexistuje.")
        return

    # Projít všechny soubory v /pdf
    files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    for filename in files:
        try:
            # Odstranit .pdf a rozdělit podle '__'
            clean_name = filename.replace('.pdf', '')
            parts = clean_name.split('__')
            
            left_part = parts[0]
            artist_part = parts[1] if len(parts) > 1 else "Neznámý interpret"
            
            # Získat ID (před prvním podtržítkem)
            first_underscore = left_part.find('_')
            id_song = left_part[:first_underscore]
            title_part = left_part[first_underscore+1:]
            
            # Formátování textu (náhrada _ za mezeru a velká písmena)
            def format_text(s):
                return s.replace('_', ' ').title()

            songs.append({
                "id": id_song,
                "title": format_text(title_part),
                "artist": format_text(artist_part),
                # URL pro GitHub Pages
                "url": f"pdf/{urllib.parse.quote(filename)}"
            })
        except Exception as e:
            print(f"Chyba při zpracování souboru {filename}: {e}")

    # Seřazení podle ID
    songs.sort(key=lambda x: x['id'])

    with open('songs.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=4)
    
    print(f"Hotovo! Zpracováno {len(songs)} písniček do songs.json.")

if __name__ == "__main__":
    generate_json()
