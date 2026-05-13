"""Default scan configuration."""

RISKY_FILE_NAMES = {
    ".env": "Environment file may contain credentials.",
    ".env.local": "Local environment file may contain credentials.",
    ".env.production": "Production environment file may contain credentials.",
    "id_rsa": "SSH private key file.",
    "id_dsa": "SSH private key file.",
    "id_ecdsa": "SSH private key file.",
    "id_ed25519": "SSH private key file.",
    "credentials.json": "Credential file.",
    "service-account.json": "Cloud service account file.",
}


DEPENDENCY_FILES = {
    "requirements.txt": "Python dependency manifest.",
    "pyproject.toml": "Python project dependency manifest.",
    "package.json": "Node.js dependency manifest.",
    "package-lock.json": "Node.js lock file.",
    "yarn.lock": "Yarn lock file.",
    "pnpm-lock.yaml": "PNPM lock file.",
    "pom.xml": "Maven dependency manifest.",
    "build.gradle": "Gradle dependency manifest.",
    "go.mod": "Go dependency manifest.",
    "Cargo.toml": "Rust dependency manifest.",
}


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    ".idea",
    ".vscode",
}


DEFAULT_MAX_FILE_SIZE = 1024 * 1024
