import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def extract(limit=None, save_to_file=True):
    url = "https://jsonplaceholder.typicode.com/posts"

    try:
        logging.info("Extraction en cours...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logging.error(f"Erreur JSON : {e}")
            raise

        if not isinstance(data, list):
            raise ValueError("Format inattendu : liste attendue")
        
        if limit is not None:
            if not isinstance(limit, int) or limit < 1:
                raise ValueError("limit doit etre un entier positif non nul")
            data = data[:limit]
        
        if save_to_file:
            with open("data_raw.json", "w") as f:
                json.dump(data,f,indent=4)
        logging.info(f"Nombre de posts extraits : {len(data)}")

        return data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Erreur lors de l'extraction HTTP : {e}")
        raise

    except ValueError as e:
        logging.error(f"Erreur de validation : {e}")
        raise

