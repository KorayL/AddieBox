from git import Repo
import time

repo = Repo("/home/pi/AddieBox")
print(f"Seconds since epoch of last commit: {repo.head.commit.committed_date}")

