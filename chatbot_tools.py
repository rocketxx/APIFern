import wikipedia
from duckduckgo_search import DDGS
from datetime import datetime
import webbrowser
import re
import requests
def search_wikipedia(query):
    """Cerca un argomento su Wikipedia."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"Wikipedia: {summary}"
    except wikipedia.exceptions.PageError:
        return "Wikipedia: Nessuna pagina trovata."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Wikipedia: Ambiguità, prova con: {', '.join(e.options[:5])}"

def search_duckduckgo(query):
    """Cerca sul web usando DuckDuckGo e apre il primo link."""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        
        # Prepara la risposta da restituire
        result_str = "\n".join([f"{r['title']}: {r['href']}" for r in results])
        
        # Chiama la funzione per aprire il primo link
        open_first_link(result_str)
        
        return result_str

def save_to_txt(data, filename="research_output.txt"):
    """Salva i dati in un file di testo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Dati salvati in {filename}"

def open_first_link(risposta):
    # Utilizzare una espressione regolare per estrarre tutti i link
    links = re.findall(r'https?://\S+', risposta)
    
    if links:
        # Prendi il primo link
        primo_link = links[0]
        # Apri il primo link nel browser
        webbrowser.open(primo_link)
    else:
        print("Nessun link trovato.")



def calcola_distanza(query):
    """Richiama una API di test"""   
    url = "http://127.0.0.1:5000/api/data" #server flask di test
    try:
        response = requests.get(url)
        response.raise_for_status()  # Genera un'eccezione se il codice di stato è diverso da 200
        data = response.json()
        return data  # Restituisci il dizionario invece di stamparlo
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}



TOOLS = {
    "wikipedia": search_wikipedia,
    "web": search_duckduckgo,
    "save": save_to_txt,
    "distanza": calcola_distanza
}
