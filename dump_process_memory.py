import argparse
import subprocess
import os
import json
import sys

# Helper script to dump all process memory into separate folders named by process name as well as Process ID. 

def run_volatility_json(memory_file, plugin, args=[]):
    """Run a Volatility 3 plugin and return parsed JSON output"""
    cmd = ["vol", "-f", memory_file, "-r", "json", plugin] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[!] Error running Volatility plugin '{plugin}':")
        print(result.stderr)
        sys.exit(1)

    return json.loads(result.stdout)


def run_volatility_text(memory_file, plugin, args=[]):
    """Run a Volatility 3 plugin and return text output"""
    cmd = ["vol", "-f", memory_file, plugin] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[!] Error running Volatility plugin '{plugin}':")
        print(result.stderr)
        sys.exit(1)

    return result.stdout



def main():
    parser = argparse.ArgumentParser(description="Dump memory of all processes using Volatility 3")
    parser.add_argument("-f", "--memory_file", required=True, help="Path to memory image (e.g., mem.dd)")
    parser.add_argument("-o", "--output", default="dumps", help="Directory to store dumped memory (default: dumps)")

    args = parser.parse_args()
    memory_file = args.memory_file
    dump_root = args.output

    # Create output directory
    os.makedirs(dump_root, exist_ok=True)

    print(f"[+] Getting process list from {memory_file}...")
    processes = run_volatility_json(memory_file, "windows.pslist")
    process_list_text = run_volatility_text(memory_file, "windows.pslist")
    
    # Save process list to root output folder
    process_list_file = os.path.join(dump_root, "process_list.txt")
    with open(process_list_file, "w") as f:
        f.write(process_list_text)
    print(f"[+] Process list saved to {process_list_file}")

    for proc in processes:
        pid = proc.get("PID")
        pname = proc.get("ImageFileName", f"pid_{pid}").replace(" ", "_")
        outdir = os.path.join(dump_root, f"{pname}_{pid}")
        os.makedirs(outdir, exist_ok=True)

        print(f"[+] Dumping memory for {pname} (PID {pid}) to {outdir}")
        
        # Run memmap with dump once and capture its text output
        dump_cmd = [
            "vol", "-f", memory_file,
            "--output-dir", outdir,
            "windows.memmap",
            "--pid", str(pid),
            "--dump"
        ]
        result = subprocess.run(dump_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[!] Error dumping memory for PID {pid}:")
            print(result.stderr)
            continue
        
        # Save memmap text output to same folder as memory dump
        memmap_file = os.path.join(outdir, "memmap_output.txt")
        with open(memmap_file, "w") as f:
            f.write(result.stdout)
        print(f"[+] Memory dumped and memmap output saved to {memmap_file}")

    print("[+] Done.")

if __name__ == "__main__":
    main()