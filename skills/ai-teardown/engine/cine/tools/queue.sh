#!/bin/zsh
# Hàng đợi render: xử lý từng dòng của cine/queue.txt (số bài|tiêu đề|giây ảnh bìa), từng bài một clips → record → finish → deliver, xong thì ghi build/.delivered
# Python: CINE_PY (cần có numpy scipy pillow playwright), mặc định python3; cổng: CINE_PORT, mặc định 8964 (nếu không ai lắng nghe thì tự khởi động một máy chủ tĩnh)
cd "${0:A:h}/../.."
PY=${CINE_PY:-python3}; PORT=${CINE_PORT:-8964}
$PY -c "import numpy, scipy, PIL, playwright" 2>/dev/null || { echo "$PY thiếu numpy/scipy/pillow/playwright, hãy đặt CINE_PY trỏ tới Python đã cài đủ"; exit 1; }
if ! curl -sf -o /dev/null "http://127.0.0.1:$PORT/cine/index.html"; then
  python3 -m http.server $PORT --bind 127.0.0.1 >/dev/null 2>&1 & SRV=$!; trap "kill $SRV 2>/dev/null" EXIT; sleep 1
fi
while true; do
  line=$(while IFS= read -r l; do n=${l%%|*}; [[ -n "$n" && ! -f lessons/$n/build/.delivered ]] && { echo "$l"; break; }; done < cine/queue.txt)
  [[ -z "$line" ]] && break
  n=${line%%|*}; rest=${line#*|}; title=${rest%%|*}; poster=${rest#*|}
  echo "== $(date +%H:%M) bài $n: $title"
  $PY cine/tools/clips.py $n --port $PORT > lessons/$n/build/clips.log 2>&1 || { echo "cắt đoạn thất bại $n"; break; }   # bài không có clips vẫn chạy được, 0 đoạn
  $PY cine/tools/record.py $n --port $PORT > lessons/$n/build/record.log 2>&1 || { echo "ghi hình thất bại $n"; break; }
  $PY cine/tools/finish.py $n --port $PORT > lessons/$n/build/finish.log 2>&1 || { echo "ghép thất bại $n"; break; }
  ./cine/tools/deliver.sh $n "$title" $poster > lessons/$n/build/deliver.log 2>&1 || { echo "giao thất bại $n"; break; }
  touch lessons/$n/build/.delivered
  echo "DONE $n $(date +%H:%M) $(tail -1 lessons/$n/build/deliver.log)"
done
echo "Hàng đợi đã trống"
