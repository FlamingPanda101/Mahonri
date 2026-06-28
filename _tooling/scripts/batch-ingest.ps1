# Batch-ingest into the apologetics library, in controlled batches (DEEP mode, self-verifying).
# Usage:
#   batch-ingest.ps1 -Count 20      process up to 20 from ingest-queue.txt; only SUCCESSFUL ones are removed
#   batch-ingest.ps1                 process the whole queue
#   batch-ingest.ps1 <url1> <url2>   ad-hoc (does not touch the queue)
# Per source: BUILD (deep) -> verify a Source note appeared -> retry once if not -> CHECK+DEPTH.
# A video is only marked done (and removed from the queue) if a Source note for its video ID exists.
param([int]$Count = 0, [Parameter(ValueFromRemainingArguments = $true)][string[]]$Urls)
$ErrorActionPreference = "SilentlyContinue"
$hermes = "C:\Users\Josep\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
$queue  = "C:\Users\Josep\AppData\Local\hermes\scripts\ingest-queue.txt"
$donef  = "C:\Users\Josep\AppData\Local\hermes\scripts\ingest-done.txt"
$srcdir = "C:\Users\Josep\hermes-advocate\Sources"
$log    = "C:\Users\Josep\AppData\Local\hermes\logs\batch-ingest.log"
$env:OBSIDIAN_VAULT_PATH = "C:\Users\Josep\hermes-advocate"
$env:HERMES_ACCEPT_HOOKS = "1"
function Log($m) { ("$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  $m") | Out-File -FilePath $log -Append -Encoding ascii }
function VidOf($u) { if ($u -match '(?:youtu\.be/|/live/|v=)([A-Za-z0-9_-]{11})') { $Matches[1] } else { $u } }
function HasSource($vid) {
  $hit = Get-ChildItem $srcdir -Filter *.md -EA SilentlyContinue | Where-Object { (Get-Content $_.FullName -Raw -EA SilentlyContinue) -match [regex]::Escape($vid) } | Select-Object -First 1
  return [bool]$hit
}
$BUILD = "Ingest this source into the apologetics library following your FULL protocol AND the DEPTH MANDATE in your SOUL - prioritize MAXIMUM depth and detail; brevity is not wanted. Dedup first (UPDATE existing notes with new evidence instead of duplicating). Then create: a Source note with authority tier; a Concept note for EVERY distinct argument/objection/rebuttal (not just the main ones), each with several numbered evidence points, the opposing view STEELMANNED, relevant scholarly/historical/linguistic context, and MULTIPLE verbatim quotes - each with its own [^n] footnote carrying its [MM:SS] timestamp; Scripture notes (KJV + key Greek/Hebrew terms + cross-tradition readings where relevant); rich People notes (bio + credentials). Bidirectionally link everything. Long, thorough, richly-linked notes are the goal: "

if (-not $Urls -or $Urls.Count -eq 0) {
  $all = @(Get-Content $queue | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith("#") } | ForEach-Object { $_.Trim() })
  if ($Count -gt 0) { $Urls = @($all | Select-Object -First $Count) } else { $Urls = $all }
}
Log ("=== batch start: " + (@($Urls).Count) + " source(s) ===")
$succeeded = @(); $failed = @()
foreach ($url in @($Urls)) {
  $u = $url.Trim(); if (-not $u) { continue }
  $vid = VidOf $u
  if (HasSource $vid) { Log ("SKIP (already ingested) " + $u); $succeeded += $u; continue }
  Log ("BUILD " + $u)
  & $hermes -p apologist -z ($BUILD + $u) 2>&1 | Out-Null
  if (-not (HasSource $vid)) {
    Log ("RETRY (no source note yet) " + $u)
    Start-Sleep -Seconds 25
    & $hermes -p apologist -z ($BUILD + $u) 2>&1 | Out-Null
  }
  if (HasSource $vid) {
    Log ("CHECK " + $u)
    & $hermes -p apologist -z ("CHECKER + DEPTH PASS for the source just ingested (" + $u + "). Find its notes and VERIFY + FIX: (1) every quote/claim has a [^n] footnote with a [MM:SS] timestamp and a [[Source]] link; (2) every person named is wiki-linked to their [[People]] note (create it if missing); (3) every scripture is wiki-linked to its [[Scripture]] note; (4) DEPTH: any Concept that is THIN must be EXPANDED - more numbered evidence points, steelman the other side, additional verbatim quotes (with [MM:SS]), scholarly/linguistic context. Patch anything missing or shallow. Report what you fixed.") 2>&1 | Out-Null
    Log ("DONE  " + $u)
    $succeeded += $u
  } else {
    Log ("FAILED (no source note after retry; left in queue) " + $u)
    $failed += $u
  }
  Start-Sleep -Seconds 8
}
# remove ONLY succeeded from the queue; failed stay for next run
if ($succeeded.Count -gt 0) {
  Add-Content -Path $donef -Value $succeeded -Encoding ascii
  $sset = @{}; foreach ($s in $succeeded) { $sset[(VidOf $s)] = $true }
  $remaining = @(Get-Content $queue | Where-Object { $_.Trim() -and -not $_.Trim().StartsWith("#") } | ForEach-Object { $_.Trim() } | Where-Object { -not $sset[(VidOf $_)] })
  Set-Content -Path $queue -Value (@("# Apologetics queue (remaining, not yet ingested) - run in batches of 20") + $remaining) -Encoding ascii
}
Log ("=== batch complete: " + $succeeded.Count + " ok, " + $failed.Count + " failed/left ===")
Write-Host ("Done this run: " + $succeeded.Count + " ok, " + $failed.Count + " failed (still queued).")
