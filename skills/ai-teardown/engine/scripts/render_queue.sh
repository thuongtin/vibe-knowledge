#!/bin/zsh
# Hàng đợi render: xuất thành phẩm từng bài một (render song song lại chậm hơn).
# Cách dùng: scripts/render_queue.sh <thư mục series>; thêm số bài vào <thư mục series>/render.queue (mỗi dòng một số, vd 05), ghi END để kết thúc.
S=${1:?thư mục series}; Q=$S/render.queue; touch $Q
while true; do
  n=$(head -1 $Q)
  if [[ -z $n ]]; then sleep 20; continue; fi
  [[ $n == END ]] && { sed -i '' 1d $Q; echo "Hàng đợi kết thúc"; exit 0; }
  echo "$(date +%H:%M) bắt đầu render bài $n"
  python3 scripts/make_lesson.py $S/lessons/$n final > $S/lessons/$n/final.log 2>&1 \
    && echo "$(date +%H:%M) bài $n hoàn tất: $(grep -h 'Hoàn tất "final"' $S/lessons/$n/final.log)" \
    || echo "$(date +%H:%M) bài $n thất bại, xem $S/lessons/$n/final.log"
  sed -i '' 1d $Q
done
