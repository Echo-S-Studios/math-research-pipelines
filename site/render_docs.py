#!/usr/bin/env python3
"""
render_docs.py — render every Markdown doc in papers/ to a themed HTML page.

Used by the GitHub Pages workflow. Each papers/<name>.md (except README.md)
becomes <out_dir>/<name>.html: a dark/gold article page that matches the
landing site, with LaTeX math typeset by KaTeX. Drop a .md in /papers and it
is rendered automatically on the next deploy — no edits here.

Usage:  python site/render_docs.py papers _site/papers
Deps:   markdown, pymdown-extensions   (pip install markdown pymdown-extensions)
"""
import os
import re
import sys
import html

import markdown

SKIP = {"readme.md"}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} — Echo-S Studios</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#05060b">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2032%2032'%3E%3Crect%20width='32'%20height='32'%20rx='7'%20fill='%2305060b'/%3E%3Ctext%20x='16'%20y='23'%20font-size='20'%20text-anchor='middle'%20fill='%23e9c46a'%20font-family='Georgia,serif'%3E%CF%86%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" crossorigin="anonymous">
<style>
  :root{{
    --void:#05060b; --panel1:#0f1120; --ink:#e7eaf6; --muted:#a2a7c0; --line:#23273d; --edge:#2a2e44;
    --gold:#e9c46a; --teal:#5cc9c0; --violet:#8fb6ff;
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
    --ui:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
  }}
  *{{ box-sizing:border-box }}
  html,body{{ margin:0 }}
  body{{ background:radial-gradient(120% 90% at 50% 0%, #11142a 0%, #0b0d18 46%, var(--void) 100%);
    color:var(--ink); font-family:var(--ui); min-height:100vh; padding:0 0 80px; line-height:1.65;
    -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility }}
  .wrap{{ max-width:760px; margin:0 auto; padding:0 clamp(16px,4vw,28px) }}
  .topbar{{ padding:22px 0 0; font-family:var(--mono); font-size:12px; letter-spacing:.04em }}
  .topbar a{{ color:var(--muted); text-decoration:none; border-bottom:1px solid transparent }}
  .topbar a:hover,.topbar a:focus-visible{{ color:var(--ink); border-color:var(--edge); outline:none }}
  article{{ padding-top:8px }}
  article h1{{ font-family:var(--serif); font-weight:500; font-size:clamp(28px,5vw,42px); line-height:1.08;
    margin:22px 0 6px; background:linear-gradient(180deg,#fff,#d9c79a 75%,#b8975a);
    -webkit-background-clip:text; background-clip:text; color:transparent }}
  article h2{{ font-family:var(--serif); font-weight:500; font-size:25px; margin:38px 0 10px;
    padding-bottom:8px; border-bottom:1px solid var(--line) }}
  article h3{{ font-family:var(--serif); font-weight:500; font-size:20px; margin:26px 0 8px }}
  article p,article li{{ font-size:16.5px; color:#d6d9ec }}
  article em{{ color:#cfd3e6 }}
  article strong{{ color:#fff }}
  article a{{ color:var(--gold); text-decoration:none; border-bottom:1px solid var(--edge) }}
  article a:hover{{ border-color:var(--gold) }}
  blockquote{{ margin:18px 0; padding:2px 18px; border-left:3px solid var(--gold);
    background:rgba(233,196,106,.05); color:#dfe2f1; border-radius:0 8px 8px 0 }}
  hr{{ border:none; border-top:1px solid var(--line); margin:34px 0 }}
  code{{ font-family:var(--mono); font-size:.92em; background:rgba(143,182,255,.1); color:#cfe0ff;
    padding:1px 6px; border-radius:6px }}
  pre{{ background:var(--panel1); border:1px solid var(--line); border-radius:12px; padding:14px 16px; overflow:auto }}
  pre code{{ background:none; padding:0; color:var(--ink) }}
  table{{ width:100%; border-collapse:collapse; margin:20px 0; font-size:15px }}
  th,td{{ border:1px solid var(--line); padding:9px 12px; text-align:left; vertical-align:top }}
  th{{ background:rgba(143,182,255,.08); font-family:var(--mono); font-size:12px; letter-spacing:.04em;
    text-transform:uppercase; color:#cdd2e8 }}
  tr:nth-child(even) td{{ background:rgba(255,255,255,.015) }}
  .katex-display{{ overflow-x:auto; overflow-y:hidden; padding:4px 0 }}
  footer{{ margin-top:46px; padding-top:20px; border-top:1px solid var(--line);
    font-family:var(--mono); font-size:12px; color:var(--muted); display:flex; flex-wrap:wrap; gap:8px 20px }}
  footer a{{ color:var(--muted); text-decoration:none; border-bottom:1px solid transparent }}
  footer a:hover,footer a:focus-visible{{ color:var(--ink); border-color:var(--edge); outline:none }}
  @media (prefers-reduced-motion: reduce){{ *,*::before,*::after{{ transition:none !important; animation:none !important }} }}
  @media print{{ body{{ background:#fff; color:#111 }} article h1{{ -webkit-text-fill-color:#111; color:#111 }} }}
</style>
</head>
<body>
<div class="wrap">
  <nav class="topbar"><a href="../index.html">&larr; All papers</a></nav>
  <article>
{body}
  </article>
  <footer>
    <span>&copy; 2026 Echo-S Studios</span>
    <a href="{src}">Markdown source</a>
    <a href="https://github.com/Echo-S-Studios/math-research-pipelines">GitHub</a>
  </footer>
</div>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
<script>
  window.addEventListener("DOMContentLoaded", function () {{
    if (typeof renderMathInElement !== "function") return;
    renderMathInElement(document.body, {{
      delimiters: [
        {{ left: "\\\\[", right: "\\\\]", display: true }},
        {{ left: "\\\\(", right: "\\\\)", display: false }}
      ],
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
      throwOnError: false
    }});
  }});
</script>
</body>
</html>
"""


def first_heading(text, fallback):
    m = re.search(r'^\#\s+(.+?)\s*$', text, re.M)
    return m.group(1).strip() if m else fallback


def first_para(md_html):
    m = re.search(r'<p>(.*?)</p>', md_html, re.S)
    if not m:
        return ""
    plain = re.sub(r'<[^>]+>', '', m.group(1))
    plain = plain.replace('\\(', '').replace('\\)', '').replace('\\[', '').replace('\\]', '')
    plain = re.sub(r'\s+', ' ', plain).strip()
    return plain[:200]


def render_one(src_path, out_dir):
    raw = open(src_path, encoding="utf-8").read()
    stem = os.path.splitext(os.path.basename(src_path))[0]
    md = markdown.Markdown(extensions=[
        "tables", "fenced_code", "sane_lists", "attr_list",
        "pymdownx.arithmatex",
    ], extension_configs={"pymdownx.arithmatex": {"generic": True}})
    body = md.convert(raw)
    title = first_heading(raw, stem)
    desc = first_para(body)
    out = PAGE.format(
        title=html.escape(title), desc=html.escape(desc), body=body,
        src=html.escape(os.path.basename(src_path)),
    )
    out_path = os.path.join(out_dir, stem + ".html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    return out_path


def main(argv):
    src_dir = argv[1] if len(argv) > 1 else "papers"
    out_dir = argv[2] if len(argv) > 2 else "_site/papers"
    os.makedirs(out_dir, exist_ok=True)
    rendered = []
    for name in sorted(os.listdir(src_dir)):
        if name.lower().endswith(".md") and name.lower() not in SKIP:
            rendered.append(render_one(os.path.join(src_dir, name), out_dir))
    print(f"[render_docs] rendered {len(rendered)} doc(s):")
    for p in rendered:
        print("   ->", p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
