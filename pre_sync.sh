#!/bin/bash
git clone "$GIT_REMOTE_URL" content
cd content
git switch -c "$GIT_BRANCH_NAME"
git config user.name "$GIT_USER_NAME"
git config user.email "$GIT_USER_EMAIL"
git remote add origin "$GIT_REMOTE_URL"
git fetch
# The next command could fail if the branch is not yet created on the remote.
git branch --set-upstream-to="origin/$GIT_BRANCH_NAME"
if [ $? -eq 0 ]; then
    git pull
fi