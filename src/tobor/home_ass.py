import subprocess
import json
import datetime

class HomeAss:
    def __init__(self, host: str, ball_file: str, log_level=1):
        self.host = host
        self.ball_file = ball_file
        self.ball_object = {}
        self.log_level=log_level

    def log(self, message: str, level=1):
        if self.log_level >= level:
           now = datetime.datetime.utcnow()
           print(f"{now}: {message}")

    def logon_run(self, cmd: list):
        ssh_cmd = ["ssh", "-o" "StrictHostKeychecking=no", self.host, ] + cmd
        self.log(" ".join(ssh_cmd))
        return subprocess.check_output(ssh_cmd).decode("utf-8")

    def put_object(self):
        cmd = ["echo '", json.dumps(self.ball_object),  "' | jq -c . >" , self.ball_file]
        self.logon_run(cmd)

    def get_object(self):
        data=self.logon_run(['jq', '.', self.ball_file])
        self.log(data)
        self.ball_object = json.loads(data)
        self.log(self.ball_object)
        return self.ball_object

    def reset_object(self, reset=None):
        if reset is not None:
           self.ball_object = reset 
        self.put_object()
        return self.ball_object

    def put_keys(self, **kwargs):
        self.get_object()
        self.ball_object.update(kwargs)
        self.put_object()
        return self.ball_object

    def put_balls(self, ball_number: int, key="balls"):
        self.get_object()
        if self.ball_object.get(key) is None:
            self.ball_object.update({key: 0})
        self.log(f"{self.ball_object.get(key)} previous balls")
        self.ball_object[key] += ball_number 
        self.log(f"{self.ball_object.get(key)} new balls")
        self.put_object()
