---
name: southern-vietnamese-editorial-style
description: Chuẩn hóa văn phong và ngữ pháp tiếng Việt miền Nam theo truyền thống Việt Nam Cộng hòa (VNCH pre-1975). Bao gồm: từ vựng, chính tả, cú pháp, danh từ chỉ định, trạng từ, thể khía, đại từ nhân xưng, từ nối logic, chủ động hóa. Dựa trên 29 quy tắc trong STYLE_GUIDE_PHAN_B.md v2.3 và Bảng đối chiếu từ ngữ VNCH-VC từ "Đối Chiếu Tiếng Việt" (T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP).
---

# Skill: Southern Vietnamese Editorial Style — Văn Phong Biên Tập Miền Nam VNCH

## 1. MỤC ĐÍCH
Đảm bảo toàn bộ bản dịch tuân thủ **tiếng Việt miền Nam theo chuẩn VNCH trước 1975** xuyên suốt 77 chương. Đây là yêu cầu cốt lõi của dự án.

## 2. KHI NÀO KÍCH HOẠT
- **Bắt buộc** khi dịch mỗi câu (Grammar Engine Bước 5).
- Khi chạy `apply_vnch_fixes.py` / `vnch_orthography.py` sau khi dịch xong chương.
- Khi review/audit văn phong (Deep Translation Review, Translation Quality Gate).

## 3. NGUYÊN TẮC CỐT LÕI (Style Guide Phần B v2.3)

> **Bản dịch dùng tiếng Việt miền Nam theo truyền thống ngôn ngữ, văn chương, báo chí và học thuật của Việt Nam Cộng hòa trước năm 1975.**

### 3.1 5 Lớp Xác Minh (Phase 0)
1. **Xác minh nguồn** — nguồn tồn tại, đúng thư mục.
2. **Xác minh nội dung** — định nghĩa/cách dùng có trong nguồn.
3. **Xác minh ngữ cảnh** — cách dùng đúng ngữ cảnh.
4. **Xác minh mức độ phổ biến** — KHÔNG tự động suy ra từ 1 nguồn.
5. **Xác minh sắc thái vùng miền/thời kỳ** — phải có bằng chứng riêng.

## 4. HỆ THỐNG TỪ VỰNG VNCH (29 Quy Tắc — STYLE_GUIDE_PHAN_B v2.3 + Bảng Đối Chiếu Tiếng Việt PDF)

### 4.1 Thuật ngữ Cốt Lõi (Quy tắc 1-6, 12, 15) — CRITICAL

| Miền Bắc / Hiện nay | Miền Nam VNCH (Chuẩn) | Quy tắc | Nguồn |
|---|---|---|---|
| **chính trị** | **chánh trị** | 1, 4, 12 | SRC-001, PDF |
| **chính phủ** | **chánh phủ** | 1, 4, 12 | SRC-001, SRC-009, SRC-023, PDF |
| **chính đảng** | **chánh đảng** | 4 | SRC-023, PDF |
| **đảo chính** | **đảo chánh** | 1 | SRC-001, PDF |
| **tài chính** | **tài chánh** | 3 | SRC-001, ORTHO CH-15, PDF |
| **đại biểu** | **dân biểu** | 4 | SRC-001, SRC-023, PDF |
| **nghị sĩ** | **nghị sĩ** (VNCH: Thượng nghị viện) | 4 | SRC-001, SRC-023 |
| **lương hưu** | **hưu bổng** | 3 | SRC-001, PDF |
| **bất động sản** | **địa ốc** | 3 | SRC-001, PDF |
| **ngân sách (cơ quan)** | **ngân khố** | 3 | SRC-001, PDF |
| **ngân sách (kế hoạch)** | **ngân sách** | 3 | SRC-023 |
| **giải phóng** | **độc lập** / **kháng cự** | 8, 15 | SRC-001, SRC-023, PDF |
| **đồng chí** | **đồng đạo** | 8 | SRC-001, SRC-023, PDF |
| **Annam** | **Trung Kỳ (Annam)** | 15 | SRC-001, PDF |
| **Tonkin** | **Bắc Kỳ (Tonkin)** | 15 | SRC-001, PDF |
| **Cochinchina/Cochinchine** | **Nam Kỳ (Cochinchina)** | 15 | SRC-001, PDF |
| **Indochine** | **Đông Dương (Indochine)** | 15 | SRC-001, PDF |
| **bảo hiểm** | **an toàn** | PDF | PDF: "bảo hiểm (mù) → an toàn (mù)" |
| **báo cáo** | **thưa trình, nói, kể** | PDF | PDF: "báo cáo → thưa trình, nói, kể" |
| **bảo quản** | **che chở, gìn giữ, bảo vệ** | PDF | PDF |
| **bài nói** | **diễn văn** | PDF | PDF |
| **bản đồ** | **tức cẩu** (thuộc địa) | PDF | PDF |
| **bác sĩ / ca sĩ** | **bác sĩ / ca sĩ** (giữ nguyên) | PDF | PDF: "bác sĩ / ca sĩ → bác sĩ / ca sĩ" |
| **bang** | **tiêu bang (State)** | PDF | PDF |
| **bắc bộ / trung bộ / nam bộ** | **bắc phần / trung phần / nam phần** | PDF | PDF |
| **bảo tàng** | **bảo tàng** (giữ nguyên) | PDF | - |
| **biểu tượng** | **ký hiệu, tượng trưng** | PDF | PDF |
| **bồi thường** | **bồi thường** | PDF | - |
| **bổ sung** | **thêm, bổ túc** | PDF | PDF |
| **bồi đường** | **nghề ngờ, tạm bợ, sẵn sàng, chăm nom, ăn uống đầy đủ** | PDF | PDF |
| **bóng đá** | **túc cầu** | PDF | PDF |
| **bực xúc** | **doãn nén, bức tác** | PDF | PDF |
| **bất ngờ** | **ngạc nhiên (surprised)** | PDF | PDF |
| **bổ túc** | **thêm** | PDF | PDF |
| **cách ly** | **cô lập** | PDF | PDF |
| **cảnh báo** | **báo động, phải chú ý** | PDF | PDF |
| **cái A-lô** | **cái điện thoại (telephone receiver)** | PDF | PDF |
| **cái đai** | **cái đeo tay (watch strap)** | PDF | PDF |
| **căng (làm)** | **căng thẳng (intense)** | PDF | PDF |
| **cầu lông** | **vũ cầu** | PDF | PDF |
| **chất lượng** | **phẩm chất tốt (chỉ cấp phẩm "quality", không cấp lượng "quantity")** | PDF | PDF |
| **chất xám** | **trí tuệ, sự thông minh** | PDF | PDF |
| **chế độ** | **quy chế** | PDF | PDF |
| **chỉ đạo** | **chỉ thị, ra lệnh** | PDF | PDF |
| **chỉ tiêu** | **định suất** | PDF | PDF |
| **chúng nhiêm** | **trường ban, khoa trưởng** | PDF | PDF |
| **chú trễ** | **chú tôa** | PDF | PDF |
| **chửa cháy** | **cầu hỏa** | PDF | PDF |
| **chiếu đãi** | **thất đãi** | PDF | PDF |
| **chui** | **lén lút** | PDF | PDF |
| **chuyện chèo** | **nói lên, nêu ra** | PDF | PDF |
| **chuyện ngữ** | **dịch** | PDF | PDF |
| **chứng minh nhân dân** | **thẻ căn cước** | PDF | PDF |
| **chữ đạo** | **chính** | PDF | PDF |
| **co cụm** | **thu hẹp** | PDF | PDF |
| **công đoàn** | **nghiệp đoàn** | PDF | PDF |
| **công nghiệp** | **kỹ nghê** | PDF | PDF |
| **công trình** | **công tác** | PDF | PDF |
| **cơ bản** | **căn bản** | PDF | PDF |
| **cơ khí** | **cần bản** | PDF | PDF |
| **cơ sở** | **căn bản, nguồn gốc** | PDF | PDF |
| **cửa khẩu** | **phi cảng, hải cảng** | PDF | PDF |
| **cụm từ** | **nhóm chữ** | PDF | PDF |
| **cứu hộ** | **cứu cấp** | PDF | PDF |
| **diễn** | **thành phần** | PDF | PDF |
| **đấu kiện** | **phương định** | PDF | PDF |
| **đại học mái** | **???** | PDF | PDF |
| **đạo trí** | **tự nhiên** | PDF | PDF |
| **đầu ra / đầu vào** | **xuất lượng / nhập lượng** | PDF | PDF |
| **đại tiệc / tiểu tiệc** | **nấu ăn chung, ăn tập thể / nấu ăn riêng, ăn gia đình** | PDF | PDF |
| **đại trà** | **quy mô, cỡ lớn** | PDF | PDF |
| **đảm bảo** | **bảo đảm** | PDF | PDF |
| **đăng ký** | **ghi danh, ghi tên** | PDF | PDF |
| **đáp án** | **kết quả, trả lời** | PDF | PDF |
| **đăng kí** | **ghi danh** | PDF | PDF |
| **đồng bằng** | **phi đạo** | PDF | PDF |
| **đường cao tốc** | **xa lộ** | PDF | PDF |
| **gia công** | **làm ăn công** | PDF | PDF |
| **giải phóng** | **lấy lại, đem đi... (riêng chữ này bị VC dùng rất nhiều)** | PDF | PDF |
| **giải phóng mặt bằng** | **đứt cho đất bằng** | PDF | PDF |
| **giản đơn** | **đơn giản** | PDF | PDF |
| **giao lưu** | **giao tiếp, trao đổi** | PDF | PDF |
| **hạch toán** | **kế toán** | PDF | PDF |
| **hải quan** | **quan thuế** | PDF | PDF |
| **hàng không dân dụng** | **hàng không dân sự** | PDF | PDF |
| **hát đôi** | **song ca** | PDF | PDF |
| **hát tập** | **hợp ca** | PDF | PDF |
| **hát nhân (vũ khí)** | **nguyên tử** | PDF | PDF |
| **hậu cần** | **tiếp liệu** | PDF | PDF |
| **học vị** | **bằng cấp** | PDF | PDF |
| **hệ quả** | **hậu quả** | PDF | PDF |
| **hiện đại** | **tối tân** | PDF | PDF |
| **hộ nhà** | **gia đình** | PDF | PDF |
| **hộ chiếu** | **sổ thông hành** | PDF | PDF |
| **họp hội** | **phân khu** | PDF | PDF |
| **họ khẩu** | **tổ khai gia đình** | PDF | PDF |
| **hội chữ thập đỏ** | **hội Hồng Thập Tự** | PDF | PDF |
| **kiều hời** | **ngoại tệ** | PDF | PDF |
| **kiệt xuất** | **giải, xuất sắc** | PDF | PDF |
| **kinh qua** | **trải qua** | PDF | PDF |
| **làm gái** | **làm điếm** | PDF | PDF |
| **làm việc** | **thẩm vấn, điều tra** | PDF | PDF |
| **lâu năm góc / nhà tráng** | **ngụy Giác Đốc / Tòa Bạch ốc** | PDF | PDF |
| **liên hoan** | **đại hội, ăn mừng** | PDF | PDF |
| **liên hệ** | **liên lạc (contact)** | PDF | PDF |
| **linh tinh** | **vỏ vần** | PDF | PDF |
| **lính gái** | **nữ quân nhân** | PDF | PDF |
| **lính thủy đánh bộ** | **thủy quân lực lượng chiến** | PDF | PDF |
| **lợi nhuận** | **lợi tức** | PDF | PDF |
| **lực tôm** | **tôm lực** | PDF | PDF |
| **lý giải** | **giải thích (explain)** | PDF | PDF |
| **máy bay lên thẳng** | **trực thăng** | PDF | PDF |
| **múa đòi** | **khiêu vũ** | PDF | PDF |
| **mĩ — Mĩ (Hoa kỳ - USA)** | **Mỹ** | PDF | PDF |
| **nằm bật** | **nằm ngửa** | PDF | PDF |
| **nâng cấp** | **nâng, hoặc đưa giá trị lên** | PDF | PDF |
| **năng nổ** | **siêng năng, tháo vát** | PDF | PDF |
| **nghệ nhân** | **thờ, nghệ sỹ** | PDF | PDF |
| **nghệ danh** | **Tên (nghệ sỹ - stage name) dùng ngoài tên thật** | PDF | PDF |
| **nghĩa vụ quân sự** | **Đi quân dịch** | PDF | PDF |
| **nghiêm túc** | **nghiêm chính** | PDF | PDF |
| **nghiệp dư** | **Đi làm thêm (2nd job / nghề phụ, nghề tay trái)** | PDF | PDF |
| **nhà khách** | **khách sạn** | PDF | PDF |
| **nhất trí** | **đồng lòng, đồng ý** | PDF | PDF |
| **nhất quán** | **luôn luôn, trước sau như một** | PDF | PDF |
| **người nước ngoài** | **ngoại kiều** | PDF | PDF |
| **noi niệm (tính từ!)** | **viễn suy tư** | PDF | PDF |
| **phân cứng** | **cường liệu** | PDF | PDF |
| **phân mềm** | **nhu liệu** | PDF | PDF |
| **phản ánh** | **phản ảnh** | PDF | PDF |
| **phản hồi** | **trả lời, hồi âm** | PDF | PDF |
| **phát sóng** | **phát thanh** | PDF | PDF |
| **phó tiến sĩ** | **cao học** | PDF | PDF |
| **phi khẩu** | **phi trường, phi cảng** | PDF | PDF |
| **phi vụ** | **một vụ trao đổi thường mại (a business deal - thương vụ)** | PDF | PDF |
| **phục hồi nhân phẩm** | **hoàn lượng** | PDF | PDF |
| **phương án** | **kế hoạch** | PDF | PDF |
| **quá tài** | **quá sướng, quá mức** | PDF | PDF |
| **quan triết** | **hiểu rõ** | PDF | PDF |
| **quân lý** | **quân trị** | PDF | PDF |
| **quảng trường** | **công trường** | PDF | PDF |
| **quân hàm** | **cấp bậc** | PDF | PDF |
| **quy hoạch** | **kế hoạch** | PDF | PDF |
| **quy trình** | **tiến trình** | PDF | PDF |
| **sốc (shocked)** | **kinh hoàng, kinh ngạc, ngạc nhiên** | PDF | PDF |
| **sổ tân** | **tân cương** | PDF | PDF |
| **sư - sư đoàn** | **sư đoàn** | PDF | PDF |
| **sức khỏe công dân** | **y tế công cộng** | PDF | PDF |
| **sự cố** | **trở ngại** | PDF | PDF |
| **tạp đoàn / doanh nghiệp** | **công ty** | PDF | PDF |
| **tên lứa** | **hòa tiến** | PDF | PDF |
| **tham gia lưu thông (xe cộ)** | **lưu hành** | PDF | PDF |
| **tham quan** | **thẩm viếng** | PDF | PDF |
| **thanh lý** | **thanh toán, chứng minh** | PDF | PDF |
| **thần thượng** | **thần mê** | PDF | PDF |
| **thi công** | **làm** | PDF | PDF |
| **thí phần** | **thí trường** | PDF | PDF |
| **thu nhập** | **lợi tức** | PDF | PDF |
| **thư giãn** | **tĩnh táo, giải trí** | PDF | PDF |
| **thuyết phục (tính)** | **có lý (makes sense), hợp lý - tin được** | PDF | PDF |
| **tiến tiến** | **xuất sắc** | PDF | PDF |
| **tiến công** | **tấn công** | PDF | PDF |
| **tiếp thu** | **tiếp nhận, thâu nhận, lãnh hội** | PDF | PDF |
| **tiêu dùng** | **tiêu thụ** | PDF | PDF |
| **tổ lái** | **phi hành đoàn** | PDF | PDF |
| **tổ rơi** | **truyền đơn** | PDF | PDF |
| **tranh thủ** | **cố gắng** | PDF | PDF |
| **trí tuệ** | **kiến thức** | PDF | PDF |
| **triển khai** | **khai triển** | PDF | PDF |
| **tư duy** | **suy nghĩ** | PDF | PDF |
| **tư liệu** | **tài liệu** | PDF | PDF |
| **từ** | **tiếng, chữ** | PDF | PDF |
| **uốn tạc** | **tắt nghiêng** | PDF | PDF |
| **văn dân** | **văn đề** | PDF | PDF |
| **văn động viên** | **lực sĩ** | PDF | PDF |
| **viện ung bướu** | **viện ung thư** | PDF | PDF |
| **vô tư** | **tự nhiên** | PDF | PDF |
| **xác tín** | **chính xác** | PDF | PDF |
| **xe con** | **xe du lịch** | PDF | PDF |
| **xe khách** | **xe đồ** | PDF | PDF |
| **xử lý** | **giải quyết, thi hành** | PDF | PDF |

**Lưu ý Quy tắc 15**: Tên riêng, tên sách, tên báo, thuật ngữ pháp lý — **giữ nguyên** dạng gốc, thêm tên VNCH trong ngoặc đơn lần đầu. Trong trích dẫn tiếng Pháp/Anh — giữ nguyên hoàn toàn.

### 4.2 Cặp Từ Văn Phong (Quy tắc 2, 7, 22, 23, 25) — MAJOR

| Miền Bắc / Hiện nay | Miền Nam VNCH | Quy tắc | Ghi chú |
|---|---|---|---|
| **này** | **nầy** | 2, 22 | Trừ: "trong nầy, ngoài nầy, trước nầy, sau nầy" |
| **mà không / mà chẳng / mà đâu** | **chớ không / chớ chẳng / chớ đâu** | 2, 7, 25 | "chớ" thay "mà/nhưng" khi nhấn mạnh tương phản |
| **mặc dù** | **dầu / dẫu** | 2, 25 | "Dầu đã nỗ lực..." |
| **tuy nhiên** | **tuy vậy / đã vậy / song** | 25 | "Tuy vậy, kết quả..." |
| **vì vậy / do đó** | **bởi thế / do đó / cho nên** | 25 | "Bởi thế, chánh phủ..." |
| **hơn nữa / hơn thế nữa** | **vả / lại / cũng / thêm chi** | 25 | "Vả, còn có..." |
| **ngược lại** | **trái lại** | 25 | "Trái lại, miền Nam..." |

### 4.3 Ngữ Pháp Miền Nam VNCH (Quy tắc 21-26) — BẮT BUỘC MỖI CÂU

#### A. Danh Từ Chỉ Định (Classifiers) — Quy tắc 21
| Loại từ | Chỉ định Nam Bộ | Ví dụ |
|---|---|---|
| Con người (trẻ em) | **con** | *một con người, một con nhỏ* |
| Cây cối, đồ vật dài | **cây** | *một cây bút, một cây cầu* |
| Khối, vật tròn/vuông | **cục** | *một cục đá, một cục đường* |
| Vật tổng quát | **cái** | *một cái sách, một cái bàn* |
| Người (trang trọng) | **người / ngài** | *một người ấy, một ngài quan lại* |
| Sách, vở, báo | **cuốn** | *một cuốn sách, một cuốn báo* |
| Câu chuyện, bài báo | **cái / bài** | *một cái bài, một bài viết* |

**Áp dụng**: Khi dịch "a/an/the + noun" → thêm chỉ định phù hợp.

#### B. Trạng Từ Không Gian/Thời Gian — Quy tắc 22
| Cặp đối lập | Nam Bộ VNCH | Cách dùng học thuật |
|---|---|---|
| Đây — Đó — Kia | **nầy — đó — kia** | **BẮT BUỘC**: *nầy* (gần), *đó* (gần người nghe), *kia* (xa) |
| Trước — Sau | **trước — sau** | *trước nầy, sau nầy, năm nầy, ngày nầy* |

**Cấm**: *này, năm này, trước đây, sau này* (trừ cụ trúc "trong này, ngoài này, trước này, sau này").

#### C. Thể Khía (Aspect) — Quy tắc 23
| Thể | Dạng rút gọn (cấm) | Dạng đầy đủ Nam Bộ (bắt buộc) | Ví dụ |
|---|---|---|---|
| Hoàn thành | *đã* | **đã... rùi / đã... hẵng** | "đã kết thúc rùi", "đã ký hẵng" |
| Đang diễn ra | *đang* | **đang... xong / đang tiến hành** | "đang tiến hành ký kết" (văn viết) |
| Sắp tới | *sẽ* | **sắp sẽ / chuẩn bị sẽ** | "sắp sẽ ký", "chuẩn bị sẽ triển khai" |
| Vừa mới | *vừa / vừa mới* | **vừa... mới / mới... xong** | "vừa ký xong", "mới kết thúc xong" |
| Chưa | *chưa* | **chưa... bao giờ / vẫn chưa** | "chưa bao giờ ký", "vẫn chưa quyết định" |

#### D. Đại Từ Nhân Xưng — Quy tắc 24
| Người | Đơn số | Số nhiều | Cấm dùng |
|---|---|---|---|
| 1 | **tôi / tác giả** | **chúng tôi / chúng ta** | *ta, tui, mình* |
| 2 | **ông / bà / quý vị** | **các ông / các bà / quý vị** | *mày, tao, cậu, mình* |
| 3 | **người ấy / ông ấy / bà ấy / nó** (vật) | **họ / những người ấy / chúng nó** (vật) | **CẤM**: *hắn, y, nó* chỉ người |

#### E. Từ Nối Logic Nam Bộ — Quy tắc 25
| Quan hệ | Ưu tiên VNCH | Hạn chế / Tránh |
|---|---|---|
| Nhượng bộ | **dầu, dẫu** | *mặc dù* |
| Tương phản | **trái lại** | *ngược lại* |
| Chuyển ý | **tuy vậy, đã vậy, song** | *tuy nhiên* |
| Nhân quả | **bởi thế, do đó, cho nên** | *vì vậy* |
| Bổ sung | **vả, lại, cũng** | *hơn nữa* |

#### F. Chủ Động Hóa (Active Voice) — Quy tắc 26 (QUY TẮC VÀNG)
| Cấu trúc tiếng Anh | Xử lý VNCH | Ví dụ |
|---|---|---|
| Passive *was/were + V3* | **Chủ động hóa** nếu tự nhiên hơn | "was signed by the government" → "Chánh phủ đã ký..." |
| Passive mang sắc thái tiêu cực | Giữ *bị + V* | "bị trấn áp", "bị tước đoạt" |
| *get/have + V3* (causative) | **Chủ động hóa** | "had the treaty signed" → "làm ký hiệp định" |

## 5. KIỂM TRA VĂN PHONG MỖI CÂU (Checklist S13-S20)

```
[ ] S13: Không dùng từ miền Bắc (này, giải phóng, đồng chí, chính phủ, chính trị, bài nói, báo cáo, bảo quản, cách ly, cái đai, cân, chất lượng, chế độ, chỉ đạo, chỉ tiêu, chúng nhiêm, chú trễ, chửa cháy, chiếu đãi, chui, chuyện chèo, chuyện ngữ, chứng minh nhân dân, chữ đạo, co cụm, công đoàn, công nghiệp, công trình, cơ bản, cơ khí, cơ sở, cửa khẩu, cụm từ, cứu hộ, diễn, đấu kiện, đại học mái, đạo trí, đầu ra/đầu vào, đại tiệc/tiểu tiệc, đại trà, đảm bảo, đăng ký, đáp án, đăng kí, đồng bằng, đường cao tốc, gia công, giải phóng, giải phóng mặt bằng, giản đơn, giao lưu, hạch toán, hải quan, hàng không dân dụng, hát đôi, hát tập, hát nhân, hậu cần, học vị, hệ quả, hiện đại, hộ nhà, hộ chiếu, họp hội, họ khẩu, hội chữ thập đỏ, kiều hời, kiệt xuất, kinh qua, làm gái, làm việc, lâu năm góc/nhà tráng, liên hoan, liên hệ, linh tinh, lính gái, lính thủy đánh bộ, lợi nhuận, lực tôm, lý giải, máy bay lên thẳng, múa đòi, mĩ, nằm bật, nâng cấp, năng nổ, nghệ nhân, nghệ danh, nghĩa vụ quân sự, nghiêm túc, nghiệp dư, nhà khách, nhất trí, nhất quán, người nước ngoài, noi niệm, phân cứng, phân mềm, phản ánh, phản hồi, phát sóng, phó tiến sĩ, phi khẩu, phi vụ, phục hồi nhân phẩm, phương án, quá tài, quan triết, quân lý, quảng trường, quân hàm, quy hoạch, quy trình, sốc, sổ tân, sư đoàn, sức khỏe công dân, sự cố, tạp đoàn/doanh nghiệp, tên lứa, tham gia lưu thông, tham quan, thanh lý, thần thượng, thi công, thí phần, thu nhập, thư giãn, thuyết phục, tiến tiến, tiến công, tiếp thu, tiêu dùng, tổ lái, tổ rơi, tranh thủ, trí tuệ, triển khai, tư duy, tư liệu, từ, uốn tạc, văn dân, văn động viên, viện ung bướu, vô tư, xác tín, xe con, xe khách, xử lý)
[ ] S14: Không dùng từ hiện đại áp đặt (tài chính→tài chánh, đại biểu→dân biểu, lương hưu→hưu bổng, ngân sách cơ quan→ngân khố, bất động sản→địa ốc, bảo hiểm→an toàn, báo cáo→thưa trình/nói/kể, bảo quản→che chở/gìn giữ/bảo vệ, bài nói→diễn văn, cách ly→cô lập, cảnh báo→báo động/phải chú ý, cái A-lô→cái điện thoại, cân→căng thẳng, cầu lông→vũ cầu, chất lượng→phẩm chất tốt, chất xám→trí tuệ/sự thông minh, chế độ→quy chế, chỉ đạo→chỉ thị/ra lệnh, chỉ tiêu→định suất, chúng nhiêm→trường ban/khoa trưởng, chú trễ→chú tôa, chửa cháy→cầu hỏa, chiếu đãi→thất đãi, chui→lén lút, chuyện chèo→nói lên/nêu ra, chuyện ngữ→dịch, chứng minh nhân dân→thẻ căn cước, chữ đạo→chính, co cụm→thu hẹp, công đoàn→nghiệp đoàn, công nghiệp→kỹ nghê, công trình→công tác, cơ bản→căn bản, cơ khí→cần bản, cơ sở→căn bản/nguồn gốc, cửa khẩu→phi cảng/hải cảng, cụm từ→nhóm chữ, cứu hộ→cứu cấp, diễn→thành phần, đấu kiện→phương định, đạo trí→tự nhiên, đầu ra/đầu vào→xuất lượng/nhập lượng, đại tiệc/tiểu tiệc→nấu ăn chung/ăn tập thể/nấu ăn riêng/ăn gia đình, đại trà→quy mô/cỡ lớn, đảm bảo→bảo đảm, đăng ký→ghi danh/ghi tên, đáp án→kết quả/trả lời, đăng kí→ghi danh, đồng bằng→phi đạo, đường cao tốc→xa lộ, gia công→làm ăn công, giải phóng→lấy lại/đem đi, giản đơn→đơn giản, giao lưu→giao tiếp/trao đổi, hạch toán→kế toán, hải quan→quan thuế, hàng không dân dụng→hàng không dân sự, hát đôi→song ca, hát tập→hợp ca, hát nhân→nguyên tử, hậu cần→tiếp liệu, học vị→bằng cấp, hệ quả→hậu quả, hiện đại→tối tân, hộ nhà→gia đình, hộ chiếu→sổ thông hành, họp hội→phân khu, họ khẩu→tổ khai gia đình, hội chữ thập đỏ→hội Hồng Thập Tự, kiều hời→ngoại tệ, kiệt xuất→giải/xuất sắc, kinh qua→trải qua, làm gái→làm điếm, làm việc→thẩm vấn/điều tra, lâu năm góc/nhà tráng→ngụy Giác Đốc/Tòa Bạch ốc, liên hoan→đại hội/ăn mừng, liên hệ→liên lạc, linh tinh→vỏ vần, lính gái→nữ quân nhân, lính thủy đánh bộ→thủy quân lực lượng chiến, lợi nhuận→lợi tức, lực tôm→tôm lực, lý giải→giải thích, máy bay lên thẳng→trực thăng, múa đòi→khiêu vũ, mĩ→Mỹ, nằm bật→nằm ngửa, nâng cấp→nâng/đưa giá trị lên, năng nổ→siêng năng/tháo vát, nghệ nhân→thờ/nghệ sỹ, nghệ danh→Tên nghệ sỹ, nghĩa vụ quân sự→Đi quân dịch, nghiêm túc→nghiêm chính, nghiệp dư→đi làm thêm, nhà khách→khách sạn, nhất trí→đồng lòng/đồng ý, nhất quán→luôn luôn/trước sau như một, người nước ngoài→ngoại kiều, noi niệm→viễn suy tư, phân cứng→cường liệu, phân mềm→nhu liệu, phản ánh→phản ảnh, phản hồi→trả lời/hồi âm, phát sóng→phát thanh, phó tiến sĩ→cao học, phi khẩu→phi trường/phi cảng, phi vụ→một vụ trao đổi thường mại, phục hồi nhân phẩm→hoàn lượng, phương án→kế hoạch, quá tài→quá sướng/quá mức, quan triết→hiểu rõ, quân lý→quân trị, quảng trường→công trường, quân hàm→cấp bậc, quy hoạch→kế hoạch, quy trình→tiến trình, sốc→kinh hoàng/kinh ngạc/ngạc nhiên, sổ tân→tân cương, sư đoàn, sức khỏe công dân→y tế công cộng, sự cố→trở ngại, tạp đoàn/doanh nghiệp→công ty, tên lứa→hòa tiến, tham gia lưu thông→lưu hành, tham quan→thẩm viếng, thanh lý→thanh toán/chứng minh, thần thượng→thần mê, thi công→làm, thí phần→thí trường, thu nhập→lợi tức, thư giãn→tĩnh táo/giải trí, thuyết phục→có lý/hợp lý/tin được, tiến tiến→xuất sắc, tiến công→tấn công, tiếp thu→tiếp nhận/thâu nhận/lãnh hội, tiêu dùng→tiêu thụ, tổ lái→phi hành đoàn, tổ rơi→truyền đơn, tranh thủ→cố gắng, trí tuệ→kiến thức, triển khai→khai triển, tư duy→suy nghĩ, tư liệu→tài liệu, từ→tiếng/chữ, uốn tạc→tắt nghiêng, văn dân→văn đề, văn động viên→lực sĩ, viện ung bướu→viện ung thư, vô tư→tự nhiên, xác tín→chính xác, xe con→xe du lịch, xe khách→xe đồ, xử lý→giải quyết/thi hành)
[ ] S15: Chỉ định danh từ đúng Nam Bộ (cuốn/cái/con/cây/cục/bài/người/ngài)
[ ] S16: Trạng từ không gian/thời gian dùng nầy/đó/kia (năm nầy, trước nầy, sau nầy...)
[ ] S17: Thể khía đầy đủ (đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa)
[ ] S18: Bị động đã chủ động hóa (nếu tự nhiên hơn) — Quy tắc 26
[ ] S19: Đại từ nhân xưng trang trọng (người ấy/ông ấy/bà ấy/họ — CẤM hắn/y/nó chỉ người)
[ ] S20: Từ nối logic Nam Bộ (dầu/dẫu, trái lại, tuy vậy/đã vậy, bởi thế/do đó, vả/lại/cũng)
```

## 6. SCRIPT TỰ ĐỘNG HÓA: `vnch_orthography.py` (Common Script)

Script này áp dụng **30+ quy tắc VNCH** tự động SAU KHI DỊCH XONG, TRƯỚC KHI BUILD DOCX.

**Các quy tắc chính từ PDF + Style Guide (tổng ~120 cặp từ):**

**Nhóm 1: Thuật ngữ chính trị - hành chính (CRITICAL)**
1. `chính trị` → `chánh trị`
2. `chính phủ` → `chánh phủ`
3. `chính đảng` → `chánh đảng`
4. `đảo chính` → `đảo chánh`
5. `tài chính` → `tài chánh`
6. `đại biểu` → `dân biểu`
7. `lương hưu` → `hưu bổng`
8. `bất động sản` → `địa ốc`
9. `ngân sách (cơ quan)` → `ngân khố`
10. `giải phóng` → `độc lập` / `kháng cự` (thân bài; tên riêng giữ nguyên có ghi chú)
11. `đồng chí` → `đồng đạo` (thân bài; tên tổ chức giữ nguyên)
12. `Annam` → `Trung Kỳ (Annam)`
13. `Tonkin` → `Bắc Kỳ (Tonkin)`
14. `Cochinchina/Cochinchine` → `Nam Kỳ (Cochinchina)`
15. `Indochine` → `Đông Dương (Indochine)`
16. `bảo hiểm` → `an toàn`
17. `báo cáo` → `thưa trình, nói, kể`
18. `bảo quản` → `che chở, gìn giữ, bảo vệ`
19. `bài nói` → `diễn văn`
20. `cách ly` → `cô lập`
... (tổng ~120 cặp từ từ PDF)

**Nhóm 2: Văn phong (MAJOR)**
- `này` → `nầy` (trừ "trong nầy, ngoài nầy, trước nầy, sau nầy")
- `mà không` → `chớ không`
- `mặc dù` → `dầu/dẫu`
- `tuy nhiên` → `tuy vậy/đã vậy`
- `vì vậy` → `bởi thế/do đó`
- `hơn nữa` → `vả/lại`
- `ngược lại` → `trái lại`

**Nhóm 3: Ngữ pháp (BẮT BUỘC)**
- Chỉ định danh từ: cuốn/cái/con/cây/cục/bài/người/ngài
- Trạng từ: nầy/đó/kia (năm nầy, trước nầy, sau nầy)
- Thể khía đầy đủ: đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa
- Đại từ: người ấy/ông ấy/bà ấy/họ (CẤM hắn/y/nó chỉ người)
- Từ nối: dầu/dẫu, trái lại, tuy vậy/đã vậy, bởi thế/do đó, vả/lại/cũng
- Chủ động hóa passive (Quy tắc 26)

**False Positive (KHÔNG SỬA)**: 43 lỗi trong tên sách, trích dẫn, tên tổ chức tiếng Pháp.

## 7. LIÊN KẾT SKILLS
- **historical-book-translation**: Bước 3.5, Bước 4.
- **contextual-translation**: Dùng từ nối, trạng từ, đại từ phù hợp ngữ cảnh.
- **translation-error-detection**: Phát hiện lỗi từ miền Bắc, từ hiện đại, sai văn phong.
- **deep-translation-review**: Kiểm tra văn phong khi audit.
- **translation-quality-gate**: Orthography check (0× "chính trị", 0× từ Bắc).
- **historical-terminology-research**: Thuật ngữ chuẩn cho Orthography.

---

*Cập nhật: 2026-11-20 — Dựa trên STYLE_GUIDE_PHAN_B.md v2.3 (29 quy tắc), Grammar Engine v2.1 §1.2-1.8, Audit 6 chương, Bảng Đối Chiếu Tiếng Việt (PDF: doi-chieu-tieng-viet.pdf, T.V.G., Đặc San Kỷ Niêm 25 Năm TNSP, ~120 cặp từ VNCH-VC).*