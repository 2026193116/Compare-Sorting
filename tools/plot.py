import csv
import html
import os

COLORS = {
    "shellSort": "#4e79a7",
    "countingSort": "#59a14f",
    "cocktailShakerSort": "#e15759",
}

NAMES = {
    "shellSort": "Shell",
    "countingSort": "Counting",
    "cocktailShakerSort": "Cocktail",
}

INPUTS = [
    "random",
    "sorted",
    "reverse",
    "duplicates",
]


def read_rows(path="report/results.csv"):
    with open(path, newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))

    if not rows:
        raise SystemExit(
            f"No result data found in {path}"
        )

    return rows


def smart_format(value):
    if value == 0:
        return "0"

    if abs(value) < 0.001:
        return f"{value:.1e}"
    if abs(value) < 1:
        return f"{value:.3f}"
    if abs(value) < 1000:
        if value == int(value):
            return f"{int(value)}"
        return f"{value:.1f}"
    if abs(value) < 1_000_000:
        return f"{value / 1000:.1f}K"

    return f"{value / 1_000_000:.2f}M"


def write_svg(path, title, ylabel, series, x_labels):
    width, height = 860, 470
    left, top, plot_w, plot_h = 80, 65, 735, 320

    values = [
        value
        for points in series.values()
        for _, value in points
    ]

    maximum = max(values or [1])
    if maximum <= 0:
        maximum = 1

    chunks = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {width} {height}">'
        ),
        (
            "<style>"
            "text{font:13px sans-serif}"
            ".title{font-size:20px;font-weight:bold}"
            ".axis{stroke:#555}"
            ".grid{stroke:#ddd}"
            ".legend{font-size:12px}"
            ".point-label{font-size:10px}"
            "</style>"
        ),
        (
            f'<text class="title" x="{left}" y="30">'
            f'{html.escape(title)}</text>'
        ),
        (
            f'<text transform="translate(18 '
            f'{top + plot_h / 2}) rotate(-90)" '
            f'text-anchor="middle">'
            f'{html.escape(ylabel)}</text>'
        ),
        (
            f'<line class="axis" '
            f'x1="{left}" y1="{top}" '
            f'x2="{left}" y2="{top + plot_h}"/>'
            f'<line class="axis" '
            f'x1="{left}" y1="{top + plot_h}" '
            f'x2="{left + plot_w}" y2="{top + plot_h}"/>'
        ),
    ]

    for tick in range(5):
        y = top + plot_h - tick * plot_h / 4
        value = maximum * tick / 4

        chunks.append(
            f'<line class="grid" '
            f'x1="{left}" y1="{y:.1f}" '
            f'x2="{left + plot_w}" y2="{y:.1f}"/>'
        )

        chunks.append(
            f'<text x="{left - 8}" y="{y + 4:.1f}" '
            f'text-anchor="end">'
            f'{smart_format(value)}</text>'
        )

    count = max(len(x_labels), 1)

    for index, label in enumerate(x_labels):
        x = left + index * plot_w / max(count - 1, 1)

        chunks.append(
            f'<text x="{x:.1f}" '
            f'y="{top + plot_h + 24}" '
            f'text-anchor="middle">'
            f'{html.escape(str(label))}</text>'
        )

    for name, points in series.items():
        coords = []

        for index, (_, value) in enumerate(points):
            x = left + index * plot_w / max(count - 1, 1)
            y = (
                top
                + plot_h
                - value / maximum * plot_h
            )

            coords.append(f"{x:.1f},{y:.1f}")

        color = COLORS.get(name, "#777")

        chunks.append(
            f'<polyline fill="none" '
            f'stroke="{color}" stroke-width="3" '
            f'points="{" ".join(coords)}"/>'
        )

        for i, point in enumerate(coords):
            x, y = point.split(",")
            value = points[i][1]

            chunks.append(
                f'<circle cx="{x}" cy="{y}" '
                f'r="4" fill="{color}"/>'
            )

            label = smart_format(value)

            chunks.append(
                f'<text class="point-label" '
                f'x="{x}" y="{float(y) - 12:.1f}" '
                f'text-anchor="middle" '
                f'fill="{color}">'
                f'{label}</text>'
            )

    for index, name in enumerate(series):
        x = left + index * 170
        color = COLORS.get(name, "#777")

        chunks.append(
            f'<line x1="{x}" '
            f'y1="{height - 28}" '
            f'x2="{x + 20}" '
            f'y2="{height - 28}" '
            f'stroke="{color}" stroke-width="3"/>'
        )

        chunks.append(
            f'<text class="legend" '
            f'x="{x + 26}" '
            f'y="{height - 24}">'
            f'{html.escape(NAMES.get(name, name))}</text>'
        )

    chunks.append("</svg>")

    with open(path, "w", encoding="utf-8") as target:
        target.write("\n".join(chunks))


def grouped(rows, metric, groups):
    result = {}

    for algorithm in COLORS:
        result[algorithm] = []

        for group in groups:
            matches = [
                row
                for row in rows
                if (
                    row["algorithm"] == algorithm
                    and row["input"] == group
                )
            ]

            if not matches:
                raise SystemExit(
                    "Missing data: "
                    f"algorithm={algorithm}, "
                    f"input={group}"
                )

            values = [
                float(row[metric])
                for row in matches
            ]

            result[algorithm].append(
                (
                    group,
                    sum(values) / len(values)
                )
            )

    return result


def main():
    rows = read_rows()

    os.makedirs("report", exist_ok=True)

    # 1. Conceptual, not measured, complexity illustration.
    write_svg(
        "report/complexity.svg",
        "Conceptual complexity growth (illustrative)",
        "illustrative relative cost",
        {
            "shellSort": [
                ("n", 1),
                ("n^1.5", 3),
            ],
            "countingSort": [
                ("n", 1),
                ("n+k", 2),
            ],
            "cocktailShakerSort": [
                ("n", 1),
                ("n^2", 6),
            ],
        },
        ["small", "large"],
    )

    input_rows = [
        row
        for row in rows
        if row["input"] in INPUTS
    ]

    input_sizes = {
        int(row["n"])
        for row in input_rows
    }

    if len(input_sizes) != 1:
        raise SystemExit(
            f"Expected one common input size for input-order "
            f"graphs, found: {sorted(input_sizes)}"
        )

    input_n = next(iter(input_sizes))

    # 2. Execution time by input order.
    write_svg(
        "report/input-time.svg",
        f"Execution time by input order (n={input_n})",
        "time (ms)",
        grouped(
            rows,
            "time_ms",
            INPUTS,
        ),
        INPUTS,
    )

    # 3. Comparisons by input order.
    write_svg(
        "report/input-comparisons.svg",
        f"Comparisons by input order (n={input_n})",
        "comparisons",
        grouped(
            rows,
            "comparisons",
            INPUTS,
        ),
        INPUTS,
    )

    # 4. Moves by input order.
    write_svg(
        "report/input-moves.svg",
        f"Moves by input order (n={input_n})",
        "moves",
        grouped(
            rows,
            "moves",
            INPUTS,
        ),
        INPUTS,
    )

    # 5. Execution time as input size grows.
    block_rows = [
        row
        for row in rows
        if row["input"] == "block"
    ]

    if not block_rows:
        raise SystemExit(
            "No block data found. "
            "Run: make charts"
        )

    sizes = sorted(
        {
            int(row["n"])
            for row in block_rows
        }
    )

    if len(sizes) < 2:
        raise SystemExit(
            f"Need at least two block sizes, found: {sizes}"
        )

    scale_series = {}

    for algorithm in COLORS:
        points = []

        for size in sizes:
            matching = [
                row
                for row in block_rows
                if (
                    row["algorithm"] == algorithm
                    and int(row["n"]) == size
                )
            ]

            if len(matching) != 1:
                raise SystemExit(
                    "Expected exactly one block row "
                    f"for {algorithm}, n={size}, "
                    f"found {len(matching)}"
                )

            time_val = float(
                matching[0]["time_ms"]
            )

            points.append(
                (
                    str(size),
                    time_val,
                )
            )

        scale_series[algorithm] = points

    write_svg(
        "report/scale-time.svg",
        "Execution time scaling (random input)",
        "time (ms)",
        scale_series,
        [str(size) for size in sizes],
    )

    print("All graphs generated successfully")
    print("  - report/complexity.svg")
    print("  - report/input-time.svg")
    print("  - report/input-comparisons.svg")
    print("  - report/input-moves.svg")
    print("  - report/scale-time.svg")


if __name__ == "__main__":
    main()
