#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Split main text and footnotes
parts = text.split('--- [Cước chú trang')
main_text = parts[0]
footnotes = '--- [Cước chú trang' + parts[1] if len(parts) > 1 else ''

import re

# 1. VNCH: này -> nầy (as demonstrative pronoun/adjective)
main_text = re.sub(r'\bnày\b', 'nầy', main_text)

# 2. VNCH: giải phóng -> độc lập (except in proper names)
# Keep: 'Mặt trận Giải phóng', 'Mặt trận Dân chủ Giải phóng', 'Mặt trận Giải phóng Dân tộc'
# Replace other occurrences
main_text = re.sub(r'(?<!Mặt trận )(?<!Dân chủ )giải phóng', 'độc lập', main_text)

# 3. VNCH: Annam -> Trung Kỳ (in main text)
main_text = re.sub(r'\bAnnam\b', 'Trung Kỳ', main_text)

# 4. VNCH: cơ sở -> căn cứ (in military context)
main_text = main_text.replace('cơ sở có giới hạn', 'căn cứ có giới hạn')

# 5. Remove English terms with glosses - tribalization
main_text = main_text.replace('tribalization (xây dựng bộ tộc:', 'xây dựng bộ tộc (')
main_text = main_text.replace('tribalization (xây dựng bộ tộc)', 'xây dựng bộ tộc')

# 6. ethnicization
main_text = main_text.replace('ethnicization (dân tộc hóa:', 'dân tộc hóa (')
main_text = main_text.replace('ethnicization (dân tộc hóa)', 'dân tộc hóa')

# 7. territorialization
main_text = main_text.replace('territorialization (lãnh thổ hóa:', 'lãnh thổ hóa (')
main_text = main_text.replace('territorialization (lãnh thổ hóa)', 'lãnh thổ hóa')

# 8. Action psychologique
main_text = main_text.replace('Hành động Tâm lý (Action psychologique)', 'Hành động Tâm lý')
main_text = main_text.replace('action psychologique)', 'Hành động Tâm lý)')
main_text = main_text.replace('Action psychologique', 'Hành động Tâm lý')

# 9. Maquis / maquis
main_text = main_text.replace('Maquis (du kích vùng núi)', 'du kích vùng núi')
main_text = main_text.replace('maquis là', 'du kích vùng núi là')
main_text = main_text.replace('so với Hành động Tâm lý (action psychologique)', 'so với Hành động Tâm lý')
main_text = main_text.replace('sau các maquis', 'sau các du kích vùng núi')
main_text = main_text.replace('các maquis', 'các du kích vùng núi')
main_text = main_text.replace('maquis Hrê', 'du kích Hrê')

# 10. pourissement
main_text = main_text.replace('"thối rữa" [pourissement]', '"thối rữa"')

# 11. colonisation
main_text = main_text.replace('"colonisation à la romaine"', '"chinh điền theo kiểu La Mã"')
main_text = main_text.replace('colonisation', 'chinh điền')

# 12. raison d'être
main_text = main_text.replace("lý do tồn tại (raison d'", "lý do tồn tại")
main_text = main_text.replace("raison d'être", "lý do tồn tại")

# 13. modus vivendi
main_text = main_text.replace('modus vivendi (thỏa thuận sống chung)', 'thỏa thuận sống chung')

# 14. statut particulier
main_text = main_text.replace('statut particulier (trạng thái đặc biệt)', 'trạng thái đặc biệt')

# 15. crown domain
main_text = main_text.replace('"vùng crown domain" (miền đất thuộc hoàng gia)', '"miền đất thuộc hoàng gia"')
main_text = main_text.replace('miền đất crown domain', 'miền đất thuộc hoàng gia')

# 16. Annam Cordillera
main_text = main_text.replace('dãy Trường Sơn (Annam Cordillera)', 'dãy Trường Sơn')

# 17. Other English terms
main_text = main_text.replace('Free French', 'Pháp Tự do')
main_text = main_text.replace('Office of Strategic Services', 'Văn phòng Dịch vụ Chiến lược')

# 18. Fix specific translation issues from progress.json notes
main_text = main_text.replace('khơi mào', 'khơi dậy')
main_text = main_text.replace('giải nhiệm vụ', 'miễn nhiệm')
main_text = main_text.replace('làm nghiên cứu địa phương', 'nghiên cứu thực địa')
main_text = main_text.replace('danh nghĩa sự thật', 'vì lý do sự thật')
main_text = main_text.replace('một người ấy', 'một người')
main_text = main_text.replace('định cư làm người định cư', 'định cư')
main_text = main_text.replace('đa dân tộc hoặc đa dân tộc', 'đa dân tộc')
main_text = main_text.replace('mở rộng cao nguyên vả cho', 'mở rộng thêm cao Nguyên cho')

# 19. Fix 'ca nguegos' -> 'ca ngợi'
main_text = main_text.replace('ca nguegos', 'ca ngợi')

# 20. Fix 'không thể quyền' -> 'không xác quyền'
main_text = main_text.replace('không thể quyền', 'không xác quyền')

# 21. Fix 'phần độc lập Hrê' -> 'phong trào độc lập Hrê'
main_text = main_text.replace('phần độc lập Hrê', 'phong trào độc lập Hrê')

# 22. Fix 'các đồn điển' -> 'các đồn điền'
main_text = main_text.replace('các đồn điển', 'các đồn điền')
main_text = main_text.replace('chủ đồn điển', 'chủ đồn điền')

# 22b. Fix 'cựu chiến binh Thế Hàn' -> 'cựu chiến binh Hàn Quốc'
main_text = main_text.replace('cựu chiến binh Thế Hàn', 'cựu chiến binh Hàn Quốc')

# 23. Fix 'Võ Nguyễn Giáp' -> 'Võ Nguyên Giáp'
main_text = main_text.replace('Võ Nguyễn Giáp', 'Võ Nguyên Giáp')

# 24. Fix 'đường colonial 19' -> 'đường thuộc địa 19 (Route coloniale 19)'
main_text = main_text.replace('đường colonial 19', 'đường thuộc địa 19 (Route coloniale 19)')

# 25. Fix 'Opération Atlante' -> 'Chiến dịch Atlante (Opération Atlante)'
main_text = main_text.replace('Opération Atlante', 'Chiến dịch Atlante (Opération Atlante)')

# 26. Fix 'Battalions Montagnard' -> 'Các đại đội Montagnard'
main_text = main_text.replace('Battalions Montagnard', 'Các đại đội Montagnard')

# 27. Fix 'Pays moï (vùng mỗi)' -> 'Pays moï (vùng Mọi)'
main_text = main_text.replace('Pays moï (vùng mỗi)', 'Pays moï (vùng Mọi)')
main_text = main_text.replace('vùng mỗi', 'vùng Mọi')

# 28. Fix 'cử tri' if any
# 29. Fix 'bản đồ 9.1' -> 'Bản đồ 9.1'
main_text = main_text.replace('bản đồ 9.1', 'Bản đồ 9.1')

# 30. Fix 'đội du kích' vs 'partisans' - keep 'đội du kích' as translation
# Already has '(đội du kích)' gloss

# 31. Fix 'lực lượng Việt địa phương' -> 'lực lượng Việt Nam địa phương' for clarity
# But keep as is since 'Việt' is commonly used as abbreviation

# 32. Fix 'Ri Đê' -> 'Rhadé' (standard spelling) or keep 'Ri Đê' as VNCH
# According to MASTER_LEXICON, Rhadé = Ê-đê. But 'Ri Đê' is also used in VNCH.
# Keep 'Ri Đê' as it's the VNCH form.

# 33. Fix 'Gia Rai' -> 'Gia-rai' or 'Jarai'
# Keep as is for now

# 34. Fix 'cô gái' -> 'cô gái' (fine)

# 35. Fix 'người Mọi' capitalization - keep lowercase as ethnic term

# 36. Fix 'bộ tộc' - keep lowercase as generic term

# 37. Fix 'chính trị' -> 'chánh trị' (check if any)
main_text = main_text.replace('chính trị', 'chánh trị')

# 38. Fix 'chính phủ' -> 'chánh phủ'
main_text = main_text.replace('chính phủ', 'chánh phủ')

# 39. Fix 'đại biểu' -> 'dân biểu'
main_text = main_text.replace('đại biểu', 'dân biểu')

# 40. Fix 'ngược lại' -> 'trái lại'
main_text = main_text.replace('ngược lại', 'trái lại')

# 41. Fix 'hơn nữa' -> 'vả'
main_text = main_text.replace('hơn nữa', 'vả')

# 42. Fix 'tuy nhiên' -> 'tuy vậy'
main_text = main_text.replace('tuy nhiên', 'tuy vậy')

# 43. Fix 'vì vậy' -> 'bởi thế'
main_text = main_text.replace('vì vậy', 'bởi thế')

# 44. Fix 'căn cứ' vs 'cơ sở' - already handled

# 45. Fix 'độc lập' vs 'giải phóng' - already handled

# 46. Fix 'Trung Kỳ' vs 'Annam' - already handled

# 47. Fix 'nầy' vs 'này' - already handled

# 48. Fix 'vả' vs 'vả lại' - check
# 'vả' is correct as conjunction

# 49. Fix 'dầu' vs 'dù' - 'dầu' is correct as conjunction meaning 'although'

# 50. Fix 'trái lại' vs 'ngược lại' - already handled

# 51. Fix 'bởi thế' vs 'vì thế' - 'bởi thế' is correct

# 52. Fix 'tuy vậy' vs 'tuy nhiêu' - 'tuy vậy' is correct

# 53. Fix 'chẳng những... mà còn' - check if used

print('Main text fixes applied')

# Recombine
result = main_text + footnotes

with open(r'C:\Users\PC\Documents\AI_project\the-vietnam-war\translation-project\04_translation\v1\ch09\v1_ch09_vi.txt', 'w', encoding='utf-8', newline='\n') as f:
    f.write(result)

print('File written successfully')