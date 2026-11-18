"""Create a ShowdownAI license key for one machine.

Usage:
    python tools/generate_license.py MACHINE-ID path/to/private_key.pem

The machine ID is shown on the ShowdownAI lock screen. Keep private_key.pem
secret and never commit it: anyone who has it can make working keys.
"""
import base64
import sys

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    machine_id = sys.argv[1].strip().upper()
    with open(sys.argv[2], encoding="utf-8") as file:
        private_key = ECC.import_key(file.read())
    signature = eddsa.new(private_key, "rfc8032").sign(b"showdownai-license:v1:" + machine_id.encode("utf-8"))
    print(base64.urlsafe_b64encode(signature).decode("ascii").rstrip("="))
    return 0


if __name__ == "__main__":
    sys.exit(main())
