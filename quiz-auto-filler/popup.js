let isFilling = false;

// Lắng nghe message từ content script về progress
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'progress') {
    showStatus(request);
  }
});

document.getElementById('fillBtn').addEventListener('click', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (!tabs[0]) {
      showStatus({ type: 'error', message: '✗ Không tìm thấy tab', stats: { filled: 0, notFound: 0 } });
      return;
    }
    chrome.tabs.sendMessage(tabs[0].id, {action: 'fillAnswers'}, (response) => {
      if (chrome.runtime.lastError) {
        showStatus({ type: 'error', message: '✗ Content script chưa tải. Refresh trang và thử lại.', stats: { filled: 0, notFound: 0 } });
        return;
      }
      showStatus(response || { type: 'error', message: '✗ Không nhận được response', stats: { filled: 0, notFound: 0 } });
    });
  });
});

document.getElementById('fillAllBtn').addEventListener('click', () => {
  isFilling = true;
  document.getElementById('fillBtn').style.display = 'none';
  document.getElementById('fillAllBtn').style.display = 'none';
  document.getElementById('clearBtn').style.display = 'none';
  document.getElementById('cancelBtn').style.display = 'block';
  document.getElementById('progressBar').style.display = 'block';
  
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (!tabs[0]) {
      showStatus({ type: 'error', message: '✗ Không tìm thấy tab', stats: { filled: 0, notFound: 0 } });
      resetUI();
      return;
    }
    chrome.tabs.sendMessage(tabs[0].id, {action: 'fillAllPages'}, (response) => {
      if (chrome.runtime.lastError) {
        showStatus({ type: 'error', message: '✗ Content script chưa tải. Refresh trang và thử lại.', stats: { filled: 0, notFound: 0 } });
        resetUI();
        return;
      }
      showStatus(response || { type: 'error', message: '✗ Không nhận được response', stats: { filled: 0, notFound: 0 } });
      resetUI();
    });
  });
});

document.getElementById('clearBtn').addEventListener('click', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (!tabs[0]) {
      showStatus({ type: 'error', message: '✗ Không tìm thấy tab', stats: { filled: 0, notFound: 0 } });
      return;
    }
    chrome.tabs.sendMessage(tabs[0].id, {action: 'clearAnswers'}, (response) => {
      if (chrome.runtime.lastError) {
        showStatus({ type: 'error', message: '✗ Content script chưa tải. Refresh trang và thử lại.', stats: { filled: 0, notFound: 0 } });
        return;
      }
      showStatus(response || { type: 'error', message: '✗ Không nhận được response', stats: { filled: 0, notFound: 0 } });
    });
  });
});

document.getElementById('cancelBtn').addEventListener('click', () => {
  isFilling = false;
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    if (!tabs[0]) {
      showStatus({ type: 'error', message: '✗ Không tìm thấy tab', stats: { filled: 0, notFound: 0 } });
      resetUI();
      return;
    }
    chrome.tabs.sendMessage(tabs[0].id, {action: 'cancelFilling'}, (response) => {
      if (chrome.runtime.lastError) {
        showStatus({ type: 'error', message: '✗ Content script chưa tải.', stats: { filled: 0, notFound: 0 } });
        resetUI();
        return;
      }
      showStatus(response || { type: 'error', message: '✗ Không nhận được response', stats: { filled: 0, notFound: 0 } });
      resetUI();
    });
  });
});

function showStatus(response) {
  try {
    if (!response) return;
    
    const statusEl = document.getElementById('status');
    const statsEl = document.getElementById('stats');
    
    if (!statusEl || !statsEl) return;
    
    statusEl.textContent = response.message || 'Có lỗi xảy ra';
    statusEl.className = response.type || 'error';
    
    if (response.stats && response.stats.filled !== undefined) {
      let statsText = `Điền: ${response.stats.filled} | Không tìm thấy: ${response.stats.notFound}`;
      if (response.stats.fromAPI !== undefined) {
        statsText += ` | Từ API: ${response.stats.fromAPI}`;
      }
      statsEl.textContent = statsText;
    }
    
    if (response.progress !== undefined) {
      const progressEl = document.getElementById('progress');
      if (progressEl) {
        progressEl.style.width = response.progress + '%';
        progressEl.textContent = response.progress + '%';
      }
    }
    
    if (response.type && response.type !== 'success' && response.type !== 'info') {
      setTimeout(() => {
        statusEl.className = '';
      }, 3000);
    }
  } catch (error) {
    console.error('Error in showStatus:', error);
  }
}

function resetUI() {
  isFilling = false;
  document.getElementById('fillBtn').style.display = 'block';
  document.getElementById('fillAllBtn').style.display = 'block';
  document.getElementById('clearBtn').style.display = 'block';
  document.getElementById('cancelBtn').style.display = 'none';
  setTimeout(() => {
    document.getElementById('progressBar').style.display = 'none';
    document.getElementById('progress').style.width = '0%';
    document.getElementById('progress').textContent = '0%';
  }, 2000);
}


