#!/usr/bin/env pwsh
# Ghost CLI wrapper using Node.js 22
$ErrorActionPreference = "Stop"

$node22Dir = "D:\Desktop\开源软件作业\oss-blog\tools\node22\node-v22.23.1-win-x64"
$ghostCli = "D:\Desktop\开源软件作业\oss-blog\node_modules\ghost-cli\bin\ghost"

# Prepend Node 22 to PATH
$env:PATH = "$node22Dir;$env:PATH"

# Run ghost with Node 22
& "$node22Dir\node.exe" $ghostCli $args
exit $LASTEXITCODE
