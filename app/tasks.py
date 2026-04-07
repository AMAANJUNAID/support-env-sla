import random

ISSUES = [
    ("refund", "I want a refund for my order."),
    ("delivery", "My order hasn’t arrived yet."),
    ("double_charge", "I was charged twice for my purchase."),
    ("account", "I can't access my account."),
]

CUSTOMER_TYPES = ["normal", "premium", "enterprise"]
SENTIMENTS = ["neutral", "frustrated", "angry"]

def get_task(name):
    issue_type, base_msg = random.choice(ISSUES)
    customer_type = random.choice(CUSTOMER_TYPES)
    sentiment = random.choice(SENTIMENTS)

    sla = {
        "easy": 5,
        "medium": 4,
        "hard": 2
    }[name]

    expected_action = {
        "refund": "refund",
        "delivery": "request_info",
        "double_charge": "escalate",
        "account": "request_info"
    }[issue_type]

    return {
        "id": random.randint(100, 999),
        "message": base_msg,
        "issue_type": issue_type,
        "expected_action": expected_action,
        "priority": "high" if name == "hard" else "medium",
        "sentiment": sentiment,
        "customer_type": customer_type,
        "sla_hours_left": sla,
        "max_steps": 6 if name == "hard" else 4
    }