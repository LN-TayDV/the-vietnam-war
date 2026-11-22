$keep = @(
    "chapter_workflow.py",
    "build_chapter_docx.py", 
    "extract_images.py",
    "audit_docx_format.py",
    "build_volume_docx.py",
    "build_lexicon.py",
    "extract_chapters.py",
    "test_regression.py",
    "verify_final.py"
)

$dir = "C:\Users\PC\Documents\AI_project\the-vietnam-war\99_scripts"
$files = Get-ChildItem $dir -Filter "*.py" -Name

foreach ($f in $files) {
    if ($keep -notcontains $f) {
        Remove-Item (Join-Path $dir $f) -Force
        Write-Host "Deleted: $f"
    } else {
        Write-Host "Kept: $f"
    }
}