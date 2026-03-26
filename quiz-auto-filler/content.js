// Import dữ liệu Q&A
const qaData = {
    "Tại sao bản đồ khái niệm được xem là công cụ mô hình hóa tri thức phù hợp?": "Vì nó cho phép diễn tả khái niệm theo cách trực quan, linh hoạt và gắn kết.",
    "Tại sao bản đồ khái niệm được xem là công cụ lý tưởng để chia sẻ tri thức chuyên gia?": "Vì nó loại bỏ yếu tố ngữ cảnh và chuẩn hóa mọi tri thức.",
    "Vai trò của phần mềm CmapTools trong quá trình nắm bắt tri thức là gì?": "Hỗ trợ thu nhận, tổ chức và trình bày tri thức chuyên gia dưới dạng mô hình trực quan.",
    "Một đặc điểm giúp CITKA nổi bật so với phương pháp phỏng vấn truyền thống là gì?": "Có khả năng tạo ra cơ sở ngữ cảnh hoàn chỉnh từ các truy vấn tự động.",
    "Điểm đặc trưng của các liên kết (links) trong bản đồ khái niệm là gì?": "Chúng được gắn nhãn rõ ràng và thể hiện mối quan hệ dưới dạng mệnh đề có nghĩa.",
    "Trong hệ thống CITKA, vai trò của Knowledge Engineering Database (KEDB) là gì?": "Lưu trữ cơ sở ngữ cảnh đang được phát triển theo cấu trúc phân cấp của CxBR.",
    "Khi một ngữ cảnh chính đang hoạt động trong hệ thống CxBR, điều nào sau đây là đúng?": "Chỉ một ngữ cảnh chính được kích hoạt tại một thời điểm và kiểm soát toàn bộ hành vi.",
    "Khái niệm \"cross-links\" trong bản đồ khái niệm có ý nghĩa gì?": "Liên kết giữa các lĩnh vực tri thức khác nhau giúp nhận diện mối quan hệ liên ngành.",
    "Theo ước tính, CITKA có thể tự động xây dựng bao nhiêu phần trăm mô hình tri thức dựa trên ngữ cảnh?": "Từ 50% đến 80% tổng cấu trúc mô hình.",
    "Nếu chuyên gia mô tả tri thức theo trình tự các sự kiện xảy ra, mô hình nào được xem là thích hợp nhất?": "Mô hình dựa trên ràng buộc (constraint-based).",
    "Khác biệt cơ bản giữa bản đồ khái niệm và mạng ngữ nghĩa (semantic network) là gì?": "Bản đồ khái niệm tạo mệnh đề bằng từ nối và thường có phân cấp phục vụ học tập; mạng ngữ nghĩa nhấn mạnh quan hệ",
    "Kết luận quan trọng rút ra từ các hệ thống học tập bằng quan sát là gì?": "Có thể thu nhận tri thức từ chuyên gia thông qua tương tác gián tiếp và không xâm nhập.",
    "Một ưu điểm quan trọng của bản đồ khái niệm khi dùng trong các hệ thống tri thức là gì?": "Có khả năng mở rộng quy mô để bao quát lượng thông tin lớn.",
    "Trong hệ thống CITKA, SME Interface (SMEI) đóng vai trò gì?": "Là giao diện đồ họa động cho phép chuyên gia tương tác với các câu hỏi và quy tắc trong QRB.",
    "Điểm khác biệt giữa tri thức chiến thuật và tri thức chiến lược là gì?": "Tri thức chiến thuật mang tính ngắn hạn, còn tri thức chiến lược định hướng dài hạn.",
    "Theo các nhà nghiên cứu, ưu điểm nổi bật của CmapTools trong nắm bắt tri thức là gì?": "Khả năng hiển thị phong phú đa phương tiện và hỗ trợ học tập, cộng tác trực tuyến.",
    "Điểm khác biệt giữa observational learning và cognitive imitation là gì?": "Quan sát có thể không bao gồm hành vi bắt chước, trong khi bắt chước luôn cần quan sát.",
    "Trong hệ thống nắm bắt tri thức dựa trên bản đồ khái niệm, vai trò chính của CmapTools là gì?": "Cung cấp môi trường thu nhận, tổ chức và duyệt tri thức dưới dạng cấu trúc khái niệm.",
    "Trong hệ thống CmapTools, người học có thể thu nhận tri thức chuyên gia bằng cách nào?": "Duyệt qua các bản đồ khái niệm và khám phá mối liên kết giữa các khái niệm.",
    "Tác dụng quan trọng nhất của bản đồ khái niệm trong đào tạo là gì?": "Giúp người học nhận diện cấu trúc tri thức và mối liên hệ giữa các khái niệm.",
    "Vì sao bản đồ khái niệm được xem là công cụ hỗ trợ học tập hiệu quả?": "Vì nó cho phép người học khám phá cấu trúc tri thức của chuyên gia một cách trực quan.",
    "Vì sao CxBR được xem là mô hình trực quan để mô phỏng hành vi con người?": "Vì nó tổ chức tri thức theo cấu trúc phân cấp, mô phỏng cách con người ra quyết định theo ngữ cảnh.",
    "Cấu trúc phân cấp của bản đồ khái niệm mang lại lợi ích gì khi mở rộng quy mô tri thức?": "Giúp tích hợp dễ dàng các khái niệm của nhiều lĩnh vực vào cùng hệ thống.",
    "Một trong những hướng nghiên cứu nổi bật về học tập bằng quan sát là gì?": "Thiết kế các tác nhân thông minh có khả năng học thêm từ các trải nghiệm mới.",
    "CmapTools hỗ trợ người học thông qua đặc điểm nào sau đây?": "Tạo môi trường học tập đa phương tiện với khả năng hợp tác từ xa.",
    "Trong hệ thống CmapTools, các biểu tượng nhỏ (icons) bên dưới các nút khái niệm có chức năng gì?": "Liên kết tới các tài nguyên đa phương tiện như hình ảnh, video hoặc văn bản.",
    "Giải pháp nào được khuyến nghị để vượt qua sự e dè của chuyên gia khi tương tác với hệ thống tri thức?": "Cung cấp đào tạo phù hợp và giao diện thân thiện với người dùng.",
    "Khi nói đến \"trình duyệt dựa trên bản đồ khái niệm\", ý nghĩa chính của cụm này là gì?": "Một giao diện cho phép duyệt tri thức theo cấu trúc liên kết khái niệm thay vì theo thứ tự tuyến tính.",
    "Trong quá trình xây dựng bản đồ khái niệm, mối quan hệ giữa kỹ sư tri thức và chuyên gia lĩnh vực là gì?": "Hợp tác cùng xây dựng mô hình khái niệm chia sẻ về tri thức.",
    "Thành phần Knowledge Engineering Interface (KEI) của CITKA cung cấp điều gì?": "Một giao diện bảng biểu cho phép nhập liệu thông qua tám hộp thoại tương tác.",
    "Từ góc nhìn của chuyên gia, rào cản chính khi tương tác với hệ thống nắm bắt tri thức là gì?": "Cảm giác e ngại khi phải học cách sử dụng công nghệ mới.",
    "Phần mềm CITKA được thiết kế với mục tiêu tự động hóa điều gì?": "Quá trình thu nhận tri thức chiến thuật của chuyên gia thông qua các truy vấn thông minh.",
    "Theo quan điểm của kỹ sư tri thức, điều kiện tiên quyết để biểu diễn tri thức một cách chính xác là gì?": "Xác định sớm loại hình tri thức để chọn mô hình biểu diễn thích hợp.",
    "Trong mô hình CxBR, \"mission context\" có vai trò gì?": "Xác định phạm vi, mục tiêu và ràng buộc tổng thể của nhiệm vụ.",
    "Trong cấu trúc CITKA, Query Rule-Base (QRB) có chức năng chính nào?": "Lưu trữ và điều phối các quy tắc đối thoại với chuyên gia.",
    "Vì sao việc phát triển công cụ đa mô hình (multiparadigm tool) trong nắm bắt tri thức gần như bất khả thi?": "Vì không thể xác định trước loại tri thức phù hợp với mỗi mô hình.",
    "Tại sao bản đồ khái niệm được xem là giải pháp cho vấn đề \"điều hướng\" trong các hệ thống siêu phương tiện (hypermedia)?": "Vì nó định hướng người dùng theo mối liên hệ logic giữa các khái niệm.",
    "Khái niệm tri thức chiến thuật trong Context-Based Reasoning (CxBR) được hiểu là gì?": "Tri thức phục vụ đánh giá tình huống, lựa chọn kế hoạch hành động và thực thi kế hoạch đó.",
    "Nếu chuyên gia mô tả tri thức bằng cấu trúc \"nếu A thì B\", hình thức biểu diễn phù hợp nhất là gì?": "Mô hình dựa trên quy tắc (rule-based).",
    "Khi ứng dụng bản đồ khái niệm vào đo lường tri thức chuyên gia, lợi ích nổi bật là gì?": "Có thể đánh giá mức độ hiểu biết về chủ đề trong ngữ cảnh cụ thể.",
    "Theo lý thuyết học tập có ý nghĩa của Ausubel, điều kiện nào là cần thiết để việc học bằng bản đồ khái niệm đạt hiệu quả?": "Học viên phải có tri thức nền tảng liên quan để tích hợp khái niệm mới.",
    "Trong mô hình bản đồ khái niệm, \"proposition\" được hiểu là gì?": "Một đơn vị ngữ nghĩa tạo bởi hai khái niệm được nối bằng từ liên kết.",
    "Khái niệm cognitive imitation trong nghiên cứu về tri thức có ý nghĩa nào sau đây?": "Học viên sao chép cách chuyên gia sử dụng quy tắc để giải quyết vấn đề.",
    "Trong bản đồ khái niệm, mối quan hệ giữa hai khái niệm được thể hiện thông qua yếu tố nào?": "Từ nối (linking word) tạo nên một mệnh đề có nghĩa.",
    "Trong mô hình CxBR, \"context\" được định nghĩa là gì?": "Tập hợp các hành động và thủ tục phù hợp để xử lý một tình huống cụ thể.",
    "Kết quả thử nghiệm CITKA trong mô hình tác chiến tàu ngầm cho thấy điều gì?": "Có thể giảm tới 80% thời gian nhân công so với phương pháp phỏng vấn truyền thống.",
    "Trong cấu trúc của bản đồ khái niệm, trục dọc đóng vai trò gì?": "Biểu thị hệ thống phân cấp từ khái niệm tổng quát đến chi tiết.",
    "Khi một tình huống bất ngờ xuất hiện, điều gì xảy ra trong hệ thống CxBR?": "Một chuyển đổi giữa các ngữ cảnh được kích hoạt để phản ứng với tình huống mới.",
    "Khi một người lái xe rời đường cao tốc để vào khu vực nội đô, hành vi nào mô tả đúng bản chất của CxBR?": "Chuyển đổi từ ngữ cảnh lái xe trên cao tốc sang ngữ cảnh lái xe trong thành phố với bộ quy tắc mới.",
    "Một trong những rào cản lớn nhất đối với việc tự động thu nhận tri thức của chuyên gia là gì?": "Kỹ sư tri thức cần hình thành sớm nhận thức về bản chất và cấu trúc tri thức của chuyên gia.",
    "Một hệ thống nắm bắt tri thức lý tưởng trong tương lai cần có khả năng gì?": "Hiểu bản chất tri thức và tự động đặt câu hỏi tương thích với chuyên gia.",
    "Trong cấu trúc CxBR, \"subcontext\" có chức năng gì?": "Xử lý các hành động chi tiết thuộc một ngữ cảnh chính và có thể được tái sử dụng.",
    "CITKA hoạt động dựa trên nguyên lý nào của Context-Based Reasoning (CxBR)?": "Tổ chức tri thức thành các ngữ cảnh phân cấp có thể tái sử dụng và mở rộng.",
    "Lợi ích quan trọng nhất khi áp dụng mô hình CITKA là gì?": "Giảm mạnh nhu cầu nhân lực và sai sót khi thu nhận tri thức chuyên gia.",
    "Theo hướng tiếp cận mới, tác nhân học tập hiệu quả cần có đặc điểm gì?": "Sở hữu tri thức nền tảng để có thể tiếp thu tri thức mới một cách tích lũy."
};

// Hàm trích xuất câu hỏi từ trang
function extractQuestions() {
  const questions = [];
  const questionElements = document.querySelectorAll('div.qtext');
  
  questionElements.forEach((el, index) => {
    const questionText = el.textContent.trim();
    const container = el.closest('div.que');
    if (container && questionText) {
      questions.push({
        index,
        text: questionText,
        container: container
      });
    }
  });
  
  return questions;
}

// Hàm tìm kiếm đáp án gần nhất (fuzzy matching)
async function findBestAnswer(questionText) {
  let bestMatch = null;
  let bestScore = 0;
  
  for (const [q, a] of Object.entries(qaData)) {
    const score = calculateSimilarity(questionText, q);
    if (score > bestScore) {
      bestScore = score;
      bestMatch = { answer: a, isFromAPI: false };
    }
  }
  
  if (bestScore > 0.5) {
    return bestMatch;
  }
  
  // Nếu không tìm thấy trong data, gọi API DeepSeek
  console.log(`🔍 Không tìm thấy trong data, gọi API DeepSeek cho: ${questionText}`);
  try {
    const apiAnswer = await callDeepSeekAPI(questionText);
    if (apiAnswer) {
      return { answer: apiAnswer, isFromAPI: true };
    }
  } catch (error) {
    console.error('✗ Lỗi gọi API DeepSeek:', error);
  }
  
  return null;
}

// Hàm gọi API DeepSeek
async function callDeepSeekAPI(question) {
  const API_KEY = 'YOUR_DEEPSEEK_API_KEY'; // Thay bằng API key thực tế
  const API_URL = 'https://api.deepseek.com/v1/chat/completions';
  
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          {
            role: 'user',
            content: `Đây là câu hỏi trắc nghiệm: "${question}". Hãy trả lời ngắn gọn, chỉ nội dung đáp án chính xác.`
          }
        ],
        max_tokens: 100
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const data = await response.json();
    const answer = data.choices[0]?.message?.content?.trim();
    return answer;
  } catch (error) {
    console.error('Lỗi gọi API:', error);
    return null;
  }
}

// Hàm tính độ tương đồng giữa hai chuỗi
function calculateSimilarity(str1, str2) {
  const s1 = str1.toLowerCase().trim();
  const s2 = str2.toLowerCase().trim();
  
  if (s1 === s2) return 1;
  
  // Kiểm tra xem chuỗi này có phải là tiền tố của chuỗi khác không
  if (s1.includes(s2) || s2.includes(s1)) return 0.9;
  
  // Đếm từ chung
  const words1 = s1.split(/\s+/);
  const words2 = s2.split(/\s+/);
  
  let commonWords = 0;
  for (const w1 of words1) {
    if (w1.length > 2 && words2.some(w2 => w2.includes(w1) || w1.includes(w2))) {
      commonWords++;
    }
  }
  
  return commonWords / Math.max(words1.length, words2.length);
}

// Hàm tìm chỉ số của đáp án dựa trên nội dung text
function findAnswerIndex(container, answerText) {
  const answerElements = container.querySelectorAll('div[data-region="answer-label"] div.flex-fill');
  
  for (let i = 0; i < answerElements.length; i++) {
    const text = answerElements[i].textContent.trim();
    if (text === answerText) {
      return i;
    }
    // Fuzzy matching cho trường hợp không khớp chính xác
    if (calculateSimilarity(text, answerText) > 0.8) {
      return i;
    }
  }
  
  return -1;
}

// Hàm điền đáp án
async function fillAnswers() {
  const questions = extractQuestions();
  let filled = 0;
  let notFound = 0;
  let fromAPI = 0;
  
  for (const q of questions) {
    const result = await findBestAnswer(q.text);
    
    if (result) {
      const answerIndex = findAnswerIndex(q.container, result.answer);
      
      if (answerIndex !== -1) {
        // Tìm radio button tương ứng
        const radioButtons = q.container.querySelectorAll('input[type="radio"]');
        if (radioButtons[answerIndex]) {
          radioButtons[answerIndex].click();
          radioButtons[answerIndex].checked = true;
          filled++;
          if (result.isFromAPI) {
            fromAPI++;
            console.log(`✓ Đã điền từ API câu ${q.index + 1}: ${q.text.substring(0, 50)}...`);
          } else {
            console.log(`✓ Đã điền câu ${q.index + 1}: ${q.text.substring(0, 50)}...`);
          }
        }
      } else {
        notFound++;
        console.log(`✗ Không tìm được đáp án cho: ${q.text}`);
      }
    } else {
      notFound++;
      console.log(`✗ Không tìm được câu hỏi: ${q.text}`);
    }
  }
  
  return {
    type: 'success',
    message: `✓ Hoàn thành! Đã điền ${filled} câu (${fromAPI} từ API)`,
    stats: { filled, notFound, fromAPI }
  };
}

// Hàm xóa tất cả lựa chọn
function clearAnswers() {
  const radioButtons = document.querySelectorAll('input[type="radio"]');
  let cleared = 0;
  
  radioButtons.forEach((radio) => {
    if (radio.checked && radio.value !== '-1') {
      radio.click();
      cleared++;
    }
  });
  
  return {
    type: 'success',
    message: `✓ Đã xóa ${cleared} lựa chọn`,
    stats: { filled: 0, notFound: cleared }
  };
}

// Biến flag để kiểm soát quá trình filling toàn bộ
let shouldContinueFilling = true;

// Hàm tìm và click nút "Trang tiếp"
function goToNextPage() {
  const nextBtn = document.querySelector('input[name="next"][value="Trang tiếp"]');
  if (nextBtn) {
    console.log('✓ Tìm thấy nút "Trang tiếp", click vào...');
    nextBtn.click();
    return true;
  }
  return false;
}

// Hàm chờ trang tải xong
function waitForPageLoad(timeout = 3000) {
  return new Promise((resolve) => {
    let timeWaited = 0;
    const interval = setInterval(() => {
      const questions = document.querySelectorAll('div.qtext');
      if (questions.length > 0) {
        clearInterval(interval);
        console.log(`✓ Trang tải xong, tìm thấy ${questions.length} câu hỏi`);
        resolve(true);
      }
      timeWaited += 100;
      if (timeWaited >= timeout) {
        clearInterval(interval);
        console.warn('⚠ Timeout chờ trang tải');
        resolve(false);
      }
    }, 100);
  });
}

// Hàm điền toàn bộ các trang
async function fillAllPages() {
  shouldContinueFilling = true;
  let totalFilled = 0;
  let totalNotFound = 0;
  let totalFromAPI = 0;
  let currentPage = 1;
  const maxPages = 12; // 60 câu / 5 câu = 12 trang
  
  try {
    while (shouldContinueFilling && currentPage <= maxPages) {
      console.log(`\n📄 Đang xử lý trang ${currentPage}/${maxPages}...`);
      
      // Điền đáp án trang hiện tại
      const result = await fillAnswers();
      totalFilled += result.stats.filled;
      totalNotFound += result.stats.notFound;
      totalFromAPI += result.stats.fromAPI || 0;
      
      // Tính tiến độ
      const progress = Math.floor((currentPage / maxPages) * 100);
      
      // Gửi cập nhật progress
      chrome.runtime.sendMessage({
        type: 'progress',
        progress: progress,
        message: `Đã xử lý ${currentPage}/${maxPages} trang`,
        stats: { filled: totalFilled, notFound: totalNotFound, fromAPI: totalFromAPI }
      }).catch(() => {});
      
      // Nếu không phải trang cuối cùng, chuyển sang trang tiếp
      if (currentPage < maxPages && shouldContinueFilling) {
        // Chờ 500ms trước khi click
        await new Promise(resolve => setTimeout(resolve, 500));
        
        if (goToNextPage()) {
          // Chờ trang tải xong
          await waitForPageLoad(5000);
          currentPage++;
        } else {
          console.log('✗ Không thể tìm nút "Trang tiếp", dừng lại');
          break;
        }
      } else {
        break;
      }
    }
    
    return {
      type: 'success',
      message: `✓ Hoàn thành! Tổng cộng điền ${totalFilled} câu (${totalFromAPI} từ API, ${currentPage}/${maxPages} trang)`,
      stats: { filled: totalFilled, notFound: totalNotFound, fromAPI: totalFromAPI },
      progress: 100
    };
  } catch (error) {
    console.error('✗ Lỗi:', error);
    return {
      type: 'error',
      message: `✗ Có lỗi xảy ra: ${error.message}`,
      stats: { filled: totalFilled, notFound: totalNotFound, fromAPI: totalFromAPI },
      progress: Math.floor((currentPage / maxPages) * 100)
    };
  }
}

// Hàm dừng filling
function cancelFilling() {
  shouldContinueFilling = false;
  console.log('⛔ Dừng filling');
  return {
    type: 'info',
    message: '⛔ Đã dừng quá trình điền',
    stats: { filled: 0, notFound: 0 }
  };
}

// Xử lý tin nhắn từ popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'fillAnswers') {
    const result = fillAnswers();
    sendResponse(result);
  } else if (request.action === 'clearAnswers') {
    const result = clearAnswers();
    sendResponse(result);
  } else if (request.action === 'fillAllPages') {
    fillAllPages().then(result => {
      sendResponse(result);
    });
    return true; // Để cho phép async response
  } else if (request.action === 'cancelFilling') {
    const result = cancelFilling();
    sendResponse(result);
  }
});

// Xử lý message từ background để cập nhật progress
chrome.runtime.onMessage.addListener((request) => {
  if (request.type === 'progress') {
    // Popup sẽ xử lý message này
  }
});

console.log('Quiz Auto Filler extension loaded!');
