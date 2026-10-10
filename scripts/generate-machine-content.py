#!/usr/bin/env python3
"""Export the visible homepage to Markdown using only the Python standard library."""

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parent.parent
SITE = "https://egressfox.io/"
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if self.stack[-1].tag != tag:
            raise ValueError(f"Unbalanced HTML at </{tag}>")
        self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def walk(node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def text(node):
    if isinstance(node, str):
        return node
    if node.attrs.get("aria-hidden") == "true" or node.tag in {"svg", "script", "style"}:
        return ""
    return "".join(text(child) for child in node.children)


def compact(value):
    return re.sub(r"\s+", " ", value).strip()


def render(node):
    if isinstance(node, str):
        return re.sub(r"\s+", " ", node)
    if node.attrs.get("aria-hidden") == "true" or node.tag in {"svg", "script", "style", "i"}:
        return ""
    if node.tag == "pre":
        return "\n\n```yaml\n" + text(node).strip("\n") + "\n```\n\n"
    content = "".join(render(child) for child in node.children)
    if node.tag == "a":
        heading = next((child for child in node.children if isinstance(child, Node) and child.tag == "h3"), None)
        if heading:
            description = next((child for child in node.children if isinstance(child, Node) and child.tag == "p"), None)
            suffix = f": {compact(text(description))}" if description else ""
            return f"\n- [{compact(text(heading))}]({urljoin(SITE, node.attrs['href'])}){suffix}\n"
        return f"[{compact(content)}]({urljoin(SITE, node.attrs['href'])})"
    if node.tag == "code":
        return f"`{compact(content)}`"
    if node.tag in {"h1", "h2", "h3"}:
        level = max(2, int(node.tag[1]))
        return f"\n\n{'#' * level} {compact(content)}\n\n"
    if node.tag == "p":
        return f"\n\n{compact(content)}\n\n"
    if node.tag == "li":
        # Use bullets for prose lists; step headings retain their own structure.
        if any(isinstance(child, Node) and child.tag == "h3" for child in node.children):
            return content + "\n"
        return f"\n- {compact(content)}\n"
    if node.tag in {"ul", "ol"}:
        items = [render(child).strip() for child in node.children if isinstance(child, Node) and child.tag == "li"]
        return "\n\n" + "\n".join(items) + "\n\n"
    if node.tag == "figcaption":
        return "\n\n" + " · ".join(compact(text(child)) for child in node.children if isinstance(child, Node)) + "\n\n"
    if node.tag == "br":
        return " "
    if node.tag in {"section", "article", "aside", "footer"}:
        return "\n\n" + content.strip() + "\n\n"
    return content


def generate():
    parser = PageParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    parser.close()
    if len(parser.stack) != 1:
        raise ValueError("Unclosed HTML tags")
    nodes = list(walk(parser.root))
    main = next(node for node in nodes if node.tag == "main")
    footer = next(node for node in nodes if node.tag == "footer")
    lede = next(node for node in nodes if "lede" in node.attrs.get("class", "").split())
    status = next(node for node in nodes if node.attrs.get("id") == "status")
    status_intro = next(node for node in walk(status) if node.tag == "p" and "section-intro" in node.attrs.get("class", "").split())
    status_badge = next(node for node in walk(status) if "status-badge" in node.attrs.get("class", "").split())
    eyebrow = next(node for node in walk(main) if "eyebrow" in node.attrs.get("class", "").split())
    stage = [compact(text(child)) for child in eyebrow.children if isinstance(child, Node) and compact(text(child))][-1]

    full = f"# EgressFox\n\nSource: {SITE}\n\n" + render(main) + render(footer)
    lines = []
    in_code = False
    for line in full.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        lines.append(line.rstrip() if in_code else compact(line))
    full = "\n".join(lines)
    # Collapse block spacing without changing YAML indentation.
    full = re.sub(r"\n(?:[ \t]*\n){2,}", "\n\n", full).strip() + "\n"

    short = f"# EgressFox\n\n> {compact(text(lede))}\n\nStatus: {stage}; {compact(text(status_badge))}.\n\n{compact(text(status_intro))}\n\n"
    short += "## Website\n\n"
    short += f"- [Homepage in Markdown]({SITE}index.html.md): Product, audience, workflow, YAML example, implemented capabilities, limitations, maintainer, and contact.\n"
    short += f"- [Full website text]({SITE}llms-full.txt): The complete public homepage in one Markdown document.\n"
    short += f"- [Homepage]({SITE}): The human-readable website.\n"
    short += "\n## Documentation\n\n"
    seen = set()
    for node in walk(main):
        href = node.attrs.get("href", "")
        if node.tag != "a" or "/egressfox-io/egressfox/blob/main/" not in href or href in seen:
            continue
        seen.add(href)
        title = compact(text(node))
        # Documentation cards include a heading and a description in one link.
        heading = next((child for child in node.children if isinstance(child, Node) and child.tag == "h3"), None)
        description = next((child for child in node.children if isinstance(child, Node) and child.tag == "p"), None)
        title = compact(text(heading)) if heading else title
        suffix = f": {compact(text(description))}" if description else ""
        raw = href.replace("https://github.com/egressfox-io/egressfox/blob/main/", "https://raw.githubusercontent.com/egressfox-io/egressfox/main/")
        short += f"- [{title}]({raw}){suffix}\n"
    short += "\n## Source and licensing\n\n"
    short += "- [Source repository](https://github.com/egressfox-io/egressfox): Public implementation and project README.\n"
    short += "- [License](https://raw.githubusercontent.com/egressfox-io/egressfox/main/LICENSE): Apache-2.0 for EgressFox itself.\n"
    short += "- [Third-party notices](https://raw.githubusercontent.com/egressfox-io/egressfox/main/THIRD_PARTY_NOTICES.md): Separate licenses and notices for bundled engines.\n"
    return {"index.html.md": full, "llms-full.txt": full, "llms.txt": short}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--check", action="store_true", help="Fail if committed exports differ from the homepage")
    args = cli.parse_args()
    stale = []
    for name, content in generate().items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(name)
        else:
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {name}")
    if stale:
        cli.exit(1, f"Stale machine-readable files: {', '.join(stale)}\nRun python3 scripts/generate-machine-content.py\n")
    if args.check:
        print("Machine-readable files match index.html")


if __name__ == "__main__":
    main()
