# QALQON-Allowlist — ready for your GitHub repository

**Repository:** `aex-3-14/QALQON-Allowlist` (branch `main`).

**Upload from this package to the GitHub repository root:** `allowlist.txt`, `scripts/`, `.github/`. You may optionally replace the existing `README.md` with this file. **Do not upload the `android/` directory to the allowlist repository**; it contains an example to integrate locally into your Android project instead.

**Important:** Your current GitHub repository has an `AGPL-3.0` LICENSE. Review whether you want that license to apply to repository files; particularly avoid copying a repository-licensed Kotlin file into an app with incompatible licensing without deciding its license first.

**Live TXT URL after upload:** `https://raw.githubusercontent.com/aex-3-14/QALQON-Allowlist/main/allowlist.txt`

---

# QALQON browser allowlist (repository starter)

This repository is a remote source for QALQON's **browser strict-mode** DNS allowlist. It is **not** a malware database and must not be used as proof that listed websites are safe.

## Edit the list

1. Open `allowlist.txt` on GitHub and click the pencil icon.
2. Add or remove **one ASCII lowercase domain per line**, without `https://` and without any slash or wildcard.
3. Click **Commit changes**. The raw link tracks the latest `main` commit. GitHub Actions validates the syntax.
4. QALQON checks the raw file **during its existing daily hash database update check**. QALQON should compare SHA-256 to the local version, and only replace the active file when changed and valid. The update isn't immediate.

## Raw URL to add to Android code

`https://raw.githubusercontent.com/aex-3-14/QALQON-Allowlist/main/allowlist.txt`

This URL is already configured for the public repository `aex-3-14/QALQON-Allowlist`. No GitHub token should be embedded in the APK.

## Initial contents

The initial `allowlist.txt` is copied from the earlier 78-domain QALQON core file. Those entries had documented owner/domain references in the previous package. **They have not all been reverified for this template**, and this is **not** a 3000–5000-domain verified list. Review before publishing in a product.

## Critical safeguards

- Treat the remote TXT as untrusted until validated. Reject bad domains, duplicate entries, tiny/empty files and excessive size. Keep last known-good local copy on any error.
- Prefer only exact hosts unless you have deliberately scoped rules for subdomains.
- Never allow entire shared hosting/CDN platforms purely because of their parent domain.
- Keep Quad9 malware blocking active: an allowlisted website can still host phishing.
- A hash comparison **detects changes, not authenticity**. For high-trust production distribution, sign approved releases with an offline private key, and pin the public key in the APK. Consider branch protection and required CI checks; they don't substitute for content review.
- If a phone has no usable local allowlist, the app should **not** silently enable broken strict mode. Use the verified bundled fallback or mark strict filtering unavailable.
- A GitHub raw URL is appropriate for a small project; for large user bases evaluate release assets/CDN hosting. GitHub APIs have rate limits, and raw files may be cached briefly.

## Integration

See `android/AllowlistUpdater.kt` and `android/INTEGRATION.md`. This is a standalone example: it must be wired into QALQON's existing worker and VPN engine, and tested on actual Android devices.
