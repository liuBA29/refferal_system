# users/tokens.py

import random
import time
import logging

logger = logging.getLogger(__name__)

# временно храним коды в памяти
verification_storage = {}
all_codes = {}

def generate_verification_code():
    return str(random.randint(1000, 9999))

def send_code(phone_number):
    time.sleep(1.5)  # задержка имитации отправки

    code = generate_verification_code()
    verification_storage[phone_number] = code
    all_codes[phone_number] = code  #  сохраняем для отладки
    logger.debug(f"[DEBUG] Code for {phone_number}: {code}")
    return code

def verify_code(phone_number, code):
    return verification_storage.get(phone_number) == code
