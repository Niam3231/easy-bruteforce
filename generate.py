import itertools
import sys
import time
import os
import subprocess
import shutil
import platform
import random

print("\nScript by Niam3231 (L.V.D.N.)")
print("\033[1;31mIf you know, for example all the uppercase characters and their position.\033[0m")
print("\033[1;31mPlease say no to the question: Does it contain uppercase? Or any other.\033[0m")
print("\033[1;31mThis can sometimes save hours of generating and hashing.\033[0m\n")

def is_linux():
    return platform.system().lower() == "linux"

def ask_hashcat_mode():
    examples = {
        "0": "MD5",
        "100": "SHA1",
        "1000": "NTLM",
        "1400": "SHA256",
        "1800": "sha512crypt $6$, SHA512 (Unix)",
        "12500": "RAR3-hp",
        "13000": "RAR5"
    }
    while True:
        mode = input("Enter hash-type mode (as hashcat uses). Enter '?' to see examples: ").strip()
        if mode == '?':
            print("\nSome example hashcat mode numbers:")
            for k, v in examples.items():
                print(f"{k} - {v}")
            print("For more codes go to: https://hashcat.net/wiki/doku.php?id=example_hashes\n")
            continue
        if mode == "":
            print("Please enter a hash mode number (e.g. 0, 1000, 1400).")
            continue
        if not mode.isdigit():
            print("Hash mode must be numeric (digits only).")
            continue
        return mode

def ensure_file(path):
    if not os.path.exists(path):
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            try:
                os.makedirs(parent, exist_ok=True)
            except Exception as e:
                print(f"Warning: cannot create directory {parent}: {e}")
        open(path, "a").close()
        print(f"Created file: {path}")

def run_hashcat(hash_mode, hashes_file, cracked_file, wordlist_file):
    hc_path = shutil.which("hashcat")
    if not hc_path:
        print("hashcat executable not found in PATH. Install hashcat or run this script on a system with hashcat installed.")
        return
    cmd = [hc_path, "-m", str(hash_mode), "-a", "0", hashes_file, wordlist_file, "-o", cracked_file, "-O"]
    print("Running hashcat with command:")
    print(" ".join(cmd))
    try:
        proc = subprocess.run(cmd)
        if proc.returncode == 0:
            print("Hashcat finished successfully.")
        else:
            print(f"Hashcat exited with return code {proc.returncode}.")
    except Exception as e:
        print(f"Error running hashcat: {e}")

def get_yes_no_idk(prompt):
    while True:
        ans = input(prompt + " (y/n/idk): ").strip().lower()
        if ans in ['y', 'n', 'idk']:
            return ans
        print("Please enter 'y', 'n', or 'idk'.")

def get_yes_no(prompt):
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            return ans
        print("Please enter 'y' or 'n'.")

def get_int_pair(prompt):
    while True:
        span = input(prompt + " (min-max): ").strip()
        try:
            mn, mx = map(int, span.split('-'))
            return mn, mx
        except:
            print("Enter two numbers split by '-' (e.g., 4-6).")

def get_chars(prompt):
    chars = input(prompt + " (use a comma to enter more characters): ").strip()
    return [c.strip() for c in chars.split(',') if c.strip()]

def get_positions_per_spot(chars, max_length):
    """Return dict: position (1-based) -> list of possible characters, and unknown-position chars list"""
    pos_map = {}
    unknown_pos_chars = []
    for ch in chars:
        while True:
            pos_input = input(f'Do you know at what place(s) "{ch}" could be? (0=unknown, or comma-separated positions): ').strip()
            if pos_input == "0":
                unknown_pos_chars.append(ch)
                break
            try:
                positions = [int(p.strip()) for p in pos_input.split(',') if 1 <= int(p.strip()) <= max_length]
                for pos in positions:
                    if pos not in pos_map:
                        pos_map[pos] = []
                    pos_map[pos].append(ch)
                break
            except:
                print(f"Enter valid positions 1-{max_length}, comma-separated.")
    return pos_map, unknown_pos_chars

def human_format(num):
    if num >= 1_000_000:
        return f"{num/1_000_000:.2f} MH/s"
    elif num >= 1_000:
        return f"{num/1_000:.2f} kH/s"
    else:
        return f"{num:.2f} H/s"

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}h {m}m {s}s"

def print_status(percent, count, total, status, current_speed, avg_speed, max_speed, min_speed, time_estimated, first_print=[True]):
    if not first_print[0]:
        sys.stdout.write("\033[F"*6)
    else:
        first_print[0] = False

    # Easter egg conditions
    if time_estimated > 33e9 * 365.25 * 24 * 3600:  # > 33 billion years in seconds
        time_str = "Somewhere far after the universe has already ended."
    elif time_estimated > 5e9 * 365.25 * 24 * 3600:  # > 5 billion years in seconds
        time_str = "Until the end of humanity."
    elif time_estimated > 200 * 365.25 * 24 * 3600:  # > 200 years in seconds
        time_str = "You won't even exist by then."
    else:
        time_str = format_time(time_estimated)

    sys.stdout.write(
        f"Progress........: {percent:6.2f}%\n"
        f"Progress-2......: {count}/{total}\n"
        f"Status..........: {status}\n"
        f"Speed...........: Current: {human_format(current_speed)}; "
        f"Average: {human_format(avg_speed)}; "
        f"Max: {human_format(max_speed)}; "
        f"Min: {human_format(min_speed)}\n"
        f"Time-Estimated..: {time_str}\n"
        "\n"
    )
    sys.stdout.flush()

def main():
    print("Password Wordlist Advanced Generator\n")

    pw_min, pw_max = get_int_pair("How long is the password?")

    uppercase = get_yes_no_idk("Does it contain uppercase?")
    lowercase = get_yes_no_idk("Does it contain lowercase?")
    special = get_yes_no_idk("Does it contain special?")
    contains_int = get_yes_no_idk("Does it contain any integers?")

    charsets = []
    if uppercase == 'y':
        charsets.append("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if lowercase == 'y':
        charsets.append("abcdefghijklmnopqrstuvwxyz")
    if uppercase == 'idk' or lowercase == 'idk':
        charsets.append("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    digits = "0123456789"
    if contains_int == 'y' or contains_int == 'idk':
        charsets.append(digits)
    special_chars = "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~"
    if special == 'y' or special == 'idk':
        charsets.append(special_chars)

    full_charset = sorted(set("".join(charsets)))

    # --- Must letters and positions ---
    must_letters = []
    must_positions = {}
    unknown_pos_chars = []
    if get_yes_no("Do you know any characters that are definitely in the password?") == 'y':
        must_letters = get_chars("|__ What letters? ")
        must_positions, unknown_pos_chars = get_positions_per_spot(must_letters, pw_max)

    # --- Letters definitely NOT in password ---
    not_letters = []
    if get_yes_no("Do you know any characters that are definitely NOT in the password?") == 'y':
        not_letters = get_chars("|__ What letters? ")

    # --- Build candidate charset ---
    candidate_charset = [c for c in full_charset if c not in not_letters]
    for c in must_letters + unknown_pos_chars:
        if all(c not in lst for lst in must_positions.values()) and c not in candidate_charset:
            candidate_charset.append(c)

    print("Done, confirm to generate, list could be very long (y/n)")
    if input().strip().lower() != 'y':
        print("Cancelled.")
        return

    filename = "wordlist.txt"
    with open(filename, "w", encoding="utf-8") as f:
        total_combos = 0
        combos_per_length = {}

        # Precompute template info
        for pw_length in range(pw_min, pw_max + 1):
            fill_options = []
            for i in range(pw_length):
                if i+1 in must_positions:
                    fill_options.append(must_positions[i+1])
                else:
                    fill_options.append(candidate_charset)
            combos = 1
            for opts in fill_options:
                combos *= len(opts)
            total_combos += combos
            combos_per_length[pw_length] = fill_options

        # --- Generation loop ---
        count = 0
        status = "Generating"
        speeds = []
        min_speed = float('inf')
        max_speed = 0
        start_time = time.time()
        last_time = start_time
        last_count = 0
        update_interval = 0.5
        next_update = start_time + update_interval
        current_speed = 0
        avg_speed = 0
        percent = 0
        time_estimated = 0
        first_print = [True]

        print_status(0, 0, total_combos, status, 0, 0, 0, 0, 0, first_print)

        for pw_length in range(pw_min, pw_max + 1):
            fill_options = combos_per_length[pw_length]

            for combo in itertools.product(*fill_options):
                combo = list(combo)

                # Insert unknown-position letters randomly
                for ch in unknown_pos_chars:
                    available_indices = [i for i in range(pw_length) if (i+1) not in must_positions]
                    if available_indices:
                        idx = random.choice(available_indices)
                        combo[idx] = ch
                        available_indices.remove(idx)

                f.write(''.join(combo) + "\n")
                count += 1

                now = time.time()
                if now >= next_update or count == total_combos:
                    elapsed = now - start_time
                    interval = now - last_time if now - last_time > 0 else 1e-6
                    current_speed = (count - last_count) / interval
                    speeds.append(current_speed)
                    min_speed = min(min_speed, current_speed)
                    max_speed = max(max_speed, current_speed)
                    avg_speed = sum(speeds) / len(speeds) if speeds else current_speed
                    percent = (count * 100.0 / total_combos) if total_combos else 100.0
                    time_estimated = ((total_combos - count) / avg_speed) if avg_speed > 0 else 0

                    print_status(percent, count, total_combos, status, current_speed, avg_speed, max_speed, min_speed, time_estimated, first_print)
                    last_time = now
                    last_count = count
                    next_update = now + update_interval

        status = "Done"
        print_status(100.0, count, total_combos, status, current_speed, avg_speed, max_speed, min_speed, 0, first_print)
        print(f"\nWordlist generation complete! {count} passwords written to {filename}")

    # --- Optional Hashcat phase (Linux only) ---
    if not is_linux():
        print("\nNot running on Linux; hashcat cracking option is not available on this platform.")
        return

    if get_yes_no("Do you also want to begin cracking with hashcat?") == 'n':
        print("Okay. Leaving just the wordlist.txt. Bye.")
        return

    hashes_file = input("Path to file containing hashes (press Enter for 'hashes.txt'): ").strip() or "hashes.txt"
    cracked_file = input("Path to output cracked hashes file (press Enter for 'cracked.txt'): ").strip() or "cracked.txt"

    ensure_file(hashes_file)
    ensure_file(cracked_file)

    try:
        if os.path.getsize(hashes_file) == 0:
            print(f"Note: {hashes_file} is empty. There's nothing to crack unless you add hashes.")
    except Exception as e:
        print(f"Warning checking {hashes_file}: {e}")

    hash_mode = ask_hashcat_mode()
    print(f"\nAbout to run hashcat -m {hash_mode} -a 0 {hashes_file} {filename} -o {cracked_file} -O")
    if get_yes_no("Proceed to run hashcat now?") == 'y':
        run_hashcat(hash_mode, hashes_file, cracked_file, filename)
    else:
        print("Cracking skipped. Wordlist saved as wordlist.txt. Have a nice day.")

if __name__ == "__main__":
    main()