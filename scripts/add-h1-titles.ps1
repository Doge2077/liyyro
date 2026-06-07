# 为所有markdown文件添加文件名作为一级标题
# 对于已有h1的文件，标题层级自动后移

$docsDir = "C:\Codes\doc\liyyro\docs"

# 获取所有md文件（排除index.md）
$mdFiles = Get-ChildItem -Path $docsDir -Recurse -Filter "*.md" | Where-Object { $_.Name -ne "index.md" }

$addedCount = 0
$shiftedCount = 0

foreach ($file in $mdFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $lines = $content -split "`n"
    
    # 第一步：检测是否在代码块内，找出所有h1-h5的位置
    $inCodeBlock = $false
    $h1Positions = @()
    $h2Positions = @()
    $h3Positions = @()
    $h4Positions = @()
    $h5Positions = @()
    
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        
        # 检测代码块开始/结束
        if ($line -match '^\s*```') {
            $inCodeBlock = -not $inCodeBlock
            continue
        }
        
        # 只在代码块外检查标题
        if (-not $inCodeBlock) {
            if ($line -match '^#####\s+') { $h5Positions += $i }
            elseif ($line -match '^####\s+') { $h4Positions += $i }
            elseif ($line -match '^###\s+') { $h3Positions += $i }
            elseif ($line -match '^##\s+') { $h2Positions += $i }
            elseif ($line -match '^#\s+') { $h1Positions += $i }
        }
    }
    
    $hasH1 = $h1Positions.Count -gt 0
    
    # 构建新内容
    $newLines = @()
    
    # 找到frontmatter结束位置
    $frontmatterEnd = -1
    $inFrontmatter = $false
    
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^---\s*$') {
            if (-not $inFrontmatter) {
                $inFrontmatter = $true
            } else {
                $frontmatterEnd = $i
                break
            }
        }
    }
    
    if ($hasH1) {
        # 已有h1：添加文件名作为新的h1，原h1变为h2，以此类推
        $shiftedCount++
        
        # 添加frontmatter部分
        for ($i = 0; $i -le $frontmatterEnd; $i++) {
            $newLines += $lines[$i]
        }
        
        # 添加新的h1标题
        $fileName = $file.BaseName
        $newLines += ""
        $newLines += "# $fileName"
        $newLines += ""
        
        # 添加frontmatter之后的内容，标题层级后移
        $inCodeBlock = $false
        for ($i = $frontmatterEnd + 1; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            
            # 检测代码块开始/结束
            if ($line -match '^\s*```') {
                $inCodeBlock = -not $inCodeBlock
                $newLines += $line
                continue
            }
            
            # 只在代码块外进行标题层级后移
            if (-not $inCodeBlock) {
                if ($line -match '^######\s+') {
                    # h6保持不变（已经是最高级）
                    $newLines += $line
                }
                elseif ($line -match '^#####\s+') {
                    # h5 → h6
                    $newLines += $line -replace '^#####\s+', '###### '
                }
                elseif ($line -match '^####\s+') {
                    # h4 → h5
                    $newLines += $line -replace '^####\s+', '##### '
                }
                elseif ($line -match '^###\s+') {
                    # h3 → h4
                    $newLines += $line -replace '^###\s+', '#### '
                }
                elseif ($line -match '^##\s+') {
                    # h2 → h3
                    $newLines += $line -replace '^##\s+', '### '
                }
                elseif ($line -match '^#\s+') {
                    # h1 → h2
                    $newLines += $line -replace '^#\s+', '## '
                }
                else {
                    $newLines += $line
                }
            } else {
                $newLines += $line
            }
        }
        
        Write-Host "Shifted titles: $($file.Name)"
    } else {
        # 没有h1：在frontmatter后添加h1
        $addedCount++
        
        # 添加frontmatter部分
        for ($i = 0; $i -le $frontmatterEnd; $i++) {
            $newLines += $lines[$i]
        }
        
        # 添加h1标题
        $fileName = $file.BaseName
        $newLines += ""
        $newLines += "# $fileName"
        $newLines += ""
        
        # 添加frontmatter之后的内容
        for ($i = $frontmatterEnd + 1; $i -lt $lines.Count; $i++) {
            $newLines += $lines[$i]
        }
        
        Write-Host "Added h1: $($file.Name)"
    }
    
    # 写回文件
    $newContent = $newLines -join "`n"
    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
}

Write-Host ""
Write-Host "=== 完成 ==="
Write-Host "添加h1标题（无h1的文件）: $addedCount 个文件"
Write-Host "标题层级后移（有h1的文件）: $shiftedCount 个文件"
Write-Host "总计: $($addedCount + $shiftedCount) 个文件"