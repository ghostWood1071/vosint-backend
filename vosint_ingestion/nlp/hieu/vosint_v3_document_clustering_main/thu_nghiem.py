# -*- coding: utf-8 -*-
query = ['vn', 'đường sắt', 'đô thị', 'nlđ', 'hội thảo', 'đường sắt', 'đô thị', 'tổ chức', 'hà', 'nội', 'cục trưởng', 'cục', 'đường sắt', 'vn', 'vũ', 'xuân hồng', 'tiến độ', 'vn', 'tuyến', 'đường sắt', 'đô thị', 'đầu tiên', 'tuyến', 'đường', 'sắt', 'bến', 'thành', 'chợ', 'suối tiên', 'xây dựng', 'tphcm', 'tổng', 'kinh phí', 'triệu', 'usd', 'chủ trương', 'xây dựng', 'đường sắt', 'đô thị', 'vn', 'hình thành', 'giúp đỡ', 'kỹ thuật', 'phủ', 'nhật', 'kinh nghiệm', 'phát triển', 'đường sắt', 'đô thị', 'tuyến', 'đường', 'sắt', 'tsukuba', 'chiều', 'km', 'xây dựng', 'tổng', 'kinh phí', 'tỉ', 'yen', 'xây dựng', 'vận hành', 'đường sắt', 'đô thị', 'thiết', 'tham gia', 'giải phóng', 'mặt', 'quyền', 'địa phương', 'trợ giúp', 'vốn', 'đầu tư', 'phủ']

vocab = ['vòng', 'giới', 'sức', 'đầu tiên', 'đấu', 'hai', 'giành', 'chiến thắng', 'trận', 'vô địch', 'chủ', 'đức', 'giải', 'nhiên', 'bảng', 'hy', 'lạp', 'đầu', 'hàng', 'công', 'phòng ngự', 'thắng', 'bồ đào', 'nha', 'kết', 'bóng đá', 'cup', 'trẻ', 'cầu thủ', 'thua', 'sân', 'bàn', 'pha', 'dứt', 'sút', 'bóng', 'đội', 'brazil', 'tiền đạo', 'dự', 'nam', 'hlv', 'thể', 'ghi bàn', 'phút', 'tiếp tục', 'tiền vệ', 'thi đấu', 'đội hình', 'kỹ thuật', 'chân', 'lối', 'hiệp', 'lan', 'hội', 'cú', 'đi', 'thủ môn', 'lượt', 'đội tuyển', 'văn', 'đồng', 'việt', 'league', 'm', 'u', 'villarreal', 'champions', 'lọt', 'trực tiếp', 'fc', 'nhật', 'thái', 'vn', 'sea', 'games', 'thưởng', 'lđbđ', 'u23', 'u20', 'riedl', 'đoạt', 'hcv', 'chelsea', 'liverpool', 'inter', 'milan', 'ac', 'đh', 'tavares']
score = 0
for i in query:
    if i in vocab:
        score += 1
print(score)


