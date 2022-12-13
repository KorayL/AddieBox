from git import Repo
import time

repo = Repo("/home/pi/AddieBox")
print(f"Seconds Since Epoch of Last Commit: {repo.head.commit.committed_date}")

