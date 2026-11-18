"""One-machine license keys for ShowdownAI.

Each copy of ShowdownAI shows a machine ID. The owner signs that ID with
their private key (see tools/generate_license.py) and the resulting key only
unlocks ShowdownAI on that one machine. The private key never ships with the
app; only the public key below does.
"""
from __future__ import annotations

import base64
import hashlib
import platform
import uuid
from pathlib import Path

import toml
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa

from utils import resolve_project_path

PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAg2RTeRJo5dv34+4NXEa5e8jh07ICU7lU0nPh/8rd8r8=
-----END PUBLIC KEY-----"""

LICENSE_FILE = "cfg/license.toml"
_SIGNED_PREFIX = b"showdownai-license:v1:"


def _raw_machine_identifier() -> str:
    if platform.system() == "Windows":
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Cryptography",
                0,
                winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
            ) as key:
                value, _ = winreg.QueryValueEx(key, "MachineGuid")
                if value:
                    return str(value)
        except OSError:
            pass
    for candidate in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
        try:
            value = Path(candidate).read_text(encoding="utf-8").strip()
            if value:
                return value
        except OSError:
            continue
    return f"node-{uuid.getnode():012x}"


def get_machine_id() -> str:
    """Short, stable ID for this computer, e.g. 3F2A-91C0-7B44-E1D8."""
    digest = hashlib.sha256(("showdownai:" + _raw_machine_identifier()).encode("utf-8")).hexdigest().upper()
    return "-".join(digest[i:i + 4] for i in range(0, 16, 4))


def _normalize_key(license_key: str) -> str:
    return "".join(str(license_key or "").split())


def verify_license_key(license_key: str, machine_id: str | None = None) -> bool:
    machine_id = machine_id or get_machine_id()
    key = _normalize_key(license_key)
    if not key:
        return False
    try:
        signature = base64.urlsafe_b64decode(key + "=" * (-len(key) % 4))
        verifier = eddsa.new(ECC.import_key(PUBLIC_KEY_PEM), "rfc8032")
        verifier.verify(_SIGNED_PREFIX + machine_id.encode("utf-8"), signature)
        return True
    except (ValueError, TypeError):
        return False


def load_saved_key() -> str:
    path = resolve_project_path(LICENSE_FILE)
    try:
        return str(toml.load(path).get("license_key", ""))
    except (OSError, toml.TomlDecodeError):
        return ""


def save_key(license_key: str) -> None:
    path = resolve_project_path(LICENSE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        toml.dump({"license_key": _normalize_key(license_key)}, file)


def is_licensed() -> bool:
    return verify_license_key(load_saved_key())


def license_status() -> dict:
    return {"licensed": is_licensed(), "machine_id": get_machine_id()}


def activate(license_key: str) -> dict:
    if not verify_license_key(license_key):
        return {"ok": False, "message": "This key isn't valid for this computer.", **license_status()}
    save_key(license_key)
    return {"ok": True, "message": "ShowdownAI is unlocked.", **license_status()}
