# 修复HTML实体转义问题
# 替换 &lt; -> <, &gt; -> >, &amp; -> &

$docsDir = "C:\Codes\doc\liyyro\docs"

# 获取所有md文件
$mdFiles = Get-ChildItem -Path $docsDir -Filter "*.md" -Recurse

foreach ($file in $mdFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    
    # 检查是否包含需要替换的HTML实体
    if ($content -match '&lt;|&gt;|&amp;') {
        Write-Host "修复文件: $($file.FullName)"
        
        # 替换HTML实体
        $newContent = $content -replace '&lt;', '<'
        $newContent = $newContent -replace '&gt;', '>'
        $newContent = $newContent -replace '&amp;', '&'
        
        # 写回文件
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
    }
}

Write-Host "修复完成"