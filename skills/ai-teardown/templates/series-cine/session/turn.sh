#!/bin/zsh
# Ghi lại phiên thật: chạy một lượt bằng SESSION_CC trong SESSION_PROJ (cấu hình xem session.env cùng thư mục).
# Cách dùng: session/turn.sh <số lượt> "<prompt>"     lượt 1 mở phiên mới, sau đó tự động --continue nối tiếp cùng một phiên
# Chú ý: ở chế độ -p, phần render nó đẩy xuống nền sẽ bị giết cùng khi lượt này kết thúc; muốn render thì cho chạy ở tiền cảnh.
set -e
N=$1; PROMPT=$2
HERE="${0:A:h}"
source "$HERE/session.env"
PROJ=${~SESSION_PROJ}; CC=${~SESSION_CC:-claude}
mkdir -p "$PROJ"
if [[ -n "$SITE_DIR" ]]; then
  lsof -iTCP:$SITE_PORT -sTCP:LISTEN -n -P >/dev/null 2>&1 || (cd ${~SITE_DIR} && nohup python3 -m http.server $SITE_PORT --bind 127.0.0.1 >/dev/null 2>&1 &)
fi
CONT=(); [[ $N -gt 1 ]] && CONT=(--continue)
cd "$PROJ"
date +%s > "$HERE/turn$N.start"
print -r -- "$PROMPT" > "$HERE/turn$N.prompt.txt"
CLAUDE_CONFIG_DIR=${~SESSION_CONFIG} DISABLE_AUTOUPDATER=1 "$CC" -p "$PROMPT" $CONT --permission-mode ${SESSION_PERMISSION:-auto} --output-format stream-json --verbose > "$HERE/turn$N.jsonl" 2> "$HERE/turn$N.err"
date +%s > "$HERE/turn$N.end"
echo "Lượt $N kết thúc: $(( $(cat $HERE/turn$N.end) - $(cat $HERE/turn$N.start) )) giây"
