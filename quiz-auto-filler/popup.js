let isFilling = false;

// Lắng nghe message từ content script về progress
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'progress') {
    showStatus(request);
  }
});

document.getElementById('fillBtn').addEventListener('click', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {action: 'fillAnswers'}, (response) => {
      showStatus(response);
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
    chrome.tabs.sendMessage(tabs[0].id, {action: 'fillAllPages'}, (response) => {
      showStatus(response);
      resetUI();
    });
  });
});

document.getElementById('clearBtn').addEventListener('click', () => {
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {action: 'clearAnswers'}, (response) => {
      showStatus(response);
    });
  });
});

document.getElementById('cancelBtn').addEventListener('click', () => {
  isFilling = false;
  chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {action: 'cancelFilling'}, (response) => {
      showStatus(response);
      resetUI();
    });
  });
});

function showStatus(response) {
  const statusEl = document.getElementById('status');
  const statsEl = document.getElementById('stats');
  
  statusEl.textContent = response.message;
  statusEl.className = response.type;
  
  if (response.stats) {
    statsEl.textContent = `✓ Điền: ${response.stats.filled} | ✗ Không tìm: ${response.stats.notFound}`;
  }
  
  if (response.progress !== undefined) {
    const progressEl = document.getElementById('progress');
    progressEl.style.width = response.progress + '%';
    progressEl.textContent = response.progress + '%';
  }
  
  if (response.type !== 'success' && response.type !== 'info') {
    setTimeout(() => {
      statusEl.className = '';
    }, 3000);
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


