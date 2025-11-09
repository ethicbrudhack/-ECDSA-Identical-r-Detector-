# 💥 ECDSA Identical-r Detector  
`find_identical_r.py`

> ⚙️ Scans extracted ECDSA signatures to detect the **critical “same r, different s”** condition —  
> the hallmark of nonce reuse in ECDSA, which instantly reveals the private key.

---

## 🚀 Overview

This script reads all collected signatures from `signatures.txt`, groups them by their `r` values,  
and reports any cases where **the same `r`** is used but **different `s`** values appear.

Such cases indicate **nonce reuse (`k` reused)** — the most severe ECDSA vulnerability.  
If two distinct messages share the same nonce `k`, the private key `d` can be computed directly.

---

## ⚠️ Why It Matters

ECDSA signature equation:
s = k⁻¹ (z + r·d) mod n


If two signatures reuse the same `k` → same `r`:


s₁ = k⁻¹ (z₁ + r·d)
s₂ = k⁻¹ (z₂ + r·d)


Then:


k = (z₁ - z₂) * (s₁ - s₂)⁻¹ mod n
d = (s₁·k - z₁) * r⁻¹ mod n


👉 Just two signatures with identical `r` and different `s` are enough to **fully recover the private key**.

---

## 🧩 Features

| Feature | Description |
|----------|-------------|
| 💥 **Identifies same `r`, different `s`** | Detects immediate nonce reuse |
| 📊 **Grouped by r** | Efficient grouping and comparison |
| 🧾 **Readable log file** | Saves all matching pairs to `identical_r_found.txt` |
| 🧠 **Minimal & fast** | Runs even on large datasets in seconds |
| 🧩 **Integrates with earlier tools** | Works directly with `signatures.txt` output |

---

## 📂 File Inputs and Outputs

| File | Purpose |
|------|----------|
| `signatures.txt` | Input file of parsed signatures (from transaction extraction) |
| `identical_r_found.txt` | Output report listing all same-r / different-s pairs |

---

### 🔹 Expected Input (`signatures.txt`)

Each signature block must have:

txid: ...
address: ...
pubkey: ...
r: 0x...
s: 0x...
z: 0x...

---

## ⚙️ How It Works

1. Reads all signatures from `signatures.txt`
2. Groups them by their `r` value  
3. For each group:
   - If there’s more than one distinct `s` value, prints and logs the case
4. Each detected pair is saved in `identical_r_found.txt` with full data for further analysis

---

## 🧠 Example Output

### Console

Loaded 152 signatures.
Checking r: 0x53133471acd440676d66...
R: 0x53133471acd440676d66... - found 2 different 's' values.
[=] IDENTICAL R DETECTED:
Txid1: 3d92b04f...
Address1: 1ABCxyz...
r: 0x53133471acd44067...
s1: 0x5d3313bb527c3842...
z1: 0x64e929eff3671f88...
Txid2: 27ad50ff...
Address2: 1ABCxyz...
r: 0x53133471acd44067...
s2: 0x5ad8abf5c54985a0...
z2: 0x77c027ad88d087b7...

⚡ Saved to identical_r_found.txt


### Output file (`identical_r_found.txt`)

Txid1: 3d92b04f...
Address1: 1ABCxyz...
Pubkey1: 02ab4d...
r: 0x53133471acd44067...
s1: 0x5d3313bb527c3842...
z1: 0x64e929eff3671f88...
Txid2: 27ad50ff...
Address2: 1ABCxyz...
Pubkey2: 02ab4d...
r: 0x53133471acd44067...
s2: 0x5ad8abf5c54985a0...
z2: 0x77c027ad88d087b7...

---

## ⚡ Performance

| Dataset size | Time |
|---------------|------|
| 100 signatures | <1s |
| 1,000 signatures | ~3s |
| 10,000 signatures | <30s |

---

## 🧩 Key Functions

| Function | Description |
|-----------|-------------|
| `read_signatures()` | Reads and parses signature blocks from `signatures.txt` |
| `analyze_signatures()` | Groups by `r` and detects duplicates |
| `save_identical_r(sig1, sig2)` | Saves all found identical-r pairs |
| `main()` | Program entry point |

---

## ⚙️ Usage

```bash
python3 find_identical_r.py


When finished:

✅ Signature analysis complete.
⚡ All identical-r pairs saved in identical_r_found.txt

🔒 Ethical Use Notice

This utility is intended strictly for cryptographic security analysis and self-audit.
It demonstrates the catastrophic effect of nonce reuse in ECDSA.

You may:

Audit your own signature generation systems

Use it for research on deterministic nonce safety

You must not:

Use it to analyze unauthorized third-party signatures

Apply it to mainnet data without explicit consent

⚖️ Ethical cryptography means respecting privacy and consent at all times.

🪪 License

MIT License
© 2025 — Author: [Ethicbrudhack]

💡 Summary

This script is your first-line detector in any ECDSA dataset.
It isolates every case of identical r across signatures — the clearest signal
of nonce reuse and potential private key exposure.

“If two signatures share an r, they share a secret.”
— [Ethicbrudhack]

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
