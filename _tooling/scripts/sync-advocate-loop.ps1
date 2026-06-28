# Every 10 min: daily consolidation scan, then commit+push the vault if changed.
# HARDENED 2026-06: surfaces git failures (no more silent 2>$null swallowing),
# AUTO-HEALS a corrupt .git/index (the failure that once killed sync for ~a day),
# and writes a heartbeat so "last successful sync" is always visible.
$vault = "C:\Users\Josep\hermes-advocate"
$log   = "C:\Users\Josep\AppData\Local\hermes\logs\advocate-sync.log"
$py    = "C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
$scan  = "C:\Users\Josep\AppData\Local\hermes\scripts\consolidation-scan.py"
$beat  = "C:\Users\Josep\AppData\Local\hermes\logs\advocate-sync-heartbeat.txt"
$lastScan = ""
function Log($m) { "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $m" | Out-File -FilePath $log -Append -Encoding ascii }

while ($true) {
    try {
        # --- daily consolidation/rot scan (writes a report into the vault) ---
        $today = Get-Date -Format 'yyyy-MM-dd'
        if ($today -ne $lastScan) {
            try { & $py $scan 2>$null | Out-Null } catch { Log "scan error: $($_.Exception.Message)" }
            $lastScan = $today; Log "ran consolidation scan"
        }

        # --- health check: can git read the index? ---
        $st = git -C $vault status --porcelain 2>&1
        if ($LASTEXITCODE -ne 0) {
            $err = ($st | Select-Object -First 1)
            Log "WARNING: git status failed -> $err"
            if ("$st" -match "index") {
                # corrupt/unreadable .git/index: rebuild from HEAD (working tree untouched)
                Remove-Item "$vault\.git\index" -Force -ErrorAction SilentlyContinue
                git -C $vault read-tree HEAD 2>&1 | Out-Null
                $st = git -C $vault status --porcelain 2>&1
                if ($LASTEXITCODE -eq 0) { Log "AUTO-HEALED corrupt .git/index from HEAD" }
                else { Log "ERROR: could not heal index -> $($st | Select-Object -First 1)"; Start-Sleep 600; continue }
            } else { Start-Sleep 600; continue }
        }

        # --- commit + push any changes ---
        if ($st) {
            git -C $vault add -A 2>$null
            git -C $vault commit -m "advocate sync $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>$null | Out-Null
            if ($LASTEXITCODE -ne 0) { Log "ERROR: commit failed (rc=$LASTEXITCODE)" }
            $pout = git -C $vault push origin main 2>&1
            if ($LASTEXITCODE -ne 0) { Log "ERROR: push failed -> $($pout | Select-Object -Last 1)" }
            else { Log ("pushed " + ($st | Measure-Object -Line).Lines + " changed paths") }
        }

        # --- heartbeat (every cycle, even on no-op) so a stall is detectable ---
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  ok (pending=$(($st | Measure-Object -Line).Lines))" | Out-File -FilePath $beat -Encoding ascii
    } catch {
        Log "EXCEPTION: $($_.Exception.Message)"
    }
    Start-Sleep -Seconds 600
}
