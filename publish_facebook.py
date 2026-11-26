"""Facebook Page/Reels publishing adapter built on the existing Graphpost project.

Safe by default: without --publish, this script performs a dry run only.
Credentials are read from environment variables, never from source code.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish a video to a Facebook Page using Graphpost.")
    parser.add_argument("--video", required=True, help="Local video file path")
    parser.add_argument("--caption", default="", help="Facebook caption")
    parser.add_argument("--title", default="", help="Optional video title")
    parser.add_argument("--publish", action="store_true", help="Actually publish; default is dry-run")
    parser.add_argument("--draft", action="store_true", help="Upload as an unpublished draft (still transfers the video to Meta)")
    args = parser.parse_args()

    video = Path(args.video).expanduser().resolve()
    if not video.is_file():
        parser.error(f"Video file not found: {video}")

    page_id = os.environ.get("FB_PAGE_ID", "").strip()
    token = os.environ.get("GRAPHPOST_PAGE_TOKEN", "").strip()
    if not page_id:
        parser.error("FB_PAGE_ID is not set. Add it as a GitHub Actions Secret/Variable before testing.")
    if args.publish and not token:
        parser.error("GRAPHPOST_PAGE_TOKEN is required for real publishing. Never paste it into source code or chat.")

    runtime = Path(os.environ.get("GRAPHPOST_HOME", ".runtime/graphpost")).resolve()
    runtime.mkdir(parents=True, exist_ok=True)
    config_path = runtime / "config.json"
    config_path.write_text(json.dumps({"page_id": page_id, "graph_version": "v25.0"}, indent=2) + "\n", encoding="utf-8")
    os.environ["GRAPHPOST_HOME"] = str(runtime)

    spec = {
        "title": args.title or video.stem,
        "posts": [{
            "network": "facebook",
            "kind": "reel",
            "video": str(video),
            "title": args.title or video.stem,
            "caption": args.caption,
        }],
    }

    with tempfile.TemporaryDirectory(prefix="viral-video-") as tmp:
        spec_path = Path(tmp) / "post.json"
        spec_path.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
        command = ["graphpost", "post", str(spec_path), "--only", "facebook"]
        if not args.publish:
            command.append("--dry-run")
        if args.draft:
            command.append("--draft")
        executable = shutil.which("graphpost")
        if not executable:
            raise SystemExit("Graphpost command not found. Install requirements.txt first.")
        result = subprocess.run(command, check=False)
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
