import json

# Global language variable
LANG = "eng"

# Load translations from file
def load_translations(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        return json.load(f)
    
# Function to fetch the current translation
def t(key, translations):
    return translations[key].get(LANG, key)  # Default to key if no translation exists

# Example usage
translations = load_translations("lang.json")
print(t("save", translations))  # Outputs: титул
print(t("save", translations))  # Outputs: Сохранить
print(t("delete", translations))  # Outputs: unknown_key (default to key)
