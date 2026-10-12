#!/usr/bin/env python3
"""
build_pages.py —— 生成温润质感（Notion / Linear 暖灰风）的源首页与详情页
- 浅色：柔和米白纸质底色（#fbfbfa），石墨暖黑文字（#37352f），柔和微光分界
- 深色：石墨沉静底色（#181819），微凸卡片（#212123），温润柔白文字（#ececed）
- 无高饱和刺眼蓝，去除所有 AI 味模板套路，回归精致克制的手工感
"""
import html
import os

REPO_URL = "https://repo.paynexss.fun"
REPO_TITLE = "paynexss's repo"


def human_size(n):
    try:
        n = float(n)
    except (ValueError, TypeError):
        return "-"
    if n < 1024:
        return f"{int(n)} B"
    elif n < 1024 * 1024:
        return f"{n / 1024:.1f} KB"
    else:
        return f"{n / (1024 * 1024):.1f} MB"


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
    rows = []
    for p in packages:
        pkg_id = p.get("Package", "")
        name = p.get("Name") or pkg_id
        version = p.get("Version", "1.0.0")
        desc = p.get("Description", "").split("\n")[0]
        size_str = human_size(p.get("Size", 0))

        filename = p.get("Filename", "")
        deb_href = filename[2:] if filename.startswith("./") else filename

        icon_path = f"icons/{pkg_id}.png"
        if not os.path.isfile(icon_path):
            icon_path = "CydiaIcon.png"

        depiction_href = f"depictions/{pkg_id}.html"

        row = f"""
        <div class="pkg-row" data-name="{html.escape(name.lower())}" data-id="{html.escape(pkg_id.lower())}" data-desc="{html.escape(desc.lower())}">
          <a class="row-main" href="{depiction_href}">
            <img class="pkg-icon" src="{icon_path}" alt="" width="42" height="42" loading="lazy">
            <div class="pkg-body">
              <div class="pkg-header">
                <span class="pkg-name">{html.escape(name)}</span>
                <span class="pkg-ver">v{html.escape(version)}</span>
              </div>
              <div class="pkg-id">{html.escape(pkg_id)}</div>
              <div class="pkg-desc">{html.escape(desc)}</div>
            </div>
          </a>
          <div class="row-side">
            <a class="btn-deb" href="{html.escape(deb_href)}" download title="下载 deb ({size_str})">deb</a>
            <a class="row-arrow" href="{depiction_href}" aria-label="查看详情">
              <svg width="6" height="10" viewBox="0 0 6 10" fill="none"><path d="M1 1l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </a>
          </div>
        </div>"""
        rows.append(row)

    rows_html = "\n".join(rows)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(REPO_TITLE)}</title>
  <link rel="icon" type="image/png" href="CydiaIcon.png">
  <style>
    :root {{
      --bg: #fbfbfa;
      --card-bg: #ffffff;
      --border: #eceae5;
      --border-subtle: #f2f0eb;
      --text: #37352f;
      --text-sec: #787774;
      --text-ter: #9b9a97;
      --primary-btn-bg: #2f2e2c;
      --primary-btn-text: #ffffff;
      --sec-btn-bg: #f1f0ec;
      --sec-btn-text: #37352f;
      --sec-btn-hover: #e8e6e0;
      --search-bg: #f4f3ef;
      --badge-bg: #f1f0ec;
      --badge-text: #6b6965;
      --radius: 12px;
      --font: -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Hiragino Sans GB", "Segoe UI", sans-serif;
      --mono: ui-monospace, "SF Mono", Menlo, Monaco, monospace;
    }}

    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #181819;
        --card-bg: #212123;
        --border: #2e2e31;
        --border-subtle: #272729;
        --text: #ececed;
        --text-sec: #9b9b9f;
        --text-ter: #68686c;
        --primary-btn-bg: #ececed;
        --primary-btn-text: #181819;
        --sec-btn-bg: #2c2c2f;
        --sec-btn-text: #ececed;
        --sec-btn-hover: #36363a;
        --search-bg: #262629;
        --badge-bg: #2a2a2d;
        --badge-text: #a8a8ac;
      }}
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: env(safe-area-inset-top, 24px) 16px env(safe-area-inset-bottom, 32px);
      -webkit-font-smoothing: antialiased;
    }}

    .container {{
      max-width: 560px;
      margin: 0 auto;
    }}

    /* 顶部标题栏 */
    .header {{
      display: flex;
      align-items: center;
      gap: 13px;
      padding: 18px 4px 16px;
    }}
    .repo-icon {{
      width: 44px;
      height: 44px;
      border-radius: 10px;
      border: 1px solid var(--border);
      flex-shrink: 0;
    }}
    .header-text {{
      flex: 1;
      min-width: 0;
    }}
    .header-title {{
      font-size: 1.22rem;
      font-weight: 650;
      letter-spacing: -0.015em;
      color: var(--text);
    }}
    .header-sub {{
      font-size: 0.81rem;
      color: var(--text-sec);
      margin-top: 1px;
    }}

    /* 源地址卡片 */
    .source-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 12px 14px;
      margin-bottom: 16px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }}
    .source-url-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 10px;
    }}
    .source-url {{
      font-family: var(--mono);
      font-size: 0.84rem;
      color: var(--text);
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      user-select: all;
    }}
    .btn-copy {{
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text);
      background: var(--sec-btn-bg);
      border: 1px solid var(--border);
      cursor: pointer;
      padding: 3px 9px;
      border-radius: 6px;
      flex-shrink: 0;
      transition: background 0.15s;
    }}
    .btn-copy:hover {{
      background: var(--sec-btn-hover);
    }}
    .source-actions {{
      display: flex;
      gap: 8px;
      padding-top: 10px;
      border-top: 1px solid var(--border-subtle);
    }}
    .btn-action {{
      flex: 1;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 8px 12px;
      font-size: 0.82rem;
      font-weight: 600;
      border-radius: 7px;
      text-decoration: none;
      transition: opacity 0.15s, background 0.15s;
    }}
    .btn-action.primary {{
      background: var(--primary-btn-bg);
      color: var(--primary-btn-text);
    }}
    .btn-action.secondary {{
      background: var(--sec-btn-bg);
      color: var(--sec-btn-text);
    }}
    .btn-action:hover {{
      opacity: 0.88;
    }}

    /* 搜索栏 */
    .search-wrap {{
      position: relative;
      margin-bottom: 14px;
    }}
    .search-input {{
      width: 100%;
      height: 35px;
      padding: 0 12px 0 32px;
      background: var(--search-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.86rem;
      color: var(--text);
      outline: none;
      font-family: inherit;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--text-sec);
    }}
    .search-input::placeholder {{
      color: var(--text-ter);
    }}
    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 13px;
      height: 13px;
      stroke: var(--text-ter);
      fill: none;
      stroke-width: 2;
      stroke-linecap: round;
      pointer-events: none;
    }}

    /* 列表头 */
    .list-title {{
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--text-ter);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0 4px 6px;
      display: flex;
      justify-content: space-between;
    }}

    /* 分组列表 (Inset Grouped) */
    .pkg-group {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }}
    .pkg-row {{
      display: flex;
      align-items: center;
      padding: 11px 13px;
      transition: background 0.1s;
    }}
    .pkg-row + .pkg-row {{
      border-top: 1px solid var(--border-subtle);
    }}
    .pkg-row:hover {{
      background: var(--sec-btn-bg);
    }}
    .row-main {{
      display: flex;
      align-items: center;
      gap: 12px;
      flex: 1;
      min-width: 0;
      text-decoration: none;
      color: inherit;
    }}
    .pkg-icon {{
      width: 40px;
      height: 40px;
      border-radius: 9px;
      border: 1px solid var(--border);
      flex-shrink: 0;
      object-fit: cover;
    }}
    .pkg-body {{
      flex: 1;
      min-width: 0;
    }}
    .pkg-header {{
      display: flex;
      align-items: baseline;
      gap: 6px;
    }}
    .pkg-name {{
      font-size: 0.94rem;
      font-weight: 600;
      color: var(--text);
    }}
    .pkg-ver {{
      font-size: 0.72rem;
      font-family: var(--mono);
      color: var(--badge-text);
      background: var(--badge-bg);
      padding: 1px 5px;
      border-radius: 4px;
    }}
    .pkg-id {{
      font-family: var(--mono);
      font-size: 0.72rem;
      color: var(--text-ter);
      margin-top: 1px;
    }}
    .pkg-desc {{
      font-size: 0.78rem;
      color: var(--text-sec);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-top: 2px;
    }}
    .row-side {{
      display: flex;
      align-items: center;
      gap: 6px;
      margin-left: 8px;
      flex-shrink: 0;
    }}
    .btn-deb {{
      padding: 3px 8px;
      font-size: 0.72rem;
      font-weight: 600;
      font-family: var(--mono);
      color: var(--sec-btn-text);
      background: var(--sec-btn-bg);
      border: 1px solid var(--border);
      border-radius: 5px;
      text-decoration: none;
      transition: background 0.15s;
    }}
    .btn-deb:hover {{
      background: var(--sec-btn-hover);
    }}
    .row-arrow {{
      color: var(--text-ter);
      display: flex;
      align-items: center;
      padding: 4px 2px;
      text-decoration: none;
    }}

    .empty {{
      display: none;
      padding: 24px;
      text-align: center;
      font-size: 0.84rem;
      color: var(--text-ter);
    }}

    /* 脚注 */
    .footer {{
      text-align: center;
      font-size: 0.76rem;
      color: var(--text-ter);
      padding: 12px 0 20px;
    }}
    .footer a {{
      color: var(--text-sec);
      text-decoration: none;
      border-bottom: 1px dotted var(--text-ter);
    }}
    .footer a:hover {{
      color: var(--text);
      border-bottom-color: var(--text);
    }}

    /* 复制轻提示 */
    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(50px);
      background: var(--primary-btn-bg);
      color: var(--primary-btn-text);
      padding: 6px 14px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 500;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      z-index: 100;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header class="header">
      <img class="repo-icon" src="CydiaIcon.png" alt="">
      <div class="header-text">
        <h1 class="header-title">{html.escape(REPO_TITLE)}</h1>
        <div class="header-sub">Rootless / Dopamine · iphoneos-arm64 · 自用源</div>
      </div>
    </header>

    <div class="source-card">
      <div class="source-url-row">
        <span class="source-url" id="repoUrl">{html.escape(REPO_URL)}</span>
        <button class="btn-copy" id="copyBtn" onclick="copyUrl()">复制</button>
      </div>
      <div class="source-actions">
        <a class="btn-action primary" href="sileo://source/{REPO_URL}/">加到 Sileo</a>
        <a class="btn-action secondary" href="zbra://sources/add/{REPO_URL}/">加到 Zebra</a>
      </div>
    </div>

    <div class="search-wrap">
      <svg class="search-icon" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
      <input class="search-input" id="searchInput" type="search" placeholder="搜索插件..." autocomplete="off">
    </div>

    <div class="list-title">
      <span>插件</span>
      <span id="pkgCount">{len(packages)} 个</span>
    </div>

    <div class="pkg-group" id="pkgGroup">
{rows_html}
      <div class="empty" id="emptyState">未找到匹配插件</div>
    </div>

    <div class="footer">
      <p>
        <a href="Packages">Packages</a> ·
        <a href="Packages.gz">Packages.gz</a> ·
        <a href="Release">Release</a>
      </p>
    </div>
  </div>

  <div class="toast" id="toast">已复制</div>

  <script>
    function copyUrl() {{
      const text = document.getElementById('repoUrl').innerText.trim();
      const btn = document.getElementById('copyBtn');
      const toast = document.getElementById('toast');
      navigator.clipboard.writeText(text).then(() => {{
        btn.textContent = '已复制';
        toast.classList.add('show');
        setTimeout(() => {{
          btn.textContent = '复制';
          toast.classList.remove('show');
        }}, 1800);
      }}).catch(() => prompt('复制源地址：', text));
    }}

    const input = document.getElementById('searchInput');
    const rows = Array.from(document.querySelectorAll('.pkg-row'));
    const count = document.getElementById('pkgCount');
    const empty = document.getElementById('emptyState');

    input.addEventListener('input', (e) => {{
      const q = e.target.value.trim().toLowerCase();
      let matched = 0;
      rows.forEach(r => {{
        const ok = !q || r.dataset.name.includes(q) || r.dataset.id.includes(q) || r.dataset.desc.includes(q);
        r.style.display = ok ? '' : 'none';
        if (ok) matched++;
      }});
      count.textContent = matched + ' 个';
      empty.style.display = matched === 0 ? 'block' : 'none';
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
    size_str = human_size(pkg.get("Size", 0))

    filename = pkg.get("Filename", "")
    deb_href = "../" + (filename[2:] if filename.startswith("./") else filename)

    icon_rel = f"icons/{pkg_id}.png"
    icon_src = f"../{icon_rel}" if os.path.isfile(icon_rel) else "../CydiaIcon.png"

    desc_paragraphs = "\n".join(f"<p>{html.escape(line.strip())}</p>" for line in desc.split("\n") if line.strip())

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(name)}</title>
  <style>
    :root {{
      --bg: #fbfbfa;
      --card-bg: #ffffff;
      --border: #eceae5;
      --border-subtle: #f2f0eb;
      --text: #37352f;
      --text-sec: #787774;
      --text-ter: #9b9a97;
      --primary-btn-bg: #2f2e2c;
      --primary-btn-text: #ffffff;
      --sec-btn-bg: #f1f0ec;
      --sec-btn-text: #37352f;
      --radius: 12px;
      --font: -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", sans-serif;
      --mono: ui-monospace, "SF Mono", Menlo, monospace;
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --bg: #181819;
        --card-bg: #212123;
        --border: #2e2e31;
        --border-subtle: #272729;
        --text: #ececed;
        --text-sec: #9b9b9f;
        --text-ter: #68686c;
        --primary-btn-bg: #ececed;
        --primary-btn-text: #181819;
        --sec-btn-bg: #2c2c2f;
        --sec-btn-text: #ececed;
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: var(--font);
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: env(safe-area-inset-top, 20px) 16px env(safe-area-inset-bottom, 28px);
      -webkit-font-smoothing: antialiased;
    }}
    .container {{
      max-width: 520px;
      margin: 0 auto;
    }}
    .nav {{
      margin-bottom: 12px;
    }}
    .nav a {{
      color: var(--text-sec);
      text-decoration: none;
      font-size: 0.86rem;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}
    .nav a:hover {{
      color: var(--text);
    }}
    .header-card {{
      background: var(--card-bg);
      border-radius: var(--radius);
      border: 1px solid var(--border);
      padding: 13px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }}
    .pkg-icon {{
      width: 48px;
      height: 48px;
      border-radius: 10px;
      border: 1px solid var(--border);
      object-fit: cover;
    }}
    .header-info {{
      flex: 1;
      min-width: 0;
    }}
    .pkg-name {{
      font-size: 1.12rem;
      font-weight: 650;
      color: var(--text);
    }}
    .pkg-id {{
      font-family: var(--mono);
      font-size: 0.72rem;
      color: var(--text-ter);
      margin-top: 1px;
    }}
    .btn-download {{
      padding: 6px 13px;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--primary-btn-text);
      background: var(--primary-btn-bg);
      border-radius: 7px;
      text-decoration: none;
      transition: opacity 0.15s;
    }}
    .btn-download:hover {{
      opacity: 0.88;
    }}
    .card {{
      background: var(--card-bg);
      border-radius: var(--radius);
      border: 1px solid var(--border);
      padding: 14px;
      margin-bottom: 12px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
    }}
    .card-title {{
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--text-ter);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 8px;
    }}
    .desc p {{
      font-size: 0.86rem;
      color: var(--text);
      line-height: 1.55;
    }}
    .table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
    }}
    .table tr + tr {{
      border-top: 1px solid var(--border-subtle);
    }}
    .table th {{
      text-align: left;
      padding: 7px 0;
      color: var(--text-sec);
      font-weight: 400;
      width: 32%;
    }}
    .table td {{
      padding: 7px 0;
      color: var(--text);
      word-break: break-all;
    }}
    .footer {{
      text-align: center;
      font-size: 0.74rem;
      color: var(--text-ter);
      margin-top: 16px;
    }}
    .footer code {{
      font-family: var(--mono);
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="nav">
      <a href="../index.html">‹ 返回源首页</a>
    </div>

    <div class="header-card">
      <img class="pkg-icon" src="{icon_src}" alt="">
      <div class="header-info">
        <h1 class="pkg-name">{html.escape(name)}</h1>
        <div class="pkg-id">{html.escape(pkg_id)} · v{html.escape(version)}</div>
      </div>
      <a class="btn-download" href="{html.escape(deb_href)}" download>下载</a>
    </div>

    <div class="card">
      <div class="card-title">简介</div>
      <div class="desc">{desc_paragraphs}</div>
    </div>

    <div class="card">
      <div class="card-title">信息</div>
      <table class="table">
        <tr><th>标识</th><td><code>{html.escape(pkg_id)}</code></td></tr>
        <tr><th>版本</th><td>{html.escape(version)}</td></tr>
        <tr><th>架构</th><td>{html.escape(arch)}</td></tr>
        <tr><th>分类</th><td>{html.escape(section)}</td></tr>
        <tr><th>大小</th><td>{size_str}</td></tr>
        <tr><th>依赖</th><td>{html.escape(depends)}</td></tr>
        <tr><th>维护者</th><td>{html.escape(maintainer)}</td></tr>
      </table>
    </div>

    <div class="footer">
      paynexss's repo · <code>{html.escape(REPO_URL)}</code>
    </div>
  </div>
</body>
</html>"""


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)

    packages = parse_packages(os.path.join(root, "Packages"))
    print(f"[*] 读取 Packages 成功，共 {len(packages)} 个包")

    with open(os.path.join(root, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_index_html(packages))
    print("  + 已更新 index.html")

    dep_dir = os.path.join(root, "depictions")
    os.makedirs(dep_dir, exist_ok=True)
    for p in packages:
        pkg_id = p.get("Package", "")
        with open(os.path.join(dep_dir, f"{pkg_id}.html"), "w", encoding="utf-8") as f:
            f.write(generate_depiction_html(p))
        print(f"  + 已更新 depictions/{pkg_id}.html")

    print("[✓] 页面生成完毕！")


if __name__ == "__main__":
    main()
