# Integration into existing QALQON hash-update check

This helper **does not** automatically integrate into the existing QALQON code. Move `AllowlistUpdater.kt` into the appropriate package and verify the configured raw GitHub URL. Ensure the app has `android.permission.INTERNET` and Kotlin coroutines (usually already installed in Android projects).

**Reuse QALQON's existing hash update worker/coroutine:**

```kotlin
// In the already existing daily updater, on a background thread:
val hashes = try { updateThreatHashes() } catch (e: Exception) { /* log failure */ }
val allowlist = AllowlistUpdater(applicationContext).check()
if (allowlist.error != null) {
    // log allowlist update failure, keep current file
} else if (allowlist.changed) {
    // ATOMICALLY reload in-memory browser allowlist snapshot from browser_allowlist.txt
    // log "allowlist updated", count, timestamp; update user-facing last-check status
}
```

Replace `updateThreatHashes()` with the REAL QALQON function; it is deliberately pseudocode because the current source code was not provided for this integration. Do **not** skip the allowlist check when the hash check fails, and do not create a second periodic scheduler.

The TXT lives in internal app storage (`filesDir/browser_allowlist.txt`), separate from the bundled fallback and the built-in/downloaded threat hash databases. QALQON's VPN filtering engine must read this file **only for browser strict mode** and must keep Quad9 protection active for other app traffic. Whitelist domain ownership and phishing safety are different things. Prefer using a signed release mechanism before widespread deployment.

The `If-None-Match` request allows a fast HTTP 304 response when unmodified; SHA-256 ensures a cached or re-fetched 200 response only replaces local data when its content has actually changed. GitHub raw caching may delay propagation of a commit. WorkManager's daily run is approximate, not precisely at a fixed time.
