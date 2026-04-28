from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import tempfile
import re
import random

# Khởi tạo App Flask
app = Flask(__name__)
CORS(app) # Cho phép Web HTML gọi API

# --- 1. HÀM TIỀN XỬ LÝ TEXT ---
import re
def preprocess_text(text):
    emo_dict = {
        "😕": " bối rối ",      # Confused face
        "😝": " trêu chọc ",    # Squinting face with tongue (trêu đùa)
        "😣": " chịu đựng ",    # Persevering face (cố kìm nén, khổ sở)
        "🌧": " mưa buồn ",     # Cloud with rain (thường dùng khi tâm trạng buồn)
        "🥵": " vã mồ hôi ",
        
        # --- Nhóm Tích cực (Vui, Cười, Yêu thích) ---
        "😂": " cười vui ",    "🤣": " cười lăn lộn ", "😁": " cười tươi ", 
        "😊": " cười mỉm ",    "🙂": " cười nhẹ ",     "😆": " cười lớn ", 
        "😄": " vui vẻ ",      "😃": " vui ",          "😀": " hạnh phúc ", 
        "😅": " cười trừ ",    "😍": " yêu thích ",    "🥰": " yêu thương ", 
        "😘": " hôn ",         "😚": " hôn gió ",      "💋": " nụ hôn ", 
        "💕": " yêu ",         "💗": " trái tim ",     "💓": " tim đập ", 
        "😻": " mê mẩn ",      "🤩": " tuyệt vời ",    "🤪": " tinh nghịch ", 
        "😜": " trêu đùa ",    "🤗": "ôm",           "🌸": " hoa đẹp ", 
        "👏": " hoan hô ",     "👍": "tốt",          "👌": " ok ", 
        "💪": " cố lên ",      "😎": "ngầu",         "😋": " ngon ", 
        "😹": " cười ra nước mắt ", "💃": "nhảy múa", "🌝": " vui vẻ ", 

        # --- Nhóm Tiêu cực (Buồn, Khóc, Thất vọng) ---
        "😭": " khóc lớn ",    "😢": " buồn khóc ",    "😔": " buồn ", 
        "😞": " thất vọng ",   "☹": " buồn rầu ",      "🙁": " lo lắng ", 
        "😟": " lo âu ",       "😥": " toát mồ hôi ",  "😓": " lo sợ ", 
        "😿": " mèo khóc ",    "💔": " đau lòng ",     "😩": " than thở ", 
        "😫": " mệt mỏi ",     "😪": " buồn ngủ ",     "😴": " ngủ ", 
        "🤕": " bị thương ",   "🥀": " héo úa ",       "👎": " tệ ", 

        # --- Nhóm Tức giận, Khó chịu ---
        "😡": " giận dữ ",     "😠": " phẫn nộ ",      "🤬": " chửi bới ", 
        "😤": " bực mình ",    "😒": " khó chịu ",     "🙄": " ngán ngẩm ", 
        "😑": " cạn lời ",     "😐": " ba chấm ",      "😶": " im lặng ", 
        "😖": " khổ sở ",      "🤢": " buồn nôn ",     "🤮": " ghê tởm ", 
        "👎": " chê ",         "💩": " tệ hại ",       "👺": " quỷ ", 

        # --- Nhóm Ngạc nhiên, Sợ hãi ---
        "😱": " hoảng hốt ",   "😨": " sợ hãi ",       "😰": " lo lắng tột độ ", 
        "😳": " ngại ngùng ",  "😮": " ngạc nhiên ",   "😧": " sững sờ ", 
        "😦": " sốc ",         "🤯": " nổ não ",       "😬": " lo ngại ", 

        # --- Nhóm Thái độ, Mỉa mai, Khác ---
        "😌": " nhẹ nhõm ",    "😏": " nhếch mép ",    "🤔": " suy nghĩ ", 
        "🙃": " cười ngược ",  "🤭": " cười che miệng ","🤐": " kín miệng ", 
        "🧐": " soi xét ",     "🤨": " nghi ngờ ",     "🤠": " cao bồi ", 
        "😈": " ác quỷ ",      "👻": " ma ",           "💀": " chết chóc ", 
        "🌚": " đen tối ",     "🤤": " thèm thuồng ",  "🤧": " hắt hơi ", 
        "😷": " đeo khẩu trang ","🤫": " trật tự ",    "🙏": " cầu nguyện ", 
        "🤦": " bó tay ",      "🤷": " không biết ",   "🙎": " dỗi ", 

        # --- Xử lý các icon đặc biệt hoặc vô nghĩa ---
        "🏻": "", "🏼": "", "🏽": "", "🏾": "", "🏿": "", # Màu da -> xóa
        "🕸": " mạng nhện ",   "🐶": " chó ",          "🐕": " chó ", 
        "🤑": " tham tiền ",   "😗": " hôn nhẹ ",      "😉": " nháy mắt "
    }
    for emo, word in emo_dict.items():
        text = text.replace(emo, word)
        
    #text = ViTokenizer.tokenize(text)
    
    # 2. Chuyển thành chữ thường
    text = text.lower()
    
    # 3. Thay thế dấu câu bằng khoảng trắng
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 4. Xóa Stop words bằng danh sách vietnamese_stopwords mới
    # words = text.split()
    # filtered_words = [word for word in words if word not in vietnamese_stopwords]
    # text = " ".join(filtered_words)
    
    # 5. DỌN DẸP KHOẢNG TRẮNG THỪA VÀ KHOẢNG TRẮNG ĐẦU/CUỐI CÂU
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# ==========================================
# 2. WRAPPER CHO CNN (CẦU NỐI ML + DL) (new)
# ==========================================
import joblib
import pandas as pd
import numpy as np
import torch
from sklearn.base import BaseEstimator, ClassifierMixin
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Layer, Input, SpatialDropout1D, Conv1D, GlobalMaxPooling1D, Reshape, Concatenate, Dropout, Dense
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K

@tf.keras.utils.register_keras_serializable(package="MyLayers")
class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        # input_shape: (batch_size, 4, 300) -> 4 nhánh, mỗi nhánh 300 filters
        self.W = self.add_weight(name="att_weight", 
                                 shape=(input_shape[-1], 1),
                                 initializer="glorot_uniform",
                                 trainable=True)
        self.b = self.add_weight(name="att_bias", 
                                 shape=(input_shape[1], 1),
                                 initializer="zeros",
                                 trainable=True)
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        # Tính toán điểm số quan trọng (score) cho từng nhánh [cite: 61, 78]
        # x shape: (batch_size, 4, 300), W shape: (300, 1) -> score shape: (batch_size, 4, 1)
        score = K.tanh(K.dot(x, self.W) + self.b)
        
        # Chuyển điểm số thành trọng số xác suất bằng Softmax [cite: 42, 61]
        weights = K.softmax(score, axis=1)
        
        # Nhân trọng số với đặc trưng và tổng hợp lại
        context_vector = x * weights
        return K.sum(context_vector, axis=1)

    def get_config(self):
        config = super().get_config()
        return config

class TransformerCNNWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, model_name='dangvantuan/vietnamese-document-embedding', 
                 max_len=100, epochs=10, batch_size=32, device=None, X_val=None, y_val=None):
        self.model_name = model_name
        self.max_len = max_len
        self.epochs = epochs
        self.batch_size = batch_size
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        self.X_val = X_val
        self.y_val = y_val
        self.model = None
        self.embed_model = None
        self.classes_ = None

    def _get_embeddings(self, X):
        # Tải model transformer nếu chưa có
        if self.embed_model is None:
            from sentence_transformers import SentenceTransformer
            self.embed_model = SentenceTransformer(self.model_name, trust_remote_code=True).to(self.device)
        
        # Trích xuất token embeddings [cite: 37]
        features = self.embed_model.encode(X, output_value='token_embeddings', show_progress_bar=False)
        
        # Padding/Truncate về max_len [cite: 38]
        padded = []
        for f in features:
            f_np = f.cpu().numpy() if torch.is_tensor(f) else f
            if f_np.shape[0] >= self.max_len:
                padded.append(f_np[:self.max_len, :])
            else:
                pad_width = ((0, self.max_len - f_np.shape[0]), (0, 0))
                padded.append(np.pad(f_np, pad_width, mode='constant'))
        return np.array(padded)

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        num_classes = len(self.classes_)
        
        # Chuyển văn bản sang embedding
        X_embed = self._get_embeddings(X)
        val_data = None
        if self.X_val is not None and self.y_val is not None:
            val_data = (self._get_embeddings(self.X_val), self.y_val)

        # Xây dựng kiến trúc CNN + Attention từ file 3 [cite: 41]
        inputs = Input(shape=(self.max_len, 768)) # 768 là dim của vdn-embedding 
        x = SpatialDropout1D(0.2)(inputs)
        
        branches = []
        for size in [2, 3, 4, 5]: # Các kernel size [cite: 9, 41]
            branch = Conv1D(filters=300, kernel_size=size, padding='same', activation='relu')(x)
            branch = GlobalMaxPooling1D()(branch)
            branch = Reshape((1, 300))(branch)
            branches.append(branch)
            
        concat = Concatenate(axis=1)(branches)
        att_output = AttentionLayer()(concat)
        x = Dropout(0.4)(att_output)
        outputs = Dense(num_classes, activation='softmax')(x)
        
        self.model = Model(inputs=inputs, outputs=outputs)
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        
        # Huấn luyện [cite: 42]
        self.model.fit(X_embed, y, epochs=self.epochs, batch_size=self.batch_size,
                      validation_data=val_data, verbose=0,
                      callbacks=[tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)])
        return self

    def predict_proba(self, X):
        X_embed = self._get_embeddings(X)
        return self.model.predict(X_embed, verbose=0)

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)

    def __getstate__(self):
        import tempfile
        import os
        state = self.__dict__.copy()
        
        # Bỏ qua SentenceTransformer, nó sẽ tự động tải lại [cite: 7]
        state['embed_model'] = None
        
        # Biến Keras model thành dạng bytes để nhét vào joblib [cite: 12]
        if self.model is not None:
            fd, path = tempfile.mkstemp(suffix='.keras')
            os.close(fd)
            self.model.save(path)
            with open(path, 'rb') as f:
                state['keras_model_bytes'] = f.read()
            os.remove(path)
            
        state['model'] = None
        return state

    def __setstate__(self, state):
        import tempfile
        import os
        from tensorflow.keras.models import load_model
        
        keras_model_bytes = state.pop('keras_model_bytes', None)
        self.__dict__.update(state)
        
        # Khôi phục lại Keras model từ bytes
        if keras_model_bytes is not None:
            fd, path = tempfile.mkstemp(suffix='.keras')
            with os.fdopen(fd, 'wb') as f:
                f.write(keras_model_bytes)
            # Khôi phục thành công
            self.model = load_model(path)
            os.remove(path)

#.venv\Scripts\Activate.ps1
# --- 2. LOAD MODEL (Chạy 1 lần khi bật server) ---
print("Đang tải model, vui lòng đợi...")
# Đảm bảo class TransformerCNNWrapper đã được import hoặc định nghĩa ở đây để joblib có thể load
try:
    loaded_stacking = joblib.load('../hybrid_stacking_vsmec.joblib')
    loaded_le = joblib.load('../label_encoder.joblib')
    cnn_index = [name for name, _ in loaded_stacking.estimators].index('cnn_transformer')
    loaded_stacking.estimators_[cnn_index].device = 'cpu'
    print("Tải model thành công!")
except Exception as e:
    print(f"LỖI TẢI MODEL: {e}. Vui lòng kiểm tra đường dẫn.")

# --- 3. API DỰ ĐOÁN 1 BÌNH LUẬN ---
@app.route('/api/predict', methods=['POST'])
def predict_single():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    clean_text = preprocess_text(text)
    # Model dự đoán
    y_pred = loaded_stacking.predict([clean_text])
    emotion = loaded_le.inverse_transform(y_pred)[0]
    
    return jsonify({
        'text': text,
        'emotion': emotion
    })

# --- THÊM VÀO DƯỚI API PREDICT CŨ TRONG app.py ---

@app.route('/api/predict_batch', methods=['POST'])
def predict_batch():
    data = request.json
    comments = data.get('comments', [])
    
    if not comments:
        return jsonify({'error': 'No comments provided'}), 400
    
    results = []
    
    # Tiền xử lý tất cả bình luận
    clean_comments = [preprocess_text(text) for text in comments]
    
    # Đưa vào mô hình Stacking dự đoán 1 lần (Batch prediction nhanh hơn rất nhiều)
    try:
        y_preds = loaded_stacking.predict(clean_comments)
        emotions = loaded_le.inverse_transform(y_preds)
        
        for i in range(len(comments)):
            results.append({
                'text': comments[i],
                'emotion': emotions[i]
            })
    except Exception as e:
        print(f"Lỗi khi dự đoán batch: {e}")
        return jsonify({'error': 'Prediction failed'}), 500
        
    return jsonify(results)

# --- 4. API LOAD 240 COMMENT TỪ FILE ---
@app.route('/api/load_data', methods=['GET'])
def load_file_data():
    try:
        file_path = r"D:\NCKH\web\predictions_data.json"
        df = pd.read_json(file_path, encoding='utf-8-sig')

        df = df.dropna(subset=['emotion'])

        emotion_counts = df['emotion'].value_counts(normalize=True)
        sample_size = 240

        sampled_data = pd.DataFrame()
        for emotion, prop in emotion_counts.items():
            n_samples = int(np.round(prop * sample_size))
            emo_df = df[df['emotion'] == emotion]
            if len(emo_df) > 0:
                n_samples = min(n_samples, len(emo_df))
                sampled_data = pd.concat([sampled_data, emo_df.sample(n=n_samples)])

        if len(sampled_data) < sample_size:
            diff = sample_size - len(sampled_data)
            remaining = df.drop(sampled_data.index)
            sampled_data = pd.concat([sampled_data, remaining.sample(n=min(diff, len(remaining)))])

        sampled_data = sampled_data.sample(frac=1).reset_index(drop=True)

        results = []
        for _, row in sampled_data.iterrows():
            results.append({
                'text': row['text'] if pd.notna(row['text']) else "",
                'emotion': row['emotion'].strip()
            })

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=== SERVER API ĐÃ KHỞI ĐỘNG TẠI http://127.0.0.1:5000 ===")
    app.run(port=5000, debug=True)