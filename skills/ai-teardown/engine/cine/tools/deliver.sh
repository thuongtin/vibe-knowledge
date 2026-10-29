#!/bin/zsh
# Bàn giao sau khi ra phim: bản chia sẻ 1080p60 ở màn hình nền (CRF 23) + bản web 720p30 cho trang khóa học (sau khử nhiễu khoảng 2 MB/phút) + ảnh bìa
# Cách dùng: cine/tools/deliver.sh <số-bài> "<tiêu-đề>" <giây-ảnh-bìa>
# Nơi đến ghi trong cine/deliver.env (do new_series.py tạo): D=thư mục màn hình nền; WEB=thư mục xuất bản trang khóa học; STRIP=tiền tố số bài được bỏ khỏi tên file (như p)
set -e
cd "${0:A:h}/../.."
N=$1; TITLE=$2; POSTER=${3:-12}
SRC=lessons/$N/build/lesson$N.mp4
D="$HOME/Desktop/${PWD:t}_视频"; WEB=publish/course; STRIP=""
[[ -f cine/deliver.env ]] && source cine/deliver.env
NAME=$N; [[ -n "$STRIP" ]] && NAME=${N#$STRIP}
mkdir -p "$D" $WEB
ffmpeg -y -loglevel error -i $SRC -c:v libx264 -preset slow -crf 23 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a copy -movflags +faststart "$D/${NAME}_${TITLE}.mp4"   # Bài có hạt đầy màn hình thì bitrate sẽ vọt lên 20M+, giới hạn tối đa 6M
ffmpeg -y -loglevel error -i $SRC -vf "scale=1280:-2,fps=30,hqdn3d=3:2:5:4" -c:v libx264 -preset slow -crf 29 -maxrate 520k -bufsize 1040k -pix_fmt yuv420p -c:a aac -b:a 64k -ac 1 -movflags +faststart $WEB/lesson$N.mp4
ffmpeg -y -loglevel error -ss $POSTER -i $SRC -frames:v 1 -vf scale=1280:-2 -q:v 3 $WEB/lesson$N.jpg
ls -la "$D/${NAME}_${TITLE}.mp4" $WEB/lesson$N.mp4 | awk '{print $5, $NF}'
ffprobe -v error -show_entries format=duration -of csv=p=0 $SRC
