#!/bin/bash
# 自动推送 AI Knowledge Vault 到 GitHub
# 由 batch_process.py 每次处理完一个日期后调用

VAULT_DIR="/home/admin/.openclaw/workspace/01-AI-Knowledge-Vault"
LOG_FILE="$VAULT_DIR/../git-sync.log"

cd "$VAULT_DIR" || exit 1

# 检查是否有变更
if git diff --quiet && git diff --staged --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] No changes to commit" >> "$LOG_FILE"
    exit 0
fi

git add -A
git commit -m "sync: $(date '+%Y-%m-%d %H:%M:%S') auto update"
git push origin main >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push success" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push FAILED" >> "$LOG_FILE"
    exit 1
fi
