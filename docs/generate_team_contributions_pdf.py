"""Create a printable PDF describing the HBntory team contributions."""

from pathlib import Path
from textwrap import wrap


PAGE_WIDTH, PAGE_HEIGHT = 595.28, 841.89  # A4 portrait
OUTPUT = Path(__file__).with_name("team_contributions_report.pdf")


def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


class Report:
    def __init__(self) -> None:
        self.pages: list[list[str]] = []
        self.commands: list[str] = []
        self.y = 0.0

    def new_page(self, title: str, subtitle: str) -> None:
        if self.commands:
            self.pages.append(self.commands)
        self.commands = ["0.97 0.98 1 rg 0 0 595.28 841.89 re f"]
        self.y = 775
        self.text(42, self.y, title, 20, True, "0.06 0.12 0.24")
        self.y -= 20
        self.text(42, self.y, subtitle, 9, False, "0.28 0.35 0.46")
        self.y -= 18
        self.commands.append("0.15 0.38 0.75 RG 1.4 w 42 728 m 553 728 l S")
        self.y = 700

    def finish(self) -> None:
        if self.commands:
            self.pages.append(self.commands)
            self.commands = []

    def text(self, x: float, y: float, value: str, size: float = 10, bold: bool = False, color: str = "0.08 0.12 0.2") -> None:
        font = "F2" if bold else "F1"
        self.commands.append(f"BT /{font} {size} Tf {color} rg {x} {y} Td ({escape(value)}) Tj ET")

    def paragraph(self, value: str, width: int = 76, size: float = 9.2, leading: float = 14) -> None:
        for line in wrap(value, width=width):
            self.text(55, self.y, line, size)
            self.y -= leading
        self.y -= 7

    def section(self, title: str, color: str) -> None:
        self.commands.append(f"{color} rg 42 {self.y - 6} 511 26 re f")
        self.text(54, self.y + 3, title, 12, True, "1 1 1")
        self.y -= 40

    def technology(self, technology: str, reason: str) -> None:
        lines = wrap(reason, width=62)
        height = 28 + len(lines) * 13
        self.commands.append(f"1 1 1 rg 51 {self.y - height + 8} 493 {height} re f")
        self.commands.append(f"0.82 0.86 0.92 RG 0.7 w 51 {self.y - height + 8} 493 {height} re S")
        self.text(63, self.y - 12, technology, 10, True, "0.06 0.25 0.5")
        line_y = self.y - 28
        for line in lines:
            self.text(63, line_y, line, 8.8)
            line_y -= 13
        self.y -= height + 10

    def footer(self, page: int) -> None:
        self.text(42, 28, "HBntory - Rapport de contributions techniques", 8, False, "0.35 0.4 0.48")
        self.text(510, 28, f"Page {page}", 8, False, "0.35 0.4 0.48")


def make_pdf() -> bytes:
    report = Report()

    report.new_page("HBntory - Contributions de l'equipe", "Synthese des responsabilites et des choix techniques par developpeur")
    report.section("Objectif du projet", "0.1 0.33 0.66")
    report.paragraph(
        "HBntory est une application de gestion de stocks multi-agences. Elle combine "
        "une interface de questionnement client, un agent IA, un backoffice et des "
        "services de donnees pour les produits, les utilisateurs, les agences et le stock."
    )
    report.section("Repartition des responsabilites", "0.08 0.43 0.46")
    report.technology("Thélyaan - Web et Agent IA", "Interface Web client et service IA qui traite les questions en langage naturel, appelle le LLM et recupere les informations produits et stocks.")
    report.technology("Collins - Backoffice", "Interface d'administration des utilisateurs et des stocks. Elle couvre la connexion, la gestion des comptes et les operations de stock par agence.")
    report.technology("Harold - Backend et serveur MCP", "API metier centralisee, securite, persistance PostgreSQL, routes internes de stock et serveur MCP fournissant les outils produits et inventaire.")
    report.section("Lecture du rapport", "0.44 0.26 0.65")
    report.paragraph("Les pages suivantes presentent, pour chaque partie, les technologies visibles dans le depot et la raison pratique de leur utilisation.")
    report.footer(1)

    report.new_page("Thélyaan - Web et Agent IA", "Responsabilite : parcours de question client et reponse en langage naturel")
    report.section("Partie Web client", "0.12 0.42 0.74")
    report.technology("HTML5, CSS3 et JavaScript", "Creation d'une interface legere, sans framework lourd, pour saisir une question, afficher l'etat de chargement et presenter la reponse de l'assistant dans le navigateur.")
    report.technology("Fetch API et JSON", "Envoi asynchrone des questions du navigateur vers le service IA. JSON fournit un format simple et standard pour transporter la question et la reponse.")
    report.technology("CORS", "Autorise le Client Web et le service IA, servis sur des ports differents en developpement, a communiquer depuis le navigateur.")
    report.section("Service Agent IA", "0.12 0.42 0.74")
    report.technology("Python et FastAPI", "Expose une API REST rapide et concise (POST /api/v1/query). FastAPI apporte la validation du format de requete et une base claire pour un microservice.")
    report.technology("Groq SDK et LLM avec tool calling", "Le modele interprete la question, decide quelles donnees consulter et formule une reponse. Le tool calling limite les reponses aux donnees retournees par les outils.")
    report.technology("HTTPX", "Client HTTP Python utilise pour recuperer le catalogue produits et les informations de stock aupres des services internes.")
    report.technology("python-dotenv et variables d'environnement", "Charge la cle Groq et les URL de services hors du code source, ce qui facilite la configuration locale et protege les secrets.")
    report.footer(2)

    report.new_page("Collins - Frontend du Backoffice", "Responsabilite : interface interne de gestion des utilisateurs et des stocks")
    report.section("Application et affichage", "0.1 0.5 0.3")
    report.technology("FastAPI", "Fournit les routes du backoffice : connexion, creation d'utilisateur, activation, desactivation, suppression et mise a jour de stock.")
    report.technology("Jinja2", "Genere les pages HTML cote serveur a partir de modeles. Ce choix est adapte a un outil interne simple, avec formulaires et tableaux de gestion.")
    report.technology("HTML, CSS et formulaires POST", "Construit les ecrans de connexion, de gestion des utilisateurs et de stock. Les formulaires transmettent les actions administratives de maniere directe.")
    report.section("Donnees et securite", "0.1 0.5 0.3")
    report.technology("SQLAlchemy", "Mappe les modeles User, Branch et Stock vers la base de donnees et evite d'ecrire des requetes SQL repetitives dans les routes Web.")
    report.technology("SQLite", "Base de donnees locale du backoffice, facile a lancer sans serveur de base supplementaire pendant le developpement et la demonstration.")
    report.technology("python-jose, Passlib et bcrypt", "Gere les jetons JWT de session et le hachage securise des mots de passe. Les mots de passe ne sont donc pas enregistres en clair.")
    report.technology("Uvicorn et Docker", "Uvicorn execute l'application ASGI et Docker rend le backoffice reproductible avec le reste des services du projet.")
    report.footer(3)

    report.new_page("Harold - Backend", "Responsabilite : donnees metier et API securisee")
    report.section("Backend metier", "0.53 0.25 0.18")
    report.technology("FastAPI et Pydantic", "Expose les API d'authentification, utilisateurs, agences, stocks et routes internes. Pydantic valide les donnees recues et structure les reponses.")
    report.technology("SQLAlchemy, PostgreSQL et Psycopg", "SQLAlchemy gere les modeles et les transactions ; PostgreSQL sert de base relationnelle partagee du backend ; Psycopg assure la connexion Python a PostgreSQL.")
    report.technology("Alembic", "Prepare la gestion versionnee des evolutions de schema de base de donnees, utile lorsque les tables et contraintes evoluent.")
    report.technology("PyJWT et Argon2", "Met en place l'authentification par jeton JWT et le hachage moderne des mots de passe. Les roles admin et employe sont verifies dans les dependances FastAPI.")
    report.technology("Cle X-Internal-API-Key", "Protege les routes internes consultees par les services techniques, notamment les donnees de stock et d'agences utilisees par l'agent IA.")
    report.footer(4)

    report.new_page("Harold - Serveur MCP et integrations", "Responsabilite : outils produits / stocks et orchestration des services")
    report.section("Serveur MCP", "0.53 0.25 0.18")
    report.technology("MCP Python SDK et FastMCP", "Expose des outils standards : details produit, liste produits, disponibilite, inventaire et agences. MCP rend ces fonctions reutilisables par un agent compatible.")
    report.technology("HTTPX et API Produits", "Le serveur MCP appelle l'API Produits et le Backend via HTTP afin d'agreger catalogue et stock sans dupliquer ces donnees.")
    report.technology("Docker Compose", "Orchestre PostgreSQL, Backend, Backoffice, API Produits, MCP, service IA et Client Web pour demarrer l'environnement complet avec des ports isoles.")
    report.footer(5)
    report.finish()

    objects: list[bytes] = [b"<< /Type /Catalog /Pages 2 0 R >>"]
    page_ids = [3 + page * 2 for page in range(len(report.pages))]
    objects.append(f"<< /Type /Pages /Kids [{' '.join(f'{item} 0 R' for item in page_ids)}] /Count {len(page_ids)} >>".encode())
    for page_commands in report.pages:
        page_object = len(objects) + 1
        contents_object = page_object + 1
        stream = "\n".join(page_commands).encode("latin-1")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] /Resources << /Font << /F1 {3 + len(report.pages) * 2} 0 R /F2 {4 + len(report.pages) * 2} 0 R >> >> /Contents {contents_object} 0 R >>".encode())
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    objects.extend([
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    ])

    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, content in enumerate(objects, start=1):
        offsets.append(len(result))
        result.extend(f"{number} 0 obj\n".encode())
        result.extend(content)
        result.extend(b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(result)


if __name__ == "__main__":
    OUTPUT.write_bytes(make_pdf())
    print(f"PDF created: {OUTPUT}")
