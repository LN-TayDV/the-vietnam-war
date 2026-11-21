---
name: historical-terminology-research
description: Nghiên cứu và chuẩn hóa thuật ngữ lịch sử, chính trị, quân sự, kinh tế, địa lý cho bản dịch The Cambridge History of the Vietnam War. Tra cứu từ điển Nam Bộ, nguồn VNCH sơ cấp, đối chiếu ngữ cảnh lịch sử. Dựa trên MASTER_LEXICON.csv (321+ mục), STYLE_GUIDE_PHAN_B.md, AUDIT_REPORT_CH01-06.md, Bảng Đối Chiếu Tiếng Việt PDF (doi-chieu-tieng-viet.pdf, ~120 cặp từ VNCH-VC).
---

# Skill: Historical Terminology Research — Nghiên Cứu Thuật Ngữ Lịch Sử

## 1. MỤC ĐÍCH
Đảm bảo mọi thuật ngữ lịch sử, chính trị, quân sự, kinh tế, địa lý, ngoại giao trong bản dịch:
- Chính xác về mặt lịch sử và chính trị.
- Tuân thủ văn phong VNCH (pre-1975).
- Nhất quán xuyên suốt 77 chương.
- Có căn cứ nguồn sơ cấp (Lê Văn Đức 1970, Hiến pháp VNCH 1967, Bách Khoa 405, Phan Khôi 1955, Bảng Đối Chiếu Tiếng Việt PDF).

## 2. KHI NÀO KÍCH HOẠT
- **Bắt buộc** tại Grammar Engine Bước 4 (Xác định nghĩa thuật ngữ).
- Khi gặp thuật ngữ chuyên ngành mới (quân sự, ngoại giao, kinh tế, hành chánh).
- Khi audit thuật ngữ (Deep Translation Review, Translation Quality Gate).
- Khi cập nhật `MASTER_LEXICON.csv` và `uncertain_terms.md`.

## 3. NGUYÊN TẮC TRA CỨU (Thứ tự BẮT BUỘC)

### 3.1 Thứ Tự Tra Cứu (Grammar Engine §4.4)
| Thứ tự | Nguồn | Mô tả |
|---|---|---|
| **1** | `MASTER_LEXICON.csv` (321+ mục) | Từ điển Nam Bộ đã kiểm chứng — **Ưu tiên cao nhất** |
| **2** | `VNCH Grammar Database` (Grammar Engine §1.2-1.8) | Từ chức năng: chỉ định, trạng từ, đại từ, thể, từ nối |
| **3** | Nguồn VNCH sơ cấp | Lê Văn Đức 1970 (SRC-001/002), Hiến pháp VNCH 1967 (SRC-023), Bách Khoa 405 (SRC-009) |
| **4** | `03_terminology/SOURCES.md` | 23 nguồn tham chiếu ngôn ngữ miền Nam |
| **5** | `03_terminology/glossary_nam_bac_compare.tsv` | Tra cứu từ Bắc/Nam (KHÔNG tự ý kết luận nếu chưa có nguồn) |
| **6** | **Bảng Đối Chiếu Tiếng Việt PDF** | `books/doi-chieu-tieng-viet.pdf` — ~120 cặp từ VNCH-VC từ T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP |
| **7** | Giữ nguyên thuật ngữ gốc | In nghiêng + giải nghĩa lần đầu + đánh dấu `[CẦN BỔ SUNG LEXICON]` |

### 3.2 Nguyên Tắc Xử Lý (Style Guide Quy tắc 9, 10, 12, 15)
| Quy tắc | Nội dung |
|---|---|
| **Quy tắc 9** | Thuật ngữ không có tương đương → giữ nguyên (in nghiêng) + giải nghĩa lần đầu. KHÔNG tự tạo từ mới. |
| **Quy tắc 10** | Thuật ngữ đa nghĩa → phân tích ngữ cảnh, không tự động đồng nhất. |
| **Quy tắc 12** | KHÔNG hiện đại hóa văn phong (dân biểu → đại biểu, chánh phủ → chính phủ, tài chánh → tài chính). |
| **Quy tắc 15** | Tên gọi thuộc địa Pháp (Annam, Tonkin, Cochinchina, Indochine) → dùng tên VNCH (Trung Kỳ, Bắc Kỳ, Nam Kỳ, Đông Dương) + gốc trong ngoặc lần đầu. Trong trích dẫn tiếng Anh/Pháp → giữ nguyên. |

## 4. CÁC LĨNH VỰC THUẬT NGỮ CHÍNH

### 4.1 Chính Trị - Hành Chánh (Quy tắc 4, 12, 15)
| Thuật ngữ gốc | VNCH Chuẩn | Nguồn | Ghi chú |
|---|---|---|---|
| government | **chánh phủ** | SRC-001, SRC-009, SRC-023, PDF | Hiến pháp 1967 Điều 67 |
| politics/political | **chánh trị** | SRC-001, PDF | Rule 1, 4, 12 |
| party (political) | **chánh đảng** | SRC-023, PDF | |
| coup d'état | **đảo chánh** | SRC-001, PDF | |
| minister | **Tổng trưởng** (VNCH: Bộ trưởng) | SRC-023 | |
| parliament/congress | **Nghị viện** (Hạ/Thượng) | SRC-023 | |
| deputy/representative | **dân biểu** (Hạ) / **nghị sĩ** (Thượng) | SRC-001, SRC-023, PDF | KHÔNG "đại biểu" |
| constitution | **hiến pháp** | SRC-023 | |
| sovereignty | **chủ quyền** | SRC-002 | |
| territory | **lãnh thổ** | SRC-001 | |
| insurance | **an toàn** | PDF | "bảo hiểm (mù) → an toàn (mù)" |
| report | **thưa trình, nói, kể** | PDF | "báo cáo → thưa trình, nói, kể" |
| preservation | **che chở, gìn giữ, bảo vệ** | PDF | "bảo quản → che chở, gìn giữ, bảo vệ" |
| speech | **diễn văn** | PDF | "bài nói → diễn văn" |
| state (US) | **tiêu bang** | PDF | "Bang → Tiêu bang (State)" |
| region (Bắc/Trung/Nam Bộ) | **bắc phần / trung phần / nam phần** | PDF | "Bắc bộ/Trung bộ/Nam bộ → Bắc phần/Trung phần/Nam phần" |

### 4.2 Kinh Tế - Tài Chánh (Quy tắc 3)
| Thuật ngữ gốc | VNCH Chuẩn | Nguồn | Ghi chú |
|---|---|---|---|
| finance/financial | **tài chánh** | SRC-001, ORTHO CH-15, PDF | Rule 3 |
| budget (agency) | **ngân khố** | SRC-001, PDF | Cơ quan |
| budget (plan) | **ngân sách** | SRC-023 | Kế hoạch chi thu |
| pension/retirement | **hưu bổng** | SRC-001, PDF | Rule 3 |
| real estate | **địa ốc** | SRC-001, PDF | Rule 3 |
| central bank | **ngân khố** (cơ quan) | SRC-001 | |
| tax | **thuế vụ** | SRC-001 | |
| currency/money | **hiện kim / giấy bạc** | SRC-002 | |
| union (labor) | **nghiệp đoàn** | PDF | "công đoàn → nghiệp đoàn" |
| industry | **kỹ nghê** | PDF | "công nghiệp → kỹ nghê" |
| project/work | **công tác** | PDF | "công trình → công tác" |
| basic/fundamental | **căn bản** | PDF | "cơ bản → căn bản" |
| mechanical | **cần bản** | PDF | "cơ khí → cần bản" |
| infrastructure/base | **căn bản, nguồn gốc** | PDF | "cơ sở → căn bản, nguồn gốc" |
| port | **phi cảng, hải cảng** | PDF | "cửa khẩu → phi cảng, hải cảng" |
| phrase/group of words | **nhóm chữ** | PDF | "cụm từ → nhóm chữ" |
| rescue | **cứu cấp** | PDF | "cứu hộ → cứu cấp" |
| component/element | **thành phần** | PDF | "diễn → thành phần" |
| determination/decision | **phương định** | PDF | "đấu kiện → phương định" |
| natural/reasonable | **tự nhiên** | PDF | "đạo trí → tự nhiên" |
| output/input | **xuất lượng / nhập lượng** | PDF | "đầu ra / đầu vào → xuất lượng / nhập lượng" |
| banquet/small party | **nấu ăn chung, ăn tập thể / nấu ăn riêng, ăn gia đình** | PDF | "đại tiệc / tiểu tiệc → ..." |
| large scale | **quy mô, cỡ lớn** | PDF | "đại trà → quy mô, cỡ lớn" |
| guarantee/ensure | **bảo đảm** | PDF | "đảm bảo → bảo đảm" |
| register | **ghi danh, ghi tên** | PDF | "đăng ký → ghi danh, ghi tên" |
| answer/solution | **kết quả, trả lời** | PDF | "đáp án → kết quả, trả lời" |
| plain/flatland | **phi đạo** | PDF | "đồng bằng → phi đạo" |
| highway/expressway | **xa lộ** | PDF | "đường cao tốc → xa lộ" |
| processing/machining | **làm ăn công** | PDF | "gia công → làm ăn công" |
| liberate/liberation | **lấy lại, đem đi...** | PDF | "giải phóng → lấy lại, đem đi (VC dùng nhiều)" |
| land liberation | **đứt cho đất bằng** | PDF | "giải phóng mặt bằng → đứt cho đất bằng" |
| simple | **đơn giản** | PDF | "giản đơn → đơn giản" |
| exchange/interact | **giao tiếp, trao đổi** | PDF | "giao lưu → giao tiếp, trao đổi" |
| accounting | **kế toán** | PDF | "hạch toán → kế toán" |
| customs | **quan thuế** | PDF | "hải quan → quan thuế" |
| civil aviation | **hàng không dân sự** | PDF | "hàng không dân dụng → hàng không dân sự" |
| duet (singing) | **song ca** | PDF | "hát đôi → song ca" |
| choir | **hợp ca** | PDF | "hát tập → hợp ca" |
| nuclear (weapon) | **nguyên tử** | PDF | "hát nhân (vũ khí) → nguyên tử" |
| logistics | **tiếp liệu** | PDF | "hậu cần → tiếp liệu" |
| degree/qualification | **bằng cấp** | PDF | "học vị → bằng cấp" |
| consequence/result | **hậu quả** | PDF | "hệ quả → hậu quả" |
| modern | **tối tân** | PDF | "hiện đại → tối tân" |
| household/family | **gia đình** | PDF | "hộ nhà → gia đình" |
| passport | **sổ thông hành** | PDF | "hộ chiếu → sổ thông hành" |
| meeting/assembly | **phân khu** | PDF | "họp hội → phân khu" |
| household register | **tổ khai gia đình** | PDF | "họ khẩu → tổ khai gia đình" |
| Red Cross | **hội Hồng Thập Tự** | PDF | "hội chữ thập đỏ → hội Hồng Thập Tự" |
| foreign currency | **ngoại tệ** | PDF | "kiều hời → ngoại tệ" |
| outstanding/excellent | **giải, xuất sắc** | PDF | "kiệt xuất → giải, xuất sắc" |
| experience/go through | **trải qua** | PDF | "kinh qua → trải qua" |
| prostitute | **làm điếm** | PDF | "làm gái → làm điếm" |
| work/investigate | **thẩm vấn, điều tra** | PDF | "làm việc → thẩm vấn, điều tra" |
| safe house/villa | **ngụy Giác Đốc / Tòa Bạch ốc** | PDF | "lâu năm góc / Nhà tráng → ..." |
| festival/celebration | **đại hội, ăn mừng** | PDF | "liên hoan → đại hội, ăn mừng" |
| contact | **liên lạc** | PDF | "liên hệ → liên lạc (contact)" |
| miscellaneous | **vỏ vần** | PDF | "linh tinh → vỏ vần" |
| female soldier | **nữ quân nhân** | PDF | "lính gái → nữ quân nhân" |
| naval infantry | **thủy quân lực lượng chiến** | PDF | "lính thủy đánh bộ → thủy quân lực lượng chiến" |
| profit | **lợi tức** | PDF | "lợi nhuận → lợi tức" |
| shrimp paste | **tôm lực** | PDF | "lực tôm → tôm lực" |
| explain | **giải thích** | PDF | "lý giải → giải thích (explain)" |
| helicopter | **trực thăng** | PDF | "máy bay lên thẳng → trực thăng" |
| dance | **khiêu vũ** | PDF | "múa đòi → khiêu vũ" |
| USA | **Mỹ** | PDF | "Mĩ — Mĩ (Hoa kỳ - USA) → Mỹ" |
| supine | **nằm ngửa** | PDF | "nằm bật → nằm ngửa" |
| upgrade | **nâng, hoặc đưa giá trị lên** | PDF | "nâng cấp → nâng, hoặc đưa giá trị lên" |
| energetic/active | **siêng năng, tháo vát** | PDF | "năng nổ → siêng năng, tháo vát" |
| artisan/craftsman | **thờ, nghệ sỹ** | PDF | "nghệ nhân → thờ, nghệ sỹ" |
| stage name | **Tên (nghệ sỹ - stage name) dùng ngoài tên thật** | PDF | "nghệ danh → Tên nghệ sỹ" |
| military service | **Đi quân dịch** | PDF | "nghĩa vụ quân sự → Đi quân dịch" |
| serious | **nghiêm chính** | PDF | "nghiêm túc → nghiêm chính" |
| side job | **Đi làm thêm (2nd job / nghề phụ, nghề tay trái)** | PDF | "nghiệp dư → Đi làm thêm" |
| hotel | **khách sạn** | PDF | "nhà khách → khách sạn" |
| consensus | **đồng lòng, đồng ý** | PDF | "nhất trí → đồng lòng, đồng ý" |
| consistent | **luôn luôn, trước sau như một** | PDF | "nhất quán → luôn luôn, trước sau như một" |
| foreigner/overseas Vietnamese | **ngoại kiều** | PDF | "người nước ngoài → ngoại kiều" |
| nostalgia/sentiment | **viễn suy tư** | PDF | "noi niệm (tính từ!) → viễn suy tư" |
| solid fertilizer | **cường liệu** | PDF | "phân cứng → cường liệu" |
| soft fertilizer | **nhu liệu** | PDF | "phân mềm → nhu liệu" |
| reflect | **phản ảnh** | PDF | "phản ánh → phản ảnh" |
| feedback/response | **trả lời, hồi âm** | PDF | "phản hồi → trả lời, hồi âm" |
| broadcast | **phát thanh** | PDF | "phát sóng → phát thanh" |
| PhD/associate prof | **cao học** | PDF | "phó tiến sĩ → cao học" |
| airport/airfield | **phi trường, phi cảng** | PDF | "phi khẩu → phi trường, phi cảng" |
| business deal | **một vụ trao đổi thường mại** | PDF | "phi vụ → một vụ trao đổi thường mại (a business deal - thương vụ)" |
| rehabilitation | **hoàn lượng** | PDF | "phục hồi nhân phẩm → hoàn lượng" |
| plan/proposal | **kế hoạch** | PDF | "phương án → kế hoạch" |
| too lucky/excessive | **quá sướng, quá mức** | PDF | "quá tài → quá sướng, quá mức" |
| understand clearly | **hiểu rõ** | PDF | "quan triết → hiểu rõ" |
| military administration | **quân trị** | PDF | "quân lý → quân trị" |
| public square | **công trường** | PDF | "quảng trường → công trường" |
| military rank | **cấp bậc** | PDF | "quân hàm → cấp bậc" |
| planning | **kế hoạch** | PDF | "quy hoạch → kế hoạch" |
| process/procedure | **tiến trình** | PDF | "quy trình → tiến trình" |
| shock | **kinh hoàng, kinh ngạc, ngạc nhiên** | PDF | "sốc (shocked) → kinh hoàng, kinh ngạc, ngạc nhiên" |
| new/recent | **tân cương** | PDF | "sổ tân → tân cương" |
| division (military) | **sư đoàn** | PDF | "sư - sư đoàn → sư đoàn" |
| public health | **y tế công cộng** | PDF | "sức khỏe công dân → y tế công cộng" |
| incident/accident | **trở ngại** | PDF | "sự cố → trở ngại" |
| regiment/enterprise | **công ty** | PDF | "tạp đoàn / doanh nghiệp → công ty" |
| pseudonym/pen name | **hòa tiến** | PDF | "tên lứa → hòa tiến" |
| traffic participation | **lưu hành** | PDF | "tham gia lưu thông (xe cộ) → lưu hành" |
| visit/inspect | **thẩm viếng** | PDF | "tham quan → thẩm viếng" |
| settle/liquidate | **thanh toán, chứng minh** | PDF | "thanh lý → thanh toán, chứng minh" |
| ecstasy/rapture | **thần mê** | PDF | "thần thượng → thần mê" |
| construct/build | **làm** | PDF | "thi công → làm" |
| test site/field | **thí trường** | PDF | "thí phần → thí trường" |
| income | **lợi tức** | PDF | "thu nhập → lợi tức" |
| relax | **tĩnh táo, giải trí** | PDF | "thư giãn → tĩnh táo, giải trí" |
| persuasive (adj) | **có lý (makes sense), hợp lý - tin được** | PDF | "thuyết phục (tính) → có lý, hợp lý, tin được" |
| outstanding | **xuất sắc** | PDF | "tiến tiến → xuất sắc" |
| attack | **tấn công** | PDF | "tiến công → tấn công" |
| receive/accept | **tiếp nhận, thâu nhận, lãnh hội** | PDF | "tiếp thu → tiếp nhận, thâu nhận, lãnh hội" |
| consume | **tiêu thụ** | PDF | "tiêu dùng → tiêu thụ" |
| flight crew | **phi hành đoàn** | PDF | "tổ lái → phi hành đoàn" |
| airdrop | **truyền đơn** | PDF | "tổ rơi → truyền đơn" |
| strive | **cố gắng** | PDF | "tranh thủ → cố gắng" |
| intellect/knowledge | **kiến thức** | PDF | "trí tuệ → kiến thức" |
| deploy/expand | **khai triển** | PDF | "triển khai → khai triển" |
| thought/thinking | **suy nghĩ** | PDF | "tư duy → suy nghĩ" |
| document/material | **tài liệu** | PDF | "tư liệu → tài liệu" |
| word | **tiếng, chữ** | PDF | "từ → tiếng, chữ" |
| distort | **tắt nghiêng** | PDF | "uốn tạc → tắt nghiêng" |
| literature | **văn đề** | PDF | "văn dân → văn đề" |
| cultural troupe | **lực sĩ** | PDF | "văn động viên → lực sĩ" |
| cancer institute | **viện ung thư** | PDF | "viện ung bướu → viện ung thư" |
| spontaneous | **tự nhiên** | PDF | "vô tư → tự nhiên" |
| accurate/precise | **chính xác** | PDF | "xác tín → chính xác" |
| car/sedan | **xe du lịch** | PDF | "xe con → xe du lịch" |
| bus/truck | **xe đồ** | PDF | "xe khách → xe đồ" |
| handle/process | **giải quyết, thi hành** | PDF | "xử lý → giải quyết, thi hành" |

### 4.3 Quân Sự - Chiến Tranh
| Thuật ngữ gốc | VNCH Chuẩn | Nguồn | Ghi chú |
|---|---|---|---|
| liberation / liberate | **độc lập** / **kháng cự** | SRC-001, SRC-023, PDF | Rule 8, 15 — KHÔNG "giải phóng" |
| liberation army | **Quân Giải phóng** (tên riêng) / **Quân kháng cự** | | Tên riêng giữ "Giải Phóng" có ghi chú |
| comrade | **đồng đạo** | SRC-001, SRC-023, PDF | Rule 8 — Tên tổ chức giữ "Đồng Chí" |
| revolutionary | **cách mạng** | | |
| coup | **đảo chánh** | SRC-001, PDF | |
| colonial | **thực dân** | SRC-001 | Rule 6 |
| colony | **thuộc địa** | SRC-001 | Rule 6 |

### 4.4 Địa Lý - Hành Chánh (Quy tắc 5, 15)
| Thuật ngữ gốc | VNCH Chuẩn | Nguồn | Ghi chú |
|---|---|---|---|
| Annam | **Trung Kỳ (Annam)** | SRC-001, PDF | Rule 15 |
| Tonkin | **Bắc Kỳ (Tonkin)** | SRC-001, PDF | Rule 15 |
| Cochinchina/Cochinchine | **Nam Kỳ (Cochinchina)** | SRC-001, PDF | Rule 15 |
| Indochine/Indochina | **Đông Dương (Indochine)** | SRC-001, PDF | Rule 15 |
| province | **tỉnh** | SRC-023 | Rule 5 |
| district | **quận** (VNCH: cấp dưới tỉnh) | SRC-023 | Rule 5 |
| canton/commune | **tổng** | SRC-023 | Rule 5 |
| village/hamlet | **xã / ấp / làng** | SRC-023 | Rule 5 |
| capital | **thủ đô** | SRC-023 | |

### 4.5 Ngoại Giao - Pháp Lý
| Thuật ngữ gốc | VNCH Chuẩn | Nguồn |
|---|---|---|
| diplomacy | **ngoại giao** | SRC-002 |
| treaty | **hiệp định / hòa ước** | SRC-001 |
| protectorate | **bảo hộ** (thuộc địa) | SRC-001 | Phân biệt với *bảo hộ mậu dịch* |
| diplomatic relations | **bang giao** | SRC-001 |
| agreement | **hiệp định sơ bộ / bản ghi chép** | SRC-001 |

## 5. XỬ LÝ TRƯỜNG HỢP ĐẶC BIỆT

### 5.1 Tên Riêng & Tên Tổ Chức (Quy tắc 15)
- **Việt Nam Thanh Niên Cách Mạng Đồng Chí Hội** → Giữ nguyên "Đồng Chí" (tên riêng).
- **Cờ Giải Phóng, Quân Giải Phóng, Mặt Trận Giải Phóng** → Giữ nguyên "Giải Phóng" (tên riêng), thêm ghi chú `[ND: tên riêng, VNCH dùng "độc lập/kháng cự"]`.
- **Trường Chinh, Hồ Chí Minh, Lê Duẩn** → Giữ nguyên tên riêng.

### 5.2 Trích Dẫn Tiếng Anh/Pháp (Quy tắc 11, 15)
- Trong cước chú, tên sách, tên báo, tên tổ chức pháp lý tiếng Anh/Pháp → **Giữ nguyên hoàn toàn**.
- Ví dụ: "Indochine", "Annam", "Tonkin" trong trích dẫn → không đổi.

### 5.3 Thuật ngữ Không Có Tương Đương (Quy tắc 9)
| Thuật ngữ | Xử lý |
|---|---|
| *domino theory* | *thuyết domino* (in nghiêng) + giải nghĩa lần đầu: "[ND: thuyết rằng sự sụp đổ của một quốc gia cộng sản sẽ kéo theo các quốc gia lân cận]" |
| *strategic hamlet* | *ấp chiến lược* (in nghiêng lần đầu) + giải nghĩa |
| *search and destroy* | *tìm kiếm và tiêu diệt* (dịch nghĩa, không in nghiêng) |

### 5.4 Thuật ngữ Đa Nghĩa (Quy tắc 10)
| Thuật ngữ | Nghĩa 1 | Nghĩa 2 | Cách phân biệt |
|---|---|---|---|
| *bảo hộ* | Protectorate (thuộc địa) | Protectionism (bảo hộ mậu dịch) | Xem ngữ cảnh: chính trị → protectorate; kinh tế → protectionism |
| *đại biểu* | Delegate (hiện nay) | Dân biểu (VNCH) | Rule 12: VNCH dùng "dân biểu" |

## 6. CẬP NHẬT MASTER_LEXICON.CSV

### 6.1 Khi Thêm Mục Mới
| Cột | Nội dung | Ví dụ |
|---|---|---|
| tu_chuan | Thuật ngữ chuẩn VNCH | chánh phủ |
| loai_tu | Loại từ (danh_tu, động_tu, tính_tu, liên_tu, phó_tu, đại_tu, cụm_tu, định_lượng) | danh_tu |
| nghia | Định nghĩa ngắn gọn | Cơ quan cao hơn hết trong một nước... |
| cach_dung | Cách dùng trong ngữ cảnh VNCH | Dùng trong văn bản chính trị, hành chính |
| vi_du_nguyen_ban | Ví dụ từ nguồn gốc | "Chánh phủ Việt Nam Cộng Hòa" (Hiến pháp 1967) |
| nguon | Mã nguồn (SRC-001, SRC-002, SRC-009, SRC-021, SRC-023, PDF) | SRC-023 |
| trang | Trang trong nguồn (nếu có) | Điều 67 |
| thoi_ky | Thời kỳ lịch sử | viet_nam_cong_hoa |
| muc_xac_minh | Mức độ xác minh (VERIFIED, CROSS_VERIFIED, PARTIALLY_VERIFIED, UNVERIFIED) | VERIFIED |
| linh_vuc | Lĩnh vực (chinh_tri, kinh_te, quan_su, dia_ly, ngoai_giao, van_hoa_hoc_thuat, chinh_ta, van_dung, hoc_thuat, nong_nghiep, bao_chi, tai_chinh, luat_phap) | chinh_tri |
| ghi_chu | Ghi chú bổ sung | Hiến pháp 1967 Điều 67 |
| muc_loi_vuc | Mức lỗi vực (nếu có) |  |
| muc_phu | Mục phụ (nếu có) |  |
| thoi_ky_lich_su | Thời kỳ lịch sử chi tiết | 1955-1975 |
| phan_loai_khu_vuc | Phân loại khu vực (nam_bo, bac_bo, trung_bo, chung) | nam_bo |
| van_phong | Văn phong (trang_nghiem, van_dung, hoc_thuat, bao_chi) | trang_nghiem |

### 6.2 Các Mục Cần Bổ Sung Từ PDF (120+ cặp từ VNCH-VC)
Cần thêm vào MASTER_LEXICON.csv các thuật ngữ từ `books/doi-chieu-tieng-viet.pdf` (T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP) bao gồm:
- Chính trị: chánh trị, chánh phủ, chánh đảng, đảo chánh, dân biểu, nghị sĩ, an toàn, thưa trình/nói/kể, diễn văn, tiêu bang, bắc phần/trung phần/nam phần
- Kinh tế: tài chánh, ngân khố, hưu bổng, địa ốc, nghiệp đoàn, kỹ nghê, công tác, căn bản, cần bản, phi cảng/hải cảng, nhóm chữ, cứu cấp, thành phần, phương định, tự nhiên, xuất lượng/nhập lượng, nấu ăn chung/ăn tập thể/nấu ăn riêng/ăn gia đình, quy mô/cỡ lớn, bảo đảm, ghi danh/ghi tên, kết quả/trả lời, phi đạo, xa lộ, làm ăn công, lấy lại/đem đi, đứt cho đất bằng, đơn giản, giao tiếp/trao đổi, kế toán, quan thuế, hàng không dân sự, song ca, hợp ca, nguyên tử, tiếp liệu, bằng cấp, hậu quả, tối tân, gia đình, sổ thông hành, phân khu, tổ khai gia đình, hội Hồng Thập Tự, ngoại tệ, giải/xuất sắc, trải qua, làm điếm, thẩm vấn/điều tra, ngụy Giác Đốc/Tòa Bạch ốc, đại hội/ăn mừng, liên lạc, vỏ vần, nữ quân nhân, thủy quân lực lượng chiến, lợi tức, tôm lực, giải thích, trực thăng, khiêu vũ, Mỹ, nằm ngửa, nâng/đưa giá trị lên, siêng năng/tháo vát, thờ/nghệ sỹ, tên nghệ sỹ, Đi quân dịch, nghiêm chính, Đi làm thêm, khách sạn, đồng lòng/đồng ý, luôn luôn/trước sau như một, ngoại kiều, viễn suy tư, cường liệu, nhu liệu, phản ảnh, trả lời/hồi âm, phát thanh, cao học, phi trường/phi cảng, một vụ trao đổi thường mại, hoàn lượng, kế hoạch, quá sướng/quá mức, hiểu rõ, quân trị, công trường, cấp bậc, kế hoạch, tiến trình, kinh hoàng/kinh ngạc/ngạc nhiên, tân cương, sư đoàn, y tế công cộng, trở ngại, công ty, hòa tiến, lưu hành, thẩm viếng, thanh toán/chứng minh, thần mê, làm, thí trường, lợi tức, tĩnh táo/giải trí, có lý/hợp lý/tin được, xuất sắc, tấn công, tiếp nhận/thâu nhận/lãnh hội, tiêu thụ, phi hành đoàn, truyền đơn, cố gắng, kiến thức, khai triển, suy nghĩ, tài liệu, tiếng/chữ, tắt nghiêng, văn đề, lực sĩ, viện ung thư, tự nhiên, chính xác, xe du lịch, xe đồ, giải quyết/thi hành

## 7. QUY TRÌNH KHI GẶP THUẬT NGỮ KHÓ (Quy tắc 20)

1. **Mở rộng ngữ cảnh** → đọc đoạn trước/sau, heading, chương liên quan.
2. **Xác định ý đồ tác giả** → lập luận gì, sắc thái gì.
3. **Tra cứu theo thứ tự** → Lexicon → VNCH Grammar → Nguồn VNCH → SOURCES.md → **Bảng Đối Chiếu PDF**.
4. **Đối chiếu chỗ khác** → từ này xuất hiện ở đâu nữa trong sách.
5. **Tái dựng & diễn đạt** → kết hợp nghĩa nguyên văn + ngữ cảnh + văn phong VNCH.
6. **Ghi nhận căn cứ** → căn cứ văn bản, ngữ cảnh, nguồn, lập luận, mức độ chắc chắn.

## 8. LIÊN KẾT SKILLS
- **historical-book-translation**: Bước 3.4.
- **contextual-translation**: Phân tích ngữ cảnh thuật ngữ.
- **southern-vietnamese-editorial-style**: Dùng thuật ngữ VNCH chuẩn.
- **deep-translation-review**: Kiểm tra thuật ngữ khi audit.
- **translation-error-detection**: Phát hiện sai thuật ngữ.
- **translation-quality-gate**: Orthography check.

---

*Cập nhật: 2026-11-20 — Dựa trên MASTER_LEXICON.csv (321+ mục), STYLE_GUIDE_PHAN_B.md v2.3, Grammar Engine v2.1, Audit 6 chương, Bảng Đối Chiếu Tiếng Việt (PDF: doi-chieu-tieng-viet.pdf, T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP, ~120 cặp từ VNCH-VC).*