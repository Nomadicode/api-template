import uuid

def generate_reset_token():
    token_str = str(uuid.uuid4()).replace('-', '')
    return token_str
