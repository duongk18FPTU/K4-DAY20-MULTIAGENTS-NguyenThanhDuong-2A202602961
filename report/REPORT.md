# Báo cáo Lab: Self evolving Agentic


## 1. Thông tin nhóm và cấu hình

| Họ tên | Mã sinh viên | Phần đóng góp |
|---|---|---|
| Nguyễn Thành Dương | 2A202602961 | Toàn bộ (làm cá nhân) |

- Mô hình: `google_genai:gemini-3.5-flash-lite` (khóa API Gemini gói miễn phí, không ghi khóa vào báo cáo). `LAB_TEMPERATURE=0` đã đặt, nhưng thư viện cảnh báo mô hình này dùng tham số lấy mẫu cố định nên `temperature` bị bỏ qua. `recursion_limit` = 60 (mặc định của `runner`).
- Deep Agents 0.7.21, LangChain 1.4.3, Python 3.12. Máy chủ là Windows 10; shell của tác tử cần `/bin/sh` nên toàn bộ lệnh `pytest`, `runner`, `curator` chạy trong Docker (`python:3.12-slim`, xem `Dockerfile`), thư mục kho được gắn vào `/lab`. Các script chỉ đọc dữ liệu (`compare`, `check_breakdown`, `verify_freeze`) chạy bằng venv trên máy chủ.
- Số lần chạy: 9 lần chạy Gemini hoàn chỉnh ở giai đoạn học (3 điều kiện x 3 tác vụ học), cộng các lần chạy bổ sung nằm trong các thư mục lưu riêng (xem Phụ lục). **Chưa chạy lần nào trên tác vụ đánh giá**: hạn mức miễn phí 500 request mỗi ngày mỗi mô hình của Gemini đã hết (lỗi 429 `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, hồi lại sau khoảng 6 giờ 40 phút) và phải nộp bài trước thời điểm đó.
- Commit của tag `freeze`: `4130524` (commit `hypotheses`: `0201fab`).

## 2. Giả thuyết (commit TRƯỚC tag `freeze`, Phần 4.0)


- H1 (subagents so với baseline): `subagents` sẽ KHÔNG cao hơn `baseline` về điểm trên tác vụ đánh giá (dự đoán chênh lệch trong khoảng ±1 check) và tốn token gấp khoảng 1,5 đến 2 lần. Lý do: ở giai đoạn học, `subagents` đạt đúng cùng 17/27 check với `baseline`, chỉ khác ở token (803.466 so với 460.592, gấp 1,74 lần); các check thất bại đều là check quy ước `rule_` mà đề bài không nêu, nên giao việc cho subagent không đưa thêm thông tin quy ước nào. Căn cứ tài liệu: bài báo của Anthropic về hệ thống nghiên cứu đa tác tử ghi nhận chi phí token cao hơn nhiều so với một tác tử.
- H2 (skills-auto so với baseline): `skills-auto` sẽ cao hơn `baseline` không đáng kể trên tác vụ đánh giá (dự đoán +0 đến +2 check trên tổng 9 đến 10 check mỗi họ), và chủ yếu ở các quy ước đã xuất hiện ở tác vụ học (chú thích kiểu, test hồi quy, changelog), không ở quy ước mới của tác vụ đánh giá. Lý do: ở giai đoạn học, skill chỉ giúp thêm 1 check (`rule_type_hints`, 18/27 so với 17/27), cả hai skill đều được đọc (`skills_read` = 2) nhưng các quy tắc cụ thể về tiền theo cent, khối `meta`, sắp xếp, tiêu đề lược đồ không được viết đủ chi tiết nên tác tử không làm theo. Căn cứ: SkillsBench ghi nhận skill do mô hình tự sinh trung bình không có lợi.
- H3 (tác vụ học so với tác vụ đánh giá): điểm `skills-auto` trên tác vụ đánh giá sẽ thấp hơn hoặc bằng điểm trên tác vụ học, tức lợi ích (nếu có) không chuyển sang tác vụ mới. Lý do: tác vụ đánh giá có thêm một quy ước mới không có trong phản hồi của tác vụ học nên curator không thể viết trước được; skill sinh ra chứa các quy tắc gắn với quy ước của tác vụ học. Căn cứ: SkillEvolBench ghi nhận lợi ích trên tác vụ học thường không chuyển sang tác vụ mới (quá khớp).

## 3. Làm quen Deep Agents (Phần 0.3)

1. Công cụ mặc định (kết quả `python scripts/tour.py`): `ls`, `read_file`, `write_file`, `edit_file`, `delete`, `glob`, `grep` (công cụ tệp), `execute` (shell) và `task` (giao việc cho subagent). Chỉ `execute` cho phép chạy lệnh.
2. Mô tả của `task` nói `general-purpose` là subagent cho "complex questions, searching for files and content, and executing multi-step tasks", và "has access to all tools as the main agent". Mỗi lần gọi là một subagent tạm thời, không giữ trạng thái: "the agent sees only the prompt you give it and returns a single final report". Vì vậy nó không thấy ngữ cảnh hội thoại của tác tử chính, chỉ thấy nội dung prompt mà tác tử chính gửi.
3. Câu hướng dẫn hành vi trong mô tả `task`: "Launch multiple agents concurrently when their tasks are independent, using a single message with multiple tool calls." Câu trong mô tả `execute`: "You MUST avoid using search commands like find and grep. Instead use the grep, glob tools to search."

## 4. Đường cơ sở và phân loại lỗi (Phần 2.2)

Dữ liệu: `results/baseline/` (Gemini). Mỗi dòng là một check thất bại của tác vụ học.

| Tác vụ | Check thất bại | Nhóm lỗi | Bằng chứng |
|---|---|---|---|
| code-learn | `tests_not_modified` | G (lỗi môi trường, không phải lỗi của tác tử) | Vết chỉ ghi tệp mới `workspace/tests/test_additional.py` và chỉ đọc `test_report.py`; không có lệnh sửa tệp test gốc. Nguyên nhân: kho bật `core.autocrlf=true` nên `test_report.py` có đuôi dòng CRLF, SHA-256 là `efb5e765...`; sau khi chuyển về LF là `79e05f4c...`, đúng bằng hash trong `check.py`. Chạy lại baseline sau khi sửa (`autocrlf=false`, checkout lại `tasks/`) cho 7/10 và check này đạt (`results-gemini-clean-rerun/`). |
| code-learn | `rule_type_hints` | E | `detail`: "RULE: every public function ... has type annotations on all parameters and on the return value." Quy ước không có trong đề. |
| code-learn | `rule_regression_tests` | E | "RULE: add tests/test_regressions.py with one test function per bug you fixed (at least 3)". |
| code-learn | `rule_changelog` | E | "RULE: record each fix in CHANGELOG.md under '## Unreleased' as a bullet '- fix(<function name>): ...'". |
| data-learn | `rule_money_in_cents` | E | "RULE: money values in answer.json are integer cents (1606.67 USD is written 160667)." |
| data-learn | `rule_meta_block` | E | "RULE: answer.json has an object `meta` = {source, rows_in, rows_used}." |
| data-learn | `rule_clean_csv` | E | "RULE: write workspace/clean.csv with the header order_id,timestamp_utc,region,amount_cents ...". |
| logs-learn | `rule_service_names` | E | "RULE: service names ... lower-case with '-' replaced by '_'". |
| logs-learn | `rule_sorted_errors` | E | "RULE: `errors` is sorted by service, then by timestamp_utc, ascending." |
| logs-learn | `rule_schema_header` | E | "RULE: the top-level object has "schema_version": 2 and "generated_by": "log-triage"." |

Nhận xét. 9 trên 10 check thất bại thuộc nhóm E (quy ước tổ chức: tên `rule_`, `detail` bắt đầu bằng `RULE:`); check còn lại là lỗi môi trường. **Bằng chứng phủ định cho các nhóm A đến D** (`python scripts/check_breakdown.py`): check kỹ thuật đạt 17/18 ở `baseline` và 17/18 ở `subagents`, trong đó chỉ `tests_not_modified` thất bại và đó là lỗi môi trường nêu trên (loại ra là 18/18), còn check quy ước đạt 0/9 ở cả hai điều kiện. Trong vết của baseline `code-learn`, tác tử có đọc docstring và README, sửa các hàm đúng nguyên nhân và chạy lại `pytest` (không thuộc A, B, C). Với nhóm F, tôi chỉ đọc kỹ thông điệp cuối của `code-learn` và thấy nó chỉ liệt kê tệp thật sự sửa; chưa kiểm tra mọi vết nên không khẳng định cho nhóm này. Nguyên nhân chung của nhóm E: đề bài chỉ nói chung "Acme conventions" và các quy ước cụ thể nằm ở nơi tác tử không tự đi tìm. Skill có thể phòng ngừa nhóm này nếu nêu đủ chi tiết quy ước, nhưng chỉ khi quy ước đó lặp lại ở tác vụ mới (xem mục 6 và 8).

## 5. Điều kiện `subagents` (Phần 2.3)

- Subagent đã định nghĩa (`src/lab/subagents.py`): `explorer` (chỉ đọc README, docstring, mẫu dữ liệu và báo cáo quy ước; dùng đầu tiên), `implementer` (thực hiện thay đổi, chạy test hoặc script, báo cáo thật; `description` yêu cầu truyền ĐỦ quy tắc vì subagent chỉ thấy prompt được gửi), `reviewer` (kiểm tra độc lập ở cuối, không sửa). Ba vai trò tách biệt theo quy trình đọc, làm, kiểm.
- `subagent_calls` (từ `run.json`): code-learn 1 (explorer), data-learn 4 (explorer x2, implementer, reviewer), logs-learn 2 (explorer, reviewer). Tác tử chính có giao việc ở cả 3 tác vụ, và giao nhiều hơn khi tác vụ phức tạp hơn (data-learn).
- Thông tin khi giao việc (trích `trace.md`): lời giao việc cho `explorer` ở data-learn chỉ nói "check Acme reporting conventions" mà không nêu quy ước cụ thể (tác tử chính cũng chưa biết), và lời giao cho `implementer` chứa cả đoạn tự suy nghĩ dở dang ("Wait, let's check what README says ...") thay vì một bản đặc tả sạch. Tác tử chính không kiểm lại độc lập báo cáo của subagent; `reviewer` xác nhận kết quả nhưng vẫn không bắt được lỗi nhóm E vì cũng không biết quy ước. Vết chỉ ghi luồng chính nên việc subagent làm bên trong không quan sát được.
- Token và thời gian: tổng 803.466 token so với 460.592 của baseline (gấp 1,74 lần): code-learn 225k so với 167k (1,35 lần), data-learn 417k so với 223k (1,87 lần), logs-learn 161k so với 71k (2,26 lần). Thời gian dài hơn tương ứng (115,7 s so với 53,9 s ở code-learn). Điểm không đổi (17/27 cả hai). Số liệu bổ sung từ lần chạy GLM trên NVIDIA (`results-nvidia-glm/`): logs-learn `subagents` 206k token so với baseline 66k (gấp 3,1 lần), cùng điểm 6/9.

## 6. Self-evolving: skill do curator sinh (Phần 3)

- Lần chạy curator: (a) lần đầu với Gemini sinh 0 skill vì lỗi mã của tôi: Gemini trả `content` là danh sách các phần (`[{"type": "text", "text": ...}]`) nên `parse_skill_blocks(str(reply))` không khớp; tôi sửa `curate_skills` lấy `response.text`; (b) lần chạy sau khi sửa sinh 2 skill, là bộ skill được đóng băng; (c) trước đó, với GLM trên NVIDIA, curator sinh 3 skill (lưu ở `results-nvidia-glm/skills-auto-generated/`, không dùng cho kết quả chính vì đổi mô hình). Không xóa skill nào và không sửa tay skill nào.
- Hạn chế của bộ skill đã đóng băng: curator đọc phản hồi của check `tests_not_modified`, là lỗi giả do CRLF (mục 4), nên dòng "Never modify original test files" trong `software-repo-constraints` xuất phát từ lỗi môi trường chứ không từ hành vi sai của tác tử. Tôi phát hiện sau khi curator đã chạy; lẽ ra phải chạy lại curator (còn trong ngân sách 2 lần chạy lại) nhưng hạn mức API đã hết (mục 1) nên giữ nguyên bộ skill này.

| Skill | Tổng quát hay riêng cho tác vụ học? | Đúng hay sai | Độ dài, `description`, `skills_read` (Phần 3.4) |
|---|---|---|---|
| `adhere-to-formatting-and-naming-rules` | Nửa tổng quát: mở đầu chung ("read all schema requirements"), nhưng ví dụ trong thân lấy từ quy ước của tác vụ học ("integer cents", "UTC ISO formats", "underscore replacements for hyphens", "metadata blocks", "schema version headers"). Có rủi ro quá khớp. | Không sai và không gây hại, nhưng quá mơ hồ để thực thi: không nêu cấu trúc `meta`, thứ tự sắp xếp hay giá trị `schema_version`. | 7 dòng, ngắn. `description`: "Use when generating JSON, CSV, or structured output files where specific naming, keys, casing, or value representations are requested." Rộng, khớp cả 3 tác vụ. Được đọc ở cả 3 lần chạy (`skills_read` = 2, cùng với skill kia). |
| `software-repo-constraints` | Một phần: các quy tắc về tệp test gốc, test hồi quy, changelog, chú thích kiểu đều là quy ước của tác vụ học họ `code`; áp dụng được cho tác vụ sửa mã có cùng quy ước, không cho họ khác. | Một dòng xuất phát từ lỗi giả (không sửa tệp test gốc; vô hại vì đề cũng nói vậy). Các dòng còn lại đúng nhưng thiếu định dạng chính xác. | 8 dòng. `description`: "Use when fixing bugs, adding features, or modifying codebases that have strict repository structure and process rules." Được đọc ở cả 3 lần chạy dù chỉ liên quan tới tác vụ code. |

Dev (Phần 3.4), `results/skills-auto-dev/`: cả 3 lần chạy đọc cả 2 skill (`skills_read` = 2, `skills_modified` = false). Mức độ làm theo ở mục 8.

## 7. Kết quả so sánh (Phần 4.3, 4.4)

**Bảng chính** (`report/table.md`, do `python -m lab.compare` sinh ra từ `results/`). Cột `skills-auto` không có và hàng tác vụ đánh giá trống vì **chưa có lần chạy chính thức nào sau freeze và chưa có lần chạy nào trên tác vụ đánh giá** (hết hạn mức API, mục 1):

```text
| Task | baseline | subagents |
|---|---|---|
| code-learn | 6/10 | 6/10 |
| data-learn | 5/8 | 5/8 |
| logs-learn | 6/9 | 6/9 |
| **Mean score - learning tasks** | 0.63 | 0.63 |
| **Mean score - evaluation tasks** | - | - |
| **Mean tokens per run** | 153,530 | 267,822 |
| **Runs that read a skill** | 0/3 | 0/3 |
```

**Bảng phụ**: các lần chạy `skills-auto` ở giai đoạn phát triển (Phần 3.4, chạy TRƯỚC khi đóng băng, đã chuyển sang `results/skills-auto-dev/` theo GUIDE). Không dùng được như kết quả chính thức vì chạy trước tag `freeze`; chỉ để mô tả:

```text
| Task | baseline | subagents | skills-auto |
|---|---|---|---|
| code-learn | 6/10 | 6/10 | 7/10 |
| data-learn | 5/8 | 5/8 | 5/8 |
| logs-learn | 6/9 | 6/9 | 6/9 |
| **Mean score - learning tasks** | 0.63 | 0.63 | 0.66 |
| **Mean score - evaluation tasks** | - | - | - |
| **Mean tokens per run** | 153,530 | 267,822 | 156,600 |
| **Runs that read a skill** | 0/3 | 0/3 | 3/3 |
```

`python scripts/check_breakdown.py` (chỉ hai điều kiện có kết quả chính thức):

```text
condition     role    technical  house rules  mean tokens  read a skill
baseline      learn    17/18         0/9          153,530      0/3
subagents     learn    17/18         0/9          267,822      0/3
```

Cho `skills-auto-dev` (tự đếm từ `run.json`): check kỹ thuật 17/18, check quy ước 1/9 (`rule_type_hints` ở code-learn), token trung bình 156.600, đọc skill 3/3.

Các lần chạy lỗi hoặc không dùng: lần chạy `subagents` code-learn cuối cùng bị 429 (hết hạn mức ngày), ghi nhận là lỗi hạ tầng và không dùng (`results-infra-errors/subagents-code-learn-429/`). Lần chạy `baseline` code-learn sau khi sửa CRLF (7/10) nằm ở `results-gemini-clean-rerun/` và không thay vào bảng chính, để cả 9 lần chạy cùng một điều kiện môi trường. Không lần chạy nào có `skills_modified = true`. `python scripts/verify_freeze.py` (với `PYTHONUTF8=1`) báo `OK` nhưng chỉ vì `checked 0 runs of skill conditions`: nó chỉ xác nhận có commit `hypotheses` đã điền H1 đến H3 đứng trước tag `freeze` và `skills/` không đổi từ tag, không xác nhận được gì về kết quả chính thức.

## 8. Phân tích

1. **Tác vụ học và đánh giá.** Trên tác vụ học: `subagents` không cải thiện (17/27, bằng baseline); `skills-auto` (dev) cải thiện 1 check (18/27; code-learn 7/10 so với 6/10; điểm trung bình 0,66 so với 0,63). **Trên tác vụ đánh giá không có số liệu nào**, nên không trả lời được phần còn lại của câu hỏi (cải thiện học nhưng không cải thiện đánh giá) và không kiểm chứng được H1 đến H3 bằng dữ liệu. Chênh lệch +1 check trên 27 trong một lần chạy là quá nhỏ để coi là hiệu quả thật.
2. **Check kỹ thuật so với quy ước.** Check kỹ thuật gần như đạt hết ở mọi điều kiện (17/18; lỗi duy nhất là lỗi môi trường). Check quy ước: baseline 0/9, subagents 0/9, skills-auto-dev 1/9. Skill chỉ giúp thêm `rule_type_hints`. Tác vụ đánh giá có quy ước mới nên chưa thể nói skill có giúp hay không; có thể suy luận rằng skill không chứa được quy ước mà curator chưa từng thấy, nhưng đó chỉ là suy luận.
3. **Một check skill giúp, một check không.** *Giúp*: `rule_type_hints` ở code-learn. Skill `software-repo-constraints` được đọc từ đầu (`skills_read` = 2 trong `run.json`; `trace.md` có các lệnh `read_file` tới `skills/.../SKILL.md`) và có dòng rõ ràng "Ensure all public functions have complete type annotations on all parameters and return values"; tác tử làm theo và check đạt. *Không giúp*: `rule_changelog` và `rule_regression_tests` ở cùng lần chạy. Skill được đọc nhưng chỉ nói chung "changelog under the designated heading" và "specified count and filename conventions"; tác tử thêm bullet tự do dạng "- Fixed price parsing ..." thay vì `- fix(<function>): ...`, và đặt tên tệp `workspace/tests/test_regression.py` (số ít) thay vì `test_regressions.py`. Đây là trường hợp "đọc nhưng chỉ làm một phần" vì skill thiếu định dạng chính xác. Ở data-learn và logs-learn, skill `adhere-to-formatting-and-naming-rules` được đọc nhưng các check `rule_` vẫn thất bại vì skill không nêu cấu trúc cụ thể.
4. **Chi phí.** Token trung bình mỗi lần chạy: baseline 153.530, subagents 267.822 (gấp 1,74 lần), skills-auto-dev 156.600 (gấp 1,02 lần). Số check đạt trên 100 nghìn token: baseline 3,69, subagents 2,12, skills-auto-dev 3,83. Đa tác tử không đáng chi phí trong thí nghiệm này: thêm 74% token, thời gian gần gấp đôi và không thêm check nào, vì các lỗi là nhóm E mà subagent cũng không biết quy ước.
5. **Rò rỉ và quá khớp.** Không có rò rỉ vật chất của tác vụ đánh giá: curator chỉ đọc tác vụ học (`role == "learn"`), `validate_skill` kiểm tra bằng `eval_markers()` và cả hai skill hợp lệ; tôi cũng không mở `tasks/*-eval/` trước freeze. Có dấu hiệu quá khớp: các skill mang theo giá trị quy ước của tác vụ học (cent, đổi dấu gạch nối, test hồi quy, changelog). Vì chưa chạy tác vụ đánh giá nên chưa đo được mức quá khớp thực tế.
6. **Nhiễu.** Không so sánh được điểm tác vụ học của Phần 3.4 với điểm sau đóng băng vì không có lần chạy sau đóng băng. Có hai gợi ý gián tiếp: `baseline` code-learn chạy hai lần cho 6/10 (còn lỗi CRLF) và 7/10 (đã sửa); chênh lệch này giải thích được bằng lỗi môi trường, còn token chênh 3,6% (166.579 và 160.661). Trên NVIDIA/GLM, baseline đạt 5/8, 6/10, 6/9, trùng điểm với Gemini ở cả 3 tác vụ, cho thấy điểm khá ổn định giữa hai mô hình nhưng vẫn chỉ là một lần chạy mỗi ô.

## 9. Hạn chế và tính hợp lệ

1. **Không có dữ liệu tác vụ đánh giá và không có lần chạy sau freeze.** Hạn mức miễn phí của Gemini (500 request/ngày/mô hình) đã hết. Ảnh hưởng: H1 đến H3 chưa được kiểm chứng; kết luận về `skills-auto` chỉ dựa trên 3 tác vụ học chạy một lần trước freeze; không đo được quá khớp hay nhiễu. Đây là hạn chế lớn nhất, và các nhận định về khả năng chuyển sang tác vụ mới trong mục 8 chỉ là suy luận, không phải kết quả đo.
2. **Số mẫu nhỏ và một lần chạy mỗi ô.** 3 tác vụ mỗi vai trò, 8 đến 10 check mỗi tác vụ, mỗi cấu hình chạy một lần. Chênh lệch 1 check (7/10 so với 6/10) nằm trong biên nhiễu có thể có nên không đủ để kết luận skill có hiệu quả.
3. **Lỗi môi trường làm sai một check và sai nguồn học của curator.** `tests_not_modified` luôn thất bại do CRLF trên Windows; nó làm giảm điểm code-learn của cả 3 điều kiện thêm 1 check (không ảnh hưởng so sánh tương đối) nhưng đồng thời đưa một quy tắc không cần thiết vào skill. Do hết hạn mức, không chạy lại được curator.
4. **Đổi nhà cung cấp giữa chừng và một mô hình duy nhất cho kết quả chính.** Ban đầu dùng NVIDIA/GLM (rất chậm, hay timeout), thử Groq (không chạy được), rồi dùng Gemini. Kết quả chính chỉ dùng Gemini; dữ liệu GLM chỉ để bổ sung. Mô hình bỏ qua `temperature` nên các lần chạy không xác định hoàn toàn, và kết luận chỉ áp dụng cho một mô hình nhỏ.
5. **Tác vụ do giảng viên thiết kế sẵn quy ước.** Phần lớn lỗi là quy ước do giảng viên đặt, nên "tác tử tốt về kỹ thuật nhưng không biết quy ước" là hệ quả của thiết kế chứ chưa chắc phản ánh tác vụ thực tế.
6. **Các lần chạy `skills-auto` giai đoạn phát triển nằm trước tag `freeze`** nên không thể dùng làm kết quả chính thức theo quy trình đóng băng.

## 10. Kết luận

Trên 3 tác vụ học, hầu hết check kỹ thuật đều đạt ở mọi điều kiện và hầu như toàn bộ lỗi là vi phạm quy ước tổ chức (nhóm E). Đa tác tử tăng token 1,74 lần mà không thêm check nào đạt. Skill do curator sinh giúp thêm một check ở tác vụ học (+1/27, một lần chạy) với chi phí token gần như không đổi, nhưng chưa đủ để kết luận hiệu quả. Chưa có dữ liệu trên tác vụ đánh giá nên H1 đến H3 chưa được kiểm chứng và không thể kết luận về khả năng chuyển sang tác vụ mới. Đề xuất tiếp theo: khi hạn mức hồi lại, chạy lại curator trên baseline đã sửa CRLF, đóng băng bộ skill mới rồi chạy `baseline`, `subagents`, `skills-auto` trên tác vụ đánh giá và lặp thêm ít nhất 2 lần để đo nhiễu.

## Phụ lục

- Lệnh đã chạy (theo thứ tự, trong Docker bằng `docker run --rm --env-file .env -v <kho>:/lab lab-deepagents bash -c "..."`): `pytest tests` (32 test đạt, gồm `test_01` đến `test_04`); `python scripts/tour.py`; `python -m lab.runner --condition baseline --tasks data-learn code-learn logs-learn`; `python -m lab.runner --condition subagents --tasks learn`; `python -m lab.curator`; `python -m lab.runner --condition skills-auto --tasks learn`; commit `hypotheses`, tag `freeze`; `mv results/skills-auto results/skills-auto-dev`. Trên máy chủ: `python -m lab.compare > report/table.md`, `python scripts/check_breakdown.py`, `PYTHONUTF8=1 python scripts/verify_freeze.py`.
- Sửa mã ngoài pseudo-code: `curate_skills` và `run_task` lấy `response.text` khi `content` là danh sách các phần (Gemini); không sửa tệp có sẵn nào.
- Các thư mục kết quả lưu riêng: `results-nvidia-glm/` (lần chạy trên NVIDIA/GLM, có lần bị timeout), `results-gemini-crlf-artifact/` (bản sao kết quả chính trước khi sửa CRLF, trùng với `results/`), `results-gemini-clean-rerun/` (baseline code-learn sau khi sửa CRLF), `results-infra-errors/` (các lần chạy bị 429 hoặc timeout, không dùng).
- Môi trường: `git config core.autocrlf false` và checkout lại `tasks/` để khôi phục hash của tệp test; `git status` sau đó không có thay đổi nào trong `tasks/`. `skills_sha256` trong `run.json` được tính trong Linux; `verify_freeze.py` chạy trên Windows sẽ tính hash khác do dấu phân cách đường dẫn, nên chạy trong Linux (container cần cài `git`).
- Ghi chú khác: tôi chưa mở `tasks/*-eval/` (đề, dữ liệu, `check.py`) ở bất kỳ thời điểm nào.
