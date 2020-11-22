set -e

WORKTREE_BRANCH="gh_pages"
WORKTREE_LOC="docs"

if [ -d "${WORKTREE_LOC}" ]; then
    echo "Worktree exists"
    exit 0
fi

HOME_LOC="$(pwd)"
if [ -n "$(git branch --list ${WORKTREE_BRANCH})" ]; then
    git worktree add "${WORKTREE_LOC}" "${WORKTREE_BRANCH}"
else
    git worktree add --detach "${WORKTREE_LOC}"
    cd "${WORKTREE_LOC}"
    git checkout --orphan "${WORKTREE_BRANCH}"
    git reset
    git clean -fdx
    cp "${HOME_LOC}/scripts/.pages_gitignore" ".gitignore"
    git add .gitignore
    git commit -m "Initialize gh_pages with gitignore"
fi
