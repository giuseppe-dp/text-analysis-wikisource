from gestione_data import process_book_to_dataframe
from scraping_script import scraping_data
import os
import pandas as pd

if __name__ == "__main__":
  # ho tolto {"name": "Don_Chisciotte_della_Mancia"}
  books_to_mine = [
    {"name": "Le_avventure_di_Pinocchio", "language": "it"},
    {"name": "I_Malavoglia", "language": "it"}, 
    {"name": "La_coscienza_di_Zeno", "language": "it"}, 
    {"name": "Gli_sposi_promessi", "language": "it"}, 
    {"name": "Le_tigri_di_Mompracem", "language": "it"},
    {"name": "Romanzo_dei_Tre_Regni", "language": "zh"}
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
      raw_content, book_name = scraping_data(book_name=book['name'], language=book["language"])
      
      with open(filename, "w", encoding="utf-8") as f:
        f.write(raw_content) 
    
    df_book = process_book_to_dataframe(book['name'], raw_content, language=book["language"])
    all_data.append(df_book)

  # Unisci tutto in un unico mega-dataset
  final_df = pd.concat(all_data, ignore_index=True)

  # Salva in formato compresso (CSV)
  print("creazione del database in panda...")
  final_df.to_csv("books_words_data.csv", index=False)
  print("Database creato!")
