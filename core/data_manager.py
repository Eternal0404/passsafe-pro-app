import json
import os
import uuid
import datetime
import bcrypt
import sys
from .encryption import derive_key, encrypt_data, decrypt_data

DATA_DIR = os.path.join(sys._MEIPASS, 'data') if hasattr(sys, '_MEIPASS') else 'data'
VAULT_FILE = os.path.join(DATA_DIR, 'vault.json')
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')
SETTINGS_FILE = os.path.join(DATA_DIR, 'settings.json')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    ensure_data_dir()
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def set_master_password(password):
    salt = os.urandom(16).hex()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    settings = load_settings()
    settings['master_hash'] = hashed
    settings['salt'] = salt
    save_settings(settings)

def verify_master_password(password):
    settings = load_settings()
    if 'master_hash' not in settings:
        return False
    return bcrypt.checkpw(password.encode(), settings['master_hash'].encode())

def get_encryption_key(password):
    settings = load_settings()
    salt = bytes.fromhex(settings['salt'])
    return derive_key(password, salt)

def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return []
    with open(VAULT_FILE, 'r') as f:
        data = json.load(f)
    vault = []
    for item in data:
        item_copy = item.copy()
        item_copy['password'] = decrypt_data(item['password_enc'], key)
        del item_copy['password_enc']
        vault.append(item_copy)
    return vault

def save_vault(vault, key):
    data = []
    for item in vault:
        item_copy = item.copy()
        item_copy['password_enc'] = encrypt_data(item['password'], key)
        del item_copy['password']
        data.append(item_copy)
    ensure_data_dir()
    with open(VAULT_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_vault_entry(account, username, password, tags, key):
    vault = load_vault(key)
    entry = {
        'uuid': str(uuid.uuid4()),
        'account': account,
        'username': username,
        'password': password,
        'tags': tags,
        'timestamp': datetime.datetime.now().isoformat()
    }
    vault.append(entry)
    save_vault(vault, key)

def update_vault_entry(uuid, account, username, password, tags, key):
    vault = load_vault(key)
    for item in vault:
        if item['uuid'] == uuid:
            item['account'] = account
            item['username'] = username
            item['password'] = password
            item['tags'] = tags
            item['timestamp'] = datetime.datetime.now().isoformat()
            break
    save_vault(vault, key)

def delete_vault_entry(uuid, key):
    vault = load_vault(key)
    vault = [item for item in vault if item['uuid'] != uuid]
    save_vault(vault, key)

def search_vault(query, key):
    vault = load_vault(key)
    results = []
    for item in vault:
        if query.lower() in item['account'].lower() or query.lower() in item['username'].lower() or any(query.lower() in tag.lower() for tag in item['tags']):
            results.append(item)
    return results

def load_notes(key):
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, 'r') as f:
        data = json.load(f)
    notes = []
    for item in data:
        item_copy = item.copy()
        item_copy['content'] = decrypt_data(item['content_enc'], key)
        del item_copy['content_enc']
        notes.append(item_copy)
    return notes

def save_notes(notes, key):
    data = []
    for item in notes:
        item_copy = item.copy()
        item_copy['content_enc'] = encrypt_data(item['content'], key)
        del item_copy['content']
        data.append(item_copy)
    ensure_data_dir()
    with open(NOTES_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_note(account_uuid, content, key):
    notes = load_notes(key)
    note = {
        'uuid': str(uuid.uuid4()),
        'account_uuid': account_uuid,
        'content': content,
        'timestamp': datetime.datetime.now().isoformat()
    }
    notes.append(note)
    save_notes(notes, key)

def update_note(uuid, content, key):
    notes = load_notes(key)
    for item in notes:
        if item['uuid'] == uuid:
            item['content'] = content
            item['timestamp'] = datetime.datetime.now().isoformat()
            break
    save_notes(notes, key)

def delete_note(uuid, key):
    notes = load_notes(key)
    notes = [item for item in notes if item['uuid'] != uuid]
    save_notes(notes, key)

def search_notes(query, key):
    notes = load_notes(key)
    results = []
    for item in notes:
        if query.lower() in item['content'].lower():
            results.append(item)
    return results

def get_theme():
    settings = load_settings()
    return settings.get('theme', 'light')

def set_theme(theme):
    settings = load_settings()
    settings['theme'] = theme
    save_settings(settings)

def get_auto_lock():
    settings = load_settings()
    return settings.get('auto_lock', 300)

def set_auto_lock(seconds):
    settings = load_settings()
    settings['auto_lock'] = seconds
    save_settings(settings)