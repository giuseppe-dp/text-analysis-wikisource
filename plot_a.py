import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

# Impostiamo lo stile generale
plt.style.use('bmh')
plt.rc('font', family='serif', serif='Times New Roman')
# Diciamo a Matplotlib di usare un font compatibile con la matematica
plt.rcParams['mathtext.fontset'] = 'cm'

plt.rcParams.update({'font.size': 10})        # Font base
plt.rcParams.update({'axes.titlesize': 10})   # Titoli dei grafici
plt.rcParams.update({'axes.labelsize': 10})   # Label dei grafici
plt.rcParams.update({'legend.fontsize': 8})   # Legenda
plt.rcParams.update({'lines.linewidth': 1})   # Larghezza linee
plt.rcParams.update({'lines.markersize': 5})  # Grandezza marker

# carichiamo i dati del csv in df
cartella_script = Path(__file__).parent
file_dati = cartella_script / 'books_words_data.csv'
df = pd.read_csv(file_dati, sep=',')
df['word_position'] = pd.to_numeric(df['word_position'])

# Verifichiamo di aver importato tutto correttamente stampando le prime 5 righe
print(df.head())


#-----------------------------------------------------------------------------------------
# a. Come aumenta il numero di parole distinte utilizzate con la lunghezza di un testo?
#    a1 - se si tronca uno stesso testo a lunghezze diverse
#    a2 - se confronto testi diversi (di lunghezza diversa)
#-----------------------------------------------------------------------------------------

# Creiamo una figura con 2 grafici affiancati
width  = 7
height = width / 1.618

fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(width, height))
fig1.suptitle('Andamento parole distinte utilizzate con la lunghezza di un testo', fontweight='bold')

# a1:

# Calcolo della crescita per ogni libro
# Usiamo un ciclo per calcolare la curva di ogni libro separatamente
for book_name in df['book'].unique():
  # Filtriamo il dataframe per il libro corrente
  df_book = df[df['book'] == book_name].copy()
  
  # Identifichiamo le parole uniche: True (1) se la parola non è un duplicato
  df_book['is_unique'] = ~df_book['word'].duplicated()
  
  # Somma cumulata dei True: otteniamo il numero di parole distinte a ogni posizione (word_position)
  df_book['unique_growth'] = df_book['is_unique'].cumsum()
  #print(df_book)

  if book_name == "Romanzo_dei_Tre_Regni":
    # plottiamo la linea nera per il book cinese
    ax1.plot(df_book['word_position'], df_book['unique_growth'], color='black', linestyle='--', label=book_name.replace('_', ' '))
  else:
    # plottiamo la linea per ogni book italiano
    ax1.plot(df_book['word_position'], df_book['unique_growth'], label=book_name.replace('_', ' '))

ax1.set_title('Troncamento stesso testo a lunghezze diverse')
ax1.set_xlabel('Numero totale di parole nel testo (N)')
ax1.set_ylabel('Numero di parole distinte (V)')
ax1.legend(loc='center right')

#a2:

for book_name in df['book'].unique():
  # Filtriamo il dataframe per il libro corrente
  df_book = df[df['book'] == book_name].copy()
  
  # Identifichiamo le parole uniche: True (1) se la parola non è un duplicato
  df_book['is_unique'] = ~df_book['word'].duplicated()
  
  # Somma cumulata dei True: otteniamo il numero di parole distinte a ogni posizione (word_position)
  distinct_words = df_book['is_unique'].sum()
  book_lenght = df_book['word_position'].max()

  if book_name == "Romanzo_dei_Tre_Regni":
    # Disegniamo il punto nero di questo book cinese e gli diamo la sua label
    ax2.scatter(book_lenght, distinct_words, color='black', label=book_name.replace('_', ' '))
    print(distinct_words)
  else:
    # Disegniamo il punto di questo book ita e gli diamo la sua label
    ax2.scatter(book_lenght, distinct_words, label=book_name.replace('_', ' '))

ax2.set_title('Testi con lunghezza diversa')
ax2.set_xlabel('Numero totale di parole nel testo (N)')
ax2.set_ylabel('Numero di parole distinte (V)')
'''ax2.set_xscale('log')
ax2.set_yscale('log')'''
ax2.grid(True)
ax2.legend(loc='center right')

# salvo il plot in PDF
plt.tight_layout()
cartella_salvataggio = cartella_script / 'latex'
percorso_finale = cartella_salvataggio / f'Andamento_parole_di_un_testo.pdf'
fig1.savefig(percorso_finale, format='pdf', bbox_inches='tight')
print(f"Salvato con successo in: {percorso_finale}")


#-----------------------------------------------------------------------------------------
# b. come si comporta l’istogramma di occorrenza delle parole (numero, frazione, o densita’ di parole usate n volte)?
#    b1 - se si tronca uno stesso testo a lunghezze diverse
#    b2 - in testi diversi
#-----------------------------------------------------------------------------------------

fig2, (bx1, bx2) = plt.subplots(1, 2, figsize=(width, height))
fig2.suptitle("Comportamento dell’istogramma di occorrenza delle parole", fontweight='bold')

# b1:

# Calcolo dell occorrenza delle parole per un libro specifico
book_name = df['book'].unique()[2]

# estraiamo i dati per un libro specifico
df_book = df[df['book'] == book_name].copy()

L = 5000           # Punto di partenza
moltiplicatore = 3 # fattore di crescita
book_lenght = len(df_book)

while L < book_lenght:
  # Esegui lo slicing e il plot
  df_troncato = df_book.iloc[:L]
  counts = df_troncato['word'].value_counts().value_counts().sort_index()
  bx1.loglog(counts.index, counts.values, label=f'Parole: {L}')
  
  # Incremento geometrico
  L = int(L * moltiplicatore)

# ultimo plot per il libro completo
df_completo = df_book
counts_fine = df_completo['word'].value_counts().value_counts().sort_index()
bx1.loglog(counts_fine.index, counts_fine.values, label=f'Libro completo ({book_lenght})')

bx1.set_title(f'Testo troncato a lunghezze diverse ({book_name.replace('_', ' ')})')
bx1.set_xlabel('Numero di occorrenze (N)')
bx1.set_ylabel('Numero di parole con N occorrenze')
bx1.legend(loc='upper right')

#b2:

for book_name in df['book'].unique():
  # Filtriamo il dataframe per il libro corrente
  df_book = df[df['book'] == book_name].copy()
  
  counts = df_book['word'].value_counts().value_counts().sort_index()

  if book_name == "Romanzo_dei_Tre_Regni":
    bx2.loglog(counts.index, counts.values, color='black', linestyle='--', label=book_name.replace('_', ' '))
  else:
    bx2.loglog(counts.index, counts.values, label=book_name.replace('_', ' '))

bx2.set_title('Testi diversi')
bx2.set_xlabel('Numero di occorrenze (N)')
bx2.set_ylabel('Numero di parole con N occorrenze')
bx2.legend(loc='upper right')

# salvo il plot in PDF
plt.tight_layout()
percorso_finale = cartella_salvataggio / f'Istogramma_di_occorrenza.pdf'
fig2.savefig(percorso_finale, format='pdf', bbox_inches='tight')
print(f"Salvato con successo in: {percorso_finale}")

plt.show()