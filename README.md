<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nguyễn Ngọc Thắng - AI Engineer Portfolio</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --bg-color: #f8fafc;
            --text-main: #334155;
            --text-light: #64748b;
            --white: #ffffff;
            --border-color: #e2e8f0;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.7;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Header & Banner */
        .header {
            background: linear-gradient(135deg, #0f172a 0%, #3b82f6 100%);
            color: var(--white);
            padding: 3rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .header h1 {
            font-size: 2.8rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }

        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }

        .badge {
            background: rgba(255, 255, 255, 0.15);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            backdrop-filter: blur(4px);
        }

        /* Sections */
        .section {
            background: var(--white);
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 2rem;
            border: 1px solid var(--border-color);
        }

        .section h2 {
            color: var(--primary-color);
            font-size: 1.8rem;
            margin-bottom: 1rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.5rem;
        }

        .section h3 {
            color: #0f172a;
            margin: 1.5rem 0 0.8rem 0;
            font-size: 1.3rem;
        }

        .section p {
            margin-bottom: 1rem;
            color: var(--text-main);
        }

        /* Lists */
        ul.custom-list {
            list-style-type: none;
            padding-left: 0;
            margin-bottom: 1.5rem;
        }
        
        ul.custom-list li {
            position: relative;
            padding-left: 1.5rem;
            margin-bottom: 0.8rem;
        }
        
        ul.custom-list li::before {
            content: "▹";
            position: absolute;
            left: 0;
            color: var(--primary-color);
            font-weight: bold;
            font-size: 1.2rem;
        }

        /* Buttons & Links */
        a {
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.3s ease;
        }

        a:hover {
            color: var(--secondary-color);
            text-decoration: underline;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            background-color: var(--primary-color);
            color: var(--white);
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            margin-top: 1rem;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
            transition: all 0.3s ease;
        }

        .btn:hover {
            background-color: var(--secondary-color);
            transform: translateY(-2px);
            box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.4);
            color: var(--white);
            text-decoration: none;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background: var(--white);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        th, td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background-color: #f1f5f9;
            font-weight: 600;
            color: #0f172a;
        }

        tr:hover {
            background-color: #f8fafc;
        }

        /* Code Blocks */
        pre {
            background: #0f172a;
            color: #f8fafc;
            padding: 1.5rem;
            border-radius: 8px;
            overflow-x: auto;
            font-family: "Fira Code", Consolas, monospace;
            font-size: 0.95rem;
            margin: 1.5rem 0;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
        }

        code {
            background: #f1f5f9;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Consolas, monospace;
            font-size: 0.9em;
            color: #db2777;
        }

        pre code {
            background: transparent;
            color: inherit;
            padding: 0;
        }

        /* Projects Grid */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }

        .project-card {
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            border-radius: 8px;
            background: #f8fafc;
            transition: all 0.3s ease;
        }

        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            border-color: #cbd5e1;
        }

        .project-card h4 {
            color: var(--primary-color);
            font-size: 1.2rem;
            margin-bottom: 0.8rem;
        }
        
        .project-card p {
            font-size: 0.95rem;
            color: var(--text-light);
        }
    </style>
</head>
<body>

<div class="container">
    <header class="header">
        <h1>Nguyễn Ngọc Thắng</h1>
        <p>AI Engineer @ TA Solutions | Software Technology Engineering</p>
        <div class="badges">
            <span class="badge">Python</span>
            <span class="badge">Deep Learning</span>
            <span class="badge">NLP</span>
            <span class="badge">Data Engineering</span>
            <span class="badge">.NET Core</span>
        </div>
    </header>

    <section class="section">
        <h2>👨‍💻 Giới thiệu bản thân</h2>
        <p>Xin chào! Tôi là Thắng, hiện đang là sinh viên năm 4 và công tác với vị trí <strong>AI Engineer tại TA Solutions</strong>. Tôi có niềm đam mê mãnh liệt với Trí tuệ nhân tạo, đặc biệt trong các bài toán Xử lý ngôn ngữ tự nhiên (Sentiment Analysis), Trích xuất thông tin tài liệu (Deepseek OCR, Llama 3.2) và Xây dựng Hệ thống gợi ý Graph-based (Neo4j).</p>
        <p>Vừa qua, tôi vinh dự đạt <strong>Giải 3 Nghiên cứu Khoa học cấp Khoa</strong> (Trường Đại học Công Thương TP.HCM) với đề tài nghiên cứu chuyên sâu về phân loại cảm xúc văn bản tiếng Việt.</p>
    </section>

    <section class="section">
        <h2>🏆 Dự án Nổi bật: TNG Hybrid Stacking</h2>
        <p><strong>Paper:</strong> <em>Phân loại cảm xúc văn bản tiếng Việt bằng phương pháp TNG Hybrid Stacking tích hợp cơ chế Attention</em>.</p>
        
        <h3>💡 Thuật toán (Algorithm)</h3>
        <p>Trong nghiên cứu này, chúng tôi đề xuất phương pháp <strong>TNG HYBRID STACKING</strong> kết hợp giữa mô hình Học máy truyền thống và các kiến trúc Học sâu tiên tiến để phân loại các nhãn cảm xúc trên bộ dữ liệu ngôn ngữ tiếng Việt.</p>
        <ul class="custom-list">
            <li><strong>Lớp Mô hình Cơ sở (Level-0):</strong> Tận dụng đặc trưng TF-IDF cho 6 mô hình Học máy (LR, NB, SVM, KNN, Random Forest, XGBoost) kết hợp cùng kỹ thuật Transformer-based embedding (tích hợp cơ chế Attention, Multi-channel CNN).</li>
            <li><strong>Lớp Siêu mô hình (Level-1):</strong> Kết quả đầu ra là phân bố xác suất dự đoán, sau đó đi qua bộ phân loại Meta-model (Logistic Regression) để đưa ra nhãn cảm xúc cuối cùng.</li>
            <li><strong>Tiền xử lý nâng cao:</strong> Tích hợp bộ từ điển chuyển đổi Emoji (Vd: "😭" -> "khóc lớn") và mô hình BartPho-Syllable để tự động sửa lỗi chính tả, teencode mạng xã hội.</li>
        </ul>

        <h3>📊 Thực nghiệm & Kết quả (Experiments & Results)</h3>
        <p>Thực nghiệm được tiến hành trên hai tập dữ liệu cảm xúc tiếng Việt: <strong>UIT-VSMEC</strong> và <strong>UIT-VSFC</strong>. Mô hình lai của chúng tôi giải quyết triệt để vấn đề mất cân bằng dữ liệu của các phương pháp trước đây.</p>
        
        <table>
            <thead>
                <tr>
                    <th>Mô hình / Dataset</th>
                    <th>Accuracy (%)</th>
                    <th>F1-Score (Weighted) (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>UIT-VSMEC:</strong> TextCNN + Attention (DL Base)</td>
                    <td>59.74</td>
                    <td>58.95</td>
                </tr>
                <tr>
                    <td><strong>UIT-VSMEC:</strong> TNG Hybrid Stacking (Proposed)</td>
                    <td><strong>65.22</strong></td>
                    <td><strong>64.88</strong></td>
                </tr>
                <tr>
                    <td><strong>UIT-VSFC:</strong> Sentiment Classification</td>
                    <td><strong>91.81</strong></td>
                    <td><strong>90.94</strong></td>
                </tr>
            </tbody>
        </table>

        <h3>💻 Code & Kiến trúc Deep Learning</h3>
        <p>Trích xuất biểu diễn ngữ nghĩa bằng <code>dangvantuan/vietnamese-document-embedding</code> kết hợp cùng 4 nhánh Conv1D (N-grams) và <code>AttentionLayer</code> chuyên dụng:</p>
<pre><code># Khởi tạo kiến trúc CNN + Attention đa nhánh
inputs = Input(shape=(self.max_len, 768)) 
x = SpatialDropout1D(0.2)(inputs)

branches = []
for size in [2, 3, 4, 5]: # Kích thước cửa sổ trượt N-grams
    branch = Conv1D(filters=300, kernel_size=size, padding='same', activation='relu')(x)
    branch = GlobalMaxPooling1D()(branch)
    branch = Reshape((1, 300))(branch)
    branches.append(branch)
    
concat = Concatenate(axis=1)(branches)
att_output = AttentionLayer()(concat) # Cơ chế Attention tính trọng số
x = Dropout(0.4)(att_output)
outputs = Dense(num_classes, activation='softmax')(x)</code></pre>

        <h3>▶️ Usage / Video Demo</h3>
        <p>Xem luồng hoạt động trực tiếp của hệ thống dự đoán cảm xúc (Demo phân loại văn bản mạng xã hội) tại đây:</p>
        <a href="https://drive.google.com/file/d/1OoqRIvLckIQpuaPMbN6wkSMQx8cb21Nm/view?usp=sharing" target="_blank" class="btn">
            🎬 Xem Video Thực Tế (Google Drive)
        </a>
    </section>

    <section class="section">
        <h2>🛠 Các Dự Án & Kinh Nghiệm Khác</h2>
        <div class="projects-grid">
            <div class="project-card">
                <h4>Hệ thống Trích xuất Hóa đơn (OCR)</h4>
                <p>Nghiên cứu và triển khai máy chủ trích xuất dữ liệu đa định dạng (Hóa đơn, Biên lai, Phiếu giao hàng). Cải thiện độ chính xác thông tin đầu ra theo vùng bằng việc ứng dụng <strong>Deepseek OCR</strong> kết hợp mô hình ngôn ngữ lớn <strong>Llama 3.2</strong>.</p>
            </div>
            <div class="project-card">
                <h4>Hệ thống Gợi ý Khóa học (Graph-based)</h4>
                <p>Xây dựng hệ thống Data Pipeline và Recommendation System cho nền tảng khóa học trực tuyến. Ứng dụng truy vấn Cypher trên <strong>Neo4j</strong> để thiết lập bản đồ quan hệ và tính toán độ tương đồng kết hợp hệ sinh thái Big Data (Spark, ClickHouse, MinIO).</p>
            </div>
        </div>
    </section>

</div>

</body>
</html>