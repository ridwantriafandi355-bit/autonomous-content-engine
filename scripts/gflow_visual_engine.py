#!/usr/bin/env python3
"""
Autonomous Content Engine - GFlow Visual & Video Generation Bridge
Drives Google Flow (Imagen 3 / Veo) via gflow-cli to produce high-impact
visual backgrounds for carousel covers and teaser motion clips.
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

DEFAULT_GFLOW_DIR = os.environ.get("GFLOW_CLI_DIR", "/home/ubuntu/gflow-cli")
UV_BIN = shutil.which("uv") or "/home/ubuntu/.local/bin/uv"

def run_command(cmd, cwd=None):
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after 180 seconds"
    except Exception as e:
        return -2, "", str(e)

def generate_image(prompt, output_path, aspect="9:16", model="nano2", gflow_dir=DEFAULT_GFLOW_DIR):
    """
    Generate an image using Google Flow Imagen via gflow-cli.
    """
    if not os.path.isdir(gflow_dir):
        return {"success": False, "error": f"gflow directory not found at {gflow_dir}"}

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        UV_BIN, "run", "gflow", "image", "t2i",
        prompt,
        "--aspect", aspect,
        "--model", model,
        "-o", str(out_file)
    ]

    print(f"[gflow] Generating image: '{prompt}' (aspect: {aspect})...")
    code, stdout, stderr = run_command(cmd, cwd=gflow_dir)

    if code == 0 and out_file.exists():
        return {"success": True, "output": str(out_file)}
    else:
        return {
            "success": False,
            "exit_code": code,
            "error": stderr.strip() or stdout.strip() or "Image file was not generated"
        }

def generate_video(prompt, output_path, aspect="9:16", duration=4, gflow_dir=DEFAULT_GFLOW_DIR):
    """
    Generate a teaser video using Google Flow Veo via gflow-cli.
    """
    if not os.path.isdir(gflow_dir):
        return {"success": False, "error": f"gflow directory not found at {gflow_dir}"}

    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        UV_BIN, "run", "gflow", "video", "t2v",
        prompt,
        "--aspect", aspect,
        "--duration", str(duration),
        "-o", str(out_file)
    ]

    print(f"[gflow] Generating video: '{prompt}' (duration: {duration}s, aspect: {aspect})...")
    code, stdout, stderr = run_command(cmd, cwd=gflow_dir)

    if code == 0 and out_file.exists():
        return {"success": True, "output": str(out_file)}
    else:
        return {
            "success": False,
            "exit_code": code,
            "error": stderr.strip() or stdout.strip() or "Video file was not generated"
        }

def main():
    parser = argparse.ArgumentParser(description="Generate AI visuals via GFlow (Google Flow)")
    parser.add_argument("--type", choices=["image", "video"], default="image", help="Asset type")
    parser.add_argument("--prompt", required=True, help="Text prompt for image or video generation")
    parser.add_argument("--output", required=True, help="Destination output file (.png or .mp4)")
    parser.add_argument("--aspect", default="9:16", choices=["9:16", "16:9", "1:1", "4:3", "3:4"], help="Aspect ratio")
    parser.add_argument("--duration", type=int, default=4, choices=[4, 6, 8, 10], help="Video duration in seconds")
    parser.add_argument("--model", default="nano2", help="Model alias")
    parser.add_argument("--gflow-dir", default=DEFAULT_GFLOW_DIR, help="Path to gflow-cli repo")

    args = parser.parse_args()

    if args.type == "image":
        res = generate_image(
            prompt=args.prompt,
            output_path=args.output,
            aspect=args.aspect,
            model=args.model,
            gflow_dir=args.gflow_dir
        )
    else:
        res = generate_video(
            prompt=args.prompt,
            output_path=args.output,
            aspect=args.aspect,
            duration=args.duration,
            gflow_dir=args.gflow_dir
        )

    print(json.dumps(res, indent=2))
    sys.exit(0 if res.get("success") else 1)

if __name__ == "__main__":
    main()
