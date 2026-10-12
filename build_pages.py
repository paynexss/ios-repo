#!/usr/bin/env python3
"""
build_pages.py —— 生成现代 iOS 原生风格的源首页与详情页
- 纯原生 HTML/CSS/JS，零外部 CDN 依赖，暗色/亮色自适应
- 支持 Sileo / Zebra 一键加源跳转、一键复制源地址、实时搜索过滤
"""
import html
import os
import re

REPO_URL = "http://repo.paynexss.fun"
REPO_TITLE = "paynexss's repo"
REPO_DESC = "给越狱设备（Rootless / Dopamine）自用的 iOS Tweak 集合"


def human_size(n):
    try:
        n = float(n)
    except (ValueError, TypeError):
        return "-"
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024.0 or unit == "MB":
            return f"{n:.1f} {unit}".replace(".0 ", " ")
        n /= 1024.0
    return f"{n:.1f} MB"


def parse_packages(path="Packages"):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    blocks = content.strip().split("\n\n")
    packages = []
    for block in blocks:
        item = {}
        curr_key = None
        for line in block.split("\n"):
            if not line:
                continue
            if line[0] in (" ", "\t") and curr_key:
                item[curr_key] += "\n" + line.strip()
            elif ":" in line:
                key, val = line.split(":", 1)
                curr_key = key.strip()
                item[curr_key] = val.strip()
        if item.get("Package"):
            packages.append(item)
    return packages


def generate_index_html(packages):
    pkg_cards = []
    for p in packages:
        pkg_id = p.get("Package", "")
        name = p.get("Name") or pkg_id
        version = p.get("Version", "1.0.0")
        desc = p.get("Description", "").split("\n")[0]
        size_str = human_size(p.get("Size", 0))
        filename = p.get("Filename", "")
        if filename.startswith("./"):
            deb_href = filename[2:]
        else:
            deb_href = filename

        icon_path = f"icons/{pkg_id}.png"
        if not os.path.isfile(icon_path):
            icon_path = "CydiaIcon.png"

        depiction_href = f"depictions/{pkg_id}.html"

        card = f"""
      <article class="pkg-card" data-name="{html.escape(name.lower())}" data-id="{html.escape(pkg_id.lower())}" data-desc="{html.escape(desc.lower())}">
        <div class="pkg-main">
          <a class="pkg-icon-link" href="{depiction_href}" title="查看详情">
            <img class="pkg-icon" src="{icon_path}" alt="{html.escape(name)}" loading="lazy">
          </a>
          <div class="pkg-info">
            <div class="pkg-header">
              <a class="pkg-name" href="{depiction_href}">{html.escape(name)}</a>
              <span class="badge badge-version">v{html.escape(version)}</span>
              <span class="badge badge-arch">rootless</span>
            </div>
            <div class="pkg-id">{html.escape(pkg_id)}</div>
            <p class="pkg-desc">{html.escape(desc)}</p>
          </div>
        </div>
        <div class="pkg-footer">
          <div class="pkg-meta">
            <span class="meta-tag">{html.escape(p.get('Section', 'Tweaks'))}</span>
            <span class="meta-dot">·</span>
            <span class="meta-size">{size_str}</span>
          </div>
          <div class="pkg-actions">
            <a class="btn btn-secondary btn-sm" href="{depiction_href}">查看详情</a>
            <a class="btn btn-primary btn-sm" href="{html.escape(deb_href)}" download>下载 deb</a>
          </div>
        </div>
      </article>"""
        pkg_cards.append(card)

    cards_html = "\n".join(pkg_cards)
    total_count = len(packages)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(REPO_TITLE)}</title>
  <meta name="description" content="{html.escape(REPO_DESC)}">
  <link rel="icon" type="image/png" href="CydiaIcon.png">
  <link rel="apple-touch-icon" href="CydiaIcon.png">
  <style>
    :root {{
      --bg: #f2f2f7;
      --card-bg: #ffffff;
      --card-border: rgba(60, 60, 67, 0.1);
      --card-hover: rgba(60, 60, 67, 0.16);
      --text-main: #1c1c1e;
      --text-sub: #636366;
      --text-tertiary: #8e8e93;
      --tint: #007aff;
      --tint-hover: #0062cc;
      --tint-light: rgba(0, 122, 255, 0.1);
      --badge-bg: rgba(142, 142, 147, 0.12);
      --badge-text: #48484a;
      --input-bg: #ffffff;
      --input-border: rgba(60, 60, 67, 0.15);
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 18px;
      --radius-xl: 22px;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
      --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.06);
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #000000;
        --card-bg: #1c1c1e;
        --card-border: rgba(255, 255, 255, 0.08);
        --card-hover: rgba(255, 255, 255, 0.16);
        --text-main: #f5f5f7;
        --text-sub: #aeaeb2;
        --text-tertiary: #636366;
        --tint: #0a84ff;
        --tint-hover: #339aff;
        --tint-light: rgba(10, 132, 255, 0.18);
        --badge-bg: rgba(255, 255, 255, 0.12);
        --badge-text: #e5e5ea;
        --input-bg: #1c1c1e;
        --input-border: rgba(255, 255, 255, 0.14);
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
      }}
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", sans-serif;
      background: var(--bg);
      color: var(--text-main);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: env(safe-area-inset-top, 24px) 16px env(safe-area-inset-bottom, 32px);
    }}

    .container {{
      width: 100%;
      max-width: 680px;
      margin: 0 auto;
      flex: 1;
    }}

    /* Header */
    .hero {{
      text-align: center;
      padding: 28px 0 20px;
    }}
    .repo-avatar {{
      width: 80px;
      height: 80px;
      border-radius: 22.5%;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
      border: 1px solid var(--card-border);
      margin-bottom: 14px;
      object-fit: cover;
    }}
    .hero-title {{
      font-size: 1.85rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }}
    .hero-subtitle {{
      font-size: 0.95rem;
      color: var(--text-sub);
      margin-bottom: 14px;
    }}
    .hero-tags {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 0.75rem;
      font-weight: 600;
      line-height: 1.2;
      background: var(--badge-bg);
      color: var(--badge-text);
    }}
    .badge-tint {{
      background: var(--tint-light);
      color: var(--tint);
    }}
    .badge-version {{
      background: var(--tint-light);
      color: var(--tint);
    }}
    .badge-arch {{
      background: var(--badge-bg);
      color: var(--badge-text);
      font-family: ui-monospace, "SF Mono", Menlo, monospace;
    }}

    /* Source Box Card */
    .source-box {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-xl);
      padding: 16px;
      box-shadow: var(--shadow-sm);
      margin-bottom: 24px;
    }}
    .url-display {{
      display: flex;
      align-items: center;
      background: var(--bg);
      border: 1px solid var(--input-border);
      border-radius: var(--radius-md);
      padding: 9px 12px;
      gap: 10px;
      margin-bottom: 12px;
    }}
    .url-text {{
      flex: 1;
      font-family: ui-monospace, "SF Mono", Menlo, monospace;
      font-size: 0.88rem;
      color: var(--text-main);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      user-select: all;
    }}
    .btn-copy {{
      background: none;
      border: none;
      color: var(--tint);
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: var(--radius-sm);
      transition: background 0.15s;
    }}
    .btn-copy:hover {{
      background: var(--tint-light);
    }}
    .quick-add-group {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 11px 16px;
      border-radius: var(--radius-md);
      font-size: 0.92rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: 1px solid transparent;
      transition: transform 0.1s, opacity 0.15s, background 0.15s;
    }}
    .btn:active {{
      transform: scale(0.98);
      opacity: 0.9;
    }}
    .btn-primary {{
      background: var(--tint);
      color: #ffffff;
    }}
    .btn-primary:hover {{
      background: var(--tint-hover);
    }}
    .btn-secondary {{
      background: var(--bg);
      color: var(--text-main);
      border-color: var(--card-border);
    }}
    .btn-secondary:hover {{
      border-color: var(--card-hover);
    }}
    .btn-sm {{
      padding: 6px 12px;
      font-size: 0.82rem;
      border-radius: var(--radius-sm);
    }}

    /* Search & Filter */
    .filter-section {{
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .search-wrap {{
      position: relative;
      flex: 1;
    }}
    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      width: 15px;
      height: 15px;
      fill: none;
      stroke: var(--text-tertiary);
      stroke-width: 2;
      stroke-linecap: round;
      pointer-events: none;
    }}
    .search-input {{
      width: 100%;
      padding: 10px 12px 10px 34px;
      background: var(--card-bg);
      border: 1px solid var(--input-border);
      border-radius: var(--radius-md);
      font-size: 0.9rem;
      color: var(--text-main);
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--tint);
      box-shadow: 0 0 0 3px var(--tint-light);
    }}
    .pkg-count {{
      font-size: 0.82rem;
      color: var(--text-tertiary);
      white-space: nowrap;
      font-weight: 500;
    }}

    /* Package Cards */
    .pkg-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 32px;
    }}
    .pkg-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
      transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
    }}
    .pkg-card:hover {{
      border-color: var(--card-hover);
      box-shadow: var(--shadow-md);
    }}
    .pkg-main {{
      display: flex;
      gap: 14px;
      align-items: flex-start;
      margin-bottom: 12px;
    }}
    .pkg-icon-link {{
      flex: 0 0 auto;
      text-decoration: none;
    }}
    .pkg-icon {{
      width: 58px;
      height: 58px;
      border-radius: 22.5%;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
      border: 1px solid var(--card-border);
      display: block;
      background: var(--bg);
      object-fit: cover;
    }}
    .pkg-info {{
      flex: 1;
      min-width: 0;
    }}
    .pkg-header {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 3px;
    }}
    .pkg-name {{
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      text-decoration: none;
      letter-spacing: -0.01em;
    }}
    .pkg-name:hover {{
      color: var(--tint);
    }}
    .pkg-id {{
      font-size: 0.78rem;
      font-family: ui-monospace, "SF Mono", Menlo, monospace;
      color: var(--text-tertiary);
      margin-bottom: 6px;
      word-break: break-all;
    }}
    .pkg-desc {{
      font-size: 0.88rem;
      color: var(--text-sub);
      line-height: 1.45;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }}
    .pkg-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1px solid var(--card-border);
      padding-top: 10px;
      gap: 12px;
    }}
    .pkg-meta {{
      font-size: 0.8rem;
      color: var(--text-tertiary);
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .meta-tag {{
      background: var(--badge-bg);
      color: var(--badge-text);
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.75rem;
    }}
    .pkg-actions {{
      display: flex;
      gap: 8px;
    }}

    .empty-state {{
      display: none;
      text-align: center;
      padding: 48px 16px;
      color: var(--text-tertiary);
      background: var(--card-bg);
      border: 1px dashed var(--card-border);
      border-radius: var(--radius-lg);
    }}

    /* Footer */
    footer {{
      text-align: center;
      font-size: 0.82rem;
      color: var(--text-tertiary);
      padding: 16px 0 24px;
      border-top: 1px solid var(--card-border);
    }}
    footer a {{
      color: var(--text-sub);
      text-decoration: none;
      margin: 0 4px;
      transition: color 0.15s;
    }}
    footer a:hover {{
      color: var(--tint);
    }}
    .footer-links {{
      margin-bottom: 8px;
    }}

    /* Toast */
    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(80px);
      background: rgba(0, 0, 0, 0.85);
      color: #fff;
      padding: 10px 20px;
      border-radius: 999px;
      font-size: 0.88rem;
      font-weight: 500;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
      pointer-events: none;
      opacity: 0;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
      z-index: 999;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="hero">
      <img class="repo-avatar" src="CydiaIcon.png" alt="源图标">
      <h1 class="hero-title">{html.escape(REPO_TITLE)}</h1>
      <p class="hero-subtitle">{html.escape(REPO_DESC)}</p>
      <div class="hero-tags">
        <span class="badge badge-tint">Rootless 越狱</span>
        <span class="badge badge-arch">iphoneos-arm64</span>
        <span class="badge badge-arch">iOS 15.0+</span>
        <span class="badge badge-tint">免公钥证书</span>
      </div>
    </header>

    <section class="source-box" aria-label="软件源添加">
      <div class="url-display">
        <span class="url-text" id="repoUrl">{html.escape(REPO_URL)}</span>
        <button class="btn-copy" id="copyBtn" onclick="copyRepoUrl()" type="button">复制</button>
      </div>
      <div class="quick-add-group">
        <a class="btn btn-primary" href="sileo://source/{REPO_URL}/">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
          加到 Sileo
        </a>
        <a class="btn btn-secondary" href="zbra://sources/add/{REPO_URL}/">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="4"/><path d="M7 8h10l-10 8h10"/></svg>
          加到 Zebra
        </a>
      </div>
    </section>

    <div class="filter-section">
      <div class="search-wrap">
        <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input class="search-input" id="searchInput" type="search" placeholder="搜索插件名称、描述或包标识..." autocomplete="off">
      </div>
      <span class="pkg-count" id="pkgCount">共 {total_count} 个插件</span>
    </div>

    <main class="pkg-list" id="pkgList">
{cards_html}
    </main>

    <div class="empty-state" id="emptyState">
      没有找到匹配的插件
    </div>

    <footer>
      <div class="footer-links">
        索引：<a href="Packages">Packages</a> ·
        <a href="Packages.gz">Packages.gz</a> ·
        <a href="Packages.bz2">Packages.bz2</a> ·
        <a href="Release">Release</a>
      </div>
      <p>{html.escape(REPO_TITLE)} · 仅用于自用设备 rootless 环境</p>
    </footer>
  </div>

  <div class="toast" id="toast">已复制源地址</div>

  <script>
    function copyRepoUrl() {{
      const text = document.getElementById('repoUrl').innerText.trim();
      const btn = document.getElementById('copyBtn');
      const toast = document.getElementById('toast');

      navigator.clipboard.writeText(text).then(() => {{
        btn.textContent = '已复制 ✓';
        toast.classList.add('show');
        setTimeout(() => {{
          btn.textContent = '复制';
          toast.classList.remove('show');
        }}, 2000);
      }}).catch(() => {{
        prompt('请手动复制源地址：', text);
      }});
    }}

    const searchInput = document.getElementById('searchInput');
    const pkgList = document.getElementById('pkgList');
    const emptyState = document.getElementById('emptyState');
    const pkgCount = document.getElementById('pkgCount');
    const cards = Array.from(document.querySelectorAll('.pkg-card'));

    searchInput.addEventListener('input', (e) => {{
      const q = e.target.value.trim().toLowerCase();
      let visible = 0;
      cards.forEach(card => {{
        const name = card.dataset.name || '';
        const id = card.dataset.id || '';
        const desc = card.dataset.desc || '';
        const match = !q || name.includes(q) || id.includes(q) || desc.includes(q);
        card.style.display = match ? '' : 'none';
        if (match) visible++;
      }});

      pkgCount.textContent = q ? `找到 ${{visible}} 个` : `共 ${{cards.length}} 个插件`;
      emptyState.style.display = (visible === 0) ? 'block' : 'none';
    }});
  </script>
</body>
</html>"""


def generate_depiction_html(pkg):
    pkg_id = pkg.get("Package", "")
    name = pkg.get("Name") or pkg_id
    version = pkg.get("Version", "1.0.0")
    desc = pkg.get("Description", "")
    arch = pkg.get("Architecture", "iphoneos-arm64")
    section = pkg.get("Section", "Tweaks")
    depends = pkg.get("Depends", "firmware (>= 15.0)")
    maintainer = pkg.get("Maintainer", "paynexc")
    author = pkg.get("Author", maintainer)
    size_str = human_size(pkg.get("Size", 0))
    inst_size = pkg.get("Installed-Size", "-")
    if inst_size != "-" and inst_size.isdigit():
        inst_size = f"{inst_size} KB"

    filename = pkg.get("Filename", "")
    if filename.startswith("./"):
        deb_href = "../" + filename[2:]
    else:
        deb_href = "../" + filename

    banner_rel = f"assets/banner-{pkg_id}.png"
    has_banner = os.path.isfile(banner_rel)
    banner_img_tag = f'<img class="banner-img" src="../{banner_rel}" alt="{html.escape(name)} banner">' if has_banner else ''

    icon_rel = f"icons/{pkg_id}.png"
    icon_src = f"../{icon_rel}" if os.path.isfile(icon_rel) else "../CydiaIcon.png"

    # Description lines
    desc_paragraphs = "\n".join(f"<p>{html.escape(line.strip())}</p>" for line in desc.split("\n") if line.strip())

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(name)} · {html.escape(REPO_TITLE)}</title>
  <style>
    :root {{
      --bg: #f2f2f7;
      --card-bg: #ffffff;
      --card-border: rgba(60, 60, 67, 0.1);
      --text-main: #1c1c1e;
      --text-sub: #636366;
      --text-tertiary: #8e8e93;
      --tint: #007aff;
      --tint-hover: #0062cc;
      --tint-light: rgba(0, 122, 255, 0.1);
      --badge-bg: rgba(142, 142, 147, 0.12);
      --badge-text: #48484a;
      --radius-md: 14px;
      --radius-lg: 18px;
      --radius-xl: 22px;
      --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.04);
      --shadow-md: 0 4px 14px rgba(0, 0, 0, 0.06);
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #000000;
        --card-bg: #1c1c1e;
        --card-border: rgba(255, 255, 255, 0.08);
        --text-main: #f5f5f7;
        --text-sub: #aeaeb2;
        --text-tertiary: #636366;
        --tint: #0a84ff;
        --tint-hover: #339aff;
        --tint-light: rgba(10, 132, 255, 0.18);
        --badge-bg: rgba(255, 255, 255, 0.12);
        --badge-text: #e5e5ea;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "PingFang SC", "Hiragino Sans GB", sans-serif;
      background: var(--bg);
      color: var(--text-main);
      line-height: 1.5;
      padding: env(safe-area-inset-top, 24px) 16px env(safe-area-inset-bottom, 32px);
    }}
    .container {{
      max-width: 640px;
      margin: 0 auto;
    }}
    .nav-bar {{
      display: flex;
      align-items: center;
      margin-bottom: 16px;
    }}
    .nav-back {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--tint);
      text-decoration: none;
      font-weight: 500;
      font-size: 0.95rem;
    }}
    .banner-wrap {{
      width: 100%;
      border-radius: var(--radius-xl);
      overflow: hidden;
      margin-bottom: 16px;
      box-shadow: var(--shadow-sm);
      border: 1px solid var(--card-border);
      background: var(--card-bg);
    }}
    .banner-img {{
      width: 100%;
      height: auto;
      display: block;
      aspect-ratio: 2.5 / 1;
      object-fit: cover;
    }}
    .header-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-xl);
      padding: 18px;
      display: flex;
      gap: 16px;
      align-items: center;
      box-shadow: var(--shadow-sm);
      margin-bottom: 16px;
    }}
    .pkg-icon {{
      width: 68px;
      height: 68px;
      border-radius: 22.5%;
      border: 1px solid var(--card-border);
      object-fit: cover;
      flex-shrink: 0;
    }}
    .header-info {{
      flex: 1;
      min-width: 0;
    }}
    .pkg-title {{
      font-size: 1.35rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      margin-bottom: 2px;
    }}
    .pkg-id {{
      font-family: ui-monospace, "SF Mono", Menlo, monospace;
      font-size: 0.78rem;
      color: var(--text-tertiary);
      margin-bottom: 6px;
      word-break: break-all;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.74rem;
      font-weight: 600;
      background: var(--tint-light);
      color: var(--tint);
    }}
    .actions-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 8px;
      margin-bottom: 16px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      padding: 10px 12px;
      border-radius: var(--radius-md);
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid transparent;
      cursor: pointer;
      transition: opacity 0.15s;
    }}
    .btn:active {{
      opacity: 0.85;
    }}
    .btn-primary {{
      background: var(--tint);
      color: #fff;
    }}
    .btn-secondary {{
      background: var(--card-bg);
      color: var(--text-main);
      border-color: var(--card-border);
    }}
    .section-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius-xl);
      padding: 18px;
      margin-bottom: 16px;
      box-shadow: var(--shadow-sm);
    }}
    .section-title {{
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-tertiary);
      margin-bottom: 10px;
    }}
    .desc-content {{
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--text-main);
    }}
    .desc-content p {{
      margin-bottom: 8px;
    }}
    .desc-content p:last-child {{
      margin-bottom: 0;
    }}
    .meta-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }}
    .meta-table tr {{
      border-bottom: 1px solid var(--card-border);
    }}
    .meta-table tr:last-child {{
      border-bottom: none;
    }}
    .meta-table th {{
      text-align: left;
      padding: 9px 0;
      color: var(--text-sub);
      font-weight: 400;
      width: 32%;
    }}
    .meta-table td {{
      padding: 9px 0;
      color: var(--text-main);
      word-break: break-all;
    }}
    .foot {{
      text-align: center;
      font-size: 0.82rem;
      color: var(--text-tertiary);
      margin-top: 24px;
    }}
    .foot a {{
      color: var(--tint);
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav class="nav-bar">
      <a class="nav-back" href="../index.html">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
        返回源首页
      </a>
    </nav>

    {banner_img_tag}

    <header class="header-card">
      <img class="pkg-icon" src="{icon_src}" alt="{html.escape(name)}">
      <div class="header-info">
        <h1 class="pkg-title">{html.escape(name)}</h1>
        <div class="pkg-id">{html.escape(pkg_id)}</div>
        <span class="badge">v{html.escape(version)}</span>
        <span class="badge" style="background:var(--badge-bg);color:var(--badge-text)">{html.escape(arch)}</span>
      </div>
    </header>

    <div class="actions-grid">
      <a class="btn btn-primary" href="sileo://package/{html.escape(pkg_id)}">Sileo 查看</a>
      <a class="btn btn-secondary" href="zbra://sources/add/{REPO_URL}/">Zebra 加源</a>
      <a class="btn btn-secondary" href="{html.escape(deb_href)}" download>下载 deb</a>
    </div>

    <section class="section-card">
      <h2 class="section-title">简介</h2>
      <div class="desc-content">
        {desc_paragraphs}
      </div>
    </section>

    <section class="section-card">
      <h2 class="section-title">详细信息</h2>
      <table class="meta-table">
        <tr><th>标识</th><td><code>{html.escape(pkg_id)}</code></td></tr>
        <tr><th>版本</th><td>{html.escape(version)}</td></tr>
        <tr><th>架构</th><td>{html.escape(arch)}</td></tr>
        <tr><th>分类</th><td>{html.escape(section)}</td></tr>
        <tr><th>安装体积</th><td>{html.escape(inst_size)}</td></tr>
        <tr><th>包大小</th><td>{size_str}</td></tr>
        <tr><th>依赖</th><td>{html.escape(depends)}</td></tr>
        <tr><th>维护者</th><td>{html.escape(maintainer)}</td></tr>
        <tr><th>作者</th><td>{html.escape(author)}</td></tr>
      </table>
    </section>

    <p class="foot">
      来自 <a href="../index.html">{html.escape(REPO_TITLE)}</a> · 源地址 <code>{html.escape(REPO_URL)}</code>
    </p>
  </div>
</body>
</html>"""


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    packages = parse_packages(os.path.join(root, "Packages"))
    print(f"[*] 读取 Packages 成功，共 {len(packages)} 个包")

    # 1. 生成 index.html
    index_html = generate_index_html(packages)
    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("  + 已更新 index.html")

    # 2. 生成 depictions/<pkg>.html
    dep_dir = os.path.join(root, "depictions")
    os.makedirs(dep_dir, exist_ok=True)
    for p in packages:
        pkg_id = p.get("Package", "")
        html_content = generate_depiction_html(p)
        out_path = os.path.join(dep_dir, f"{pkg_id}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  + 已更新 depictions/{pkg_id}.html")

    print("[✓] 页面美化生成完毕！")


if __name__ == "__main__":
    main()
