# -*- coding: utf-8 -*-
import json
from elasticsearch import Elasticsearch

from elastic_main import My_ElasticSearch
from core.config import settings

my_es = My_ElasticSearch(host=[settings.ELASTIC_CONNECT], user='USER', password='PASS', verify_certs=False)

# print(my_es.log_cluster_health())

# print(my_es.log_nodes_info())


# print(my_es.check_info_index(index_name="mingg_v3"))

# print(my_es.log_index_health(index_name="mingg_v3"))

# print(my_es.index_head(index_name='mingg_v3'))

# print(my_es.create_new_index(index_name='mingg_v5'))

# print(my_es.delete_index(index_name='.monitoring-kibana-7-2023.04.22'))

# print(my_es.show_all_indexes_in_cluster())

doc = {
    "title": "Thực hư thông tin Bình Tinh được cố nghệ sĩ Vũ Linh \"để lại hết tài sản\"",
    "author": "Văn Minh",
    "time": "Thứ ba, 28/03/2023 - 14:56",
    "pub_date": "2023-03-28T00:00:00Z",
    "content": "Tối 27/3, nghệ sĩ Bình Tinh - con gái nuôi của cố nghệ sĩ Vũ Linh - gây chú ý khi đăng tải bức ảnh chụp màn hình một video trên YouTube có nội dung \"NSƯT Vũ Linh để hết tài sản cho con nuôi Bình Tinh\" và bày tỏ sự bức xúc: \"Trời đất ơi, tội nghiệp em quá mà. Em không có một đồng mấy anh chị ơi\". \n\nDòng chia sẻ của Bình Tinh lập tức nhận được sự quan tâm của bạn bè đồng nghiệp và người hâm mộ. Một số khán giả khuyên nữ nghệ sĩ \"nguôi giận\" vì đây chỉ là chiêu trò \"câu view\" của một số kênh YouTube. \n\nHình ảnh của cố nghệ sĩ Vũ Linh bên con gái nuôi Bình Tinh (Ảnh: Facebook nhân vật).\n\nChia sẻ với phóng viên Dân trí, Bình Tinh cho biết: \"May mắn của tôi là được cha Vũ Linh yêu thương như con ruột. Nhờ có sự truyền đạt và dạy dỗ của cha mà tôi đã có những bước đi vững chắc hơn với nghề. Tôi nghĩ đây là gia tài lớn nhất mà cha đã để lại cho mình rồi. Bổn phận là con gái của cha, tôi chỉ biết mình sẽ lo lắng và chăm sóc chu đáo cho ông hết mức có thể. Ngày cha qua đời, tôi cũng sát cánh bên gia đình để lo hậu sự một cách chu toàn. Ngoài ra, tôi chưa từng có suy nghĩ dòm ngó đến bất kỳ tài sản nào của cha, một đồng tôi cũng không để ý chứ đừng nói chi là một gia sản lớn\".\n\nBình Tinh cho biết việc phải đối diện với nhiều thông tin tiêu cực khiến cô mệt mỏi và căng thẳng trong thời gian dài. Thậm chí, nữ nghệ sĩ còn ngại \"khóc nhiều\" vì sợ một số người nói cô diễn, giả vờ.\n\nNghệ sĩ Hồng Nhung (em gái NSƯT Vũ Linh) và nghệ sĩ Hồng Phượng (cháu gái NSƯT Vũ Linh) nhiều lần động viên và an ủi Bình Tinh vượt qua sóng gió dư luận.\n\nBình Tinh trong lễ cúng thất cho cha nuôi (Ảnh: Facebook nhân vật).\n\n\"Ông hoàng cải lương\" Vũ Linh qua đời vào ngày 5/3, sau thời gian chống chọi bệnh tật. Trong lễ tang của nam nghệ sĩ, bốn người con (Đức Thanh, Hồng Loan, Bình Tinh, Vũ Luân) cùng đội tang và thay phiên túc trực bên linh cữu cha.\n\nThời điểm nam nghệ sĩ mất, mạng xã hội từng xuất hiện không ít tin đồn cho rằng Bình Tinh là người được cố nghệ sĩ Vũ Linh để lại hết tài sản. Sự việc trên gây ra không ít phiền toái cho gia đình.\n\nBình Tinh được biết đến là con gái nuôi của \"ông hoàng cải lương\", được ông chỉ dạy và che chở nhiều năm qua. Ngày nghệ sĩ Vũ Linh qua đời, Bình Tinh viết dòng chia sẻ đầy xúc động trong sổ tang: \"Cha ơi, kiếp sau vẫn quánh vô đít (hành động đánh vào mông - PV) con nha cha\"...\n\nTheo chia sẻ của NSƯT Hữu Quốc, trong những ngày diễn ra tang lễ của cố nghệ sĩ Vũ Linh, Bình Tinh vừa tất bật lo hậu sự cho cha nuôi vừa phải hoàn thành nhiệm vụ với đoàn hát. Sau khi kết thúc suất diễn, cô vội vàng quay về tang lễ của cha nuôi để quỳ lạy đáp lễ.\n\nBình Tinh viết trong sổ tang của NSƯT Vũ Linh (Ảnh: Phạm Thành Trung).\n\nThời gian qua, Bình Tinh liên tục nhận tin buồn khi nhiều người thân của cô gồm cha, mẹ, anh hai, dì và cậu lần lượt ra đi và gần đây nhất là cha nuôi Vũ Linh.\n\nĐối diện với biến cố mất người thân liên tục, Bình Tinh cho biết sức khỏe và tinh thần của cô hiện tại vô cùng sa sút. \"Từ lúc mẹ mất, tâm lý của tôi bị ảnh hưởng nặng nề, nhiều đêm ở một mình tôi khóc như đứa trẻ vì tủi thân. Thời điểm cha nuôi qua đời, tôi bị lao lực khi vừa lo hậu sự cho cha, vừa đi diễn phục vụ bà con\", nữ nghệ sĩ nói. ",
    "keywords": [
        "Bình_Tinh",
        "Vũ_Linh",
        "nghệ_sĩ",
        "nuôi",
        "NSƯT",
        "diễn",
        "gái",
        "tang",
        "qua_đời",
        "hậu_sự",
        "lo",
        "lễ"
    ],
    "url": "https://dantri.com.vn/van-hoa/thuc-hu-thong-tin-binh-tinh-duoc-co-nghe-si-vu-linh-de-lai-het-tai-san-20230328063244094.htm",
    "html": "<p>Tối 27/3, nghệ sĩ Bình Tinh - con gái nuôi của cố nghệ sĩ Vũ Linh - gây chú ý khi đăng tải bức ảnh chụp màn hình một video trên YouTube có nội dung \"NSƯT Vũ Linh để hết tài sản cho con nuôi Bình Tinh\" và bày tỏ sự bức xúc: \"Trời đất ơi, tội nghiệp em quá mà. Em không có một đồng mấy anh chị ơi\".&nbsp;</p><p>Dòng chia sẻ của Bình Tinh lập tức nhận được sự quan tâm của bạn bè đồng nghiệp và người hâm mộ. Một số khán giả khuyên nữ nghệ sĩ \"nguôi giận\" vì đây chỉ là chiêu trò \"câu view\" của một số kênh YouTube.&nbsp;</p><figure class=\"image align-center\" contenteditable=\"false\"></figure><div style=\"width: 680px; position: relative; z-index: 2;\"></div><p>Chia sẻ với phóng viên <em>Dân trí</em>, Bình Tinh cho biết: \"May mắn của tôi là được cha Vũ Linh yêu thương như con ruột. Nhờ có sự truyền đạt và dạy dỗ của cha mà tôi đã có những bước đi vững chắc hơn với nghề. Tôi nghĩ đây là gia tài lớn nhất mà cha đã để lại cho mình rồi. Bổn phận là con gái của cha, tôi chỉ biết mình sẽ lo lắng và chăm sóc chu đáo cho ông hết mức có thể. Ngày cha qua đời, tôi cũng sát cánh bên gia đình để lo hậu sự một cách chu toàn. Ngoài ra, tôi chưa từng có suy nghĩ dòm ngó đến bất kỳ tài sản nào của cha, một đồng tôi cũng không để ý chứ đừng nói chi là một gia sản lớn\".</p><p>Bình Tinh cho biết việc phải đối diện với nhiều thông tin tiêu cực khiến cô mệt mỏi và căng thẳng trong thời gian dài. Thậm chí, nữ nghệ sĩ còn ngại \"khóc nhiều\" vì sợ một số người nói cô diễn, giả vờ.</p><p>Nghệ sĩ Hồng Nhung (em gái NSƯT Vũ Linh) và nghệ sĩ Hồng Phượng (cháu gái NSƯT Vũ Linh) nhiều lần động viên và an ủi Bình Tinh vượt qua sóng gió dư luận.</p><figure class=\"image align-center\" contenteditable=\"false\"></figure><p>\"Ông hoàng cải lương\" <a contenteditable=\"false\" href=\"https://dantri.com.vn/van-hoa/ong-hoang-cai-luong-vu-linh-qua-doi-20230305134825700.htm\">Vũ Linh</a> qua đời vào ngày 5/3, sau thời gian chống chọi bệnh tật. Trong lễ tang của nam nghệ sĩ, bốn người con (Đức Thanh, Hồng Loan, Bình Tinh, Vũ Luân) cùng đội tang và thay phiên túc trực bên linh cữu cha.</p><p>Thời điểm nam nghệ sĩ mất, mạng xã hội từng xuất hiện không ít tin đồn cho rằng Bình Tinh là người được cố nghệ sĩ Vũ Linh để lại hết tài sản. Sự việc trên gây ra không ít phiền toái cho gia đình.</p><p>Bình Tinh được biết đến là con gái nuôi của \"ông hoàng cải lương\", được ông chỉ dạy và che chở nhiều năm qua. Ngày nghệ sĩ Vũ Linh qua đời, Bình Tinh viết dòng chia sẻ đầy xúc động trong sổ tang: \"Cha ơi, kiếp sau vẫn quánh vô đít (hành động đánh vào mông - PV) con nha cha\"...</p><p>Theo chia sẻ của NSƯT Hữu Quốc, trong những ngày diễn ra tang lễ của cố nghệ sĩ Vũ Linh, Bình Tinh vừa tất bật lo hậu sự cho cha nuôi vừa phải hoàn thành nhiệm vụ với đoàn hát. Sau khi kết thúc suất diễn, cô vội vàng quay về tang lễ của cha nuôi để quỳ lạy đáp lễ.</p><figure class=\"image align-center\" contenteditable=\"false\"></figure><p>Thời gian qua, <a contenteditable=\"false\" href=\"https://dantri.com.vn/giai-tri/dien-vien-binh-tinh-tra-ngoc-lan-dau-thu-suc-dien-thoi-trang-20221109115449609.htm\">Bình Tinh</a> liên tục nhận tin buồn khi nhiều người thân của cô gồm cha, mẹ, anh hai, dì và cậu lần lượt ra đi và gần đây nhất là cha nuôi Vũ Linh.</p><p>Đối diện với biến cố mất người thân liên tục, Bình Tinh cho biết sức khỏe và tinh thần của cô hiện tại vô cùng sa sút. \"Từ lúc mẹ mất, tâm lý của tôi bị ảnh hưởng nặng nề, nhiều đêm ở một mình tôi khóc như đứa trẻ vì tủi thân. Thời điểm cha nuôi qua đời, tôi bị lao lực khi vừa lo hậu sự cho cha, vừa đi diễn phục vụ bà con\", nữ nghệ sĩ nói.&nbsp;</p>",
    "class_chude": [],
    "class_linhvuc": [],
    "source_name": "dantri1",
    "source_host_name": "dantri.com.vn",
    "source_language": "vi",
    "source_publishing_country": "Việt Nam",
    "source_source_type": "Báo điện tử",
    "created_at": "2023-03-28T00:00:00Z",
    "modified_at": "2023-03-28T00:00:00Z",
    "class_sacthai": "0",
    "class_tinmau": [],
    "class_object": []

}
doc_2 = {
    "title": "Thực hư thông tin Bình Tinh được cố nghệ sĩ Vũ Linh \"để lại hết tài sản\"",
    "author": "Minggz",
    "time": "Thứ ba, 28/03/2023 - 14:56",
    "pub_date": "2023-03-28T00:00:00Z",
    "content": "Tối 27/3, nghệ sĩ Bình Tinh - con gái nuôi của cố nghệ sĩ Vũ Linh - gây chú ý khi đăng tải bức ảnh chụp màn hình một video trên YouTube có nội dung \"NSƯT Vũ Linh để hết tài sản cho con nuôi Bình Tinh\" và bày tỏ sự bức xúc: \"Trời đất ơi, tội nghiệp em quá mà. Em không có một đồng mấy anh chị ơi\". \n\nDòng chia sẻ của Bình Tinh lập tức nhận được sự quan tâm của bạn bè đồng nghiệp và người hâm mộ. Một số khán giả khuyên nữ nghệ sĩ \"nguôi giận\" vì đây chỉ là chiêu trò \"câu view\" của một số kênh YouTube. \n\nHình ảnh của cố nghệ sĩ Vũ Linh bên con gái nuôi Bình Tinh (Ảnh: Facebook nhân vật).\n\nChia sẻ với phóng viên Dân trí, Bình Tinh cho biết: \"May mắn của tôi là được cha Vũ Linh yêu thương như con ruột. Nhờ có sự truyền đạt và dạy dỗ của cha mà tôi đã có những bước đi vững chắc hơn với nghề. Tôi nghĩ đây là gia tài lớn nhất mà cha đã để lại cho mình rồi. Bổn phận là con gái của cha, tôi chỉ biết mình sẽ lo lắng và chăm sóc chu đáo cho ông hết mức có thể. Ngày cha qua đời, tôi cũng sát cánh bên gia đình để lo hậu sự một cách chu toàn. Ngoài ra, tôi chưa từng có suy nghĩ dòm ngó đến bất kỳ tài sản nào của cha, một đồng tôi cũng không để ý chứ đừng nói chi là một gia sản lớn\".\n\nBình Tinh cho biết việc phải đối diện với nhiều thông tin tiêu cực khiến cô mệt mỏi và căng thẳng trong thời gian dài. Thậm chí, nữ nghệ sĩ còn ngại \"khóc nhiều\" vì sợ một số người nói cô diễn, giả vờ.\n\nNghệ sĩ Hồng Nhung (em gái NSƯT Vũ Linh) và nghệ sĩ Hồng Phượng (cháu gái NSƯT Vũ Linh) nhiều lần động viên và an ủi Bình Tinh vượt qua sóng gió dư luận.\n\nBình Tinh trong lễ cúng thất cho cha nuôi (Ảnh: Facebook nhân vật).\n\n\"Ông hoàng cải lương\" Vũ Linh qua đời vào ngày 5/3, sau thời gian chống chọi bệnh tật. Trong lễ tang của nam nghệ sĩ, bốn người con (Đức Thanh, Hồng Loan, Bình Tinh, Vũ Luân) cùng đội tang và thay phiên túc trực bên linh cữu cha.\n\nThời điểm nam nghệ sĩ mất, mạng xã hội từng xuất hiện không ít tin đồn cho rằng Bình Tinh là người được cố nghệ sĩ Vũ Linh để lại hết tài sản. Sự việc trên gây ra không ít phiền toái cho gia đình.\n\nBình Tinh được biết đến là con gái nuôi của \"ông hoàng cải lương\", được ông chỉ dạy và che chở nhiều năm qua. Ngày nghệ sĩ Vũ Linh qua đời, Bình Tinh viết dòng chia sẻ đầy xúc động trong sổ tang: \"Cha ơi, kiếp sau vẫn quánh vô đít (hành động đánh vào mông - PV) con nha cha\"...\n\nTheo chia sẻ của NSƯT Hữu Quốc, trong những ngày diễn ra tang lễ của cố nghệ sĩ Vũ Linh, Bình Tinh vừa tất bật lo hậu sự cho cha nuôi vừa phải hoàn thành nhiệm vụ với đoàn hát. Sau khi kết thúc suất diễn, cô vội vàng quay về tang lễ của cha nuôi để quỳ lạy đáp lễ.\n\nBình Tinh viết trong sổ tang của NSƯT Vũ Linh (Ảnh: Phạm Thành Trung).\n\nThời gian qua, Bình Tinh liên tục nhận tin buồn khi nhiều người thân của cô gồm cha, mẹ, anh hai, dì và cậu lần lượt ra đi và gần đây nhất là cha nuôi Vũ Linh.\n\nĐối diện với biến cố mất người thân liên tục, Bình Tinh cho biết sức khỏe và tinh thần của cô hiện tại vô cùng sa sút. \"Từ lúc mẹ mất, tâm lý của tôi bị ảnh hưởng nặng nề, nhiều đêm ở một mình tôi khóc như đứa trẻ vì tủi thân. Thời điểm cha nuôi qua đời, tôi bị lao lực khi vừa lo hậu sự cho cha, vừa đi diễn phục vụ bà con\", nữ nghệ sĩ nói. ",
    "keywords": [
        "Bình_Tinh",
        "Vũ_Linh",
        "nghệ_sĩ",
        "nuôi",
        "NSƯT",
        "diễn",
        "gái",
        "tang",
        "qua_đời",
        "hậu_sự",
        "lo",
        "lễ"
    ],
    "url": "https://dantri.com.vn/van-hoa/thuc-hu-thong-tin-binh-tinh-duoc-co-nghe-si-vu-linh-de-lai-het-tai-san-20230328063244094.htm",
    "html": "<p>Tối 27/3, nghệ sĩ Bình Tinh - con gái nuôi của cố nghệ sĩ Vũ Linh - gây chú ý khi đăng tải bức ảnh chụp màn hình một video trên YouTube có nội dung \"NSƯT Vũ Linh để hết tài sản cho con nuôi Bình Tinh\" và bày tỏ sự bức xúc: \"Trời đất ơi, tội nghiệp em quá mà. Em không có một đồng mấy anh chị ơi\".&nbsp;</p><p>Dòng chia sẻ của Bình Tinh lập tức nhận được sự quan tâm của bạn bè đồng nghiệp và người hâm mộ. Một số khán giả khuyên nữ nghệ sĩ \"nguôi giận\" vì đây chỉ là chiêu trò \"câu view\" của một số kênh YouTube.&nbsp;</p><figure class=\"image align-center\" contenteditable=\"false\"></figure><div style=\"width: 680px; position: relative; z-index: 2;\"></div><p>Chia sẻ với phóng viên <em>Dân trí</em>, Bình Tinh cho biết: \"May mắn của tôi là được cha Vũ Linh yêu thương như con ruột. Nhờ có sự truyền đạt và dạy dỗ của cha mà tôi đã có những bước đi vững chắc hơn với nghề. Tôi nghĩ đây là gia tài lớn nhất mà cha đã để lại cho mình rồi. Bổn phận là con gái của cha, tôi chỉ biết mình sẽ lo lắng và chăm sóc chu đáo cho ông hết mức có thể. Ngày cha qua đời, tôi cũng sát cánh bên gia đình để lo hậu sự một cách chu toàn. Ngoài ra, tôi chưa từng có suy nghĩ dòm ngó đến bất kỳ tài sản nào của cha, một đồng tôi cũng không để ý chứ đừng nói chi là một gia sản lớn\".</p><p>Bình Tinh cho biết việc phải đối diện với nhiều thông tin tiêu cực khiến cô mệt mỏi và căng thẳng trong thời gian dài. Thậm chí, nữ nghệ sĩ còn ngại \"khóc nhiều\" vì sợ một số người nói cô diễn, giả vờ.</p><p>Nghệ sĩ Hồng Nhung (em gái NSƯT Vũ Linh) và nghệ sĩ Hồng Phượng (cháu gái NSƯT Vũ Linh) nhiều lần động viên và an ủi Bình Tinh vượt qua sóng gió dư luận.</p><figure class=\"image align-center\" contenteditable=\"false\"></figure><p>\"Ông hoàng cải lương\" <a contenteditable=\"false\" href=\"https://dantri.com.vn/van-hoa/ong-hoang-cai-luong-vu-linh-qua-doi-20230305134825700.htm\">Vũ Linh</a> qua đời vào ngày 5/3, sau thời gian chống chọi bệnh tật. Trong lễ tang của nam nghệ sĩ, bốn người con (Đức Thanh, Hồng Loan, Bình Tinh, Vũ Luân) cùng đội tang và thay phiên túc trực bên linh cữu cha.</p><p>Thời điểm nam nghệ sĩ mất, mạng xã hội từng xuất hiện không ít tin đồn cho rằng Bình Tinh là người được cố nghệ sĩ Vũ Linh để lại hết tài sản. Sự việc trên gây ra không ít phiền toái cho gia đình.</p><p>Bình Tinh được biết đến là con gái nuôi của \"ông hoàng cải lương\", được ông chỉ dạy và che chở nhiều năm qua. Ngày nghệ sĩ Vũ Linh qua đời, Bình Tinh viết dòng chia sẻ đầy xúc động trong sổ tang: \"Cha ơi, kiếp sau vẫn quánh vô đít (hành động đánh vào mông - PV) con nha cha\"...</p><p>Theo chia sẻ của NSƯT Hữu Quốc, trong những ngày diễn ra tang lễ của cố nghệ sĩ Vũ Linh, Bình Tinh vừa tất bật lo hậu sự cho cha nuôi vừa phải hoàn thành nhiệm vụ với đoàn hát. Sau khi kết thúc suất diễn, cô vội vàng quay về tang lễ của cha nuôi để quỳ lạy đáp lễ.</p><figure class=\"image align-center\" contenteditable=\"false\"></figure><p>Thời gian qua, <a contenteditable=\"false\" href=\"https://dantri.com.vn/giai-tri/dien-vien-binh-tinh-tra-ngoc-lan-dau-thu-suc-dien-thoi-trang-20221109115449609.htm\">Bình Tinh</a> liên tục nhận tin buồn khi nhiều người thân của cô gồm cha, mẹ, anh hai, dì và cậu lần lượt ra đi và gần đây nhất là cha nuôi Vũ Linh.</p><p>Đối diện với biến cố mất người thân liên tục, Bình Tinh cho biết sức khỏe và tinh thần của cô hiện tại vô cùng sa sút. \"Từ lúc mẹ mất, tâm lý của tôi bị ảnh hưởng nặng nề, nhiều đêm ở một mình tôi khóc như đứa trẻ vì tủi thân. Thời điểm cha nuôi qua đời, tôi bị lao lực khi vừa lo hậu sự cho cha, vừa đi diễn phục vụ bà con\", nữ nghệ sĩ nói.&nbsp;</p>",
    "class_chude": [],
    "class_linhvuc": [],
    "source_name": "dantri1",
    "source_host_name": "dantri.com.vn",
    "source_language": "vi",
    "source_publishing_country": "Việt Nam",
    "source_source_type": "Báo điện tử",
    "created_at": "2023-03-28T00:00:00Z",
    "modified_at": "2023-03-28T00:00:00Z",
    "class_sacthai": "0",
    "class_tinmau": [],
    "class_object": []

}



# print(my_es.insert_document(index_name='vosint', document=doc))

# list_doc = [doc, doc_2]


# print(len(list_doc))

# f = open('collection.json')
# data_mongo = json.load(f)
# print(len(data_mongo))
# print(type(data_mongo[0]))
# print(my_es.insert_many_document(index_name='minggz', list_of_document=list_doc))

# print(my_es.insert_many_document(index_name='minggz', list_of_document=data_mongo))

# print(my_es.log_index_health(index_name='minggz'))
print(my_es.check_number_document(index_name='vosint'))



#print(my_es.index_head(index_name='vosint'))

# print(my_es.search_main(index_name="minggz", query='"nghệ sĩ" + "con gái"', k=1))


print(my_es.search_main(index_name="vosint", query='*', sentiment = '-1', lang= ['vi'], k=1,gte='1990-03-28T00:00:00Z',lte='2023-03-28T00:00:00Z'))
#print(my_es.search_main(index_name="vosint"))
