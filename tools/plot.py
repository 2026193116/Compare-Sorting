import csv
import html
import os

COLORS = {"shellSort": "#4e79a7", "countingSort": "#59a14f", "cocktailShakerSort": "#e15759"}
NAMES = {"shellSort": "Shell", "countingSort": "Counting", "cocktailShakerSort": "Cocktail"}
INPUTS = ["random", "sorted", "reverse", "duplicates"]


def read_rows(path="report/results.csv"):
    with open(path, newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def write_svg(path, title, ylabel, series, x_labels):
    width, height = 860, 470
    left, top, plot_w, plot_h = 80, 65, 735, 320
    values = [value for points in series.values() for _, value in points]
    maximum = max(values or [1]) or 1
    chunks = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<style>text{font:13px sans-serif}.title{font-size:20px;font-weight:bold}.axis{stroke:#555}.grid{stroke:#ddd}.legend{font-size:12px}</style>',
        f'<text class="title" x="{left}" y="30">{html.escape(title)}</text>',
        f'<text transform="translate(18 {top + plot_h / 2}) rotate(-90)" text-anchor="middle">{html.escape(ylabel)}</text>',
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}"/><line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>',
    ]
    for tick in range(5):
        y = top + plot_h - tick * plot_h / 4
        value = maximum * tick / 4
        chunks.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
        chunks.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{value:.2g}</text>')
    count = max(len(x_labels), 1)
    for index, label in enumerate(x_labels):
        x = left + index * plot_w / max(count - 1, 1)
        chunks.append(f'<text x="{x:.1f}" y="{top + plot_h + 24}" text-anchor="middle">{html.escape(str(label))}</text>')
    for name, points in series.items():
        coords = []
        for index, (_, value) in enumerate(points):
            x = left + index * plot_w / max(count - 1, 1)
            y = top + plot_h - value / maximum * plot_h
            coords.append(f"{x:.1f},{y:.1f}")
        color = COLORS.get(name, "#777")
        chunks.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{" ".join(coords)}"/>')
        for point in coords:
            x, y = point.split(",")
            chunks.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
    for index, name in enumerate(series):
        x = left + index * 170
        chunks.append(f'<line x1="{x}" y1="{height - 28}" x2="{x + 20}" y2="{height - 28}" stroke="{COLORS.get(name, "#777")}" stroke-width="3"/>')
        chunks.append(f'<text class="legend" x="{x + 26}" y="{height - 24}">{html.escape(NAMES.get(name, name))}</text>')
    chunks.append('</svg>')
    with open(path, "w", encoding="utf-8") as target:
        target.write("\n".join(chunks))


def grouped(rows, metric, groups):
    result = {}
    for algorithm in COLORS:
        result[algorithm] = []
        for group in groups:
            matches = [r for r in rows if r["algorithm"] == algorithm and r["input"] == group]
            result[algorithm].append((group, sum(float(r[metric]) for r in matches) / max(len(matches), 1)))
    return result


def main():
    rows = read_rows()
    os.makedirs("report", exist_ok=True)
    write_svg("report/complexity.svg", "Theoretical growth (conceptual)", "relative cost", {"shellSort": [("n", 2), ("n²", 5)], "countingSort": [("n", 1), ("n+k", 2)], "cocktailShakerSort": [("n", 1), ("n²", 6)]}, ["small", "large"])
    write_svg("report/input-time.svg", "Execution time by input order", "time (ms)", grouped(rows, "time_ms", INPUTS), INPUTS)
    write_svg("report/input-comparisons.svg", "Comparisons by input order", "comparisons", grouped(rows, "comparisons", INPUTS), INPUTS)
    write_svg("report/input-moves.svg", "Moves by input order", "moves", grouped(rows, "moves", INPUTS), INPUTS)
    block_rows = [r for r in rows if r["input"] == "block"]
    sizes = sorted({int(r["n"]) for r in block_rows})
    series = {algorithm: [(str(n), sum(float(r["time_ms"]) for r in block_rows if r["algorithm"] == algorithm and int(r["n"]) == n) / max(len([r for r in block_rows if r["algorithm"] == algorithm and int(r["n"]) == n]), 1)) for n in sizes] for algorithm in COLORS}
    write_svg("report/scale-time.svg", "Execution time as n grows", "time (ms)", series, sizes)


if __name__ == "__main__":
    main()
