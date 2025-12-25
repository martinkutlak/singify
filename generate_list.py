import os
import json
import urllib.parse

def generate_json():
    pdf_dir = 'pdf'
    songs = []
    
    if not os.path.exists(pdf_dir):
        print(f"Chyba: Složka '{pdf_dir}' neexistuje.")
        return

    files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    
    for filename in files:
        try:
            clean_name = filename.replace('.pdf', '')
            # Rozdělení podle dvojitých podtržítek: [ID_Nazev, Interpret, Capo]
            parts = clean_name.split('__')
            
            left_part = parts[0]
            artist_part = parts[1] if len(parts) > 1 else "Neznámý interpret"
            capo_part = parts[2] if len(parts) > 2 else "" # Tady získáme "capo_3"
            
            # Získání ID a Názvu
            first_underscore = left_part.find('_')
            id_song = left_part[:first_underscore]
            title_part = left_part[first_underscore+1:]
            
            def format_text(s):
                return s.replace('_', ' ').strip().title()

            songs.append({
                "id": id_song,
                "title": format_text(title_part),
                "artist": format_text(artist_part),
                "capo": capo_part.replace('_', ' '), # "capo_3" -> "capo 3"
                "url": f"pdf/{urllib.parse.quote(filename)}"
            })
        except Exception as e:
            print(f"Chyba u {filename}: {e}")

    songs.sort(key=lambda x: x['id'])
    with open('songs.json', 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=4)
    print(f"Hotovo! Zpracováno {len(songs)} písniček.")

if __name__ == "__main__":
    generate_json()
