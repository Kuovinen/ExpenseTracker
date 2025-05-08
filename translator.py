import json

# Global language variable
LANG = "rus"


# Load translations from file
def load_translations(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)
texts = load_translations("lang.json")   
reverse_translations = {v["rus"]: k for k, v in texts.items()}


# Function to fetch the current translation
def t(key ):
    return texts[key].get(LANG, key)  # Default to key if no translation exists
def t2(key ):
    return reverse_translations.get(key, key)  # Default to key if no translation exists


def change_lang(new_lang):
    global LANG
    LANG = new_lang