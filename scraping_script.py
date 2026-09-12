from playwright.sync_api import sync_playwright
import time
import random
import re

def scraping_data(language = "it", book_name: str = "Don_Chisciotte_della_Mancia"):
  domain = f"{language}.wikisource.org"
  url = f"https://{domain}/wiki/{book_name}"
  full_text = []

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=True se vuoi senza finestra
    page = browser.new_page()

    try:
      page.goto(url, timeout=5000)
      print("cerco nella pagina:", page)
    except Exception as e:
      print(f"Errore nel caricamento della pagina {url}: {e}")
      browser.close()
      return full_text, book_name

    # Estraiamo tutti gli href dai tag <a> dentro la classe .tl-testo-link (i vari capitoli)
    links = page.locator(".tl-testo-link a").evaluate_all("elements => elements.map(e => e.href)")

    for link in links:
      page.goto(link)
      # Definiamo i possibili contenitori dal più specifico al più generico
      target_classes = [".prp-pages-output", ".mw-parser-output"]
    
      chapter_text = ""
    
      for selector in target_classes:
        locator = page.locator(selector)
        # Controlliamo se l'elemento è presente e visibile
        if locator.count() > 0:
          print(f"Trovato contenuto con selettore: {selector}")
          chapter_text = locator.first.inner_text()
          break # Esci dal ciclo appena trovi qualcosa
            
      if not chapter_text:
        print(f"ATTENZIONE: Nessun contenuto trovato per {book_name}")
      else:
        full_text.append(chapter_text)

      time.sleep(random.uniform(1, 3))

    browser.close()

    testo = "\n".join(full_text)
    # Aggiungiamo encoding="utf-8" per evitare errori con simboli e lingue diverse
    with open(f"books/{book_name}.txt", "w", encoding="utf-8") as file:
      file.write(testo)
    return testo, book_name
  

if __name__ == "__main__":
  book_name = "Uno,_nessuno_e_centomila" 
  book_language = "it"
  testo , book_name = scraping_data(language=book_language, book_name=book_name)

  # Aggiungiamo encoding="utf-8" per evitare errori con simboli e lingue diverse
  with open(f"books/{book_name}.txt", "w", encoding="utf-8") as file:
    file.write(testo)

  print("Download completato e file salvato correttamente!")