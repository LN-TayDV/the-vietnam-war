$b = [System.IO.File]::ReadAllBytes('C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch06\v1_ch06_vi.txt')
if ($b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF) { 'UTF-8 with BOM' }
elseif ($b.Length -ge 2 -and $b[0] -eq 0xFF -and $b[1] -eq 0xFE) { 'UTF-16 LE' }
elseif ($b.Length -ge 2 -and $b[0] -eq 0xFE -and $b[1] -eq 0xFF) { 'UTF-16 BE' }
else { 'UTF-8 no BOM' }
$hasCR = $b -contains 0x0D
$hasLF = $b -contains 0x0A
Write-Host "Has CR: $hasCR"
Write-Host "Has LF: $hasLF"