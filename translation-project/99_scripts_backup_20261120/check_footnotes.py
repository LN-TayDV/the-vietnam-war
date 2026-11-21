import subprocess
import os
import glob

for i in range(1, 7):
    filepath = f'translation-project/09_docx/V1-C0{i}_*.docx'
    files = glob.glob(filepath)
    if files:
        filepath = files[0]
        # Use PowerShell COM to check footnotes
        ps_cmd = f'''
$w = New-Object -ComObject Word.Application; $w.Visible=$false
$d = $w.Documents.Open("{filepath}",$false,$true)
"Footnotes: " + $d.Footnotes.Count
"Pages: " + $d.Range($d.Content.End-1,$d.Content.End-1).Information(3)
$d.Close($false); $w.Quit()
'''
        # Write to temp file and run
        with open('C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\check_footnotes.ps1', 'w', encoding='utf-8') as f:
            f.write(ps_cmd)
        
        result = subprocess.run(['powershell', '-File', 'C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\check_footnotes.ps1'], 
                                capture_output=True, text=True, timeout=30)
        print(f'Ch0{i}: {result.stdout.strip()} | File size: {os.path.getsize(filepath)} bytes')
        if result.stderr:
            print(f'  ERR: {result.stderr.strip()}')
    else:
        print(f'Ch0{i}: FILE NOT FOUND')