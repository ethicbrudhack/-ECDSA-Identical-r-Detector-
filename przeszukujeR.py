import os

SIGNATURES_FILE = "signatures.txt"
IDENTICAL_R_FILE = "identical_r_found.txt"
SIGNATURES = []  # Lista do przechowywania podpisów

# Wczytywanie podpisów z pliku
def read_signatures():
    try:
        with open(SIGNATURES_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.strip().split("----------------------------------")
        parsed = []
        for block in blocks:
            lines = block.strip().split("\n")
            sig = {}
            for line in lines:
                if line.startswith("txid:"):
                    sig["txid"] = line.split(": ", 1)[1]
                elif line.startswith("address:"):
                    sig["address"] = line.split(": ", 1)[1]
                elif line.startswith("pubkey:"):
                    sig["pubkey"] = line.split(": ", 1)[1]
                elif line.startswith("r:"):
                    sig["r"] = line.split(": ", 1)[1].strip()
                elif line.startswith("s:"):
                    sig["s"] = line.split(": ", 1)[1].strip()
                elif line.startswith("z:"):
                    sig["z"] = line.split(": ", 1)[1].strip()
            if sig:  # Jeśli blok zawiera podpis, dodajemy go do listy
                parsed.append(sig)

        print(f"Loaded {len(parsed)} signatures.")
        return parsed
    except Exception as e:
        print(f"Błąd podczas odczytu pliku {SIGNATURES_FILE}: {e}")
        return []

# Zapis identycznych r do pliku
def save_identical_r(sig1, sig2):
    print(f"⚠️ ZAPISUJE identyczne r (ale różne s)")

    # Zapisujemy podpisy w czytelnym formacie
    line = (
        f"----------------------------------\n"
        f"Txid1: {sig1['txid']}\nAddress1: {sig1['address']}\nPubkey1: {sig1['pubkey']}\n"
        f"r: {sig1['r']}\ns1: {sig1['s']}\nz1: {sig1['z']}\n"
        f"Txid2: {sig2['txid']}\nAddress2: {sig2['address']}\nPubkey2: {sig2['pubkey']}\n"
        f"r: {sig2['r']}\ns2: {sig2['s']}\nz2: {sig2['z']}\n"
        f"----------------------------------\n"
    )

    # Zapis do pliku
    try:
        with open(IDENTICAL_R_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(f"⚡ Zapisano do {IDENTICAL_R_FILE}")
    except Exception as e:
        print(f"❌ Błąd podczas zapisywania do pliku: {e}")

# Przeszukiwanie podpisów, aby znaleźć identyczne r, ale różne s
def analyze_signatures(signatures):
    r_dict = {}

    # Grupujemy podpisy po r
    for sig in signatures:
        r_val = sig["r"]
        if r_val not in r_dict:
            r_dict[r_val] = []
        r_dict[r_val].append(sig)

    # Sprawdzamy podpisy z identycznym r, ale różnym s
    for r_val, entries in r_dict.items():
        if len(entries) > 1:
            print(f"Sprawdzam r: {r_val}")
            s_values = {}
            for sig in entries:
                s_val = sig["s"]
                if s_val not in s_values:
                    s_values[s_val] = []
                s_values[s_val].append(sig)

            print(f"R: {r_val} - found {len(s_values)} different 's' values.")

            if len(s_values) > 1:
                # Dla każdej unikalnej pary podpisów o tym samym r ale różnych s
                pairs = []
                all_sigs = [sig for sublist in s_values.values() for sig in sublist]
                for i in range(len(all_sigs)):
                    for j in range(i + 1, len(all_sigs)):
                        sig1 = all_sigs[i]
                        sig2 = all_sigs[j]
                        if sig1["s"] != sig2["s"]:  # tylko jeśli różne s
                            print(f"[=] IDENTICAL R DETECTED:")
                            print(f"Txid1: {sig1['txid']}\nAddress1: {sig1['address']}\nPubkey1: {sig1['pubkey']}")
                            print(f"r: {sig1['r']}\ns1: {sig1['s']}\nz1: {sig1['z']}")
                            print(f"Txid2: {sig2['txid']}\nAddress2: {sig2['address']}\nPubkey2: {sig2['pubkey']}")
                            print(f"r: {sig2['r']}\ns2: {sig2['s']}\nz2: {sig2['z']}")
                            print("----------------------------------")
                            save_identical_r(sig1, sig2)

# Główna część programu
def main():
    signatures = read_signatures()
    print(f"Wczytano {len(signatures)} podpisów.")
    
    if signatures:
        analyze_signatures(signatures)
        print("\n✅ Zakończono analizę podpisów.")
    else:
        print("Brak podpisów do analizy.")

if __name__ == "__main__":
    if os.path.exists(IDENTICAL_R_FILE):
        os.remove(IDENTICAL_R_FILE)
    
    main()
    input("Naciśnij Enter, aby zakończyć...")
