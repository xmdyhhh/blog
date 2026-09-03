#!/usr/bin/env pwsh
# Start Ghost local instance with Node 22
$ErrorActionPreference = "Stop"

$node22Dir = "D:\Desktop\开源软件作业\oss-blog\tools\node22\node-v22.23.1-win-x64"
$ghostCli = "D:\Desktop\开源软件作业\oss-blog\node_modules\ghost-cli\bin\ghost"

$env:PATH = "$node22Dir;$env:PATH"

Set-Location "D:\Desktop\开源软件作业\oss-blog\runtime"
& "$node22Dir\node.exe" $ghostCli start
exit $LASTEXITCODE
