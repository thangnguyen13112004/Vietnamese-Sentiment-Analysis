<div align="center">

# 🧠 TNG Hybrid Stacking: Phân Loại Cảm Xúc Văn Bản Tiếng Việt Tích Hợp Cơ Chế Attention

<p align="center">
  <i>Dự án nghiên cứu kết hợp Học Máy Truyền Thống (Traditional ML) và Học Sâu (Deep Learning) nhằm nâng cao hiệu suất phân loại văn bản tiếng Việt.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white" alt="Keras">
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="scikit-learn">
  <img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white" alt="Jupyter">
</p>

</div>

<br/>

## 📑 Giới Thiệu (Introduction)

Trong nghiên cứu này, chúng tôi đề xuất phương pháp **TNG HYBRID STACKING** để phân loại các nhãn cảm xúc trên bộ dữ liệu ngôn ngữ tiếng Việt. Phương pháp này là giải pháp lai (hybrid) tận dụng sức mạnh của cả mô hình Học máy truyền thống và các kiến trúc Học sâu tiên tiến, cung cấp một cách tiếp cận mạnh mẽ để giải quyết các bài toán Xử lý ngôn ngữ tự nhiên (NLP) phức tạp đối với tiếng Việt.

## ⚙️ Kiến Trúc Mô Hình (Methodology)

Phương pháp tiếp cận dựa trên kỹ thuật **Ensemble/Stacking**, được tối ưu hóa qua các bước sau:

1. **Trích xuất đặc trưng cơ sở (Base Models):** Kết hợp việc tận dụng đặc trưng tần suất từ vựng **TF-IDF** (Term Frequency–Inverse Document Frequency) và kỹ thuật nhúng **Transformer-based embedding** có tích hợp cơ chế **Attention**.
2. **Chuyển đổi đặc trưng (Feature Representation):** Kết quả đầu ra từ các mô hình cơ sở không dùng trực tiếp mà được kết hợp để tạo thành một bộ đặc trưng mới dưới dạng *phân bố xác suất dự đoán (predicted probability distributions)*.
3. **Mô hình Meta-Classifier:** Bộ đặc trưng xác suất này sau đó được đưa vào bộ phân loại **Logistic Regression** ở tầng trên (Stacking) để đưa ra nhãn cảm xúc cuối cùng.

## 📊 Bộ Dữ Liệu Thực Nghiệm (Datasets)

Mô hình được huấn luyện và đánh giá trên hai bộ dữ liệu tiêu chuẩn của tiếng Việt:
- **UIT-VSMEC:** Bộ dữ liệu nhận dạng cảm xúc ngôn ngữ mạng xã hội tiếng Việt.
- **UIT-VSFC:** Bộ dữ liệu phản hồi của sinh viên Việt Nam (đánh giá cảm xúc và phân loại chủ đề).

## 🚀 Kết Quả Đạt Được (Performance)

Mô hình chứng minh được hiệu quả vượt trội, đánh bại các kết quả được báo cáo trong các nghiên cứu trước đây trên cùng tập dữ liệu.

### 1. Kết quả trên tập dữ liệu UIT-VSMEC
| Metric | Điểm số (%) |
| :--- | :---: |
| **Độ chính xác (Average Accuracy)** | `63.84%` |
| **F1-score (Weighted)** | `63.65%` |

### 2. Kết quả trên tập dữ liệu UIT-VSFC
| Task Thực Nghiệm | Độ Chính Xác (Accuracy) | Weighted F1-score |
| :--- | :---: | :---: |
| **Phân loại Cảm xúc (Sentiment)** | `91.81%` | `90.94%` |
| **Phân loại Chủ đề (Topic)** | `87.99%` | `87.64%` |

---

## 🎥 Video Demo

Quá trình thực nghiệm, kết quả chạy thực tế và chi tiết cách mô hình hoạt động được ghi lại trong video dưới đây:

[![Video Demo Project](https://img.shields.io/badge/Google_Drive-Xem_Video_Demo-1DA462?style=for-the-badge&logo=google-drive&logoColor=white)](https://drive.google.com/file/d/1OoqRIvLckIQpuaPMbN6wkSMQx8cb21Nm/view?usp=sharing)
*(Click vào nút trên để xem video Demo)*

---

## ✍️ Tác Giả (Authors)

Công trình nghiên cứu khoa học được thực hiện bởi nhóm tác giả thuộc **Trường Đại học Công Thương Thành phố Hồ Chí Minh (HUIT)**:

- **Nguyễn Ngọc Thắng**
- **Trần Đình Toàn** (*Tác giả liên hệ / Corresponding Author*)
  - 📧 Email: `toantd@huit.edu.vn`
