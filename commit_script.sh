#!/bin/bash
cd content
git add .
git commit -m "$(date -Iseconds)"
git push --set-upstream origin $GIT_BRANCH_NAME