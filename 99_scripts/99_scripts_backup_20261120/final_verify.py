import subprocess
import os
import glob

base = r'C:\Users\PC\Documents\AI_project\the-vietnam-war'

print('=== FINAL WORD COM VERIFICATION ===')
for i in range(1, 7):
    filepath = os.path.join(base, f'translation-project/09_docx/V1-C0{i}_*.docx')
    files = glob.glob(filepath)
    if files:
        abs_path = os.path.abspath(files[0])
        
        ps_cmd = f'''
$w = New-Object -ComObject Word.Application; $w.Visible=$false
$d = $w.Documents.Open("{abs_path}",$false,$true)
"Footnotes: " + $d.Footnotes.Count
"Pages: " + $d.Range($d.Content.End-1,$d.Content.End-1).Information(3)
$d.Close($false); $w.Quit()
'''
        with open('C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\check_final.ps1', 'w', encoding='utf-8') as f:
            f.write(ps_cmd)
        
        result = subprocess.run(['powershell', '-File', 'C:\\Users\\PC\\AppData\\Local\\Temp\\kilo\\check_final.ps1'], 
                                capture_output=True, text=True, timeout=30)
        print(f'Ch0{i}: {result.stdout.strip()}')
        if result.stderr and 'Sorry' not in result.stderr:
            print(f'  ERR: {result.stderr.strip()}')