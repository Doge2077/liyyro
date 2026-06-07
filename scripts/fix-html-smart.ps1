# 智能修复HTML实体 - 只在代码块内替换，frontmatter中的Q&amp;A也修复

$docsDir = "C:\Codes\doc\liyyro\docs"

# 获取所有md文件
$mdFiles = Get-ChildItem -Path $docsDir -Filter "*.md" -Recurse

foreach ($file in $mdFiles) {
    $content = Get-Content -Path $file.FullName -Encoding UTF8
    
    $inFrontmatter = $false
    $inCodeBlock = $false
    $fixed = $false
    $newContent = @()
    
    foreach ($line in $content) {
        $newLine = $line
        
        # 检测 frontmatter
        if ($line -match '^---$') {
            if (-not $inFrontmatter -and $newContent.Count -eq 0) {
                $inFrontmatter = $true
            } elseif ($inFrontmatter) {
                $inFrontmatter = $false
            }
        }
        
        # 检测代码块
        if ($line -match '^\s*```') {
            if ($inCodeBlock) {
                $inCodeBlock = $false
            } else {
                $inCodeBlock = $true
            }
        }
        
        # frontmatter中只修复Q&amp;A
        if ($inFrontmatter) {
            if ($newLine -match 'Q&amp;A') {
                $newLine = $newLine -replace 'Q&amp;A', 'Q&A'
                $fixed = $true
            }
        }
        # 代码块内修复所有HTML实体
        elseif ($inCodeBlock) {
            if ($newLine -match '&lt;|&gt;|&amp;') {
                $newLine = $newLine -replace '&lt;', '<'
                $newLine = $newLine -replace '&gt;', '>'
                $newLine = $newLine -replace '&amp;', '&'
                $fixed = $true
            }
        }
        
        $newContent += $newLine
    }
    
    if ($fixed) {
        Write-Host "修复文件: $($file.FullName)"
        Set-Content -Path $file.FullName -Value ($newContent -join "`n") -Encoding UTF8
    }
}

Write-Host "修复完成"