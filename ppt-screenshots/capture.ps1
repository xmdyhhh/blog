Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

param(
    [string]$OutFile = "D:\Desktop\开源软件作业\oss-blog\ppt-screenshots\capture.png"
)

$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bmp = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bmp.Save($OutFile, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
Write-Output "saved: $OutFile ($((Get-Item $OutFile).Length) bytes)"
