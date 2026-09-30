import csv
import html
import os

COLORS = {"shellSort": "#4e79a7", "countingSort": "#59a14f", "cocktailShakerSort": "#e15759"}
NAMES = {"shellSort": "Shell", "countingSort": "Counting", "cocktailShakerSort": "Cocktail"}
INPUTS = ["random", "sorted", "reverse", "duplicates"]


def read_rows(path="report/results.csv"):
    with open(path, newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def smart_format(value):
    """
    Format graph values compactly.
    - Very small values: scientific notation
    - Small values: decimal precision
    - Medium values: integer or one decimal place
    - Large values: K or M units
    """
    if value == 0:
        return "0"

    if abs(value) < 0.001:
        return f"{value:.1e}"
    elif abs(value) < 1:
        return f"{value:.3f}"
    elif abs(value) < 1000:
        if value == int(value):
            return f"{int(value)}"
        return f"{value:.1f}"
    elif abs(value) < 1000000:
        return f"{value / 1000:.1f}K"
    else:
        return f"{value / 1000000:.2f}M"


def write_svg(path, title, ylabel, series, x_labels):
    width, height = 860, 470
    left, top, plot_w, plot_h = 80, 65, 735, 320
    values = [value for points in series.values() for _, value in points]
    maximum = max(values or [1]) or 1
    
    chunks = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
        '<style>text{font:13px sans-serif}.title{font-size:20px;font-weight:bold}.axis{stroke:#555}.grid{stroke:#ddd}.legend{font-size:12px}.point-label{font-size:10px}</style>',
        f'<text class="title" x="{left}" y="30">{html.escape(title)}</text>',
        f'<text transform="translate(18 {top + plot_h / 2}) rotate(-90)" text-anchor="middle">{html.escape(ylabel)}</text>',
        f'<line class="axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}"/><line class="axis" x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}"/>',
    ]
    
    # 그리드와 축 레이블 생성
    for tick in range(5):
        y = top + plot_h - tick * plot_h / 4
        value = maximum * tick / 4
        chunks.append(f'<line class="grid" x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}"/>')
        # 스마트 포맷으로 축 레이블 표시
        chunks.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end">{smart_format(value)}</text>')
    
    count = max(len(x_labels), 1)
    for index, label in enumerate(x_labels):
        x = left + index * plot_w / max(count - 1, 1)
        chunks.append(f'<text x="{x:.1f}" y="{top + plot_h + 24}" text-anchor="middle">{html.escape(str(label))}</text>')
    
    # 데이터 포인트와 선 그리기
    for name, points in series.items():
        coords = []
        for index, (_, value) in enumerate(points):
            x = left + index * plot_w / max(count - 1, 1)
            y = top + plot_h - value / maximum * plot_h
            coords.append(f"{x:.1f},{y:.1f}")
        
        color = COLORS.get(name, "#777")
        
        # 연결선
        chunks.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{" ".join(coords)}"/>')
        
        # 데이터 포인트와 값 레이블
        for i, point in enumerate(coords):
            x, y = point.split(",")
            x, y = float(x), float(y)
            
            # 원형 마커
            chunks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>')
            
            # 포인트 위에 값 표시 (반올림으로 0처럼 보이는 값도 정확히 표시)
            _, value = points[i]
            label = smart_format(value)
            chunks.append(f'<text class="point-label" x="{x:.1f}" y="{y - 12:.1f}" text-anchor="middle" fill="{color}">{label}</text>')
    
    # 범례
    for index, name in enumerate(series):
        x = left + index * 170
        chunks.append(f'<line x1="{x}" y1="{height - 28}" x2="{x + 20}" y2="{height - 28}" stroke="{COLORS.get(name, "#777")}" stroke-width="3"/>')
        chunks.append(f'<text class="legend" x="{x + 26}" y="{height - 24}">{html.escape(NAMES.get(name, name))}</text>')
    
    chunks.append('</svg>')
    with open(path, "w", encoding="utf-8") as target:
        target.write("\n".join(chunks))


def grouped(rows, metric, groups):
    """주어진 메트릭을 그룹별로 집계합니다."""
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
                raise ValueError(
                    f"Missing data: "
                    f"algorithm={algorithm}, input={group}"
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

    # 1. 이론적 복잡도 그래프
    write_svg(
        "report/complexity.svg",
        "Theoretical growth (conceptual)",
        "relative cost",
        {
            "shellSort": [("n", 2), ("n²", 5)],
            "countingSort": [("n", 1), ("n+k", 2)],
            "cocktailShakerSort": [("n", 1), ("n²", 6)]
        },
        ["small", "large"]
    )

    # 2. 입력 형태에 따른 실행 시간
    write_svg(
        "report/input-time.svg",
        "Execution time by input order (n=2000)",
        "time (ms)",
        grouped(rows, "time_ms", INPUTS),
        INPUTS
    )

    # 3. 입력 형태에 따른 비교 횟수
    write_svg(
        "report/input-comparisons.svg",
        "Comparisons by input order (n=2000)",
        "comparisons",
        grouped(rows, "comparisons", INPUTS),
        INPUTS
    )

    # 4. 입력 형태에 따른 이동 횟수
    write_svg(
        "report/input-moves.svg",
        "Moves by input order (n=2000)",
        "moves",
        grouped(rows, "moves", INPUTS),
        INPUTS
    )

    # 5. 입력 크기에 따른 실행 시간 (scale-time.svg)
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

    if sizes != [128, 256, 512, 1024, 2048]:
        raise SystemExit(
            f"Unexpected block sizes: {sizes}"
        )

    # 블록 크기별 시간 변화 그래프
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
                    f"Expected exactly one block row for "
                    f"{algorithm}, n={size}, "
                    f"found {len(matching)}"
                )

            time_val = float(matching[0]["time_ms"])
            points.append((str(size), time_val))

        scale_series[algorithm] = points

    write_svg(
        "report/scale-time.svg",
        "Execution time scaling (random input)",
        "time (ms)",
        scale_series,
        [str(s) for s in sizes]
    )

    print("✓ All graphs generated successfully")
    print("  - report/complexity.svg")
    print("  - report/input-time.svg")
    print("  - report/input-comparisons.svg")
    print("  - report/input-moves.svg")
    print("  - report/scale-time.svg")


if __name__ == "__main__":
    main()
