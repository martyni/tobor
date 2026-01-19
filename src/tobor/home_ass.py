import subprocess
import json


class HomeAss:
    def __init__(self, host: str, ball_file: str):
        self.host = host
        self.ball_file = ball_file

    def logon_run(self, cmd: list):
        ssh_cmd = ["ssh", "-o" "StrictHostKeychecking=no", self.host, ] + cmd
        return subprocess.check_output(ssh_cmd).decode("utf-8")

    def get_balls(self):
        data=self.logon_run(['jq', '.', self.ball_file])
        b = json.loads(data)
        return b["balls"]
    
    def add_balls(self, new_balls: int):
        self.new_balls = new_balls
        self.old_balls = self.get_balls()
        return self.old_balls + self.new_balls 
    
    def put_balls(self):
        self.total_balls=self.add_balls()
        return self.logon_run( ['echo',r'{\"balls\":', str(self.total_balls), '}','>',self.ball_file])
        
    def reset_balls(self):
        return self.logon_run( ['echo',r'{\"balls\":', str(self.new_balls), '}','>',self.ball_file])

