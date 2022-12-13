from git import Repo

repo = Repo("/home/pi/AddieBox")
print(repo.head.commit.committed_date)
