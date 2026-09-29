"""Bộ thuật ngữ tiếng Anh chuyên ngành Hải quan cho Daily vocab.

Mỗi dòng: ``chủ đề | thuật ngữ | từ loại | nghĩa tiếng Việt | câu ví dụ | dịch câu ví dụ``.

Căn cứ biên soạn:
- Thuật ngữ tiếng Anh: WCO "Glossary of International Customs Terms" (bản
  cập nhật đăng tại wcoomd.org, 180 mục), Công ước Kyoto sửa đổi (RKC), Hiệp
  định Trị giá WTO (Điều VII GATT), Công ước HS, Incoterms® 2020 (ICC).
- Nghĩa tiếng Việt dùng đúng từ ngữ pháp lý Việt Nam: Luật Hải quan
  54/2014/QH13 (Điều 4 — giải thích từ ngữ), Luật Thuế XK, NK 107/2016/QH13,
  Luật Quản lý thuế 38/2019/QH14, NĐ 08/2015/NĐ-CP (sửa bởi NĐ 59/2018),
  TT 38/2015/TT-BTC (sửa bởi TT 39/2018), TT 39/2015/TT-BTC (trị giá),
  TT 14/2015/TT-BTC (phân loại), TT 33/2023/TT-BTC (xuất xứ),
  NĐ 128/2020/NĐ-CP (xử phạt VPHC hải quan).
- Ví dụ: câu tự soạn theo ngữ cảnh nghiệp vụ, không chép từ tài liệu có bản quyền.

Chạy ``python tools/build_data.py`` để đóng gói thành ``data/en-5.json``.
"""

TOPICS = [
    "Cơ quan & người khai",
    "Thủ tục & thông quan",
    "Chứng từ & vận tải",
    "Thuế & nghĩa vụ tài chính",
    "Trị giá hải quan",
    "Phân loại hàng hóa (HS)",
    "Xuất xứ & FTA",
    "Loại hình & chế độ quản lý",
    "Kiểm tra sau thông quan",
    "Quản lý rủi ro & giám sát",
    "Vi phạm & chống buôn lậu",
    "Incoterms & thanh toán",
]

RAW = """
1 | customs | danh từ | Hải quan | Customs released the shipment after checking the documents. | Hải quan đã giải phóng lô hàng sau khi kiểm tra hồ sơ.
1 | customs authority | danh từ | Cơ quan hải quan | The customs authority may request additional documents. | Cơ quan hải quan có thể yêu cầu bổ sung chứng từ.
1 | customs officer | danh từ | Công chức hải quan | The customs officer examined the container at the port. | Công chức hải quan đã kiểm tra container tại cảng.
1 | customs office | danh từ | Cơ quan hải quan nơi làm thủ tục (Chi cục) | Submit the declaration to the customs office at the port of entry. | Nộp tờ khai cho chi cục hải quan tại cửa khẩu nhập.
1 | customs office of departure | danh từ | Hải quan nơi hàng đi | The customs office of departure sealed the container. | Hải quan nơi hàng đi đã niêm phong container.
1 | customs office of destination | danh từ | Hải quan nơi hàng đến | The goods must arrive at the customs office of destination within the time limit. | Hàng phải đến hải quan nơi hàng đến trong thời hạn quy định.
1 | declarant | danh từ | Người khai hải quan | The declarant is responsible for the accuracy of the declaration. | Người khai hải quan chịu trách nhiệm về tính chính xác của tờ khai.
1 | customs broker | danh từ | Đại lý làm thủ tục hải quan | We hired a customs broker to handle the import clearance. | Chúng tôi thuê đại lý làm thủ tục hải quan để làm thủ tục nhập khẩu.
1 | customs clearing agent | danh từ | Nhân viên đại lý làm thủ tục hải quan | Only a certified customs clearing agent may sign on behalf of the importer. | Chỉ nhân viên đại lý hải quan có chứng chỉ mới được ký thay người nhập khẩu.
1 | importer | danh từ | Người nhập khẩu | The importer must pay the duties before the goods are released. | Người nhập khẩu phải nộp thuế trước khi hàng được giải phóng.
1 | exporter | danh từ | Người xuất khẩu | The exporter declared the goods at the border gate. | Người xuất khẩu đã khai báo hàng hóa tại cửa khẩu.
1 | consignee | danh từ | Người nhận hàng | The consignee named on the bill of lading collected the cargo. | Người nhận hàng ghi trên vận đơn đã nhận lô hàng.
1 | consignor | danh từ | Người gửi hàng | The consignor sent the goods by sea from Shanghai. | Người gửi hàng đã gửi hàng bằng đường biển từ Thượng Hải.
1 | carrier | danh từ | Người vận chuyển | The carrier submitted the cargo manifest before arrival. | Người vận chuyển đã nộp bản lược khai hàng hóa trước khi tàu đến.
1 | freight forwarder | danh từ | Người giao nhận hàng hóa | The freight forwarder booked space on the next vessel. | Công ty giao nhận đã đặt chỗ trên chuyến tàu kế tiếp.
1 | authorized economic operator | danh từ | Doanh nghiệp ưu tiên (AEO) | As an authorized economic operator, the company enjoys fewer physical inspections. | Là doanh nghiệp ưu tiên, công ty được giảm kiểm tra thực tế hàng hóa.
1 | third party | danh từ | Bên thứ ba | A third party paid the freight on behalf of the buyer. | Một bên thứ ba đã trả cước thay cho người mua.
1 | World Customs Organization | danh từ | Tổ chức Hải quan Thế giới (WCO) | Vietnam has been a member of the World Customs Organization since 1993. | Việt Nam là thành viên Tổ chức Hải quan Thế giới từ năm 1993.
1 | mutual administrative assistance | danh từ | Hỗ trợ hành chính lẫn nhau (giữa các cơ quan hải quan) | The two administrations exchanged data under a mutual administrative assistance agreement. | Hai cơ quan hải quan trao đổi dữ liệu theo hiệp định hỗ trợ hành chính lẫn nhau.
1 | customs law | danh từ | Pháp luật hải quan | Every declarant must comply with customs law. | Mọi người khai hải quan phải tuân thủ pháp luật hải quan.
1 | customs territory | danh từ | Lãnh thổ hải quan | Goods entering the customs territory are subject to customs control. | Hàng hóa vào lãnh thổ hải quan chịu sự kiểm soát hải quan.
1 | customs operation area | danh từ | Địa bàn hoạt động hải quan | The inland clearance depot lies within the customs operation area. | Cảng cạn nằm trong địa bàn hoạt động hải quan.
2 | customs declaration | danh từ | Tờ khai hải quan | Please correct the HS code on the customs declaration. | Vui lòng sửa mã HS trên tờ khai hải quan.
2 | goods declaration | danh từ | Tờ khai hàng hóa | The goods declaration must be lodged before the goods arrive. | Tờ khai hàng hóa phải được nộp trước khi hàng đến.
2 | lodge a declaration | cụm từ | Nộp (đăng ký) tờ khai | The broker lodged the declaration electronically. | Đại lý đã nộp tờ khai bằng phương thức điện tử.
2 | customs formalities | danh từ | Thủ tục hải quan | Customs formalities for exported goods are completed at the port. | Thủ tục hải quan đối với hàng xuất khẩu được hoàn thành tại cảng.
2 | customs procedure | danh từ | Chế độ (thủ tục) hải quan | The goods were placed under the customs warehousing procedure. | Hàng hóa được đặt dưới chế độ kho ngoại quan.
2 | clearance | danh từ | Thông quan | Clearance took less than two hours for the green-channel shipment. | Lô hàng luồng xanh được thông quan chưa đầy hai giờ.
2 | customs clearance | danh từ | Thông quan hàng hóa | Customs clearance is delayed because the invoice is missing. | Việc thông quan bị chậm vì thiếu hóa đơn.
2 | clearance for home use | danh từ | Thông quan để tiêu thụ nội địa | After clearance for home use, the goods can be sold freely. | Sau khi thông quan để tiêu thụ nội địa, hàng được bán tự do.
2 | release of goods | danh từ | Giải phóng hàng | The release of goods was allowed after the importer provided a bank guarantee. | Hàng được giải phóng sau khi người nhập khẩu nộp bảo lãnh ngân hàng.
2 | release under guarantee | cụm từ | Giải phóng hàng khi có bảo lãnh | The goods were granted release under guarantee pending the valuation check. | Hàng được giải phóng khi có bảo lãnh trong lúc chờ kiểm tra trị giá.
2 | green channel | danh từ | Luồng xanh (miễn kiểm tra hồ sơ và thực tế) | The system assigned the declaration to the green channel. | Hệ thống phân tờ khai vào luồng xanh.
2 | yellow channel | danh từ | Luồng vàng (kiểm tra hồ sơ) | Yellow-channel declarations require a document check. | Tờ khai luồng vàng phải kiểm tra hồ sơ.
2 | red channel | danh từ | Luồng đỏ (kiểm tra thực tế hàng hóa) | Red-channel shipments are physically examined. | Lô hàng luồng đỏ bị kiểm tra thực tế.
2 | document check | danh từ | Kiểm tra hồ sơ hải quan | The officer completed the document check and found no errors. | Công chức đã kiểm tra hồ sơ và không phát hiện sai sót.
2 | physical examination | danh từ | Kiểm tra thực tế hàng hóa | Physical examination revealed more cartons than declared. | Kiểm tra thực tế phát hiện nhiều thùng hơn số khai báo.
2 | examination of goods | danh từ | Kiểm tra hàng hóa | The examination of goods was carried out in the presence of the declarant. | Việc kiểm tra hàng hóa được tiến hành với sự có mặt của người khai.
2 | supporting documents | danh từ | Chứng từ kèm theo (hồ sơ hải quan) | Upload the supporting documents to the customs system. | Tải các chứng từ kèm theo lên hệ thống hải quan.
2 | amend a declaration | cụm từ | Sửa tờ khai | You may amend a declaration before the channel is assigned. | Có thể sửa tờ khai trước khi được phân luồng.
2 | supplementary declaration | danh từ | Khai bổ sung | The company filed a supplementary declaration to correct the value. | Công ty khai bổ sung để điều chỉnh trị giá.
2 | cancel a declaration | cụm từ | Hủy tờ khai | The declaration was cancelled because the goods never arrived. | Tờ khai bị hủy vì hàng không đến.
2 | pre-arrival processing | danh từ | Xử lý trước khi hàng đến | Pre-arrival processing lets customs assess risk before the ship docks. | Xử lý trước khi hàng đến giúp hải quan đánh giá rủi ro trước khi tàu cập cảng.
2 | electronic customs clearance | danh từ | Thủ tục hải quan điện tử | VNACCS is the electronic customs clearance system of Vietnam. | VNACCS là hệ thống thông quan điện tử của Việt Nam.
2 | National Single Window | danh từ | Cơ chế một cửa quốc gia | Import licences are now issued through the National Single Window. | Giấy phép nhập khẩu nay được cấp qua Cơ chế một cửa quốc gia.
2 | border gate | danh từ | Cửa khẩu | Trucks queue for hours at the border gate. | Xe tải xếp hàng nhiều giờ tại cửa khẩu.
2 | port of entry | danh từ | Cửa khẩu nhập | Hai Phong port is the port of entry for this container. | Cảng Hải Phòng là cửa khẩu nhập của container này.
2 | inland clearance depot | danh từ | Cảng cạn (ICD) | The container was moved to an inland clearance depot for inspection. | Container được chuyển về cảng cạn để kiểm tra.
2 | container freight station | danh từ | Địa điểm thu gom hàng lẻ (CFS) | Less-than-container-load cargo is consolidated at the container freight station. | Hàng lẻ được gom tại địa điểm thu gom hàng lẻ.
2 | temporary storage | danh từ | Lưu giữ tạm thời | Goods in temporary storage remain under customs control. | Hàng lưu giữ tạm thời vẫn chịu sự kiểm soát hải quan.
2 | goods in free circulation | danh từ | Hàng hóa lưu thông tự do | Once duties are paid, the goods are in free circulation. | Khi đã nộp thuế, hàng được lưu thông tự do.
2 | specialized inspection | danh từ | Kiểm tra chuyên ngành | Food imports are subject to specialized inspection before clearance. | Thực phẩm nhập khẩu phải kiểm tra chuyên ngành trước khi thông quan.
2 | quarantine | danh từ | Kiểm dịch | The fruit was held for plant quarantine. | Trái cây bị giữ lại để kiểm dịch thực vật.
2 | clearance time | danh từ | Thời gian thông quan | The new system cut average clearance time by half. | Hệ thống mới giảm một nửa thời gian thông quan trung bình.
2 | trade facilitation | danh từ | Tạo thuận lợi thương mại | Paperless procedures are a key trade facilitation measure. | Thủ tục không giấy tờ là biện pháp tạo thuận lợi thương mại quan trọng.
2 | customs seal | danh từ | Niêm phong hải quan | Do not break the customs seal before the officer arrives. | Không phá niêm phong hải quan trước khi công chức đến.
2 | declared value | danh từ | Trị giá khai báo | The declared value was lower than the market price. | Trị giá khai báo thấp hơn giá thị trường.
3 | commercial invoice | danh từ | Hóa đơn thương mại | The commercial invoice shows a unit price of ten dollars. | Hóa đơn thương mại thể hiện đơn giá mười đô la.
3 | packing list | danh từ | Phiếu đóng gói (chi tiết hàng hóa) | The packing list states the gross weight of each carton. | Phiếu đóng gói ghi trọng lượng cả bì của từng thùng.
3 | sales contract | danh từ | Hợp đồng mua bán | The sales contract specifies FOB Ho Chi Minh City. | Hợp đồng mua bán quy định điều kiện FOB Thành phố Hồ Chí Minh.
3 | bill of lading | danh từ | Vận đơn (đường biển) | The bill of lading is a document of title to the goods. | Vận đơn đường biển là chứng từ sở hữu hàng hóa.
3 | master bill of lading | danh từ | Vận đơn chủ (MBL) | The shipping line issued the master bill of lading to the forwarder. | Hãng tàu cấp vận đơn chủ cho công ty giao nhận.
3 | house bill of lading | danh từ | Vận đơn thứ cấp (HBL) | The forwarder issued a house bill of lading to the shipper. | Công ty giao nhận cấp vận đơn thứ cấp cho người gửi hàng.
3 | air waybill | danh từ | Vận đơn hàng không | Check the air waybill number before you declare. | Kiểm tra số vận đơn hàng không trước khi khai báo.
3 | cargo manifest | danh từ | Bản lược khai hàng hóa | The cargo manifest lists every consignment on board. | Bản lược khai hàng hóa liệt kê mọi lô hàng trên tàu.
3 | delivery order | danh từ | Lệnh giao hàng | Take the delivery order to the terminal to collect the container. | Mang lệnh giao hàng đến cảng để lấy container.
3 | arrival notice | danh từ | Giấy báo hàng đến | We received the arrival notice two days before the ship docked. | Chúng tôi nhận giấy báo hàng đến hai ngày trước khi tàu cập.
3 | shipping line | danh từ | Hãng tàu | The shipping line charged a high demurrage fee. | Hãng tàu thu phí lưu container rất cao.
3 | vessel | danh từ | Tàu (biển) | The vessel is scheduled to arrive on Monday. | Tàu dự kiến đến vào thứ Hai.
3 | container | danh từ | Container (công-te-nơ) | The container was sealed at the factory. | Container được niêm phong tại nhà máy.
3 | full container load | danh từ | Hàng nguyên container (FCL) | We ship full container loads to Europe every month. | Mỗi tháng chúng tôi gửi hàng nguyên container sang châu Âu.
3 | less than container load | danh từ | Hàng lẻ (LCL) | Small orders are shipped as less than container load. | Đơn nhỏ được gửi dưới dạng hàng lẻ.
3 | gross weight | danh từ | Trọng lượng cả bì | The gross weight on the declaration must match the bill of lading. | Trọng lượng cả bì trên tờ khai phải khớp với vận đơn.
3 | net weight | danh từ | Trọng lượng tịnh | Net weight excludes the packaging. | Trọng lượng tịnh không tính bao bì.
3 | port of loading | danh từ | Cảng xếp hàng | The port of loading was Busan. | Cảng xếp hàng là Busan.
3 | port of discharge | danh từ | Cảng dỡ hàng | Cat Lai is the port of discharge for this shipment. | Cát Lái là cảng dỡ hàng của lô hàng này.
3 | shipment | danh từ | Lô hàng; việc gửi hàng | The shipment was split into two containers. | Lô hàng được chia vào hai container.
3 | consignment | danh từ | Lô hàng gửi | Each consignment needs its own declaration. | Mỗi lô hàng gửi cần một tờ khai riêng.
3 | freight | danh từ | Cước vận chuyển; hàng hóa vận chuyển | Freight is included in the CIF price. | Cước vận chuyển đã bao gồm trong giá CIF.
3 | demurrage | danh từ | Phí lưu container tại cảng | Delays in clearance led to heavy demurrage charges. | Chậm thông quan dẫn đến phí lưu container rất lớn.
3 | detention | danh từ | Phí lưu container ngoài cảng | The importer paid detention for keeping the container too long. | Người nhập khẩu phải trả phí lưu container vì giữ quá lâu.
3 | transport document | danh từ | Chứng từ vận tải | The transport document shows the route from Japan to Vietnam. | Chứng từ vận tải thể hiện tuyến đường từ Nhật Bản đến Việt Nam.
3 | import licence | danh từ | Giấy phép nhập khẩu | Explosive precursors require an import licence. | Tiền chất thuốc nổ phải có giấy phép nhập khẩu.
3 | certificate of quality | danh từ | Giấy chứng nhận chất lượng | The buyer asked for a certificate of quality issued by the manufacturer. | Người mua yêu cầu giấy chứng nhận chất lượng do nhà sản xuất cấp.
3 | phytosanitary certificate | danh từ | Giấy chứng nhận kiểm dịch thực vật | Fresh fruit exports must carry a phytosanitary certificate. | Trái cây tươi xuất khẩu phải có giấy chứng nhận kiểm dịch thực vật.
3 | insurance certificate | danh từ | Giấy chứng nhận bảo hiểm | The insurance certificate covers the goods up to the warehouse. | Giấy chứng nhận bảo hiểm bảo hiểm hàng đến tận kho.
3 | dangerous goods | danh từ | Hàng nguy hiểm | Dangerous goods must be labelled according to IMDG rules. | Hàng nguy hiểm phải dán nhãn theo quy định IMDG.
3 | transhipment | danh từ | Chuyển tải | Transhipment in Singapore added three days to the voyage. | Việc chuyển tải ở Singapore làm chuyến đi dài thêm ba ngày.
3 | stores | danh từ | Hàng cung ứng cho tàu (đồ dự trữ) | Ship's stores are not subject to import duty if consumed on board. | Hàng cung ứng tiêu dùng trên tàu không chịu thuế nhập khẩu.
3 | postal parcel | danh từ | Bưu kiện | Small postal parcels are cleared under a simplified procedure. | Bưu kiện nhỏ được thông quan theo thủ tục đơn giản.
3 | express consignment | danh từ | Hàng chuyển phát nhanh | Express consignments below the threshold are exempt from duty. | Hàng chuyển phát nhanh dưới ngưỡng được miễn thuế.
4 | customs duties | danh từ | Thuế hải quan (thuế xuất khẩu, nhập khẩu) | Customs duties are calculated on the customs value. | Thuế hải quan được tính trên trị giá hải quan.
4 | import duty | danh từ | Thuế nhập khẩu | The import duty on cars is very high. | Thuế nhập khẩu ô tô rất cao.
4 | export duty | danh từ | Thuế xuất khẩu | Some raw minerals are subject to export duty. | Một số khoáng sản thô chịu thuế xuất khẩu.
4 | duties and taxes | danh từ | Thuế và các khoản thu | All duties and taxes must be paid before release. | Mọi khoản thuế phải được nộp trước khi giải phóng hàng.
4 | value-added tax | danh từ | Thuế giá trị gia tăng | Value-added tax at import is ten percent for most goods. | Thuế giá trị gia tăng khâu nhập khẩu là mười phần trăm với phần lớn hàng hóa.
4 | special consumption tax | danh từ | Thuế tiêu thụ đặc biệt | Imported beer is subject to special consumption tax. | Bia nhập khẩu chịu thuế tiêu thụ đặc biệt.
4 | environmental protection tax | danh từ | Thuế bảo vệ môi trường | Petrol imports bear environmental protection tax. | Xăng nhập khẩu chịu thuế bảo vệ môi trường.
4 | anti-dumping duty | danh từ | Thuế chống bán phá giá | An anti-dumping duty was imposed on imported steel. | Thuế chống bán phá giá được áp đối với thép nhập khẩu.
4 | countervailing duty | danh từ | Thuế chống trợ cấp | Countervailing duties offset foreign government subsidies. | Thuế chống trợ cấp bù lại khoản trợ cấp của chính phủ nước ngoài.
4 | safeguard duty | danh từ | Thuế tự vệ | A safeguard duty protects domestic producers from a sudden import surge. | Thuế tự vệ bảo vệ nhà sản xuất trong nước trước sự gia tăng đột biến của hàng nhập khẩu.
4 | ad valorem duty | danh từ | Thuế theo tỷ lệ phần trăm | An ad valorem duty is a percentage of the customs value. | Thuế theo tỷ lệ phần trăm được tính bằng phần trăm trị giá hải quan.
4 | specific duty | danh từ | Thuế tuyệt đối | Used cars are subject to a specific duty per vehicle. | Ô tô đã qua sử dụng chịu thuế tuyệt đối theo chiếc.
4 | tax rate | danh từ | Thuế suất | Check the tax rate in the current tariff schedule. | Tra thuế suất trong biểu thuế hiện hành.
4 | MFN tariff rate | danh từ | Thuế suất ưu đãi (MFN) | Goods from WTO members enjoy the MFN tariff rate. | Hàng từ các nước thành viên WTO được hưởng thuế suất ưu đãi MFN.
4 | special preferential tariff | danh từ | Thuế suất ưu đãi đặc biệt | With a valid Form E, the goods qualify for the special preferential tariff. | Có C/O mẫu E hợp lệ, hàng được hưởng thuế suất ưu đãi đặc biệt.
4 | tariff quota | danh từ | Hạn ngạch thuế quan | Sugar imported within the tariff quota pays a lower rate. | Đường nhập trong hạn ngạch thuế quan chịu thuế suất thấp hơn.
4 | self-assessment | danh từ | Tự khai, tự tính, tự nộp thuế | Under self-assessment, the declarant calculates the tax payable. | Theo cơ chế tự khai tự tính, người khai tự tính số thuế phải nộp.
4 | tax assessment | danh từ | Ấn định thuế | Customs issued a tax assessment after finding the price was undervalued. | Hải quan ra quyết định ấn định thuế sau khi phát hiện khai giá thấp.
4 | tax payable | danh từ | Số thuế phải nộp | The tax payable increased after the HS code was corrected. | Số thuế phải nộp tăng lên sau khi sửa mã HS.
4 | tax exemption | danh từ | Miễn thuế | Goods imported to create fixed assets may qualify for tax exemption. | Hàng nhập khẩu tạo tài sản cố định có thể được miễn thuế.
4 | tax reduction | danh từ | Giảm thuế | Goods damaged during transport may receive a tax reduction. | Hàng bị hư hỏng trong vận chuyển có thể được giảm thuế.
4 | tax refund | danh từ | Hoàn thuế | The company applied for a tax refund on re-exported goods. | Công ty đề nghị hoàn thuế cho hàng tái xuất.
4 | drawback | danh từ | Hoàn thuế (khi xuất khẩu) | Duty drawback is granted when imported materials are used for export production. | Hoàn thuế được áp dụng khi nguyên liệu nhập khẩu được dùng sản xuất hàng xuất khẩu.
4 | non-collection of tax | danh từ | Không thu thuế | Goods returned to the seller may be eligible for non-collection of tax. | Hàng trả lại người bán có thể thuộc diện không thu thuế.
4 | late payment interest | danh từ | Tiền chậm nộp | Late payment interest is 0.03 percent per day. | Tiền chậm nộp là 0,03% mỗi ngày.
4 | tax arrears | danh từ | Nợ thuế | Enterprises with overdue tax arrears cannot clear new shipments. | Doanh nghiệp nợ thuế quá hạn không được thông quan lô hàng mới.
4 | enforcement of tax decisions | danh từ | Cưỡng chế thi hành quyết định hành chính thuế | Customs started enforcement of tax decisions by freezing the bank account. | Hải quan cưỡng chế bằng biện pháp phong tỏa tài khoản ngân hàng.
4 | bank guarantee | danh từ | Bảo lãnh của ngân hàng | A bank guarantee secures the tax amount during the grace period. | Bảo lãnh ngân hàng bảo đảm số thuế trong thời gian ân hạn.
4 | grace period | danh từ | Thời hạn ân hạn nộp thuế | Priority enterprises enjoy a thirty-day grace period for tax payment. | Doanh nghiệp ưu tiên được ân hạn nộp thuế ba mươi ngày.
4 | deposit | danh từ | Tiền đặt cọc; khoản ký quỹ | A deposit was paid to cover the possible duty. | Một khoản đặt cọc được nộp để bảo đảm số thuế có thể phát sinh.
4 | tax collection | danh từ | Thu thuế | Tax collection at the border gate exceeded the target. | Thu thuế tại cửa khẩu vượt chỉ tiêu.
4 | state budget | danh từ | Ngân sách nhà nước | Import taxes are paid into the state budget. | Thuế nhập khẩu được nộp vào ngân sách nhà nước.
4 | tax liability | danh từ | Nghĩa vụ thuế | The tax liability arises when the declaration is registered. | Nghĩa vụ thuế phát sinh khi tờ khai được đăng ký.
5 | customs value | danh từ | Trị giá hải quan | The customs value is the basis for calculating import duty. | Trị giá hải quan là cơ sở tính thuế nhập khẩu.
5 | customs valuation | danh từ | Xác định trị giá hải quan | Customs valuation follows the WTO Valuation Agreement. | Việc xác định trị giá hải quan tuân theo Hiệp định Trị giá WTO.
5 | transaction value | danh từ | Trị giá giao dịch | Transaction value is the first method of customs valuation. | Trị giá giao dịch là phương pháp xác định trị giá đầu tiên.
5 | price actually paid or payable | cụm từ | Giá thực tế đã thanh toán hay sẽ phải thanh toán | The price actually paid or payable includes the deposit sent to the seller. | Giá thực tế đã thanh toán hay sẽ phải thanh toán bao gồm cả khoản đặt cọc gửi người bán.
5 | identical goods | danh từ | Hàng hóa giống hệt | Customs compared the price with identical goods imported last month. | Hải quan so sánh giá với hàng hóa giống hệt nhập tháng trước.
5 | similar goods | danh từ | Hàng hóa tương tự | If there are no identical goods, use the value of similar goods. | Nếu không có hàng giống hệt thì dùng trị giá hàng tương tự.
5 | deductive value | danh từ | Trị giá khấu trừ | The deductive value starts from the resale price in Vietnam. | Trị giá khấu trừ tính từ giá bán lại tại Việt Nam.
5 | computed value | danh từ | Trị giá tính toán | Computed value is built from the cost of production plus profit. | Trị giá tính toán được xây dựng từ chi phí sản xuất cộng lợi nhuận.
5 | fallback method | danh từ | Phương pháp suy luận | When all other methods fail, customs applies the fallback method. | Khi các phương pháp khác không áp dụng được, hải quan dùng phương pháp suy luận.
5 | adjustment | danh từ | Khoản điều chỉnh (cộng/trừ) | Freight and insurance are adjustments added to the FOB price. | Cước và phí bảo hiểm là khoản điều chỉnh cộng vào giá FOB.
5 | royalties and licence fees | danh từ | Phí bản quyền, phí giấy phép | Royalties and licence fees related to the goods must be added to the value. | Phí bản quyền, phí giấy phép liên quan đến hàng hóa phải cộng vào trị giá.
5 | assist | danh từ | Khoản trợ giúp (người mua cung cấp miễn phí cho người bán) | Moulds supplied free of charge by the buyer are an assist. | Khuôn mẫu người mua cung cấp miễn phí là khoản trợ giúp.
5 | proceeds of resale | danh từ | Khoản tiền thu được sau khi bán lại (người bán được hưởng) | Any proceeds of resale returned to the seller are dutiable. | Khoản tiền thu từ việc bán lại trả cho người bán phải tính vào trị giá.
5 | related parties | danh từ | Các bên có mối quan hệ đặc biệt | Buyer and seller are related parties because they share the same owner. | Người mua và người bán có quan hệ đặc biệt vì cùng một chủ sở hữu.
5 | influence on price | cụm từ | Ảnh hưởng đến giá (mối quan hệ đặc biệt) | The importer proved the relationship had no influence on price. | Người nhập khẩu chứng minh mối quan hệ đặc biệt không ảnh hưởng đến giá.
5 | transfer pricing | danh từ | Chuyển giá | Transfer pricing between subsidiaries may lower the declared value. | Chuyển giá giữa các công ty con có thể làm giảm trị giá khai báo.
5 | undervaluation | danh từ | Khai thấp trị giá | Undervaluation is a common form of customs fraud. | Khai thấp trị giá là một hình thức gian lận hải quan phổ biến.
5 | price consultation | danh từ | Tham vấn giá | The importer was invited to a price consultation to explain the low value. | Người nhập khẩu được mời tham vấn để giải trình mức giá thấp.
5 | reasonable doubt | danh từ | Nghi vấn có cơ sở (về trị giá khai báo) | Customs had reasonable doubt about the truth of the declared value. | Hải quan có nghi vấn có cơ sở về tính trung thực của trị giá khai báo.
5 | valuation database | danh từ | Cơ sở dữ liệu giá | Officers check the valuation database before accepting the price. | Công chức tra cơ sở dữ liệu giá trước khi chấp nhận giá khai báo.
5 | discount | danh từ | Khoản giảm giá | A quantity discount is accepted if it is shown on the invoice. | Khoản giảm giá theo số lượng được chấp nhận nếu thể hiện trên hóa đơn.
5 | buying commission | danh từ | Phí hoa hồng mua hàng (không cộng vào trị giá) | A buying commission paid to the buyer's agent is not added to the value. | Phí hoa hồng mua hàng trả cho đại lý của người mua không cộng vào trị giá.
5 | selling commission | danh từ | Phí hoa hồng bán hàng (phải cộng vào trị giá) | Selling commissions paid by the buyer are dutiable. | Hoa hồng bán hàng do người mua trả phải tính vào trị giá.
5 | valuation method | danh từ | Phương pháp xác định trị giá | The six valuation methods must be applied in strict order. | Sáu phương pháp xác định trị giá phải áp dụng tuần tự.
5 | invoice price | danh từ | Giá hóa đơn | The invoice price did not include the packing costs. | Giá hóa đơn chưa bao gồm chi phí đóng gói.
6 | tariff classification | danh từ | Phân loại hàng hóa (áp mã số) | Correct tariff classification decides the duty rate. | Phân loại hàng hóa đúng quyết định thuế suất.
6 | Harmonized System | danh từ | Hệ thống hài hòa mô tả và mã hóa hàng hóa (HS) | The Harmonized System is used by more than two hundred countries. | Hệ thống HS được hơn hai trăm quốc gia sử dụng.
6 | HS code | danh từ | Mã HS (mã số hàng hóa) | Enter the eight-digit HS code on the declaration. | Nhập mã HS tám số trên tờ khai.
6 | tariff nomenclature | danh từ | Danh mục hàng hóa (biểu thuế) | Vietnam's tariff nomenclature is based on the ASEAN nomenclature. | Danh mục hàng hóa của Việt Nam dựa trên danh mục AHTN.
6 | chapter | danh từ | Chương (trong Danh mục HS) | Vehicles are classified in Chapter 87. | Xe cộ được phân loại ở Chương 87.
6 | section | danh từ | Phần (trong Danh mục HS) | Section XVI covers machinery and electrical equipment. | Phần XVI gồm máy móc và thiết bị điện.
6 | heading | danh từ | Nhóm (4 số) | Mobile phones fall under heading 85.17. | Điện thoại di động thuộc nhóm 85.17.
6 | subheading | danh từ | Phân nhóm (6 số) | Choose the right subheading after the heading is fixed. | Chọn đúng phân nhóm sau khi đã xác định nhóm.
6 | tariff line | danh từ | Dòng thuế (mã 8 số) | Each tariff line has its own duty rate. | Mỗi dòng thuế có thuế suất riêng.
6 | General Interpretative Rules | danh từ | Quy tắc tổng quát giải thích (GIR) | Apply the General Interpretative Rules in numerical order. | Áp dụng các Quy tắc tổng quát giải thích theo thứ tự.
6 | explanatory notes | danh từ | Chú giải chi tiết HS | The explanatory notes explain the scope of each heading. | Chú giải chi tiết giải thích phạm vi của từng nhóm.
6 | section note | danh từ | Chú giải phần | Section notes can exclude certain goods from a chapter. | Chú giải phần có thể loại trừ một số hàng khỏi một chương.
6 | essential character | danh từ | Đặc trưng cơ bản | Classify the set by the component that gives its essential character. | Phân loại bộ hàng theo thành phần tạo nên đặc trưng cơ bản.
6 | parts and accessories | danh từ | Bộ phận và phụ kiện | Parts and accessories of cars fall under heading 87.08. | Bộ phận và phụ kiện ô tô thuộc nhóm 87.08.
6 | unassembled | tính từ | Ở dạng tháo rời | Machines imported unassembled are classified as complete machines. | Máy nhập khẩu ở dạng tháo rời được phân loại như máy hoàn chỉnh.
6 | misclassification | danh từ | Phân loại sai (áp mã sai) | Misclassification led to an underpayment of duty. | Áp mã sai dẫn đến nộp thiếu thuế.
6 | advance ruling | danh từ | Xác định trước (mã số, xuất xứ, trị giá) | The importer requested an advance ruling on classification before signing the contract. | Người nhập khẩu đề nghị xác định trước mã số trước khi ký hợp đồng.
6 | sample analysis | danh từ | Phân tích mẫu (để phân loại) | The laboratory sample analysis showed the product is not food. | Kết quả phân tích mẫu cho thấy sản phẩm không phải thực phẩm.
6 | technical specifications | danh từ | Thông số kỹ thuật | Provide the catalogue and technical specifications for classification. | Cung cấp catalogue và thông số kỹ thuật để phân loại.
6 | material composition | danh từ | Thành phần cấu tạo | Textiles are classified according to their material composition. | Hàng dệt may được phân loại theo thành phần cấu tạo.
7 | rules of origin | danh từ | Quy tắc xuất xứ | Each free trade agreement has its own rules of origin. | Mỗi hiệp định thương mại tự do có quy tắc xuất xứ riêng.
7 | country of origin | danh từ | Nước xuất xứ | The country of origin must be marked on the goods. | Nước xuất xứ phải được ghi trên hàng hóa.
7 | certificate of origin | danh từ | Giấy chứng nhận xuất xứ (C/O) | Submit the certificate of origin to claim preferential tariff. | Nộp C/O để được hưởng thuế suất ưu đãi.
7 | preferential origin | danh từ | Xuất xứ ưu đãi | Goods with preferential origin pay lower duties under the FTA. | Hàng có xuất xứ ưu đãi chịu thuế thấp hơn theo FTA.
7 | non-preferential origin | danh từ | Xuất xứ không ưu đãi | Non-preferential origin matters for anti-dumping measures. | Xuất xứ không ưu đãi quan trọng với biện pháp chống bán phá giá.
7 | wholly obtained | tính từ | Xuất xứ thuần túy | Rice grown and harvested in Vietnam is wholly obtained. | Gạo trồng và thu hoạch tại Việt Nam có xuất xứ thuần túy.
7 | substantial transformation | danh từ | Chuyển đổi cơ bản | Simple packing does not amount to substantial transformation. | Đóng gói đơn giản không tạo ra chuyển đổi cơ bản.
7 | change in tariff classification | danh từ | Chuyển đổi mã số hàng hóa (CTC) | The product meets the change in tariff classification rule. | Sản phẩm đáp ứng tiêu chí chuyển đổi mã số hàng hóa.
7 | change in tariff heading | danh từ | Chuyển đổi nhóm (CTH) | Under CTH, all imported materials must be from a different heading. | Theo tiêu chí CTH, mọi nguyên liệu nhập khẩu phải thuộc nhóm khác.
7 | regional value content | danh từ | Hàm lượng giá trị khu vực (RVC) | The regional value content must be at least forty percent. | Hàm lượng giá trị khu vực phải đạt ít nhất bốn mươi phần trăm.
7 | originating materials | danh từ | Nguyên liệu có xuất xứ | Only originating materials count toward the regional value content. | Chỉ nguyên liệu có xuất xứ mới được tính vào hàm lượng giá trị khu vực.
7 | non-originating materials | danh từ | Nguyên liệu không có xuất xứ | Non-originating materials must undergo sufficient processing. | Nguyên liệu không có xuất xứ phải trải qua công đoạn chế biến đủ.
7 | de minimis | danh từ | Tỷ lệ không đáng kể (De Minimis) | The de minimis rule allows a small share of non-originating materials. | Quy tắc De Minimis cho phép một tỷ lệ nhỏ nguyên liệu không có xuất xứ.
7 | cumulation | danh từ | Cộng gộp xuất xứ | Cumulation lets ASEAN materials count as local content. | Cộng gộp cho phép nguyên liệu ASEAN được tính là hàm lượng nội khối.
7 | minimal operations | danh từ | Công đoạn gia công, chế biến đơn giản | Labelling and repacking are minimal operations. | Dán nhãn và đóng gói lại là công đoạn gia công đơn giản.
7 | direct consignment | danh từ | Vận chuyển trực tiếp | The goods must satisfy the direct consignment rule to keep preferential treatment. | Hàng phải đáp ứng quy tắc vận chuyển trực tiếp để giữ ưu đãi.
7 | back-to-back certificate of origin | danh từ | C/O giáp lưng | A back-to-back certificate of origin was issued in Singapore. | C/O giáp lưng được cấp tại Singapore.
7 | third-country invoicing | danh từ | Hóa đơn do bên thứ ba phát hành | Third-country invoicing is allowed under ATIGA. | Hóa đơn bên thứ ba được chấp nhận theo ATIGA.
7 | self-certification | danh từ | Tự chứng nhận xuất xứ | Under the CPTPP, exporters may use self-certification of origin. | Theo CPTPP, nhà xuất khẩu được tự chứng nhận xuất xứ.
7 | origin verification | danh từ | Xác minh xuất xứ | Customs sent an origin verification request to the issuing authority. | Hải quan gửi yêu cầu xác minh xuất xứ tới cơ quan cấp C/O.
7 | issuing authority | danh từ | Cơ quan, tổ chức cấp C/O | The issuing authority confirmed the certificate was genuine. | Cơ quan cấp C/O xác nhận giấy chứng nhận là thật.
7 | free trade agreement | danh từ | Hiệp định thương mại tự do (FTA) | Vietnam has signed many free trade agreements. | Việt Nam đã ký nhiều hiệp định thương mại tự do.
7 | preferential treatment | danh từ | Ưu đãi thuế quan | The C/O was rejected, so preferential treatment was denied. | C/O bị từ chối nên không được hưởng ưu đãi thuế quan.
7 | origin fraud | danh từ | Gian lận xuất xứ | Relabelling foreign goods as Made in Vietnam is origin fraud. | Dán nhãn hàng ngoại thành Made in Vietnam là gian lận xuất xứ.
8 | type of import-export | danh từ | Loại hình xuất nhập khẩu | Choose the correct type of import-export code on VNACCS. | Chọn đúng mã loại hình trên VNACCS.
8 | outright importation | danh từ | Nhập khẩu kinh doanh | Goods for outright importation are sold on the domestic market. | Hàng nhập kinh doanh được bán trên thị trường nội địa.
8 | outright exportation | danh từ | Xuất khẩu kinh doanh (xuất hẳn) | Outright exportation means the goods leave permanently. | Xuất khẩu kinh doanh nghĩa là hàng rời đi vĩnh viễn.
8 | inward processing | danh từ | Gia công cho thương nhân nước ngoài (nhận gia công) | Garment factories often work under inward processing contracts. | Các nhà máy may thường làm hợp đồng nhận gia công cho nước ngoài.
8 | outward processing | danh từ | Đặt gia công ở nước ngoài | The company sent materials abroad under outward processing. | Công ty gửi nguyên liệu ra nước ngoài theo hình thức đặt gia công.
8 | processing contract | danh từ | Hợp đồng gia công | The processing contract lists the materials supplied by the foreign party. | Hợp đồng gia công liệt kê nguyên liệu do bên nước ngoài cung cấp.
8 | production for export | danh từ | Sản xuất xuất khẩu (SXXK) | Materials imported for production for export are exempt from import duty. | Nguyên liệu nhập để sản xuất xuất khẩu được miễn thuế nhập khẩu.
8 | export processing enterprise | danh từ | Doanh nghiệp chế xuất | Sales from an export processing enterprise to the local market are imports. | Hàng doanh nghiệp chế xuất bán vào nội địa được coi là nhập khẩu.
8 | raw materials | danh từ | Nguyên liệu | Imported raw materials must be recorded in the stock ledger. | Nguyên liệu nhập khẩu phải được ghi sổ kho.
8 | consumption norm | danh từ | Định mức sử dụng nguyên liệu | The consumption norm shows how much fabric one shirt needs. | Định mức cho biết một chiếc áo cần bao nhiêu vải.
8 | wastage rate | danh từ | Tỷ lệ hao hụt | The declared wastage rate was far higher than the industry average. | Tỷ lệ hao hụt khai báo cao hơn nhiều so với mức trung bình ngành.
8 | finalization report | danh từ | Báo cáo quyết toán | Processing firms submit an annual finalization report to customs. | Doanh nghiệp gia công nộp báo cáo quyết toán năm cho hải quan.
8 | scrap | danh từ | Phế liệu | Scrap from processing must be declared if it is sold locally. | Phế liệu gia công bán vào nội địa phải làm thủ tục khai báo.
8 | temporary admission | danh từ | Tạm nhập (tái xuất) | Exhibition goods enter under temporary admission. | Hàng triển lãm được tạm nhập.
8 | temporary import for re-export | danh từ | Tạm nhập tái xuất | Temporary import for re-export must be completed within the permitted time. | Tạm nhập tái xuất phải hoàn thành trong thời hạn cho phép.
8 | temporary export for re-import | danh từ | Tạm xuất tái nhập | The machine was temporarily exported for re-import after repair. | Máy được tạm xuất tái nhập sau khi sửa chữa.
8 | re-exportation | danh từ | Tái xuất | Re-exportation of the goods ended the temporary admission. | Việc tái xuất hàng đã kết thúc thủ tục tạm nhập.
8 | re-importation | danh từ | Tái nhập | Rejected exports may be returned by re-importation. | Hàng xuất khẩu bị trả lại có thể tái nhập.
8 | ATA carnet | danh từ | Sổ tạm quản ATA | Professional equipment can travel on an ATA carnet. | Thiết bị chuyên dụng có thể đi kèm sổ tạm quản ATA.
8 | customs transit | danh từ | Vận chuyển hàng hóa chịu sự giám sát hải quan (quá cảnh hải quan) | Goods moved under customs transit to the inland depot. | Hàng được vận chuyển dưới sự giám sát hải quan về cảng cạn.
8 | transit goods | danh từ | Hàng quá cảnh | Transit goods to Laos pass through Vietnamese territory. | Hàng quá cảnh sang Lào đi qua lãnh thổ Việt Nam.
8 | bonded warehouse | danh từ | Kho ngoại quan | Goods in a bonded warehouse are not yet subject to import duty. | Hàng trong kho ngoại quan chưa phải chịu thuế nhập khẩu.
8 | tax suspension warehouse | danh từ | Kho bảo thuế | A tax suspension warehouse stores materials for production for export. | Kho bảo thuế lưu giữ nguyên liệu phục vụ sản xuất xuất khẩu.
8 | free zone | danh từ | Khu phi thuế quan | Goods brought into a free zone are treated as outside the customs territory. | Hàng đưa vào khu phi thuế quan được coi như ở ngoài lãnh thổ hải quan.
8 | duty-free shop | danh từ | Cửa hàng miễn thuế | Passengers bought perfume at the duty-free shop. | Hành khách mua nước hoa tại cửa hàng miễn thuế.
8 | on-the-spot export and import | danh từ | Xuất nhập khẩu tại chỗ | The finished goods were delivered in Vietnam as on-the-spot export and import. | Thành phẩm được giao tại Việt Nam theo hình thức xuất nhập khẩu tại chỗ.
8 | goods for personal use | danh từ | Hàng hóa phục vụ mục đích cá nhân (hành lý) | Goods for personal use within the allowance are duty-free. | Hàng tiêu dùng cá nhân trong định mức được miễn thuế.
8 | samples of no commercial value | danh từ | Hàng mẫu không có giá trị thương mại | Samples of no commercial value are cleared quickly. | Hàng mẫu không có giá trị thương mại được thông quan nhanh.
8 | relief consignment | danh từ | Hàng cứu trợ | Relief consignments after the flood received priority clearance. | Hàng cứu trợ sau lũ được ưu tiên thông quan.
9 | post-clearance audit | danh từ | Kiểm tra sau thông quan | Post-clearance audit checks declarations after the goods are released. | Kiểm tra sau thông quan kiểm tra tờ khai sau khi hàng đã được giải phóng.
9 | audit-based control | danh từ | Kiểm soát dựa trên kiểm toán | Audit-based control shifts checks from the border to the company's records. | Kiểm soát dựa trên kiểm toán chuyển việc kiểm tra từ cửa khẩu sang sổ sách doanh nghiệp.
9 | audit at the customs office | danh từ | Kiểm tra tại trụ sở cơ quan hải quan | The audit at the customs office reviewed twenty declarations. | Cuộc kiểm tra tại trụ sở cơ quan hải quan rà soát hai mươi tờ khai.
9 | audit at the enterprise premises | danh từ | Kiểm tra tại trụ sở người khai hải quan | An audit at the enterprise premises lasts no more than five working days. | Kiểm tra tại trụ sở người khai hải quan không quá năm ngày làm việc.
9 | audit decision | danh từ | Quyết định kiểm tra | The audit decision was sent to the company five days in advance. | Quyết định kiểm tra được gửi doanh nghiệp trước năm ngày.
9 | audit team | danh từ | Đoàn kiểm tra | The audit team examined the warehouse records. | Đoàn kiểm tra đã kiểm tra sổ sách kho.
9 | audit findings | danh từ | Kết quả kiểm tra (phát hiện) | The audit findings showed missing materials worth two billion dong. | Kết quả kiểm tra cho thấy nguyên liệu thiếu trị giá hai tỷ đồng.
9 | audit conclusion | danh từ | Kết luận kiểm tra | The company must pay the extra tax stated in the audit conclusion. | Doanh nghiệp phải nộp số thuế truy thu ghi trong kết luận kiểm tra.
9 | audit record | danh từ | Biên bản kiểm tra | Both parties signed the audit record at the end of the day. | Hai bên ký biên bản kiểm tra vào cuối ngày.
9 | accounting records | danh từ | Sổ sách, chứng từ kế toán | Keep accounting records for at least five years. | Lưu giữ sổ sách chứng từ kế toán ít nhất năm năm.
9 | stock ledger | danh từ | Sổ kho (thẻ kho) | The stock ledger did not match the finalization report. | Sổ kho không khớp với báo cáo quyết toán.
9 | inventory reconciliation | danh từ | Đối chiếu tồn kho | Inventory reconciliation revealed a shortage of fabric. | Đối chiếu tồn kho phát hiện thiếu vải.
9 | physical stock count | danh từ | Kiểm kê thực tế tồn kho | The team carried out a physical stock count at the factory. | Đoàn tiến hành kiểm kê thực tế tồn kho tại nhà máy.
9 | discrepancy | danh từ | Chênh lệch, sai lệch | Explain the discrepancy between the invoice and the payment. | Giải trình chênh lệch giữa hóa đơn và chứng từ thanh toán.
9 | explanation | danh từ | Giải trình | The company submitted a written explanation within ten days. | Doanh nghiệp nộp văn bản giải trình trong mười ngày.
9 | retroactive collection | danh từ | Truy thu thuế | The audit resulted in retroactive collection of import duty. | Cuộc kiểm tra dẫn đến truy thu thuế nhập khẩu.
9 | compliance | danh từ | Sự tuân thủ | High compliance reduces the chance of physical inspection. | Mức tuân thủ cao làm giảm khả năng bị kiểm tra thực tế.
9 | voluntary disclosure | danh từ | Tự nguyện khai báo (khai bổ sung) | Voluntary disclosure before the audit reduces the penalty. | Tự nguyện khai bổ sung trước khi kiểm tra giúp giảm mức phạt.
9 | payment documents | danh từ | Chứng từ thanh toán | Bank payment documents confirm the real price paid. | Chứng từ thanh toán qua ngân hàng xác nhận giá thực trả.
9 | statute of limitations | danh từ | Thời hiệu | Customs may audit within five years of registering the declaration. | Hải quan được kiểm tra trong vòng năm năm kể từ ngày đăng ký tờ khai.
10 | risk management | danh từ | Quản lý rủi ro | Risk management helps customs target high-risk shipments. | Quản lý rủi ro giúp hải quan tập trung vào lô hàng rủi ro cao.
10 | risk analysis | danh từ | Phân tích rủi ro | Risk analysis is based on the declarant's compliance history. | Phân tích rủi ro dựa trên lịch sử tuân thủ của người khai.
10 | risk profile | danh từ | Hồ sơ rủi ro (tiêu chí rủi ro) | A new risk profile targets undervalued electronics. | Hồ sơ rủi ro mới nhắm vào hàng điện tử khai giá thấp.
10 | selectivity | danh từ | Phân luồng tự động (lựa chọn kiểm tra) | The selectivity system assigns each declaration a channel. | Hệ thống phân luồng gán luồng cho mỗi tờ khai.
10 | customs control | danh từ | Kiểm soát hải quan | All goods crossing the border are subject to customs control. | Mọi hàng hóa qua biên giới đều chịu sự kiểm soát hải quan.
10 | customs supervision | danh từ | Giám sát hải quan | Goods in transit remain under customs supervision. | Hàng đang vận chuyển vẫn chịu sự giám sát hải quan.
10 | x-ray scanning | danh từ | Soi chiếu (máy soi) | X-ray scanning found hidden cigarettes in the container. | Soi chiếu phát hiện thuốc lá giấu trong container.
10 | container scanner | danh từ | Máy soi container | The container scanner can check a truck in two minutes. | Máy soi container kiểm tra một xe tải trong hai phút.
10 | seal tampering | danh từ | Can thiệp, làm hư hỏng niêm phong | Seal tampering was detected when the truck arrived. | Phát hiện niêm phong bị can thiệp khi xe đến.
10 | electronic seal | danh từ | Niêm phong điện tử (định vị) | An electronic seal tracks the container by GPS. | Niêm phong điện tử theo dõi container bằng GPS.
10 | intelligence | danh từ | Thông tin nghiệp vụ, tình báo hải quan | Customs intelligence identified the smuggling route. | Thông tin nghiệp vụ hải quan đã xác định tuyến buôn lậu.
10 | targeting | danh từ | Xác định trọng điểm | Targeting focuses inspections on suspicious consignments. | Xác định trọng điểm giúp tập trung kiểm tra vào lô hàng đáng ngờ.
10 | profiling | danh từ | Lập hồ sơ (đánh giá) rủi ro | Passenger profiling helps officers pick bags to check. | Đánh giá rủi ro hành khách giúp công chức chọn hành lý để kiểm tra.
10 | compliance level | danh từ | Mức độ tuân thủ | Enterprises are classified by compliance level. | Doanh nghiệp được phân loại theo mức độ tuân thủ.
10 | high-risk enterprise | danh từ | Doanh nghiệp rủi ro cao | Declarations of a high-risk enterprise are routed to the red channel. | Tờ khai của doanh nghiệp rủi ro cao được phân luồng đỏ.
10 | detector dog | danh từ | Chó nghiệp vụ | The detector dog found drugs in a suitcase. | Chó nghiệp vụ phát hiện ma túy trong va li.
10 | surveillance camera | danh từ | Camera giám sát | Surveillance cameras cover the entire container yard. | Camera giám sát bao quát toàn bộ bãi container.
10 | Coordinated Border Management | danh từ | Quản lý biên giới phối hợp | Coordinated Border Management links customs, police and quarantine. | Quản lý biên giới phối hợp liên kết hải quan, công an và kiểm dịch.
10 | SAFE Framework of Standards | danh từ | Khung tiêu chuẩn SAFE của WCO | The SAFE Framework of Standards secures the global supply chain. | Khung tiêu chuẩn SAFE bảo đảm an ninh chuỗi cung ứng toàn cầu.
11 | customs offence | danh từ | Vi phạm pháp luật hải quan | Failure to declare is a customs offence. | Không khai báo là hành vi vi phạm pháp luật hải quan.
11 | administrative violation | danh từ | Vi phạm hành chính | False declaration without tax loss is an administrative violation. | Khai sai không làm thiệt hại thuế là vi phạm hành chính.
11 | penalty | danh từ | Hình phạt, tiền phạt | The penalty was twenty percent of the tax shortfall. | Mức phạt là hai mươi phần trăm số thuế thiếu.
11 | penalty decision | danh từ | Quyết định xử phạt | The company appealed against the penalty decision. | Doanh nghiệp khiếu nại quyết định xử phạt.
11 | record of violation | danh từ | Biên bản vi phạm hành chính | The officer drew up a record of violation at the scene. | Công chức lập biên bản vi phạm hành chính tại chỗ.
11 | fine | danh từ | Phạt tiền | The importer paid a fine for late declaration. | Người nhập khẩu nộp phạt vì khai báo chậm.
11 | false declaration | danh từ | Khai sai | False declaration of quantity is punishable by fine. | Khai sai số lượng bị xử phạt tiền.
11 | smuggling | danh từ | Buôn lậu | Smuggling of cigarettes increased along the border. | Buôn lậu thuốc lá gia tăng dọc biên giới.
11 | illegal cross-border transportation | danh từ | Vận chuyển trái phép hàng hóa qua biên giới | He was charged with illegal cross-border transportation of goods. | Anh ta bị truy tố về tội vận chuyển trái phép hàng hóa qua biên giới.
11 | commercial fraud | danh từ | Gian lận thương mại | Commercial fraud damages honest businesses. | Gian lận thương mại gây thiệt hại cho doanh nghiệp làm ăn chân chính.
11 | tax evasion | danh từ | Trốn thuế | Using fake invoices is a form of tax evasion. | Dùng hóa đơn giả là một hình thức trốn thuế.
11 | counterfeit goods | danh từ | Hàng giả | Customs seized counterfeit goods bearing famous brands. | Hải quan tạm giữ hàng giả mang thương hiệu nổi tiếng.
11 | intellectual property rights | danh từ | Quyền sở hữu trí tuệ | Customs can suspend clearance of goods infringing intellectual property rights. | Hải quan có thể tạm dừng làm thủ tục với hàng xâm phạm quyền sở hữu trí tuệ.
11 | prohibited goods | danh từ | Hàng cấm | Prohibited goods cannot be imported under any circumstances. | Hàng cấm không được nhập khẩu trong bất kỳ trường hợp nào.
11 | restricted goods | danh từ | Hàng hạn chế (có điều kiện) | Restricted goods need a licence or permit. | Hàng hạn chế cần giấy phép.
11 | seizure | danh từ | Tạm giữ, thu giữ | The seizure of two tonnes of ivory made headlines. | Vụ thu giữ hai tấn ngà voi gây chú ý.
11 | confiscation | danh từ | Tịch thu | Confiscation of the smuggled goods was ordered by the court. | Tòa ra lệnh tịch thu hàng buôn lậu.
11 | exhibits | danh từ | Tang vật (vi phạm) | The exhibits were kept in the customs warehouse. | Tang vật được lưu giữ tại kho hải quan.
11 | drug trafficking | danh từ | Mua bán, vận chuyển trái phép chất ma túy | Drug trafficking through airports is a major threat. | Vận chuyển trái phép ma túy qua sân bay là mối đe dọa lớn.
11 | controlled delivery | danh từ | Chuyển giao có kiểm soát | Police and customs used a controlled delivery to catch the buyers. | Công an và hải quan dùng biện pháp chuyển giao có kiểm soát để bắt người mua.
11 | money laundering | danh từ | Rửa tiền | Trade-based money laundering hides illegal funds in invoices. | Rửa tiền qua thương mại che giấu tiền bất hợp pháp trong hóa đơn.
11 | concealment | danh từ | Cất giấu | The drugs were found in a false-bottom concealment. | Ma túy được phát hiện trong khoang giấu hai đáy.
11 | mitigating circumstances | danh từ | Tình tiết giảm nhẹ | Voluntary disclosure is a mitigating circumstance. | Tự nguyện khai báo là tình tiết giảm nhẹ.
11 | aggravating circumstances | danh từ | Tình tiết tăng nặng | Repeated violations are aggravating circumstances. | Vi phạm nhiều lần là tình tiết tăng nặng.
11 | appeal | danh từ | Khiếu nại | The declarant has the right of appeal against a customs decision. | Người khai có quyền khiếu nại quyết định của hải quan.
11 | prosecution | danh từ | Truy cứu trách nhiệm hình sự | The case was transferred for criminal prosecution. | Vụ việc được chuyển để truy cứu trách nhiệm hình sự.
11 | wildlife trafficking | danh từ | Buôn bán trái phép động vật hoang dã | Customs cooperates with CITES to fight wildlife trafficking. | Hải quan phối hợp với CITES chống buôn bán trái phép động vật hoang dã.
12 | Incoterms | danh từ | Điều kiện thương mại quốc tế (Incoterms) | Incoterms define who pays freight and insurance. | Incoterms xác định bên nào trả cước và phí bảo hiểm.
12 | Ex Works | danh từ | Giao tại xưởng (EXW) | Under Ex Works, the buyer collects the goods at the seller's factory. | Theo EXW, người mua nhận hàng tại xưởng của người bán.
12 | Free Carrier | danh từ | Giao cho người chuyên chở (FCA) | Free Carrier is popular for container shipments. | FCA phổ biến với hàng container.
12 | Free Alongside Ship | danh từ | Giao dọc mạn tàu (FAS) | Free Alongside Ship is used for bulk cargo. | FAS dùng cho hàng rời.
12 | Free On Board | danh từ | Giao lên tàu (FOB) | Under Free On Board, risk passes when the goods are on the vessel. | Theo FOB, rủi ro chuyển giao khi hàng đã lên tàu.
12 | Cost and Freight | danh từ | Tiền hàng và cước phí (CFR) | Cost and Freight does not include insurance. | CFR không bao gồm bảo hiểm.
12 | Cost, Insurance and Freight | danh từ | Tiền hàng, bảo hiểm và cước phí (CIF) | Vietnam calculates import duty on a CIF basis. | Việt Nam tính thuế nhập khẩu trên cơ sở giá CIF.
12 | Carriage Paid To | danh từ | Cước phí trả tới (CPT) | Carriage Paid To suits multimodal transport. | CPT phù hợp với vận tải đa phương thức.
12 | Carriage and Insurance Paid To | danh từ | Cước phí và bảo hiểm trả tới (CIP) | CIP requires the seller to buy all-risks insurance. | CIP yêu cầu người bán mua bảo hiểm mọi rủi ro.
12 | Delivered At Place | danh từ | Giao tại nơi đến (DAP) | Under Delivered At Place, the buyer handles import clearance. | Theo DAP, người mua làm thủ tục nhập khẩu.
12 | Delivered at Place Unloaded | danh từ | Giao tại nơi đến đã dỡ xuống (DPU) | DPU is the only term where the seller unloads at destination. | DPU là điều kiện duy nhất người bán dỡ hàng tại nơi đến.
12 | Delivered Duty Paid | danh từ | Giao hàng đã nộp thuế (DDP) | With Delivered Duty Paid, the seller pays the import duties. | Theo DDP, người bán nộp thuế nhập khẩu.
12 | transfer of risk | danh từ | Chuyển giao rủi ro | The Incoterm decides the point of transfer of risk. | Điều kiện Incoterms quyết định điểm chuyển giao rủi ro.
12 | letter of credit | danh từ | Thư tín dụng (L/C) | Payment was made by irrevocable letter of credit. | Thanh toán bằng thư tín dụng không hủy ngang.
12 | telegraphic transfer | danh từ | Chuyển tiền bằng điện (T/T) | Most small orders are paid by telegraphic transfer. | Đơn hàng nhỏ thường thanh toán bằng chuyển tiền điện.
12 | documents against payment | danh từ | Nhờ thu trả tiền đổi chứng từ (D/P) | Under documents against payment, the buyer pays before receiving the bill of lading. | Theo D/P, người mua trả tiền trước khi nhận vận đơn.
12 | advance payment | danh từ | Thanh toán trước | An advance payment of thirty percent was sent to the seller. | Ba mươi phần trăm tiền hàng đã được thanh toán trước cho người bán.
12 | proforma invoice | danh từ | Hóa đơn chiếu lệ | The proforma invoice is not accepted for customs valuation. | Hóa đơn chiếu lệ không được chấp nhận để xác định trị giá.
12 | purchase order | danh từ | Đơn đặt hàng | The purchase order confirms the quantity and price. | Đơn đặt hàng xác nhận số lượng và giá.
12 | exchange rate | danh từ | Tỷ giá | Customs uses the exchange rate published by the bank on the declaration date. | Hải quan dùng tỷ giá ngân hàng công bố vào ngày khai báo.
"""


def rows():
    """Tách RAW thành danh sách bộ 6 trường, bỏ dòng trống.

    Returns:
        list[tuple]: (topic_index, en, pos, vi, ex, ex_vi).
    Raises:
        ValueError: dòng thiếu trường (sai số dấu "|").
    """
    out = []
    for line in RAW.strip().splitlines():
        parts = [p.strip() for p in line.split(" | ")]
        if len(parts) != 6:
            raise ValueError(f"Dòng sai định dạng: {line}")
        out.append((int(parts[0]), *parts[1:]))
    return out
