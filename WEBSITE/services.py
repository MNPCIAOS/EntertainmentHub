import base64
import requests
from django.conf import settings

class MTNMoMoError(Exception):
    pass

def _headers():
    return {
        "Ocp-Apim-Subscription-Key": settings.MTN_MOMO_SUBSCRIPTION_KEY,
        "X-Target-Environment": settings.MTN_MOMO_TARGET_ENVIRONMENT,
        "Content-Type": "application/json",
    }

def get_access_token():
    if not settings.MTN_MOMO_SUBSCRIPTION_KEY or not settings.MTN_MOMO_API_USER or not settings.MTN_MOMO_API_KEY:
        raise MTNMoMoError("MTN MoMo credentials are not configured.")
    raw = f"{settings.MTN_MOMO_API_USER}:{settings.MTN_MOMO_API_KEY}".encode()
    url = f"{settings.MTN_MOMO_BASE_URL.rstrip('/')}/collection/token/"
    r = requests.post(url, headers={**_headers(), "Authorization": f"Basic {base64.b64encode(raw).decode()}"}, timeout=30)
    if not r.ok:
        raise MTNMoMoError(f"MTN token request failed: {r.status_code} {r.text[:300]}")
    return r.json()["access_token"]

def request_to_pay(phone_number, amount, external_id, callback_url=""):
    import uuid
    token = get_access_token()
    reference_id = str(uuid.uuid4())
    payload = {
        "amount": str(amount), "currency": settings.MTN_MOMO_CURRENCY,
        "externalId": str(external_id),
        "payer": {"partyIdType": "MSISDN", "partyId": phone_number},
        "payerMessage": "EntertainmentHub Premium subscription",
        "payeeNote": "EntertainmentHub Premium subscription",
    }
    if callback_url:
        payload["callbackUrl"] = callback_url
    r = requests.post(
        f"{settings.MTN_MOMO_BASE_URL.rstrip('/')}/collection/v1_0/requesttopay",
        headers={**_headers(), "Authorization": f"Bearer {token}", "X-Reference-Id": reference_id},
        json=payload, timeout=30,
    )
    if r.status_code not in (200, 202):
        raise MTNMoMoError(f"MTN payment request failed: {r.status_code} {r.text[:500]}")
    return reference_id

def transaction_status(reference_id):
    token = get_access_token()
    r = requests.get(
        f"{settings.MTN_MOMO_BASE_URL.rstrip('/')}/collection/v1_0/requesttopay/{reference_id}",
        headers={**_headers(), "Authorization": f"Bearer {token}"}, timeout=30,
    )
    if not r.ok:
        raise MTNMoMoError(f"MTN status request failed: {r.status_code} {r.text[:300]}")
    return r.json()

def send_payment_sms(phone_number, message):
    if not settings.SMS_USERNAME or not settings.SMS_API_KEY:
        return False
    r = requests.post(
        settings.SMS_API_URL,
        headers={"apiKey": settings.SMS_API_KEY, "Content-Type": "application/x-www-form-urlencoded"},
        data={"username": settings.SMS_USERNAME, "to": phone_number, "message": message, **({"from": settings.SMS_SENDER_ID} if settings.SMS_SENDER_ID else {})},
        timeout=30,
    )
    return r.ok
