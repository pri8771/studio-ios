#!/usr/bin/env python3
"""Create the standard local Studio workspace safely.

The script never moves, deletes, or overwrites existing user files. It previews by
default; pass --apply to create missing directories and small README markers.
"""
from __future__ import annotations

import argparse
from pathlib import Path

DOCUMENT_DIRS = [
    "00_Inbox/To_File",
    "00_Inbox/To_Review",
    "00_Inbox/To_Delete",
    "01_Studio_Operations/Company",
    "01_Studio_Operations/Strategy",
    "01_Studio_Operations/Accounts_and_Vendors",
    "01_Studio_Operations/Domains",
    "01_Studio_Operations/Automation",
    "01_Studio_Operations/Infrastructure",
    "01_Studio_Operations/Meetings",
    "01_Studio_Operations/Templates",
    "02_Products/Incubating",
    "03_Marketing/Studio_Brand",
    "03_Marketing/Content_Library/Photos",
    "03_Marketing/Content_Library/Video",
    "03_Marketing/Content_Library/Audio",
    "03_Marketing/Content_Library/Illustrations",
    "03_Marketing/Content_Library/Templates",
    "03_Marketing/Campaigns",
    "03_Marketing/Social",
    "03_Marketing/Email",
    "03_Marketing/Press",
    "03_Marketing/Analytics_Exports",
    "03_Marketing/Rights_and_Licenses",
    "04_Sales_CRM/CRM_Exports",
    "04_Sales_CRM/Outreach_Lists",
    "04_Sales_CRM/Proposals",
    "04_Sales_CRM/Customer_Research",
    "04_Sales_CRM/Partnerships",
    "04_Sales_CRM/Testimonials_and_Permissions",
    "05_Finance_Legal/Accounting",
    "05_Finance_Legal/Taxes",
    "05_Finance_Legal/Contracts",
    "05_Finance_Legal/Trademarks",
    "05_Finance_Legal/Privacy",
    "05_Finance_Legal/Terms",
    "05_Finance_Legal/Insurance",
    "05_Finance_Legal/Vendor_Agreements",
    "06_Research/Markets",
    "06_Research/Competitors",
    "06_Research/App_Store",
    "06_Research/Technology",
    "06_Research/AI_and_Automation",
    "06_Research/Open_Source",
    "06_Research/User_Problems",
    "07_Assets/Studio_Logos",
    "07_Assets/Fonts_Licensed",
    "07_Assets/Icons",
    "07_Assets/Mockups",
    "07_Assets/App_Store_Templates",
    "07_Assets/Social_Templates",
    "07_Assets/Brand_Guides",
    "08_Exports/GitHub",
    "08_Exports/Attio",
    "08_Exports/Notion",
    "08_Exports/Google",
    "08_Exports/Analytics",
    "08_Exports/Social",
    "08_Exports/App_Store",
    "09_Private/Identity",
    "09_Private/Recovery",
    "09_Private/Signing",
    "09_Private/Confidential_Client_Data",
    "09_Private/Restricted_Samples",
    "99_Archive/Products",
    "99_Archive/Operations",
    "99_Archive/Marketing",
    "99_Archive/Yearly",
]

PRODUCT_DIRS = [
    "01_Product",
    "02_Research",
    "03_Design",
    "04_Marketing",
    "05_Legal",
    "06_Beta_Feedback",
    "07_App_Store_or_Deployment",
    "08_Exports",
    "99_Archive",
]

ROOT_README = """# Local Studio Files

This directory stores non-code files, exports, large assets, signed documents,
raw research, and sensitive material. Canonical source code and engineering
records live under ~/Developer and GitHub. Customer records belong in the CRM;
secret values belong in a password or secrets manager.
"""


def ensure_directory(path: Path, apply: bool) -> bool:
    if path.exists():
        if not path.is_dir():
            raise RuntimeError(f"Expected directory but found file: {path}")
        return False
    print(f"create directory: {path}")
    if apply:
        path.mkdir(parents=True, exist_ok=False)
    return True


def write_marker(path: Path, content: str, apply: bool) -> bool:
    if path.exists():
        return False
    print(f"create file: {path}")
    if apply:
        path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview or create the local Studio workspace")
    parser.add_argument("--apply", action="store_true", help="Create directories; default is preview only")
    parser.add_argument("--documents-root", default="~/Documents/Studio")
    parser.add_argument("--developer-root", default="~/Developer")
    parser.add_argument("--product", action="append", default=[], help="Add non-code folders for a product name")
    args = parser.parse_args()

    documents_root = Path(args.documents_root).expanduser().resolve()
    developer_root = Path(args.developer_root).expanduser().resolve()
    changed = 0

    changed += ensure_directory(documents_root, args.apply)
    changed += ensure_directory(developer_root, args.apply)
    for relative in DOCUMENT_DIRS:
        changed += ensure_directory(documents_root / relative, args.apply)
    for product in args.product:
        safe_name = "_".join(product.strip().split())
        if not safe_name or any(part in {".", ".."} for part in Path(safe_name).parts):
            raise RuntimeError(f"Invalid product folder name: {product!r}")
        product_root = documents_root / "02_Products" / safe_name
        changed += ensure_directory(product_root, args.apply)
        for relative in PRODUCT_DIRS:
            changed += ensure_directory(product_root / relative, args.apply)

    changed += write_marker(documents_root / "README.md", ROOT_README, args.apply)
    mode = "applied" if args.apply else "preview"
    print(f"Local workspace {mode}: {changed} missing items identified")
    if not args.apply:
        print("Run again with --apply after reviewing the paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
