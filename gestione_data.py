from scraping_script import scraping_data
import pandas as pd
import re
import os
import regex

  
def pulizia(testo_grezzo, book_name, language = "it"):

  if language == "zh":
    # Per il cinese estraiamo ogni singolo carattere Hanzi
    # Questo ignora punteggiatura e spazi cinesi
    # words = re.findall(r'[\u4e00-\u9fff]', testo_grezzo)
    words = regex.findall(r'\p{IsHan}', testo_grezzo) # Prende TUTTI i caratteri Han esistenti
  else:
    # Rimuovi i riferimenti alle pagine di Wikisource: [p. 123 modifica]
    # cerca '[' seguito da qualsiasi carattere fino a ']'
    testo = re.sub(r'\[.*?\]', ' ', testo_grezzo)

    # Gestione apostrofi e simboli speciali
    # Sostituiamo apostrofi e trattini con uno spazio per separare le parole
    testo = testo.replace("'", " ").replace("—", " ").replace("’", " ")

    # Minuscolo e Rimozione Punteggiatura residua
    testo = testo.lower()

    # Teniamo solo caratteri alfabetici (vogliamo solo parole)
    # Questa regex cancella tutto ciò che NON è una lettera a-z o spazi
    testo = re.sub(r'[^a-z\s]', ' ', testo)

    # Creazione lista e rimozione spazi bianchi in eccesso
    words = testo.split()

  with open(f"books_words/words_{book_name}.txt", "w", encoding="utf-8") as f:
    for item in words:
      f.write(f"{item}\n") # Scrive ogni elemento su una nuova riga
  
  return words

def process_book_to_dataframe(book_name, raw_text, language='it'):
  """
  Prende il testo grezzo di un libro e restituisce un DataFrame 
  con una parola per riga.
  """

  path_parole = f"books_words/words_{book_name}.txt"

  # Recupero la lista di parole (o dalla cache o pulendo il testo)
  if os.path.exists(path_parole):
    print(f"Caricamento parole pulite da cache: {book_name}")
    with open(path_parole, "r", encoding="utf-8") as f:
      words = f.read().splitlines()
  else:
    print(f"Pulizia parole per: {book_name}")
    words = pulizia(raw_text, book_name, language=language)
  
  # creaione dataframe
  df = pd.DataFrame({
    'book': book_name,
    'word': words,
    'language': language
  })
  df['word_position'] = range(1, len(words) + 1)
  
  return df


if __name__ == "__main__":
  books_to_mine = [
    {"name": "Don_Chisciotte_della_Mancia", "language": "it"},
    {"name": "三國演義", "language": "zh"}
  ]

  all_data = []

  for book in books_to_mine:
    filename = f"books/{book['name']}.txt"

    # controllo se il file esiste già nella cartella books
    if os.path.exists(filename):
      print(f"Lettura locale: {book['name']} trovato in cache.")
      with open(filename, "r", encoding="utf-8") as f:
        raw_content = f.read()
    else:
      print(f"Scraping in corso: {book['name']} non trovato localmente...")
      raw_content, book_name = scraping_data(language=book["language"], book_name=book['name'])
      
      with open(filename, "w", encoding="utf-8") as f:
        f.write(raw_content)
    
    df_book = process_book_to_dataframe(book['name'], raw_content, language=book["language"])
    all_data.append(df_book)

  # Unisci tutto in un unico mega-dataset
  final_df = pd.concat(all_data, ignore_index=True)

  # Salva in formato compresso (CSV)
  final_df.to_csv("prova_books_words_data.csv", index=False)