# Báo cáo Lab: Self evolving Agentic

> Sao chép tệp này thành `report/REPORT.md` (đã làm ở Phần 0) và điền dần qua các Phần của lab. Xóa các dòng hướng dẫn dạng trích dẫn (bắt đầu bằng `>`). Văn phong kỹ thuật, ngắn gọn, mọi nhận định đi kèm số liệu hoặc bằng chứng. Trong buổi học: điền mục 1 đến 7 (bản nháp). Sau buổi học: hoàn thiện mục 8 đến 10.

## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| | | |

- Nhà cung cấp và mô hình (`LAB_MODEL`, không ghi khóa API), nhiệt độ (`LAB_TEMPERATURE`), `recursion_limit`:
- Phiên bản Deep Agents (`pip show deepagents`), hệ điều hành, chạy trực tiếp hay trong Docker:
- Số lần chạy tác vụ đã dùng / ngân sách:
- Commit của tag `freeze`:

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)

> Dự đoán điều kiện nào đạt điểm cao nhất trên **tác vụ đánh giá** và vì sao. Nêu căn cứ từ phân loại lỗi (mục 4) và từ tài liệu tham khảo. Điền cả ba dòng; `verify_freeze.py` kiểm tra điều này.

- H1 (subagents so với baseline): `subagents` sẽ KHÔNG cao hơn `baseline` về điểm trên tác vụ đánh giá (dự đoán chênh lệch trong khoảng ±1 check) và tốn token gấp khoảng 1,5 đến 2 lần. Lý do: ở giai đoạn học, `subagents` đạt đúng cùng 17/27 check với `baseline`, chỉ khác ở token (803.466 so với 460.592, gấp 1,74 lần); các check thất bại đều là check quy ước `rule_` mà đề bài không nêu, nên giao việc cho subagent không đưa thêm thông tin quy ước nào. Căn cứ tài liệu: bài báo của Anthropic về hệ thống nghiên cứu đa tác tử ghi nhận chi phí token cao hơn nhiều so với một tác tử.
- H2 (skills-auto so với baseline): `skills-auto` sẽ cao hơn `baseline` không đáng kể trên tác vụ đánh giá (dự đoán +0 đến +2 check trên tổng 9 đến 10 check mỗi họ), và chủ yếu ở các quy ước đã xuất hiện ở tác vụ học (chú thích kiểu, test hồi quy, changelog), không ở quy ước mới của tác vụ đánh giá. Lý do: ở giai đoạn học, skill chỉ giúp thêm 1 check (`rule_type_hints`, 18/27 so với 17/27), cả hai skill đều được đọc (`skills_read` = 2) nhưng các quy tắc cụ thể về tiền theo cent, khối `meta`, sắp xếp, tiêu đề lược đồ không được viết đủ chi tiết nên tác tử không làm theo. Căn cứ: SkillsBench ghi nhận skill do mô hình tự sinh trung bình không có lợi.
- H3 (tác vụ học so với tác vụ đánh giá): điểm `skills-auto` trên tác vụ đánh giá sẽ thấp hơn hoặc bằng điểm trên tác vụ học, tức lợi ích (nếu có) không chuyển sang tác vụ mới. Lý do: tác vụ đánh giá có thêm một quy ước mới không có trong phản hồi của tác vụ học nên curator không thể viết trước được; skill sinh ra chứa các quy tắc gắn với quy ước của tác vụ học. Căn cứ: SkillEvolBench ghi nhận lợi ích trên tác vụ học thường không chuyển sang tác vụ mới (quá khớp).

## 3. Làm quen Deep Agents (Phần 0.3)

1. Công cụ mặc định (kết quả `python scripts/tour.py`): `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep` (công cụ tệp), `execute` (shell) và `task` (giao việc cho subagent). Chỉ `execute` cho phép chạy lệnh.
2. Mô tả của `task` nói `general-purpose` là subagent cho "complex questions, searching for files and content, and executing multi-step tasks", và "has access to all tools as the main agent". Mỗi lần gọi là một subagent tạm thời, không giữ trạng thái: "the agent sees only the prompt you give it and returns a single final report". Vì vậy nó không thấy ngữ cảnh hội thoại của tác tử chính, chỉ thấy nội dung prompt mà tác tử chính gửi.
3. Câu hướng dẫn hành vi trong mô tả `task`: "Launch multiple agents concurrently when their tasks are independent, using a single message with multiple tool calls." Câu trong mô tả `execute`: "You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search."

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

> Chỉ dùng tác vụ học. Mỗi dòng là một check thất bại.

| Tác vụ | Check thất bại | Nhóm lỗi (A-G) | Bằng chứng (trích ngắn từ `detail` hoặc vết) |
|---|---|---|---|
| | | | |

Nhận xét: nhóm lỗi nào chiếm đa số? Skill có thể phòng ngừa nhóm đó không?

## 5. Điều kiện `subagents` (Phần 2.3)

- Các subagent đã định nghĩa (tên, vai trò, lý do thiết kế):
- `subagent_calls` ở từng tác vụ và nhận xét (kể cả trường hợp bằng 0):
- Thông tin thiếu hoặc thừa khi giao việc (nếu có giao việc):
- Ảnh hưởng đến token và thời gian:

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Số lần chạy curator, số skill bị xóa và lý do:

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai (nêu chỗ sai nếu có) | Độ dài, `description` và `skills_read` ở Phần 3.4 |
|---|---|---|---|
| | | | |

## 7. Kết quả so sánh (Phần 4.3, 4.4)

> Dán nội dung `report/table.md` và kết quả `python scripts/check_breakdown.py`. Nêu các lần chạy có `error` hoặc `skills_modified = true` (nếu có) và cách xử lý.

```text
(dán bảng ở đây)
```

## 8. Phân tích

> Trả lời từng câu bằng số liệu từ mục 7 và bằng chứng từ vết. Kết quả âm hoặc không có khác biệt vẫn hợp lệ nếu được phân tích tốt.

1. So với `baseline`, điều kiện nào cải thiện điểm tác vụ **học**? Điều kiện nào cải thiện điểm tác vụ **đánh giá**? Có điều kiện nào cải thiện tác vụ học nhưng không cải thiện tác vụ đánh giá? Nếu có, đó là dấu hiệu gì?
2. Tách điểm thành check kỹ thuật và check quy ước (`rule_`). Skill do curator sinh giúp nhóm check nào? Check quy ước **mới** của tác vụ đánh giá có được skill giúp không, và vì sao?
3. Dựa vào vết và `skills_read`, giải thích một check mà skill giúp đạt và một check mà skill không giúp (skill chưa được đọc, đọc nhưng không làm theo, skill thiếu hoặc sai).
4. Chi phí: so sánh số token trung bình giữa các điều kiện. Điều kiện nào có hiệu quả tốt nhất theo điểm trên mỗi token? Đa tác tử có đáng chi phí trong thí nghiệm này không?
5. Có dấu hiệu rò rỉ dữ liệu hoặc quá khớp nào trong skill sinh ra không? Nhóm đã phòng tránh như thế nào?
6. Nhiễu: so sánh điểm tác vụ học của cùng bộ skill ở Phần 3.4 (đã sao lưu) và sau đóng băng. Chênh lệch bao nhiêu? Nó cho biết điều gì về độ tin cậy của các chênh lệch trong bảng ở mục 7?

## 9. Hạn chế và tính hợp lệ

> Nêu ít nhất 3 hạn chế và ảnh hưởng của từng hạn chế đến kết luận (ví dụ: chỉ 3 tác vụ mỗi vai trò, mỗi cấu hình chạy một lần, nhiễu của mô hình, tác vụ do giảng viên thiết kế sẵn quy ước, chỉ một mô hình).

1.
2.
3.

## 10. Kết luận

> Tối đa 5 câu. Chỉ khẳng định điều số liệu hỗ trợ. Nêu một đề xuất cải tiến tiếp theo.

## Phụ lục

- Lệnh đã chạy (theo thứ tự):
- Thử thách mở rộng (nếu có): hướng chọn, kết quả, nhận xét.
- Ghi chú khác:
