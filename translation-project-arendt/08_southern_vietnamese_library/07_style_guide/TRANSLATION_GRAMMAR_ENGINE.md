# TRANSLATION GRAMMAR ENGINE
# Bộ quy tắc dịch thuật — Cambridge History of the Vietnam War

> Phiên bản: 2.1 — Cập nhật sau Audit 6 chương đầu (2026-11-19): Bổ sung §10 (Bài học tránh lặp), §11 (Workflow tích hợp), §12 (Checklist mở rộng), Cập nhật S1-S20, P1-P10, C1-C10.
> Ngày: 2026-11-19. UTF-8, NFC, không BOM.
> Quan hệ với các artifact khác:
> - **Style Guide Phan B** (`07_style_guide/STYLE_GUIDE_PHAN_B.md`) = quy tắc **từ vựng** và **văn phong** (dùng từ gì).
> - **Master Lexicon** (`08_southern_vietnamese_library/10_LEXICAL_DATABASE/MASTER_LEXICON.csv`) = **nguồn** thuật ngữ (từ nào có bằng chứng).
> - **Grammar Engine** (tệp này) = quy tắc **quy trình dịch** (dịch như thế nào) + **VNCH Grammar Database** (ngữ pháp miền Nam VNCH).
>
> Ba artifact bổ sung cho nhau: Lexicon cung cấp từ, Style Guide quy định chọn từ, Grammar Engine quy định cách ráp câu.

---

## 0. NGUYÊN TẮC CỐT LÕI

Một câu dịch chỉ được chấp nhận khi **đồng thời** thỏa mãn ba điều kiện:

1. **Đúng nghĩa nguyên tác** (semantic fidelity) — không thêm, không bớt, không đổi nghĩa.
2. **Đúng ngữ pháp tiếng Việt** (grammatical integrity) — câu đúng cấu trúc tiếng Việt, không phải cấu trúc ngoại ngữ bê nguyên.
3. **Truyền đạt rõ ràng ý tưởng tác giả** (logical clarity) — người đọc hiểu đúng ý ngay lần đọc đầu, không phải đọc lại nhiều lần để giải mã.

Ba điều kiện này là **điều kiện cần**, không phải điều kiện đủ. Một câu có thể đúng cả ba nhưng vẫn chưa đạt nếu vi phạm Style Guide (dùng từ không chuẩn Nam Bộ) hoặc Lexicon (dùng từ không có nguồn).

### Ba cấp độ kiểm soát

| Cấp độ | Câu hỏi kiểm tra | Khi nào áp dụng |
|---|---|---|
| **Sentence** (câu) | Câu này có chính xác và dễ hiểu không? | Sau khi dịch mỗi câu |
| **Paragraph** (đoạn) | Các câu có liên kết thành một ý hoàn chỉnh không? | Sau khi dịch mỗi đoạn |
| **Chapter** (chương) | Toàn chương có giữ nguyên hệ thống lập luận của tác giả không? | Sau khi dịch mỗi chương |

Mỗi cấp độ có bộ câu hỏi kiểm tra riêng (§3, §4, §5). Không được bỏ qua cấp độ nào.

---

## 1. VNCH GRAMMAR DATABASE — NGỮ PHÁP MIỀN NAM VNCH (TỪ NGUỒN SƠ CẤP)

### 1.1. Nguồn bằng chứng (Evidence Sources)

| Mã nguồn | Tác phẩm | Năm | Loại | Liên quan đến Grammar Engine |
|---|---|---|---|---|
| SRC-021 | Phan Khôi, "Việt ngữ nghiên cứu" (8 kỳ) | 1955 (xuất bản lại 1997 Nxb Đà Nẵng) | Ngữ pháp thuật | Phân cấp: tự → từ → ngữ → cú; danh từ: con/cây/cục/cái; trạng từ: trên/dưới/trong/ngoài |
| SRC-001 | Lê Văn Đức, "Tự điển Việt Nam" (2 quyển) | 1970 (Khai Trí, Sài Gòn) | Từ điển chuẩn VNCH | Từ vựng, chính tả, thuật ngữ Nam Bộ |
| SRC-009 | Bách Khoa 405 (Tạp chí Bách Khoa 1957-1975) | 1957-1975 | Bách khoa VNCH | Thuật ngữ chuyên ngành, văn phong sách |
| SRC-023 | Hiến pháp VNCH 1967 | 1967 | Văn kiện pháp lý | Thuật ngữ chính trị-hành chính: chánh phủ, dân biểu, nghị sĩ, ngân khố |
| SRC-022 | Thompson, "A Vietnamese Reference Grammar" | 1987 (UH Press) | Ngữ pháp học thuật | Ngữ pháp tham chiếu, có đối chiếu phương ngữ Nam |
| SRC-024 | Clark, "Passive and Ergative in Vietnamese" | 1974 | Ngữ pháp học thuật | Cấu trúc bị động/thể kiện Nam Bộ |

### 1.2. Phân cấp đơn vị ngôn ngữ (Theo Phan Khôi, Việt ngữ nghiên cứu)

| Cấp độ | Tên gọi | Định nghĩa | Ví dụ |
|---|---|---|---|
| 1 | **Tự** (morpheme) | Từng chữ rời ra, đơn vị nhỏ nhất có nghĩa | *việt*, *nam* |
| 2 | **Từ** (word) | Một lời để tỏ ra một khái niệm | *Việt Nam*, *cô-giáo* |
| 3 | **Ngữ** (phrase) | Nhóm từ biểu đạt khái niệm phức tạp hơn | *người cô-giáo ấy* |
| 4 | **Cú** (clause) | Nhóm từ có chủ vị, biểu đạt một tuyên bố | *cô ấy đang dạy* |

**Áp dụng dịch thuật**: Khi phân tích từ vựng (Bước 4), xác định đúng cấp độ để không dịch *tự* như *từ*, không gộp *ngữ* sai chỗ.

### 1.3. Hệ thống danh từ chỉ định (Classifiers) — Nam Bộ vs Bắc Bộ

| Chỉ định | Nam Bộ (VNCH) | Bắc Bộ / Hiện nay | Ghi chú |
|---|---|---|---|
| Con người (trẻ em) | **con** | *con* | Giống nhau |
| Cây cối, đồ vật dài | **cây** | *cây/cây* | Giống nhau |
| Khối, vật tròn/vuông | **cục** | *cục/khối* | Nam Bộ dùng *cục* nhiều hơn |
| Vật tổng quát | **cái** | *cái/chiếc* | Nam Bộ ưu tiên *cái* |
| Người (trang trọng) | **người/ngài** | *người/ngài* | Văn phong VNCH dùng *ngài* cho quan lại |
| Sách, vở, báo | **cuốn/cuốn** | *cuốn/cuốn* | Giống nhau |
| Câu chuyện, bài báo | **cái/bài** | *bài/cái* | Nam Bộ dùng *cái* cho bài viết ngắn |

**Quy tắc dịch**: Khi nguyên tác dùng "a/an/the + noun" cần dịch ra danh từ có chỉ định, chọn chỉ định theo bảng trên.

### 1.4. Trạng từ chỉ không gian/thời gian (Theo Phan Khôi, Kỳ 5-6)

| Cặp đối lập | Nam Bộ (VNCH) | Cách dùng trong văn học thuật |
|---|---|---|
| **Trên — Dưới** | *trên — dưới* | "trên chiến trường", "dưới thời Pháp cai trị" |
| **Trong — Ngoài** | *trong — ngoài* | "trong chánh phủ", "ngoài biên giới" |
| **Lên — Xuống** | *lên — xuống* | "lên đồi", "xuống đồng" |
| **Vào — Ra** | *vào — ra* | "vào năm 1945", "ra khỏi thủ đô" |
| **Trước — Sau** | *trước — sau* | "trước Thế Chiến II", "sau Hiệp định Genève" |
| **Đây — Đó — Kia** | *nầy — đó — kia* | **BẮT BUỘC** dùng *nầy* (không *này*), *đó* (gần người nghe), *kia* (xa) |

### 1.5. Hệ thống thể khía (Aspect) — Nam Bộ

| Thể | Dấu hiệu | Nam Bộ (VNCH) | Ví dụ |
|---|---|---|---|
| Hoàn thành | *đã... rồi* | *đã... rùi / đã... hẵng* | "đã kết thúc rùi", "đã ký hẵng hiệp định" |
| Đang diễn ra | *đang* | *đang... nha / đang... nãy* | "đang tranh luận nha" (văn nói), "đang tiến hành" (văn viết) |
| Sắp tới | *sắp... sẽ* | *sắp... sẽ / chuẩn bị... sẽ* | "sáp sẽ ký", "chuẩn bị sẽ triển khai" |
| Vừa mới | *vừa... mới* | *vừa... mới / mới... xong* | "vừa ký xong", "mới kết thúc xong" |
| Chưa | *chưa* | *chưa... bao giờ / vẫn chưa* | "chưa bao giờ ký", "vẫn chưa quyết định" |

**Lưu ý**: Văn học thuật VNCH dùng dạng đầy đủ (*đã... rồi, đang, sẽ, vừa... mới*) hơn dạng rút gọn hội thoại.

### 1.6. Cấu trúc bị động / thể kiện (Theo Clark 1974, Thompson 1987)

| Cấu trúc | Nam Bộ (VNCH) | Khi nào dùng trong dịch thuật |
|---|---|---|
| **Bị động ý chí** (nghĩa chủ quan) | *bị + V* | Mang sắc thái tiêu cực: "bị trấn áp", "bị tước đoạt" |
| **Bị động vô ý** (nghĩa khách quan) | *được + V* (ít dùng) / **Chủ động hóa** | **Ưu tiên chuyển sang chủ động**: "người ta ký" thay cho "được ký" |
| **Thể kiện** (ergative) | *tự + V / V + ra/khỏi* | "cuộc nổi dậy tự bùng nổ", "hiệp định tự chấm dứt" |
| **Cấu trúc "do... thực hiện"** | *do + N + V* | Văn hành chính/trang trọng: "do chánh phủ ban hành" |

**QUY TẮC VÀNG**: **Luôn ưu tiên chủ động hóa** câu bị động tiếng Anh nếu tiếng Việt tự nhiên hơn (xem Bước 5).

### 1.7. Đại từ nhân xưng học thuật VNCH

| Người | Đơn số | Số nhiều | Văn phong sách VNCH |
|---|---|---|---|
| 1 | *tôi / tác giả* | *chúng tôi / chúng ta* | Tránh *ta, tui, mình* |
| 2 | *ông / bà / quý vị* | *các ông / các bà / quý vị* | Tránh *mày, tao, cậu, mình* |
| 3 | *người ấy / ông ấy / bà ấy / nó* (vật) | *họ / những người ấy / chúng nó* (vật) | **BẮT BUỘC** dùng *người ấy, ông ấy, bà ấy* thay *hắn, y, nó* (cho người) |

### 1.8. Từ nối logic Nam Bộ (Mở rộng từ Bước 3)

| Quan hệ | Nam Bộ (VNCH) — Ưu tiên | Dùng hạn chế / Tránh | Ví dụ |
|---|---|---|---|
| Nhượng bộ | **dầu, dẫu** | *mặc dù* (quá Bắc) | "Dầu đã nỗ lực..." |
| Tương phản | **trái lại** | *ngược lại* | "Trái lại, miền Nam..." |
| Chuyển ý | **tuy vậy, đã vậy, song** | *tuy nhiên* (dùng ít) | "Tuy vậy, kết quả..." |
| Nhân quả | **bởi thế, do đó, cho nên** | *vì vậy* (dùng ít) | "Bởi thế, chánh phủ..." |
| Bổ sung | **vả, lại, cũng, thêm chi** | *hơn nữa, hơn thế nữa* | "Vả, còn có..." |
| Điều kiện | **khi... thì, nếu... thì** | *trường hợp... thì* | "Khi hiệp định ký..." |
| Mục đích | **để, hầu, nhằm** | *cho rằng* | "Để độc lập..." |
| Liệt kê | **thứ nhất, thứ hai...; một là... hai là...** | *trước hết, thứ hai* | "Một là..., hai là..." |

---

## 2. QUY TRÌNH DỊCH THUẬT 7 BƯỚC (CẬP NHẬT THEO VNCH GRAMMAR + AUDIT 6 CHƯƠNG)

### Bước 1 — Phân tích ngữ pháp nguyên tác
- Xác định cấu trúc câu: chủ thể, vị ngữ, đối tượng, mệnh đề phụ.
- Phân tích quan hệ logic giữa các mệnh đề (nhân quả, tương phản, nhượng bộ, mục đích, điều kiện, liệt kê).
- Chú ý cấu trúc bị động, thể, mệnh đề quan hệ.

### Bước 2 — Xác định chủ thể, vị ngữ, đối tượng
- Chủ thể: Ai/thứ gì thực hiện hành động?
- Vị ngữ: Hành động/tình trạng gì?
- Đối tượng: Ai/thứ gì chịu tác động?
- Nếu bị động tiếng Anh: Xác định tác nhân (bằng "by...") để chuyển sang chủ động tiếng Việt.

### Bước 3 — Phân tích quan hệ logic giữa các mệnh đề
**MỞ RỘNG**: Sử dụng bảng từ nối logic Nam Bộ (§1.8) thay vì chỉ 8 quan hệ cơ bản. Xác định đúng quan hệ: nhượng bộ, tương phản, chuyển ý, nhân quả, bổ sung, điều kiện, mục đích, liệt kê.

### Bước 4 — Xác định nghĩa thuật ngữ theo ngữ cảnh
**MỞ RỘNG THEO AUDIT 6 CHƯƠNG**:
1. Tra **MASTER_LEXICON.csv** trước.
2. Nếu có → dùng dạng trong lexicon, ghi nguồn.
3. Nếu không có → tra **VNCH Grammar Database** (§1.2-1.8) cho từ chức năng (chỉ định, trạng từ, đại từ, thể).
4. Nếu vẫn không có → tra nguồn VNCH (Lê Văn Đức, Hiến pháp 1967, Bách Khoa 405).
5. Nếu vẫn không có → **giữ nguyên thuật ngữ gốc** (in nghiêng) + giải nghĩa lần đầu + đánh dấu `[CẦN BỔ SUNG LEXICON]`.
6. **KHÔNG ĐƯỢC** tự dịch một từ mới mà không có nguồn.
7. **KHI GẶP TỪ/CÂU KHÓ** (theo Quy tắc 20): Thực hiện 5 bước: (1) Mở rộng ngữ cảnh; (2) Xác định ý đồ tác giả; (3) Tra cứu nguồn; (4) Đối chiếu chỗ khác; (5) Tái dựng ý nghĩa → diễn đạt VNCH. Ghi nhận căn cứ, mức độ chắc chắn.

### Bước 5 — Tái cấu trúc thành câu tiếng Việt tự nhiên (VNCH)

**Nguyên tắc bổ sung từ VNCH Grammar + Audit 6 chương**:
- **Chủ động hóa** câu bị động tiếng Anh (xem §1.6) — QUY TẮC VÀNG.
- **Dùng chỉ định đúng** cho danh từ (§1.3): *một cuốn sách, một cái bài, một con người, một cây bút, một cục đá, một thời kỳ nầy*.
- **Dùng trạng từ không gian/thời gian Nam Bộ** (§1.4): *nầy, đó, kia, trong, ngoài, trước, sau, ngày nầy, năm nầy, trước nầy, sau nầy*.
- **Dùng thể khía đúng** (§1.5): *đã... rùi/hẵng, đang... xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa... mới/mới... xong, chưa... bao giờ/vẫn chưa*.
- **Dùng đại từ nhân xưng trang trọng** (§1.7): *người ấy, ông ấy, bà ấy, họ* — **CẤM** *hắn, y, nó* chỉ người; *ta, tui, mình* (người 1); *mày, tao, cậu* (người 2).
- **Dùng từ nối logic Nam Bộ** (§1.8): *dầu, dẫu, trái lại, tuy vậy, đã vậy, song, bởi thế, do đó, vả, lại, một là... hai là...*.
- **CẤM KỊ**: **Không dịch từng từ rồi ghép lại** (Quy tắc 19). Phải đọc toàn câu, đoạn, ngữ cảnh → tái cấu trúc.
- **KHÔNG** giữ nguyên cấu trúc câu ngoại ngữ nếu làm tiếng Việt khó hiểu.
- **KHÔNG** dùng từ Hán Việt chỉ để tạo vẻ học thuật.
- **KHÔNG** rút gọn những đoạn có nội dung lý luận.
- **KHÔNG** tự diễn giải vượt quá ý tác giả.
- **KHÔNG** fabricate: không bịa số trang, trích dẫn, ví dụ (Quy tắc 27).

### Bước 6 — Đối chiếu lại nguyên tác
- Đối chiếu số câu: bản dịch phải có đúng số câu như nguyên tác (không thêm, không bớt).
- Đối chiếu thông tin: không mất ý chính, không thêm ý không có.
- Đối chiếu thuật ngữ: đúng lexicon, đúng VNCH Grammar.
- Đối chiếu cước chú: marker `[N]`/`N` ở đúng vị trí, đúng thứ tự 1..N.
- **Kiểm tra alignment**: số đoạn src = số đoạn vi (Quy tắc 18).

### Bước 7 — Kiểm tra tính dễ hiểu
- Đọc to câu dịch: có hiểu ngay lần đầu không?
- Có từ nào gây nhầm lẫn, câu nào rối logic không?
- Có từ miền Bắc, từ hiện đại áp đặt không?
- Có cấu trúc ngoại ngữ bê nguyên không?

---

## 3. KIỂM SOÁT CẤP SENTENCE (CẬP NHẬT THEO AUDIT)

### 3.1. Câu hỏi kiểm tra sentence — 20 mục (S1–S20)

| # | Câu hỏi | Nếu "không" |
|---|---|---|
| S1 | Chủ ngữ có rõ ràng không? | Xác định lại chủ thể |
| S2 | Vị ngữ có đúng hành động không? | Kiểm tra lại động từ |
| S3 | Đối tượng có rõ ràng không? | Xác định lại tân ngữ |
| S4 | Đại từ có rõ quy chiếu không? | Thay bằng danh từ cụ thể hoặc *người ấy/ông ấy/bà ấy* |
| S5 | Mệnh đề phụ có gắn đúng đối tượng không? | Sắp xếp lại mệnh đề |
| S6 | Quan hệ nhân quả có đúng chiều không? | Sửa liên từ theo §1.8 |
| S7 | Câu có thể hiểu ngay lần đọc đầu không? | Viết lại ngắn gọn hơn |
| S8 | Có từ Hán Việt dùng sai nghĩa không? | Tra từ điển, sửa |
| S9 | Có cấu trúc ngoại ngữ bê nguyên không? | Tái cấu trúc theo tiếng Việt + VNCH Grammar |
| S10 | Có thêm nghĩa không có trong nguyên tác không? | Bỏ phần thêm |
| S11 | Có bớt nghĩa có trong nguyên tác không? | Thêm lại phần thiếu |
| S12 | Thuật ngữ có trong lexicon không? | Tra lexicon + VNCH Grammar Database, hoặc đánh dấu |
| S13 | Có dùng từ miền Bắc không? | Thay bằng dạng Nam Bộ (Style Guide Quy tắc 2) |
| S14 | Có dùng từ hiện đại áp đặt không? | Thay bằng dạng VNCH (Style Guide Quy tắc 12) |
| S15 | **Chỉ định danh từ có đúng Nam Bộ không?** | Sửa theo §1.3 |
| S16 | **Trạng từ không gian/thời gian có dùng *nầy/đó/kia* không?** | Sửa theo §1.4 |
| S17 | **Thể khía có dùng *đã... rùi/hẵng, đang... xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa... mới/mới... xong, chưa... bao giờ/vẫn chưa* không?** | Sửa theo §1.5 |
| S18 | **Câu bị động có nên chủ động hóa không?** | Áp dụng §1.6 |
| S19 | **Đại từ nhân xưng có trang trọng không?** | Sửa theo §1.7 |
| S20 | **Từ nối logic có dùng *dầu, dẫu, trái lại, tuy vậy, bởi thế, vả* không?** | Sửa theo §1.8 |

### 3.2. Lỗi thường gặp ở cấp sentence (Mở rộng từ Quality Gate + VNCH Grammar + Audit 6 chương)

| Lỗi | Mức độ | Ví dụ | Cách sửa |
|---|---|---|---|
| Thiếu đoạn giữa câu (bỏ lửng) | CRITICAL | P012: "Thuật ngữ này —" (bỏ lửng) | Hoàn tất câu, đối chiếu số câu (Quy tắc 16) |
| Bê nguyên cấu trúc bị động | MINOR | P010: "chấm dứt bởi" | Chuyển sang chủ động (§1.6, Quy tắc 26) |
| Dùng từ không chuẩn Nam Bộ | MINOR | *mặt trận hợp nhất* → *mặt trận thống nhất* | Tra lexicon + Style Guide |
| Mất nghĩa chuyên biệt | MINOR | *polymath* → *học giả lỗi lạc* | Dùng *nhà bác học* |
| Thay đổi ngữ cảnh lịch sử | MAJOR | *Annam/Tonkin* → *Trung Kỳ/Bắc Kỳ* (cũ: giữ tên Pháp trong ngoặc) | Chỉ dùng *Nam Kỳ/Bắc Kỳ/Trung Kỳ* (Quy tắc 15 mới) |
| Sai quy chiếu đại từ | MINOR | *nó* chỉ người | Dùng *người ấy/ông ấy/bà ấy* (§1.7, Quy tắc 24) |
| Sai chỉ định danh từ | MINOR | *một sách* (thiếu chỉ định) | *một cuốn sách* / *một cái sách* (§1.3, Quy tắc 21) |
| Sai trạng từ *này/nầy* | MINOR | *năm này* | *năm nầy* (§1.4, Quy tắc 22) |
| Sai thể khía *đang* | MINOR | *đang ký kết* (văn viết) | *đang tiến hành ký kết* / *đang ký kết xong* (§1.5, Quy tắc 23) |
| Sai từ nối *tuy nhiên* | MINOR | *Tuy nhiên, kết quả...* | *Tuy vậy / Đã vậy / Bởi thế* (§1.8, Quy tắc 25) |
| **Dịch từng từ ghép lại** | CRITICAL | *chính phủ, giải phóng, đồng chí, Annam* | Quy tắc 19: đọc toàn câu → tái cấu trúc |
| **Alignment lệch đoạn** | CRITICAL | Ch1: 49 src vs 50 vi (lệch từ P008) | Quy tắc 18: check src=vi trước build |

---

## 4. KIỂM SOÁT CẤP PARAGRAPH (P1–P10)

| # | Câu hỏi kiểm tra | Nếu "không" |
|---|---|---|
| P1 | Đoạn có ý chính rõ ràng không? | Xác định lại topic sentence |
| P2 | Các câu có liên kết logic không? | Sắp xếp lại, thêm từ nối §1.8 |
| P3 | Có câu nào lặp ý hoặc thừa không? | Gộp hoặc bỏ |
| P4 | Đoạn có kết thúc bằng dấu chấm hết không? | Hoàn tất câu cuối (Quy tắc 16) |
| P5 | Số câu đoạn dịch = số câu đoạn gốc không? | Kiểm tra alignment (Quy tắc 18) |
| P6 | Cước chú marker `[N]`/`N` có đúng vị trí, thứ tự không? | Điều chỉnh marker |
| P7 | Heading có marker "— đề mục —" không? | Khôi phục marker |
| P8 | Thuật ngữ trong đoạn có nhất quán không? | Thống nhất theo lexicon |
| P9 | Văn phong đoạn có tự nhiên, mượt mà không? | Viết lại câu cứng |
| P10 | Không có fabricate (số trang, trích dẫn bịa) không? | Xóa phần bịa (Quy tắc 27) |

---

## 5. KIỂM SOÁT CẤP CHAPTER (C1–C10)

| # | Câu hỏi kiểm tra | Nếu "không" |
|---|---|---|
| C1 | Toàn chương có giữ nguyên hệ thống lập luận tác giả không? | Xác định lại cấu trúc chương |
| C2 | Số đoạn src = số đoạn vi không? | Chạy `debug_align.py`, realign (Quy tắc 18) |
| C3 | Số cước chú src = số cước chú vi không? | Kiểm tra marker, build DOCX verify |
| C4 | Thuật ngữ xuyên suốt chương có nhất quán không? | Thống nhất theo lexicon |
| C5 | Văn phong chương có đồng nhất VNCH không? | Chạy `apply_vnch_fixes.py` |
| C6 | Encoding UTF-8/NFC/no BOM/LF không? | Check encoding (Quy tắc 28) |
| C7 | DOCX build `OK N/N` không? | Fix input, rebuild |
| C8 | Word `Footnotes.Count` = `notes` trong progress.json không? | Fix marker/neo cước chú |
| C9 | Footnote chân trang 9pt, đánh số 1..N không? | Check build script |
| C10 | Quality Gate 8 tiêu chí tất cả PASS không? | Chỉ HOAN_TAT khi PASS hết (Quy tắc 29) |

---

## 6. BẢNG PHÂN LOẠI LỖI (ERROR TAXONOMY) — CẬP NHẬT AUDIT

| Mã lỗi | Tên lỗi | Mức độ | Cấp độ | Ví dụ | Quy tắc sửa |
|---|---|---|---|---|---|
| E01 | Thiếu đoạn giữa câu | CRITICAL | Sentence | "Thuật ngữ này —" | Quy tắc 16, S11 |
| E02 | Alignment lệch đoạn | CRITICAL | Chapter | Ch1: 49 src vs 50 vi | Quy tắc 18 |
| E03 | Dịch từng từ ghép lại | CRITICAL | Sentence | *chính phủ, giải phóng* | Quy tắc 19 |
| E04 | Sai thuật ngữ VNCH core | CRITICAL | Sentence | *chính trị* → *chánh trị* | Quy tắc 1, 4, 12 |
| E05 | Sai từ miền Bắc | MAJOR | Sentence | *này, giải phóng, đồng chí* | Quy tắc 2, 8, 12, 22, 24 |
| E06 | Sai từ hiện đại áp đặt | MAJOR | Sentence | *tài chính, đại biểu, lương hưu* | Quy tắc 3, 4, 12 |
| E07 | Sai tên thuộc địa | MAJOR | Sentence | *Annam, Tonkin* (giữ tên Pháp) | Quy tắc 15 |
| E08 | Bê nguyên cấu trúc bị động | MINOR | Sentence | "được ký bởi" | Quy tắc 26, S18 |
| E09 | Thiếu chỉ định danh từ | MINOR | Sentence | *một sách* | Quy tắc 21, S15 |
| E10 | Sai trạng từ *này/nầy* | MINOR | Sentence | *năm này* | Quy tắc 22, S16 |
| E11 | Sai thể khía | MINOR | Sentence | *đang ký kết* | Quy tắc 23, S17 |
| E12 | Sai từ nối logic | MINOR | Sentence | *tuy nhiên* | Quy tắc 25, S20 |
| E13 | Sai đại từ nhân xưng | MINOR | Sentence | *hắn, nó* chỉ người | Quy tắc 24, S19 |
| E14 | Fabricate thông tin | CRITICAL | Paragraph | Bịa số trang, trích dẫn | Quy tắc 27 |
| E15 | Encoding sai | CRITICAL | Chapter | cp1252, BOM, CRLF | Quy tắc 28 |
| E16 | Quality Gate không PASS | CRITICAL | Chapter | Chưa đủ 8 tiêu chí | Quy tắc 29 |

---

## 7. CHECKLIST ÁP DỤNG (CẬP NHẬT)

### 7.1. Checklist mỗi câu (Sentence) — 20 mục (S1–S20)

```
[ ] S1: Chủ ngữ rõ ràng
[ ] S2: Vị ngữ đúng hành động
[ ] S3: Đối tượng rõ ràng
[ ] S4: Đại từ có quy chiếu rõ (người ấy/ông ấy/bà ấy)
[ ] S5: Mệnh đề phụ gắn đúng đối tượng
[ ] S6: Quan hệ nhân quả đúng chiều
[ ] S7: Hiểu ngay lần đọc đầu
[ ] S8: Từ Hán Việt dùng đúng nghĩa
[ ] S9: Không có cấu trúc ngoại ngữ bê nguyên
[ ] S10: Không thêm nghĩa
[ ] S11: Không bớt nghĩa
[ ] S12: Thuật ngữ có trong lexicon hoặc đã đánh dấu
[ ] S13: Không dùng từ miền Bắc
[ ] S14: Không dùng từ hiện đại áp đặt
[ ] S15: Chỉ định danh từ đúng Nam Bộ (cuốn/cái/con/cây/cục/bài)
[ ] S16: Trạng từ không gian/thời gian dùng nầy/đó/kia
[ ] S17: Thể khía đầy đủ (đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa)
[ ] S18: Bị động đã chủ động hóa (nếu tự nhiên hơn)
[ ] S19: Đại từ nhân xưng trang trọng (người ấy/ông ấy/bà ấy/họ)
[ ] S20: Từ nối logic Nam Bộ (dầu, dẫu, trái lại, tuy vậy, bởi thế, vả)
```

### 7.2. Checklist mỗi đoạn (Paragraph) — 10 mục (P1–P10)

```
[ ] P1: Ý chính rõ ràng
[ ] P2: Các câu liên kết logic (dùng từ nối §1.8)
[ ] P3: Không lặp ý, không thừa
[ ] P4: Kết thúc bằng dấu chấm (Quy tắc 16)
[ ] P5: Số câu = gốc (Quy tắc 18)
[ ] P6: Marker cước chú `[N]`/`N` đúng vị trí, thứ tự
[ ] P7: Heading có marker "— đề mục —"
[ ] P8: Thuật ngữ nhất quán trong đoạn
[ ] P9: Văn phong tự nhiên, mượt mà
[ ] P10: Không fabricate (Quy tắc 27)
```

### 7.3. Checklist mỗi chương (Chapter) — 10 mục (C1–C10)

```
[ ] C1: Giữ nguyên hệ thống lập luận tác giả
[ ] C2: Số đoạn src = số đoạn vi (debug_align.py) — Quy tắc 18
[ ] C3: Số cước chú src = số cước chú vi
[ ] C4: Thuật ngữ xuyên suốt nhất quán
[ ] C5: Văn phong VNCH đồng nhất (apply_vnch_fixes.py)
[ ] C6: Encoding UTF-8/NFC/no BOM/LF — Quy tắc 28
[ ] C7: DOCX build "OK N/N"
[ ] C8: Word Footnotes.Count = progress.json notes
[ ] C9: Footnote chân trang 9pt, đánh số 1..N
[ ] C10: Quality Gate 8 tiêu chí PASS — Quy tắc 29
```

---

## 8. TÍCH HỢP VỚI STYLE GUIDE VÀ LEXICON

1. **Trước khi dịch đoạn**: Đọc Style Guide Phan B (17+12 quy tắc) + Grammar Engine (7 bước + VNCH Grammar Database).
2. **Bước 4 (Thuật ngữ)**: Tra MASTER_LEXICON.csv → VNCH Grammar Database (§1.2-1.8) → Nguồn VNCH → Ghi dấu `[CẦN BỔ SUNG LEXICON]`.
3. **Bước 5 (Tái cấu trúc)**: Áp dụng VNCH Grammar Database (§1.3-1.8) + Quy tắc 19 (cấm dịch từng từ) + Quy tắc 20 (5 bước từ/câu khó).
4. **Bước 6 (Đối chiếu)**: Chạy S1-S20, P1-P10, C1-C10.
5. **Sau chương**: Chạy `apply_vnch_fixes.py` → `debug_align.py` → `build_chapter_docx.py` → Quality Gate 8 tiêu chí.

---

## 9. VÍ DỤ MINH HỌA: ÁP DỤNG VNCH GRAMMAR CHO P010

### Nguyên tác
> "That brief period was brought to an end by a man named Lê Lợi, the founder of the Lê Dynasty."

### Bước 1-3: Phân tích
- Chủ thể: a man named Lê Lợi (Lê Lợi)
- Vị ngữ: was brought to an end (bị chấm dứt) → bị động
- Đối tượng: that brief period (thời kỳ ngắn ngủi nầy)
- Quan hệ: không có liên từ đặc biệt

### Bước 4: Thuật ngữ + VNCH Grammar
- *Lê Dynasty* → *triều Lê* (có trong lexicon)
- *founder* → *vị vua sáng lập* (thuật ngữ chung)
- **Chỉ định**: *thời kỳ* → *một thời kỳ* / *thời kỳ nầy* (§1.3, §1.4)
- **Thể**: *was brought to an end* → đã chấm dứt (hoàn thành §1.5)

### Bước 5: Tái cấu trúc (VNCH)
- Bị động → **Chủ động hóa** (§1.6, Quy tắc 26): "Một người tên là Lê Lợi, vị vua sáng lập triều Lê, đã chấm dứt thời kỳ ngắn ngủi nầy."
- Dùng *nầy* thay *đó/ấy* (§1.4, Quy tắc 22)
- Dùng *đã... chấm dứt* thể hoàn thành (§1.5, Quy tắc 23)
- Dùng *người ấy* thay *người đó* (§1.7, Quy tắc 24)

### Bước 6: Đối chiếu
- Chủ thể: ✅ (Lê Lợi)
- Vị ngữ: ✅ (chấm dứt)
- Đối tượng: ✅ (thời kỳ ngắn ngủi nầy)
- VNCH Grammar: ✅ chỉ định, thể, chủ động, trạng từ *nầy*, đại từ *người ấy*
- Thêm/bớt: ✅ không có

### Bước 7: Dễ hiểu
- Đọc: "Một người tên là Lê Lợi, vị vua sáng lập triều Lê, đã chấm dứt thời kỳ ngắn ngủi nầy." → hiểu ngay. ✅

---

## 10. BÀI HỌC TRÁNH LẶP TỪ AUDIT 6 CHƯƠNG ĐẦU (§10 — MỚI)

### 10.1 Alignment đoạn văn — Lỗi nghiêm trọng nhất
**Vấn đề**: Ch1 lệch từ P008, thiếu 11 đoạn cuối "Anglophone Histories"; Ch5 chỉ 9 block thay vì 15 đoạn.
**Nguyên nhân**: Dịch không giữ mapping 1-1; footnotes chen lấn; dịch gộp nhiều đoạn.
**Giải pháp**: 
- Script `debug_align.py` kiểm tra src paragraphs = vi paragraphs TRƯỚC KHI build DOCX.
- Script `ch01_realign.py` / `ch05_realign.py` căn lại theo sentence-level alignment.
- Luôn đối chiếu số câu mỗi đoạn (P5, S11).

### 10.2 Thuật ngữ VNCH — 222 lỗi fix hàng loạt
**Vấn đề**: 222 lỗi thuật ngữ sai (chính trị→chánh trị 69 lần, này→nầy 47 lần, Annam/Tonkin/Cochinchina/Indochine 38 lần, giải phóng/đồng chí 49 lần, tài chính/đại biểu/lương hưu 21 lần, từ nối logic 45 lần).
**Giải pháp**: Script `apply_vnch_fixes.py` áp dụng 30 quy tắc VNCH Grammar + Style Guide tự động SAU KHI DỊCH XONG, TRƯỚC KHI build DOCX.
**False positive**: 43 "lỗi" trong tên sách/trích dẫn/tổ chức tiếng Pháp — KHÔNG SỬA (Style Guide Quy tắc 15).

### 10.3 Dịch từng từ ghép lại — Cấm kị
**Vấn đề**: Nhiều câu dịch máy từng từ (chính phủ, giải phóng, đồng chí, Annam/Tonkin) tạo câu cứng, sai ngữ pháp, sai thuật ngữ.
**Giải pháp**: Quy tắc 19 (CẤM KỊ) + Quy trình Bước 5: đọc toàn câu/đoạn/ngữ cảnh → phân tích chủ thể/vị ngữ/đối tượng/quan hệ logic → tra lexicon/VNCH Grammar → tái cấu trúc câu Việt tự nhiên.

### 10.4 Xử lý từ/câu khó — Quy trình 5 bước bắt buộc (Quy tắc 20)
**Khi gặp từ/câu khó**: KHÔNG `UNRESOLVED`, KHÔNG bỏ qua, KHÔNG dịch từng từ.
Phải làm: (1) Mở rộng ngữ cảnh → (2) Xác định ý đồ tác giả → (3) Tra cứu nguồn → (4) Đối chiếu chỗ khác → (5) Tái dựng ý nghĩa → diễn đạt VNCH.
**Ghi nhận**: Căn cứ văn bản, ngữ cảnh, nguồn, lập luận; Phân biệt nghĩa nguyên văn/ngữ cảnh/diễn đạt; Mức độ chắc chắn + lý do.

### 10.5 VNCH Grammar Database — Tích hợp bắt buộc
**21 quy tắc Grammar** (§1.3-1.8 + Quy tắc 21-26) phải áp dụng cho MỖI CÂU:
- Chỉ định: *cuốn/cái/con/cây/cục/bài* (Quy tắc 21)
- Trạng từ: *nầy/đó/kia* (Quy tắc 22)
- Thể: *đã...rùi/hẵng, đang...xong/tiến hành, sắp sẽ/chuẩn bị sẽ, vừa...mới/mới...xong, chưa...bao giờ/vẫn chưa* (Quy tắc 23)
- Đại từ: *người ấy/ông ấy/bà ấy/họ* (Quy tắc 24)
- Từ nối: *dầu/dẫu, trái lại, tuy vậy/đã vậy/song, bởi thế/do đó/cho nên, vả/lại/cũng* (Quy tắc 25)
- Chủ động hóa (Quy tắc 26)

### 10.6 Encoding & Quality Gate — Không dung túng
**Encoding**: UTF-8, NFC, no BOM, LF (Quy tắc 28). PowerShell không dùng heredoc tiếng Việt.
**Quality Gate**: 8 tiêu chí CẤT BUỘC PASS mới được HOAN_TAT (Quy tắc 29).

---

## 11. WORKFLOW TÍCH HỢP CHO MỖI CHƯƠNG TIẾP THEO (§11 — MỚI)

### 11.1 Trước khi bắt đầu
1. Đọc `progress.json` → xác định chương tiếp theo.
2. Đọc `STYLE_GUIDE_PHAN_B.md` (v2.3, 29 quy tắc) + `TRANSLATION_GRAMMAR_ENGINE.md` (v2.1).
3. Đọc `MASTER_LEXICON.csv` + `AUDIT_REPORT_CH01-06.md` (§10).
4. Chạy `debug_align.py` trên chương trước (nếu có) để verify quy trình.

### 11.2 Khi dịch
1. **Bước 1-3**: Phân tích ngữ pháp, chủ thể/vị ngữ/đối tượng, quan hệ logic (§1.8).
2. **Bước 4**: Tra lexicon → VNCH Grammar Database → nguồn VNCH → `[CẦN BỔ SUNG LEXICON]`.
3. **Bước 5**: Tái cấu trúc theo VNCH Grammar (§1.3-1.8) + Quy tắc 19, 20.
4. **Bước 6**: Đối chiếu S1-S20, P1-P10, alignment (Quy tắc 18).
5. **Bước 7**: Kiểm tra dễ hiểu.

### 11.3 Sau khi dịch xong chương
1. Chạy `apply_vnch_fixes.py` (30 quy tắc VNCH).
2. Chạy `debug_align.py` → nếu lệch → `realign.py` (sentence-level).
3. Chạy `build_chapter_docx.py` → verify `OK N/N`.
4. Word COM check: `Footnotes.Count` = `notes` trong progress.json.
5. Cập nhật `progress.json` (status, paragraphs, footnotes, pages, docx, docx_status).
6. Quality Gate 8 tiêu chí PASS → đánh dấu `HOAN_TAT`.

### 11.4 Dọn dẹp
- Xóa file tạm `tmp_*`, `debug_*` trong workspace gốc.
- File dịch FINAL: `04_translation/v1/chNN/v1_chNN_vi_FINAL.txt`.
- DOCX: `09_docx/V1-CNN_<slug>.docx`.
- Scripts: `99_scripts/`.

---

## 12. TRẠNG THÁI VÀ BƯỚC TIẾP THEO

### 12.1 Trạng thái

- **Grammar Engine v2.1** (có VNCH Grammar Database + Audit 6 chương): HOÀN THÀNH.
- **Style Guide Phan B v2.3** (29 quy tắc): HOÀN THÀNH.
- **Master Lexicon**: 321 mục, cần bổ sung thuật ngữ VNCH Grammar (§1.2-1.8).
- **Pilot V1-Ch1 đến V1-Ch6**: HOÀN TẤT (Audit PASS, DOCX PASS).
- **V1-Ch7 đến V1-Ch21**: CHƯA BẮT ĐẦU.

### 12.2 Giai đoạn tiếp theo

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| **1. Grammar Engine** | Bộ quy tắc dịch thuật + VNCH Grammar Database + Audit lessons | ✅ HOÀN THÀNH v2.1 |
| **2. Style Guide + Lexicon** | Bổ sung thuật ngữ VNCH Grammar vào Lexicon, cập nhật 29 quy tắc | ⏳ TIẾP THEO |
| **3. V1-Ch7 pilot** | Áp dụng v2.1 + v2.3 cho chương 7, verify Quality Gate | ⏳ |
| **4. V1-Ch8-V1-Ch21** | Lặp quy trình 11.1-11.4 cho 14 chương còn lại | ⏳ |

### 12.3 Nguyên tắc cốt lõi

Grammar Engine v2.1 này là **bộ quy tắc áp dụng lặp lại cho toàn bộ 77 chương**, tích hợp:
- Ngữ pháp miền Nam VNCH từ nguồn sơ cấp (Phan Khôi 1955, Lê Văn Đức 1970, Bách Khoa 1957-1975, Hiến pháp 1967, Thompson 1987, Clark 1974).
- Bài học thực tế từ Audit 6 chương đầu (Alignment, VNCH terminology, Word-for-word ban, Hard terms workflow, Grammar integration, Encoding/QA Gate).

**Mỗi câu dịch phải đi qua 7 bước, mỗi đoạn qua P1-P10, mỗi chương qua C1-C10, mỗi câu phải đạt S1-S20.**

**Không được rút gọn quy trình vì "để nhanh". Một câu dịch đạt chuẩn quan trọng hơn mười câu dịch nhanh.**

---

*Hết Translation Grammar Engine v2.1 — Cập nhật sau Audit 6 chương đầu (2026-11-19).*