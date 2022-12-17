import dateparser
from datetime import datetime

import git

string = "2022-12-14T03:07:03Z"
lastUpdateTime = dateparser.parse(string).replace(tzinfo=None)
epochTime = datetime(1970, 1, 1)

secondsSinceEpochOfLastUpdate = (lastUpdateTime-epochTime).total_seconds()
# print(lastUpdateTime < epochTime)

repo = git.Repo("..\Addie-Box-Data")
tree = repo.tree()
for blob in tree:
    commit = next(repo.iter_commits(paths=blob.path, max_count=1))
    print(blob.path, commit.committed_date)