"""Generate a self-contained vector PDF for the current HBntory architecture."""

from pathlib import Path


PAGE_WIDTH, PAGE_HEIGHT = 841.89, 595.28  # A4 landscape, in PostScript points
OUTPUT = Path(__file__).with_name("architecture_diagram.pdf")


def pdf_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_pdf() -> bytes:
    commands: list[str] = ["0.95 0.97 1 rg 0 0 841.89 595.28 re f"]

    def text(x: float, y: float, value: str, size: float = 10, bold: bool = False) -> None:
        font = "F2" if bold else "F1"
        commands.append(f"BT /{font} {size} Tf 0.08 0.12 0.2 rg {x} {y} Td ({pdf_text(value)}) Tj ET")

    def box(x: float, y: float, width: float, height: float, title: str, details: list[str], color: str) -> None:
        commands.append(f"{color} rg {x} {y} {width} {height} re f")
        commands.append(f"0.32 0.39 0.5 RG 1.2 w {x} {y} {width} {height} re S")
        text(x + 10, y + height - 20, title, 11, True)
        for index, line in enumerate(details):
            text(x + 10, y + height - 37 - index * 13, line, 8.5)

    def arrow(x1: float, y1: float, x2: float, y2: float, label: str, dashed: bool = False) -> None:
        dash = "[4 3] 0 d" if dashed else "[] 0 d"
        commands.append(f"0.2 0.3 0.45 RG 1.25 w {dash} {x1} {y1} m {x2} {y2} l S [] 0 d")
        # Arrowhead calculated for horizontal and vertical diagram links.
        if abs(x2 - x1) >= abs(y2 - y1):
            direction = 1 if x2 >= x1 else -1
            commands.append(f"{x2} {y2} m {x2 - 7 * direction} {y2 + 4} l {x2 - 7 * direction} {y2 - 4} l h f")
        else:
            direction = 1 if y2 >= y1 else -1
            commands.append(f"{x2} {y2} m {x2 + 4} {y2 - 7 * direction} l {x2 - 4} {y2 - 7 * direction} l h f")
        if label:
            text((x1 + x2) / 2 - max(18, len(label) * 2), (y1 + y2) / 2 + 7, label, 7.5)

    text(35, 558, "HBntory - Architecture globale (etat actuel)", 20, True)
    text(35, 540, "Flux pleins : appels actifs. Flux pointilles : composant present mais non integre au parcours principal.", 9)

    # Interfaces.
    box(35, 365, 145, 72, "Client Web", ["HTML / CSS / JavaScript", "Port 8080"], "0.84 0.91 1")
    box(35, 145, 145, 72, "Backoffice", ["FastAPI - administration", "Port 8003"], "0.88 0.94 0.86")

    # Application services.
    box(285, 365, 160, 82, "Service IA", ["FastAPI", "POST /api/v1/query", "Port 8002"], "1 0.92 0.78")
    box(505, 480, 145, 52, "Groq API", ["LLM et tool calling"], "0.95 0.87 1")
    box(505, 325, 165, 82, "Backend", ["Auth - Users - Branches", "Stocks - routes internes", "Port 8000"], "0.8 0.9 0.95")
    box(700, 420, 110, 82, "API Produits", ["Catalogue", "placeholder", "Port 8001"], "1 0.9 0.82")
    box(505, 180, 165, 62, "Serveur MCP", ["FastMCP / stdio", "outils produits et stock"], "0.94 0.9 0.82")

    # Data stores.
    box(285, 145, 160, 72, "SQLite", ["backoffice.db", "base propre au backoffice"], "0.91 0.91 0.91")
    box(505, 70, 165, 72, "PostgreSQL", ["base partagee du backend", "users - branches - stocks"], "0.91 0.91 0.91")

    # Active flows.
    arrow(180, 401, 285, 401, "HTTP JSON")
    arrow(445, 420, 505, 506, "API Groq")
    arrow(445, 392, 505, 373, "")
    arrow(445, 410, 700, 461, "HTTP REST catalogue")
    arrow(180, 181, 285, 181, "SQLAlchemy")
    arrow(587, 325, 587, 142, "SQLAlchemy")

    # Present but bypassed MCP service.
    arrow(445, 372, 505, 217, "MCP non utilise", True)
    arrow(670, 211, 755, 420, "HTTP REST", True)
    arrow(587, 242, 587, 325, "HTTP interne", True)

    # Actors and explanatory note.
    text(35, 460, "Client final", 10, True)
    arrow(105, 454, 105, 437, "")
    text(35, 240, "Admin / Employe", 10, True)
    arrow(105, 234, 105, 217, "")

    commands.append("0.98 0.94 0.84 rg 35 45 410 64 re f")
    commands.append("0.75 0.57 0.2 RG 1 w 35 45 410 64 re S")
    text(48, 88, "Point d'attention", 10, True)
    text(48, 72, "Le Backoffice (SQLite) et le Backend (PostgreSQL) sont deux sources de donnees distinctes.", 8.5)
    text(48, 58, "Les modifications du Backoffice ne sont donc pas visibles dans le chatbot a ce stade.", 8.5)

    stream = "\n".join(commands).encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] /Resources << /Font << /F1 5 0 R /F2 6 0 R >> >> /Contents 4 0 R >>".encode(),
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>",
    ]
    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, content in enumerate(objects, start=1):
        offsets.append(len(result))
        result.extend(f"{number} 0 obj\n".encode())
        result.extend(content)
        result.extend(b"\nendobj\n")
    xref_offset = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode())
    return bytes(result)


if __name__ == "__main__":
    OUTPUT.write_bytes(make_pdf())
    print(f"PDF created: {OUTPUT}")
