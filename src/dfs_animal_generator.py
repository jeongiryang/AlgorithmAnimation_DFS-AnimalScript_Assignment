#!/usr/bin/env python3
"""Generate AnimalScript animation files for DFS on fixed A-G graphs."""

from __future__ import annotations

import math
import sys
from pathlib import Path


NODES = tuple("ABCDEFG")
START_NODE = "A"
NODE_RADIUS = 24

NODE_POSITIONS = {
    "A": (360, 130),
    "B": (180, 270),
    "C": (360, 270),
    "D": (540, 270),
    "E": (180, 430),
    "F": (360, 430),
    "G": (540, 430),
}

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "edge_gray": (165, 165, 165),
    "visited_gray": (190, 190, 190),
    "current_pink": (255, 174, 201),
    "candidate_blue": (128, 184, 255),
    "tree_edge": (35, 35, 35),
    "panel_fill": (245, 247, 250),
    "green": (109, 172, 97),
}


class InputError(ValueError):
    """Raised when the graph input file is invalid."""


def color(name: str) -> str:
    """Return an AnimalScript RGB color literal."""
    red, green, blue = COLORS[name]
    return f"({red}, {green}, {blue})"


def animal_text(value: str) -> str:
    """Escape text for an AnimalScript quoted string."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def normalize_edge(edge: str) -> tuple[str, str]:
    left, right = edge[0], edge[1]
    return tuple(sorted((left, right)))


def edge_id(left: str, right: str) -> str:
    first, second = sorted((left, right))
    return f"{first}{second}"


def parse_graph(input_path: Path) -> tuple[dict[str, list[str]], list[tuple[str, str]], list[str]]:
    if not input_path.exists():
        raise InputError(f"입력 파일을 찾을 수 없습니다: {input_path}")

    raw_lines = input_path.read_text(encoding="utf-8").splitlines()
    if not raw_lines:
        raise InputError("입력 파일이 비어 있습니다.")

    count_line = raw_lines[0].strip()
    if not count_line.isdigit():
        raise InputError("첫 줄에는 0 이상의 간선 개수를 숫자로 입력해야 합니다.")

    expected_count = int(count_line)
    edge_lines = [line.strip() for line in raw_lines[1:] if line.strip()]
    if len(edge_lines) != expected_count:
        raise InputError(
            f"간선 개수가 일치하지 않습니다: 첫 줄={expected_count}, 실제={len(edge_lines)}"
        )

    adjacency = {node: set() for node in NODES}
    unique_edges: list[tuple[str, str]] = []
    seen_edges: set[tuple[str, str]] = set()
    warnings: list[str] = []

    for line_number, edge in enumerate(edge_lines, start=2):
        if len(edge) != 2:
            raise InputError(f"{line_number}번째 줄의 간선 형식이 잘못되었습니다: {edge}")

        left, right = edge[0], edge[1]
        if left not in NODES or right not in NODES:
            raise InputError(
                f"{line_number}번째 줄의 노드가 허용 범위를 벗어났습니다: {edge}"
            )
        if left == right:
            raise InputError(f"{line_number}번째 줄의 자기 간선은 허용되지 않습니다: {edge}")

        normalized = normalize_edge(edge)
        if normalized in seen_edges:
            warnings.append(
                f"중복 간선을 무시했습니다: {normalized[0]}{normalized[1]} "
                f"(입력 {line_number}번째 줄)"
            )
            continue

        seen_edges.add(normalized)
        unique_edges.append(normalized)
        first, second = normalized
        adjacency[first].add(second)
        adjacency[second].add(first)

    sorted_adjacency = {node: sorted(neighbors) for node, neighbors in adjacency.items()}
    unique_edges.sort()
    return sorted_adjacency, unique_edges, warnings


def trace_dfs(adjacency: dict[str, list[str]]) -> tuple[list[str], list[tuple[str, str]], list[dict]]:
    visited: set[str] = set()
    visit_order: list[str] = []
    tree_edges: list[tuple[str, str]] = []
    events: list[dict] = []
    stack: list[str] = []

    def current_candidates(node: str) -> list[str]:
        return [neighbor for neighbor in adjacency[node] if neighbor not in visited]

    def snapshot(
        event_type: str,
        description: str,
        current: str | None = None,
        candidates: list[str] | None = None,
        selected_candidate: str | None = None,
        new_tree_edge: tuple[str, str] | None = None,
    ) -> None:
        events.append(
            {
                "type": event_type,
                "description": description,
                "current": current,
                "visited": list(visit_order),
                "stack": list(stack),
                "candidates": list(candidates or []),
                "selected_candidate": selected_candidate,
                "tree_edges": list(tree_edges),
                "new_tree_edge": new_tree_edge,
            }
        )

    def dfs(node: str) -> None:
        visited.add(node)
        visit_order.append(node)
        stack.append(node)
        candidates = current_candidates(node)
        snapshot(
            "visit",
            f"{node}를 방문합니다. 방문 순서에 {node}를 추가합니다.",
            current=node,
            candidates=candidates,
        )

        for neighbor in adjacency[node]:
            if neighbor in visited:
                continue

            remaining_candidates = current_candidates(node)
            snapshot(
                "candidate",
                f"{node}의 인접 노드 중 방문하지 않은 {neighbor}를 후보로 선택합니다.",
                current=node,
                candidates=remaining_candidates,
                selected_candidate=neighbor,
            )

            new_edge = (node, neighbor)
            tree_edges.append(new_edge)
            snapshot(
                "tree_edge",
                f"{node}에서 {neighbor}로 이동합니다. 간선 {node}{neighbor}를 DFS tree edge로 강조합니다.",
                current=node,
                candidates=[neighbor],
                selected_candidate=neighbor,
                new_tree_edge=new_edge,
            )
            dfs(neighbor)

        stack.pop()
        if stack:
            parent = stack[-1]
            snapshot(
                "backtrack",
                f"{node}의 방문 가능한 인접 노드를 모두 처리했습니다. {parent}로 되돌아갑니다.",
                current=parent,
                candidates=current_candidates(parent),
            )
        else:
            snapshot(
                "complete",
                "DFS가 완료되었습니다.",
                current=None,
                candidates=[],
            )

    dfs(START_NODE)
    return visit_order, tree_edges, events


def shortened_line_points(
    start: tuple[int, int],
    end: tuple[int, int],
    inset: int = NODE_RADIUS + 3,
) -> tuple[tuple[float, float], tuple[float, float]]:
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return start, end
    ux = dx / distance
    uy = dy / distance
    return (x1 + ux * inset, y1 + uy * inset), (x2 - ux * inset, y2 - uy * inset)


def offset_points(
    start: tuple[float, float],
    end: tuple[float, float],
    offset: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return (round(x1), round(y1)), (round(x2), round(y2))
    nx = -dy / distance
    ny = dx / distance
    return (
        (round(x1 + nx * offset), round(y1 + ny * offset)),
        (round(x2 + nx * offset), round(y2 + ny * offset)),
    )


def point(value: tuple[int, int] | tuple[float, float]) -> str:
    x, y = value
    return f"({round(x)}, {round(y)})"


def emit_set_text(name: str, value: str) -> str:
    return f'setText "{name}" "{animal_text(value)}"'


def emit_node_state(event: dict) -> list[str]:
    visited = set(event["visited"])
    candidates = set(event["candidates"])
    current = event["current"]
    selected_candidate = event["selected_candidate"]
    lines: list[str] = []

    for node in NODES:
        if node == current:
            fill = "current_pink"
        elif node == selected_candidate or (node in candidates and node not in visited):
            fill = "candidate_blue"
        elif node in visited:
            fill = "visited_gray"
        else:
            fill = "white"
        lines.append(f'setColor "node_{node}" fillColor {color(fill)}')

    return lines


def emit_tree_edge(edge: tuple[str, str]) -> list[str]:
    left, right = edge
    edge_name = edge_id(left, right)
    start, end = shortened_line_points(NODE_POSITIONS[left], NODE_POSITIONS[right])
    lines = [f'# thick DFS tree edge {left}{right}']
    for index, offset in enumerate((-3, 0, 3), start=1):
        shifted_start, shifted_end = offset_points(start, end, offset)
        lines.append(
            f'polyline "tree_{edge_name}_{index}" {point(shifted_start)} '
            f'{point(shifted_end)} color {color("tree_edge")} depth 1'
        )
    return lines


def emit_base_layout(title: str, edges: list[tuple[str, str]]) -> list[str]:
    lines = [
        "%Animal 2",
        f'title "{animal_text(title)}"',
        'author "DFS AnimalScript Generator"',
        "stepMode true",
        "",
        f'text "title" "{animal_text(title)}" (40, 30) color {color("black")} font SansSerif size 24 bold',
        f'text "subtitle" "Start node: A | Neighbor order: alphabetical | Undirected graph" (40, 62) color {color("black")} font SansSerif size 14',
        "",
        f'rect "graph_panel" (40, 90) (640, 500) color {color("edge_gray")} fillColor {color("panel_fill")} filled depth 8',
        f'text "graph_label" "Graph Area" (55, 100) color {color("black")} font SansSerif size 14 bold',
        f'rect "info_panel" (680, 90) (1080, 500) color {color("edge_gray")} fillColor {color("panel_fill")} filled depth 8',
        f'text "info_label" "DFS Trace" (695, 100) color {color("black")} font SansSerif size 14 bold',
        "",
        f'text "step_heading" "Current Step" (700, 135) color {color("black")} font SansSerif size 13 bold',
        f'text "step_text" "Initial graph loaded." (700, 160) color {color("black")} font SansSerif size 13',
        f'text "order_heading" "Visit Order" (700, 205) color {color("black")} font SansSerif size 13 bold',
        f'text "order_text" "-" (700, 230) color {color("black")} font SansSerif size 13',
        f'text "stack_heading" "DFS Stack" (700, 275) color {color("black")} font SansSerif size 13 bold',
        f'text "stack_text" "-" (700, 300) color {color("black")} font SansSerif size 13',
        f'text "candidate_heading" "Candidate Nodes" (700, 345) color {color("black")} font SansSerif size 13 bold',
        f'text "candidate_text" "-" (700, 370) color {color("black")} font SansSerif size 13',
        f'text "tree_heading" "DFS Tree Edges" (700, 415) color {color("black")} font SansSerif size 13 bold',
        f'text "tree_text" "-" (700, 440) color {color("black")} font SansSerif size 13',
        "",
        f'rect "legend_panel" (40, 525) (1080, 645) color {color("edge_gray")} fillColor {color("panel_fill")} filled depth 8',
        f'text "legend_title" "Legend" (55, 540) color {color("black")} font SansSerif size 14 bold',
    ]

    legend_items = [
        ("legend_initial", "Initial node", "white", 65, 585),
        ("legend_visited", "Visited node", "visited_gray", 230, 585),
        ("legend_current", "Current node", "current_pink", 395, 585),
        ("legend_candidate", "Candidate node", "candidate_blue", 575, 585),
    ]
    for name, label, fill, x, y in legend_items:
        lines.extend(
            [
                f'circle "{name}" ({x}, {y}) radius 12 color {color("black")} fillColor {color(fill)} filled depth 2',
                f'text "{name}_text" "{label}" ({x + 20}, {y - 8}) color {color("black")} font SansSerif size 12',
            ]
        )

    lines.extend(
        [
            f'polyline "legend_edge" (760, 585) (820, 585) color {color("edge_gray")} depth 3',
            f'text "legend_edge_text" "Initial edge" (830, 577) color {color("black")} font SansSerif size 12',
            f'polyline "legend_tree_1" (940, 582) (1000, 582) color {color("tree_edge")} depth 1',
            f'polyline "legend_tree_2" (940, 585) (1000, 585) color {color("tree_edge")} depth 1',
            f'polyline "legend_tree_3" (940, 588) (1000, 588) color {color("tree_edge")} depth 1',
            f'text "legend_tree_text" "DFS tree edge" (1010, 577) color {color("black")} font SansSerif size 12',
            "",
            "# base graph edges",
        ]
    )

    for left, right in edges:
        start, end = shortened_line_points(NODE_POSITIONS[left], NODE_POSITIONS[right])
        lines.append(
            f'polyline "edge_{edge_id(left, right)}" {point(start)} {point(end)} '
            f'color {color("edge_gray")} depth 5'
        )

    lines.extend(["", "# graph nodes"])
    for node in NODES:
        x, y = NODE_POSITIONS[node]
        lines.extend(
            [
                f'circle "node_{node}" ({x}, {y}) radius {NODE_RADIUS} color {color("black")} fillColor {color("white")} filled depth 2',
                f'text "label_{node}" "{node}" ({x - 5}, {y - 9}) color {color("black")} font SansSerif size 16 bold depth 1',
            ]
        )

    lines.extend(["", 'nextStep "Initial graph"'])
    return lines


def format_order(nodes: list[str]) -> str:
    return " -> ".join(nodes) if nodes else "-"


def format_edges(edges: list[tuple[str, str]]) -> str:
    return ", ".join(f"{left}{right}" for left, right in edges) if edges else "-"


def emit_event(event: dict, index: int) -> list[str]:
    lines = [
        "",
        f"# Step {index}: {event['type']}",
    ]
    new_tree_edge = event.get("new_tree_edge")
    if new_tree_edge:
        lines.extend(emit_tree_edge(new_tree_edge))

    lines.extend(emit_node_state(event))
    lines.extend(
        [
            emit_set_text("step_text", event["description"]),
            emit_set_text("order_text", format_order(event["visited"])),
            emit_set_text("stack_text", format_order(event["stack"])),
            emit_set_text("candidate_text", ", ".join(event["candidates"]) if event["candidates"] else "-"),
            emit_set_text("tree_text", format_edges(event["tree_edges"])),
            f'nextStep "{animal_text(event["description"][:60])}"',
        ]
    )
    return lines


def generate_animalscript(
    title: str,
    edges: list[tuple[str, str]],
    events: list[dict],
) -> str:
    lines = emit_base_layout(title, edges)
    for index, event in enumerate(events, start=1):
        lines.extend(emit_event(event, index))
    lines.append("")
    return "\n".join(lines)


def write_animalscript(
    output_path: Path,
    input_path: Path,
    edges: list[tuple[str, str]],
    events: list[dict],
) -> None:
    title = f"DFS Animation - {input_path.stem}"
    script = generate_animalscript(title, edges, events)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(script, encoding="utf-8")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python src/dfs_animal_generator.py <input-file> <output-file>",
            file=sys.stderr,
        )
        return 2

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    try:
        adjacency, edges, warnings = parse_graph(input_path)
        visit_order, tree_edges, events = trace_dfs(adjacency)
        write_animalscript(output_path, input_path, edges, events)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Error: 파일 처리 중 문제가 발생했습니다: {exc}", file=sys.stderr)
        return 1

    for warning in warnings:
        print(f"Warning: {warning}")

    print(f"DFS visit order: {format_order(visit_order)}")
    print(f"DFS tree edges: {format_edges(tree_edges)}")
    print(f"AnimalScript generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
