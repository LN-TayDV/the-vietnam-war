$w = New-Object -ComObject Word.Application
$w.Visible = $false
$f = (Get-ChildItem 'translation-project\09_docx' -Filter 'V1-C06*.docx').FullName
$d = $w.Documents.Open($f, $false, $true)
Write-Host "footnotes=" $d.Footnotes.Count
Write-Host "last-page=" $d.Range($d.Content.End-1, $d.Content.End-1).Information(3)
$d.Close($false)
$w.Quit()