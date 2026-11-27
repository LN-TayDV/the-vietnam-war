# -*- coding: utf-8 -*-
import io
p = r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project-arendt\04_translation\v2\ch13\v1_ch13_vi.txt'
t = open(p, encoding='utf-8').read()
t = t.replace('hành động accordingly', 'hành động tương ứng')
open(p, 'w', encoding='utf-8', newline='\n').write(t)
out = io.open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\99_scripts\_fix.txt', 'w', encoding='utf-8')
out.write('accordingly: %d\n' % t.count('accordingly'))
out.close()