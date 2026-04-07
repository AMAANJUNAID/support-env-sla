id="tasks_fixed"
def get_task(name="easy"):
    tasks = {
        "easy": {
            "id": 1 ,
            "message": "I can't access my account",
            "issue_type": "account",
            "expected_action": "request_info",
            "priority": "medium",
            "sentiment": "neutral",
            "customer_type": "normal",
            "sla_hours_left": 5,
            "max_steps": 4
        },

        "medium": {
            "id": 2 ,
            "message": "I was charged twice for my purchase",
            "issue_type": "double_charge",
            "expected_action": "escalate",
            "priority": "medium",
            "sentiment": "frustrated",
            "customer_type": "premium",
            "sla_hours_left": 3,
            "max_steps": 5
        },

        "hard": {
            "id": 3 ,
            "message": "My business is down due to your outage",
            "issue_type": "outage",
            "expected_action": "escalate",
            "priority": "high",
            "sentiment": "angry",
            "customer_type": "enterprise",
            "sla_hours_left": 2,
            "max_steps": 6
        }
    }

    return tasks[name]