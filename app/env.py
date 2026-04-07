from app.models import Action, Observation
from app.tasks import get_task
from app.grader import grade_step, grade_final

class SupportEnv:
    def __init__(self, task_name="easy"):
        self.task_name = task_name
        self.reset()

    def reset(self):
        self.task = get_task(self.task_name)

        self.state = {
            "ticket": self.task,
            "history": [],
            "step_count": 0,
            "done": False,
            "sentiment": self.task["sentiment"],
            "sla_hours_left": self.task["sla_hours_left"]
        }
        return self._obs()

    def _obs(self):
        return Observation(
            ticket_id=self.state["ticket"]["id"],
            message=self.state["ticket"]["message"],
            priority=self.state["ticket"]["priority"],
            sentiment=self.state["sentiment"],
            sla_hours_left=self.state["sla_hours_left"],
            customer_type=self.state["ticket"]["customer_type"],
            issue_type=self.state["ticket"]["issue_type"],
            history=self.state["history"],
            step_count=self.state["step_count"]
        )

    def step(self, action: Action):
        if self.state["done"]:
            return self._obs(), 0.0, True, {"error": "done"}

        self.state["step_count"] += 1
        self.state["history"].append(f"{action.action_type}: {action.content}")

        reward = grade_step(self.state, action)

        done = self.state["step_count"] >= self.task["max_steps"]

        if done:
            reward += grade_final(self.state)

        self.state["done"] = done

        return self._obs(), round(reward, 2), done, {"error": None}

    def state(self):
        return self.state