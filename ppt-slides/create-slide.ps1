# PPT 页面创建辅助脚本
param(
    [string]$SlideNum,
    [string]$XmlContent
)

$dir = "D:\Desktop\开源软件作业\oss-blog\ppt-slides"
$pid = "GYJFsENRDldxVQds3gWcrDECnVg"

# 写入 XML 文件
$xmlPath = "$dir\slide-$SlideNum.xml"
[System.IO.File]::WriteAllText($xmlPath, $XmlContent, [System.Text.UTF8Encoding]::new($false))

# 校验
$skillDir = "C:\Users\jl\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.skills\lark-slides-pro"
$lintResult = python "$skillDir\scripts\xml_lint.py" --input $xmlPath 2>&1 | ConvertFrom-Json
if ($lintResult.summary.error_count -ne 0) {
    Write-Output "ERROR: Slide $SlideNum validation failed"
    $lintResult.document.errors | ForEach-Object { Write-Output $_ }
    exit 1
}

# 组装 body
$bodyObj = @{ slide = @{ content = $XmlContent } }
$bodyJson = $bodyObj | ConvertTo-Json -Depth 5 -Compress
$bodyPath = "$dir\slide-$SlideNum-body.json"
[System.IO.File]::WriteAllText($bodyPath, $bodyJson, [System.Text.UTF8Encoding]::new($false))

# 创建页面
Set-Location $dir
$result = lark-cli slides xml_presentation.slide create --xml-presentation-id $pid --data "@slide-$SlideNum-body.json" 2>&1

# 解析结果
if ($result -match '"slide_id":"([^"]+)"') {
    $slideId = $Matches[1]
    Write-Output "SUCCESS: Slide $SlideNum created, slide_id=$slideId"
} else {
    Write-Output "RESULT: $result"
}
