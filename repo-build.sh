#!/usr/bin/env bash
# ===========================================================================
#  repo-build.sh —— 一条命令重建个人源（本目录就是发布目录，push 即生效）
#
#  流程: debs/*.deb → 门面(icons/assets/sileo/depictions/首页) → 索引(Packages*)
#        → Release（本源不签名：无 public.key / Release.gpg / InRelease）
#
#  加个新包: 把 .deb 路径加到下面的 SRC_DEBS（先 make package），再跑一次本脚本；
#            也可以直接把 .deb 丢进 debs/ 再跑（索引是扫全目录的）。
#  删个包  : 删掉 debs/<包>.deb 再跑一次，本脚本会顺手清掉它残留的门面文件。
#
#  产物地址: http://repo.paynexss.fun/   ← 手机上加这个源
# ===========================================================================
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

REPO="$PWD"
BASE_URL="http://repo.paynexss.fun"
TOOLKIT="${IOS_TOOLKIT:-$HOME/Reverse/tools/ios-toolkit}"

# 各包工程的产物（不存在就跳过，只看 debs/ 里已有的）
SRC_DEBS=(
  "$HOME/Reverse/projects/ios_tweaks/EgernProUnlock/packages/com.paynexc.tweak.egernprounlock_2.5.0_iphoneos-arm64.deb"
  "$HOME/Reverse/projects/ios_tweaks/SJJUnlock/packages/com.paynexc.tweak.sjjunlock_1.2.0-1+debug_iphoneos-arm64.deb"
  "$HOME/Reverse/projects/ios_tweaks/RexProUnlock/packages/com.paynexc.tweak.rexprounlock_1.8.0_iphoneos-arm64.deb"
  "$HOME/Reverse/projects/github/Tap2DebugRootless/packages/com.harans.tweak.shortcuttodebug_0.2.0-7+debug_iphoneos-arm64.deb"
)

[ -x "$TOOLKIT/debrepo.sh" ] || { echo "找不到 $TOOLKIT/debrepo.sh（可用 IOS_TOOLKIT=… 指定）" >&2; exit 1; }

ADDS=()
for d in "${SRC_DEBS[@]}"; do
  [ -f "$d" ] || { echo "[!] 跳过（工程产物不在）: $d" >&2; continue; }
  ADDS+=("$d")
done

# 清理已删包残留的门面文件（debrepo 只加不删）
for f in icons/*.png sileo/*.json depictions/*.html; do
  [ -e "$f" ] || continue
  pkg="$(basename "$f")"; pkg="${pkg%.*}"
  if ! compgen -G "debs/${pkg}_*.deb" >/dev/null; then
    echo "  - 清理残留门面 $f"
    rm -f "$f"
  fi
done
for f in assets/banner-*.png; do
  [ -e "$f" ] || continue
  pkg="$(basename "$f")"; pkg="${pkg#banner-}"; pkg="${pkg%.png}"
  if ! compgen -G "debs/${pkg}_*.deb" >/dev/null; then
    echo "  - 清理残留门面 $f"
    rm -f "$f"
  fi
done

"$TOOLKIT/debrepo.sh" -d "$REPO" ${ADDS[@]+"${ADDS[@]}"} \
  --origin "paynexss" --label "paynexss's repo" --base-url "$BASE_URL" \
  --extra "$PWD/repo-extra.conf" \
  --face --pages --no-sign

# repo-build.sh 跑完后：本源不签名 → 首页脚注里的 public.key 链接去掉
python3 - "$REPO/index.html" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
s = s.replace(' ·\n<a href="public.key">public.key</a>', '')
open(p, "w", encoding="utf-8").write(s)
PY

echo
echo "下一步: git add -A && git commit -m '源更新' && git push"
