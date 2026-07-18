# ============================================================================
# git-push.ps1 - Professional Auto-Push to GitHub
# ============================================================================
# Usage:
#   .\scripts\git-push.ps1                        # Auto commit + push
#   .\scripts\git-push.ps1 -Message "feat: ..."   # Custom commit message
#   .\scripts\git-push.ps1 -Branch "develop"      # Push to specific branch
#   .\scripts\git-push.ps1 -PushOnly              # Push only (no new commit)
#   .\scripts\git-push.ps1 -Force                  # Force push (dangerous)
#   .\scripts\git-push.ps1 -Silent                 # Suppress output
# ============================================================================

param(
    [string]$Message = "",
    [string]$Branch = "",
    [switch]$PushOnly,
    [switch]$Force,
    [switch]$Silent
)

# --- Strict Mode & Config ---------------------------------------------------
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# البحث ديناميكياً عن مجلد جذر المشروع (الذي يحتوي على مجلد .git)
$ProjectRoot = $ScriptDir
while ($ProjectRoot -and -not (Test-Path (Join-Path $ProjectRoot ".git"))) {
    $Parent = Split-Path $ProjectRoot -Parent
    if ($Parent -eq $ProjectRoot -or [string]::IsNullOrEmpty($Parent)) {
        # إذا لم يجد .git، يعود للمجلد الأساسي للسكربت كـ fallback
        $ProjectRoot = $ScriptDir
        break
    }
    $ProjectRoot = $Parent
}

$LogDir = Join-Path $ProjectRoot ".run-logs"
$LogFile = Join-Path $LogDir "git-push.log"

$MAX_RETRIES = 5
$LARGE_FILE_LIMIT = 100 * 1024 * 1024  # 100 MB
$StartTime = Get-Date

# --- Color Output Helper -----------------------------------------------------
function Write-Status {
    param([string]$Type, [string]$Msg)
    if ($Silent) { return }
    switch ($Type) {
        "OK"    { Write-Host "[OK] $Msg" -ForegroundColor Green }
        "INFO"  { Write-Host "[i] $Msg" -ForegroundColor Cyan }
        "WARN"  { Write-Host "[*] $Msg" -ForegroundColor Yellow }
        "ERR"   { Write-Host "[X] $Msg" -ForegroundColor Red }
        "HEAD"  { Write-Host "`n========== $Msg ==========" -ForegroundColor Magenta }
        "STEP"  { Write-Host "  --> $Msg" -ForegroundColor White }
        default { Write-Host $Msg }
    }
}

# --- Exit Helper --------------------------------------------------------------
function Exit-Script {
    param([int]$Code)
    # لا توقف السكربت إذا كان صامتاً أو يعمل في بيئة مؤتمتة غير تفاعلية (Input redirected)
    if (-not $Silent -and -not [Console]::IsInputRedirected) {
        Write-Host ""
        Read-Host "Press Enter to exit / اضغط Enter للخروج"
    }
    exit $Code
}

# --- Log Helper ---------------------------------------------------------------
function Write-Log {
    param([string]$Entry)
    try {
        if (-not (Test-Path $LogDir)) {
            New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
        }
        $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        $line = "[$ts] $Entry"
        Add-Content -Path $LogFile -Value $line -Encoding UTF8
    }
    catch {
        # Logging failure must never crash the script
    }
}

# --- Run Git Command with output capture --------------------------------------
function Invoke-Git {
    param([string]$Args_)
    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName = "git"
    $pinfo.Arguments = $Args_
    $pinfo.WorkingDirectory = $ProjectRoot
    $pinfo.RedirectStandardOutput = $true
    $pinfo.RedirectStandardError = $true
    $pinfo.UseShellExecute = $false
    $pinfo.CreateNoWindow = $true
    $pinfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $pinfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8

    $proc = New-Object System.Diagnostics.Process
    $proc.StartInfo = $pinfo

    try {
        $proc.Start() | Out-Null
        $stdout = $proc.StandardOutput.ReadToEnd()
        $stderr = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit()

        return @{
            ExitCode = $proc.ExitCode
            Output   = $stdout.Trim()
            Error    = $stderr.Trim()
        }
    }
    catch {
        return @{
            ExitCode = 999
            Output   = ""
            Error    = $_.Exception.Message
        }
    }
}

# =============================================================================
# PHASE 1: PRE-FLIGHT CHECKS
# =============================================================================
function Test-PreFlight {
    Write-Status "HEAD" "PHASE 1: Pre-Flight Checks"

    # 1.1 Git installed?
    Write-Status "STEP" "Checking git installation..."
    $gitPath = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitPath) {
        Write-Status "ERR" "Git is not installed or not in PATH!"
        Write-Status "ERR" "Install from: https://git-scm.com/download/win"
        Write-Log "FAIL: Git not found in PATH"
        return $false
    }
    $gitVer = (Invoke-Git "version").Output
    Write-Status "OK" "Git found: $gitVer"

    # 1.2 Inside a git repo?
    Write-Status "STEP" "Checking git repository..."
    $gitDir = Join-Path $ProjectRoot ".git"
    if (-not (Test-Path $gitDir)) {
        Write-Status "ERR" "Not a git repository! .git not found at: $ProjectRoot"
        Write-Log "FAIL: Not a git repository at $ProjectRoot"
        return $false
    }
    Write-Status "OK" "Git repository confirmed"

    # 1.3 Remote configured?
    Write-Status "STEP" "Checking remote configuration..."
    $remote = Invoke-Git "remote -v"
    if ($remote.ExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($remote.Output)) {
        Write-Status "ERR" "No remote configured! Add one with:"
        Write-Status "ERR" "  git remote add origin https://github.com/USER/REPO.git"
        Write-Log "FAIL: No remote configured"
        return $false
    }
    $remoteUrl = ($remote.Output -split "`n")[0]
    Write-Status "OK" "Remote: $remoteUrl"

    # 1.4 User config?
    Write-Status "STEP" "Checking user configuration..."
    $userName = (Invoke-Git "config user.name").Output
    $userEmail = (Invoke-Git "config user.email").Output
    if ([string]::IsNullOrWhiteSpace($userName)) {
        Write-Status "WARN" "user.name not set, setting default..."
        Invoke-Git 'config user.name "Developer"' | Out-Null
        $userName = "Developer"
    }
    if ([string]::IsNullOrWhiteSpace($userEmail)) {
        Write-Status "WARN" "user.email not set, setting default..."
        Invoke-Git 'config user.email "dev@local"' | Out-Null
        $userEmail = "dev@local"
    }
    Write-Status "OK" "User: $userName <$userEmail>"

    # 1.5 Clean git state? (no locks, conflicts, rebase)
    Write-Status "STEP" "Checking git state cleanliness..."

    # Check index.lock
    $lockFile = Join-Path $gitDir "index.lock"
    if (Test-Path $lockFile) {
        Write-Status "WARN" "Found index.lock - removing stale lock..."
        try {
            Remove-Item $lockFile -Force
            Write-Status "OK" "Lock file removed"
            Write-Log "Removed stale index.lock"
        }
        catch {
            Write-Status "ERR" "Cannot remove index.lock. Close other git processes first."
            Write-Log "FAIL: Cannot remove index.lock"
            return $false
        }
    }

    # Check rebase in progress
    $rebaseDir = Join-Path $gitDir "rebase-merge"
    $rebaseApplyDir = Join-Path $gitDir "rebase-apply"
    if ((Test-Path $rebaseDir) -or (Test-Path $rebaseApplyDir)) {
        Write-Status "WARN" "Rebase in progress, aborting it..."
        $abortResult = Invoke-Git "rebase --abort"
        if ($abortResult.ExitCode -eq 0) {
            Write-Status "OK" "Rebase aborted successfully"
            Write-Log "Aborted stale rebase"
        }
        else {
            Write-Status "ERR" "Cannot abort rebase: $($abortResult.Error)"
            Write-Log "FAIL: Cannot abort rebase"
            return $false
        }
    }

    # Check merge in progress
    $mergeHead = Join-Path $gitDir "MERGE_HEAD"
    if (Test-Path $mergeHead) {
        Write-Status "WARN" "Merge in progress, aborting it..."
        $abortResult = Invoke-Git "merge --abort"
        if ($abortResult.ExitCode -eq 0) {
            Write-Status "OK" "Merge aborted successfully"
            Write-Log "Aborted stale merge"
        }
        else {
            Write-Status "ERR" "Cannot abort merge: $($abortResult.Error)"
            Write-Log "FAIL: Cannot abort merge"
            return $false
        }
    }

    # Check cherry-pick in progress
    $cherryPick = Join-Path $gitDir "CHERRY_PICK_HEAD"
    if (Test-Path $cherryPick) {
        Write-Status "WARN" "Cherry-pick in progress, aborting it..."
        $abortResult = Invoke-Git "cherry-pick --abort"
        if ($abortResult.ExitCode -eq 0) {
            Write-Status "OK" "Cherry-pick aborted successfully"
            Write-Log "Aborted stale cherry-pick"
        }
        else {
            Write-Status "ERR" "Cannot abort cherry-pick: $($abortResult.Error)"
            Write-Log "FAIL: Cannot abort cherry-pick"
            return $false
        }
    }

    Write-Status "OK" "Git state is clean"
    return $true
}

# =============================================================================
# PHASE 2: ANALYZE CHANGES
# =============================================================================
function Get-ChangeAnalysis {
    Write-Status "HEAD" "PHASE 2: Analyzing Changes"

    # Get current branch
    $branchResult = Invoke-Git "rev-parse --abbrev-ref HEAD"
    $currentBranch = $branchResult.Output
    if ([string]::IsNullOrWhiteSpace($currentBranch)) {
        $currentBranch = "main"
    }
    Write-Status "INFO" "Current branch: $currentBranch"

    # Override branch if specified
    if (-not [string]::IsNullOrWhiteSpace($Branch)) {
        Write-Status "INFO" "Target branch override: $Branch"
        # Switch branch if different
        if ($Branch -ne $currentBranch) {
            Write-Status "STEP" "Switching to branch: $Branch"
            $checkout = Invoke-Git "checkout $Branch"
            if ($checkout.ExitCode -ne 0) {
                # Try creating the branch
                Write-Status "STEP" "Branch not found, creating: $Branch"
                $newBranch = Invoke-Git "checkout -b $Branch"
                if ($newBranch.ExitCode -ne 0) {
                    Write-Status "ERR" "Cannot switch to branch: $Branch"
                    Write-Log "FAIL: Cannot checkout branch $Branch"
                    return $null
                }
            }
            $currentBranch = $Branch
            Write-Status "OK" "Switched to branch: $currentBranch"
        }
    }

    # Check for changes with disabled quotepath to get raw UTF-8 names without octal escapes
    $status = Invoke-Git "-c core.quotepath=false status --porcelain"
    [array]$statusLines = @()
    if (-not [string]::IsNullOrWhiteSpace($status.Output)) {
        $statusLines = @($status.Output -split "`n" | Where-Object { $_.Trim() -ne "" })
    }

    $added = @()
    $modified = @()
    $deleted = @()
    $untracked = @()

    foreach ($line in $statusLines) {
        $trimmed = $line.Trim()
        if ($trimmed.Length -lt 3) { continue }
        $code = $trimmed.Substring(0, 2)
        $file = $trimmed.Substring(3).Trim().Trim('"')

        # Handle Rename operations (e.g. R  old_path -> new_path)
        if ($code.StartsWith("R") -and ($file -match " -> ")) {
            $parts = $file -split " -> "
            $file = $parts[-1].Trim().Trim('"')
        }

        switch -Wildcard ($code) {
            "??" { $untracked += $file }
            "A*" { $added += $file }
            "M*" { $modified += $file }
            "*M" { $modified += $file }
            "D*" { $deleted += $file }
            "*D" { $deleted += $file }
            "R*" { $modified += $file }
            default { $modified += $file }
        }
    }

    $totalChanges = $statusLines.Count
    Write-Status "INFO" "Changes detected: $totalChanges total"
    if ($added.Count -gt 0) { Write-Status "STEP" "  Added:     $($added.Count)" }
    if ($modified.Count -gt 0) { Write-Status "STEP" "  Modified:  $($modified.Count)" }
    if ($deleted.Count -gt 0) { Write-Status "STEP" "  Deleted:   $($deleted.Count)" }
    if ($untracked.Count -gt 0) { Write-Status "STEP" "  Untracked: $($untracked.Count)" }

    # Check for large files
    Write-Status "STEP" "Checking for large files (>100MB)..."
    $largeFiles = @()
    $allFiles = $modified + $added + $untracked
    foreach ($f in $allFiles) {
        $fullPath = Join-Path $ProjectRoot $f
        if ((Test-Path $fullPath) -and (-not (Test-Path $fullPath -PathType Container))) {
            $fileInfo = Get-Item $fullPath -ErrorAction SilentlyContinue
            if ($fileInfo -and ($fileInfo.PSObject.Properties['Length']) -and $fileInfo.Length -gt $LARGE_FILE_LIMIT) {
                $largeFiles += $f
                $sizeMB = [math]::Round($fileInfo.Length / 1MB, 1)
                Write-Status "WARN" "Large file detected: $f ($sizeMB MB)"
            }
        }
    }

    # Auto-add large files to .gitignore
    if ($largeFiles.Count -gt 0) {
        Write-Status "WARN" "Adding $($largeFiles.Count) large file(s) to .gitignore..."
        $gitignorePath = Join-Path $ProjectRoot ".gitignore"
        $gitignoreContent = ""
        if (Test-Path $gitignorePath) {
            $gitignoreContent = Get-Content $gitignorePath -Raw -ErrorAction SilentlyContinue
        }
        foreach ($lf in $largeFiles) {
            if ($gitignoreContent -notmatch [regex]::Escape($lf)) {
                Add-Content -Path $gitignorePath -Value "`n$lf" -Encoding UTF8
                Write-Status "OK" "Added to .gitignore: $lf"
                Write-Log "Added large file to .gitignore: $lf"
            }
        }
    }

    return @{
        Branch      = $currentBranch
        Added       = $added
        Modified    = $modified
        Deleted     = $deleted
        Untracked   = $untracked
        Total       = $totalChanges
        LargeFiles  = $largeFiles
    }
}

# =============================================================================
# PHASE 3: GENERATE SMART COMMIT MESSAGE
# =============================================================================
function New-SmartCommitMessage {
    param([hashtable]$Analysis)

    if (-not [string]::IsNullOrWhiteSpace($Message)) {
        return $Message
    }

    Write-Status "HEAD" "PHASE 3: Generating Smart Commit Message"

    $allFiles = @()
    $allFiles += $Analysis.Added
    $allFiles += $Analysis.Modified
    $allFiles += $Analysis.Deleted
    $allFiles += $Analysis.Untracked

    # Detect primary change type
    $prefix = "chore"
    $description = "update project files"

    # Analyze file types for smart prefix
    $hasSrc = $false
    $hasDocs = $false
    $hasConfig = $false
    $hasTest = $false
    $hasStyles = $false
    $hasFix = $false
    $primaryDirs = @{}

    foreach ($f in $allFiles) {
        $lower = $f.ToLower()
        if ($lower -match "^src[/\\]") { $hasSrc = $true }
        if ($lower -match "\.(md|txt|doc)$") { $hasDocs = $true }
        if ($lower -match "(\.config|\.json|\.yml|\.yaml|\.env|\.toml)$") { $hasConfig = $true }
        if ($lower -match "(test|spec|__test__)") { $hasTest = $true }
        if ($lower -match "\.(css|scss|less|styled)") { $hasStyles = $true }
        if ($lower -match "(fix|bug|patch|hotfix)") { $hasFix = $true }

        # Track primary directories
        $parts = $f -split "[/\\]"
        if ($parts.Count -gt 1) {
            $dir = $parts[0]
            if ($primaryDirs.ContainsKey($dir)) {
                $primaryDirs[$dir]++
            }
            else {
                $primaryDirs[$dir] = 1
            }
        }
    }

    # Determine prefix
    if ($hasFix) { $prefix = "fix" }
    elseif ($hasTest) { $prefix = "test" }
    elseif ($hasDocs -and -not $hasSrc) { $prefix = "docs" }
    elseif ($hasConfig -and -not $hasSrc) { $prefix = "config" }
    elseif ($hasStyles -and -not $hasSrc) { $prefix = "style" }
    elseif ($hasSrc) { $prefix = "feat" }

    # Build description
    $dirSummary = ""
    if ($primaryDirs.Count -gt 0) {
        $topDirs = $primaryDirs.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 3
        $dirNames = $topDirs | ForEach-Object { $_.Key }
        $dirSummary = $dirNames -join ", "
    }

    $counts = @()
    $addCount = $Analysis.Added.Count + $Analysis.Untracked.Count
    if ($addCount -gt 0) { $counts += "$addCount new" }
    if ($Analysis.Modified.Count -gt 0) { $counts += "$($Analysis.Modified.Count) modified" }
    if ($Analysis.Deleted.Count -gt 0) { $counts += "$($Analysis.Deleted.Count) deleted" }
    $countStr = $counts -join ", "

    if (-not [string]::IsNullOrWhiteSpace($dirSummary)) {
        $description = "update $dirSummary ($countStr)"
    }
    else {
        $description = "update $countStr files"
    }

    # Add timestamp
    $ts = (Get-Date).ToString("yyyy-MM-dd HH:mm")
    $commitMsg = "$prefix`: $description [$ts]"

    # Truncate if too long
    if ($commitMsg.Length -gt 120) {
        $commitMsg = $commitMsg.Substring(0, 117) + "..."
    }

    Write-Status "OK" "Commit message: $commitMsg"
    return $commitMsg
}

# =============================================================================
# PHASE 4: STAGE AND COMMIT
# =============================================================================
function Invoke-StageAndCommit {
    param([string]$CommitMessage)

    Write-Status "HEAD" "PHASE 4: Stage and Commit"

    # Stage all changes
    Write-Status "STEP" "Staging all changes (git add -A)..."
    $addResult = Invoke-Git "add -A"
    if ($addResult.ExitCode -ne 0) {
        Write-Status "ERR" "Failed to stage changes: $($addResult.Error)"
        Write-Log "FAIL: git add -A failed: $($addResult.Error)"
        return $false
    }
    Write-Status "OK" "All changes staged"

    # Verify there are staged changes
    $diffResult = Invoke-Git "diff --cached --stat"
    if ([string]::IsNullOrWhiteSpace($diffResult.Output)) {
        Write-Status "INFO" "No changes to commit after staging"
        Write-Log "INFO: No changes to commit"
        return $false
    }

    # Commit
    Write-Status "STEP" "Committing changes..."
    $safeMsg = $CommitMessage -replace '"', '\"'
    $commitResult = Invoke-Git "commit -m `"$safeMsg`""
    if ($commitResult.ExitCode -ne 0) {
        $errMsg = $commitResult.Error
        if ($errMsg -match "nothing to commit") {
            Write-Status "INFO" "Nothing to commit, working tree clean"
            Write-Log "INFO: Nothing to commit"
            return $false
        }
        Write-Status "ERR" "Commit failed: $errMsg"
        Write-Log "FAIL: git commit failed: $errMsg"
        return $false
    }

    Write-Status "OK" "Commit successful"
    if (-not [string]::IsNullOrWhiteSpace($commitResult.Output)) {
        $firstLine = ($commitResult.Output -split "`n")[0]
        Write-Status "INFO" $firstLine
    }
    return $true
}

# =============================================================================
# PHASE 5: NETWORK OPTIMIZATION
# =============================================================================
function Optimize-NetworkConfig {
    Write-Status "HEAD" "PHASE 5: Network Optimization"

    # Set http buffer
    Write-Status "STEP" "Configuring HTTP buffer (500MB)..."
    Invoke-Git "config http.postBuffer 524288000" | Out-Null

    # Set HTTP version
    Write-Status "STEP" "Setting HTTP/1.1 protocol..."
    Invoke-Git "config http.version HTTP/1.1" | Out-Null

    # Disable low speed limit
    Write-Status "STEP" "Disabling low-speed timeout..."
    Invoke-Git "config http.lowSpeedLimit 0" | Out-Null
    Invoke-Git "config http.lowSpeedTime 999999" | Out-Null

    # Check repo size and gc if needed
    $sizeResult = Invoke-Git "count-objects -v"
    if (-not [string]::IsNullOrWhiteSpace($sizeResult.Output)) {
        $sizeMatch = [regex]::Match($sizeResult.Output, "size-pack:\s*(\d+)")
        if ($sizeMatch.Success) {
            $sizePack = [int64]$sizeMatch.Groups[1].Value
            $sizePackMB = [math]::Round($sizePack / 1024, 1)
            Write-Status "INFO" "Repository pack size: $sizePackMB MB"

            if ($sizePack -gt 102400) {
                Write-Status "STEP" "Large repo detected, running git gc..."
                Invoke-Git "gc --prune=now" | Out-Null
                Write-Status "OK" "Repository cleaned"
                Write-Log "Ran git gc (pack size was $sizePackMB MB)"
            }
        }
    }

    Write-Status "OK" "Network optimizations applied"
}

# =============================================================================
# PHASE 6: PUSH WITH RETRY
# =============================================================================
function Invoke-PushWithRetry {
    param([string]$TargetBranch)

    Write-Status "HEAD" "PHASE 6: Pushing to GitHub"

    $delays = @(5, 15, 30, 60, 120)

    for ($attempt = 1; $attempt -le $MAX_RETRIES; $attempt++) {
        Write-Status "STEP" "Push attempt $attempt of $MAX_RETRIES..."

        # Build push command
        $pushArgs = "push origin $TargetBranch"
        if ($Force) {
            $pushArgs = "push origin $TargetBranch --force"
            Write-Status "WARN" "Force push enabled!"
        }

        $pushResult = Invoke-Git $pushArgs

        # === SUCCESS ===
        if ($pushResult.ExitCode -eq 0) {
            Write-Status "OK" "Push successful on attempt $attempt!"
            Write-Log "Push succeeded on attempt $attempt to branch $TargetBranch"
            return $true
        }

        $errMsg = $pushResult.Error
        Write-Status "WARN" "Push failed: $errMsg"

        # === HANDLE SPECIFIC ERRORS ===

        # Non-fast-forward (remote has new commits)
        if ($errMsg -match "non-fast-forward|fetch first|cannot be resolved") {
            Write-Status "WARN" "Remote has newer commits. Pulling with rebase..."
            $pullResult = Invoke-Git "pull --rebase origin $TargetBranch"
            if ($pullResult.ExitCode -ne 0) {
                # Rebase conflict? Try merge instead
                Write-Status "WARN" "Rebase failed, trying merge pull..."
                Invoke-Git "rebase --abort" | Out-Null
                $pullMerge = Invoke-Git "pull origin $TargetBranch --no-rebase"
                if ($pullMerge.ExitCode -ne 0) {
                    Write-Status "ERR" "Cannot sync with remote. Manual intervention needed."
                    Write-Status "ERR" "Run: git pull origin $TargetBranch"
                    Write-Log "FAIL: Cannot sync with remote"
                    return $false
                }
            }
            Write-Status "OK" "Synced with remote, retrying push..."
            # Don't count this as a failed attempt
            $attempt--
            continue
        }

        # New branch (upstream not set)
        if ($errMsg -match "no upstream|has no upstream|does not appear to be a git repository") {
            Write-Status "INFO" "Setting upstream branch..."
            $pushArgs = "push -u origin $TargetBranch"
            if ($Force) {
                $pushArgs = "push -u origin $TargetBranch --force"
            }
            $upstreamResult = Invoke-Git $pushArgs
            if ($upstreamResult.ExitCode -eq 0) {
                Write-Status "OK" "Push with upstream set successful!"
                Write-Log "Push succeeded (set upstream) to $TargetBranch"
                return $true
            }
            $errMsg = $upstreamResult.Error
        }

        # Authentication failure
        if ($errMsg -match "Authentication|403|401|credential|permission denied|access denied") {
            Write-Status "ERR" "Authentication failed!"
            Write-Status "ERR" "Fix options:"
            Write-Status "ERR" "  1. Run: git credential-manager configure"
            Write-Status "ERR" "  2. Or set token: git remote set-url origin https://TOKEN@github.com/USER/REPO.git"
            Write-Status "ERR" "  3. Or use SSH: git remote set-url origin git@github.com:USER/REPO.git"
            Write-Log "FAIL: Authentication failed"
            return $false
        }

        # Repository not found
        if ($errMsg -match "repository not found|not exist|404") {
            Write-Status "ERR" "Repository not found on GitHub!"
            Write-Status "ERR" "Verify the remote URL: git remote -v"
            Write-Log "FAIL: Repository not found"
            return $false
        }

        # Network / timeout errors - retry with backoff
        if ($attempt -lt $MAX_RETRIES) {
            $delay = $delays[$attempt - 1]
            Write-Status "WARN" "Retrying in $delay seconds..."
            Write-Log "Push attempt $attempt failed, retrying in ${delay}s: $errMsg"
            Start-Sleep -Seconds $delay
        }
    }

    Write-Status "ERR" "All $MAX_RETRIES push attempts failed!"
    Write-Log "FAIL: All push attempts exhausted"
    return $false
}

# =============================================================================
# PHASE 7: POST-PUSH REPORT
# =============================================================================
function Show-PostPushReport {
    param(
        [string]$TargetBranch,
        [hashtable]$Analysis,
        [bool]$Committed
    )

    Write-Status "HEAD" "PHASE 7: Report"

    # Get remote URL for GitHub link
    $remoteResult = Invoke-Git "remote get-url origin"
    $remoteUrl = $remoteResult.Output
    $githubUrl = $remoteUrl -replace "\.git$", ""

    # Get latest commit hash
    $hashResult = Invoke-Git "rev-parse --short HEAD"
    $commitHash = $hashResult.Output

    # Calculate elapsed time
    $elapsed = (Get-Date) - $StartTime
    $elapsedStr = "$([math]::Floor($elapsed.TotalMinutes))m $($elapsed.Seconds)s"

    # Build report
    Write-Status "OK" "======================================"
    Write-Status "OK" "  PUSH COMPLETED SUCCESSFULLY!"
    Write-Status "OK" "======================================"

    if (-not $Silent) {
        Write-Host ""
        Write-Host "  Branch:    $TargetBranch" -ForegroundColor White
        Write-Host "  Commit:    $commitHash" -ForegroundColor White
        if ($Analysis) {
            $total = $Analysis.Total
            Write-Host "  Changes:   $total file(s)" -ForegroundColor White
        }
        Write-Host "  Time:      $elapsedStr" -ForegroundColor White
        Write-Host ""
        Write-Host "  GitHub:    $githubUrl" -ForegroundColor Cyan
        Write-Host "  Commit:    $githubUrl/commit/$commitHash" -ForegroundColor Cyan
        Write-Host "  Branch:    $githubUrl/tree/$TargetBranch" -ForegroundColor Cyan
        Write-Host ""
    }

    # Log success
    $logEntry = "SUCCESS: Pushed to $TargetBranch ($commitHash)"
    if ($Analysis) {
        $logEntry += " | $($Analysis.Total) files"
    }
    $logEntry += " | $elapsedStr"
    Write-Log $logEntry
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================
function Start-GitPush {
    Write-Log "--- START git-push ---"

    if (-not $Silent) {
        Write-Host ""
        Write-Host "  =============================================" -ForegroundColor Cyan
        Write-Host "    Git Auto-Push v2.0 - Professional Edition   " -ForegroundColor Cyan
        Write-Host "  =============================================" -ForegroundColor Cyan
        Write-Host ""
    }

    # PHASE 1: Pre-flight
    $preFlightOk = Test-PreFlight
    if (-not $preFlightOk) {
        Write-Status "ERR" "Pre-flight checks failed. Aborting."
        Write-Log "ABORTED: Pre-flight failed"
        Exit-Script 1
    }

    # PHASE 2: Analyze changes
    $analysis = Get-ChangeAnalysis
    if (-not $analysis) {
        Write-Status "ERR" "Change analysis failed. Aborting."
        Write-Log "ABORTED: Change analysis failed"
        Exit-Script 1
    }

    $targetBranch = $analysis.Branch
    $committed = $false

    if (-not $PushOnly) {
        # Check if there are changes
        if ($analysis.Total -eq 0) {
            # Check if there are unpushed commits
            $unpushed = Invoke-Git "log origin/$targetBranch..HEAD --oneline"
            if ([string]::IsNullOrWhiteSpace($unpushed.Output)) {
                Write-Status "INFO" "No changes to commit and no unpushed commits."
                Write-Status "INFO" "Everything is up to date!"
                Write-Log "INFO: No changes, up to date"
                Exit-Script 0
            }
            else {
                Write-Status "INFO" "No new changes, but found unpushed commits:"
                $unpushedLines = $unpushed.Output -split "`n"
                foreach ($line in $unpushedLines) {
                    Write-Status "STEP" "  $line"
                }
                Write-Status "INFO" "Proceeding to push..."
            }
        }
        else {
            # PHASE 3: Generate commit message
            $commitMsg = New-SmartCommitMessage -Analysis $analysis

            # PHASE 4: Stage and commit
            $committed = Invoke-StageAndCommit -CommitMessage $commitMsg
            if (-not $committed) {
                # Check if there are still unpushed commits
                $unpushed = Invoke-Git "log origin/$targetBranch..HEAD --oneline"
                if ([string]::IsNullOrWhiteSpace($unpushed.Output)) {
                    Write-Status "INFO" "No commits to push. Done."
                    Write-Log "INFO: Nothing to push"
                    Exit-Script 0
                }
                Write-Status "INFO" "Commit skipped, but found unpushed commits. Proceeding to push..."
            }
        }
    }
    else {
        Write-Status "INFO" "PushOnly mode - skipping commit"
    }

    # PHASE 5: Network optimization
    Optimize-NetworkConfig

    # PHASE 6: Push
    $pushOk = Invoke-PushWithRetry -TargetBranch $targetBranch
    if (-not $pushOk) {
        Write-Status "ERR" "Push failed after all retries!"
        Write-Log "FAILED: Push could not complete"
        Exit-Script 1
    }

    # PHASE 7: Report
    Show-PostPushReport -TargetBranch $targetBranch -Analysis $analysis -Committed $committed

    Write-Log "--- END git-push ---"
    Exit-Script 0
}

# --- EXECUTE ---
try {
    Start-GitPush
}
catch {
    Write-Status "ERR" "Unexpected error: $_"
    Write-Status "ERR" "Stack: $($_.ScriptStackTrace)"
    Write-Log "CRASH: $_ | $($_.ScriptStackTrace)"
    Exit-Script 1
}
