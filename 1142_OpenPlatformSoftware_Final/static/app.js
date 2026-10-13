const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-text");

// Tab 切換元素
const tabChat = document.getElementById("tab-chat");
const tabDb = document.getElementById("tab-db");
const chatView = document.getElementById("chat-view");
const dbView = document.getElementById("db-view");

// Modal 彈窗元素
const faqModal = document.getElementById("faq-modal");
const modalClose = document.getElementById("modal-close");
const modalCategory = document.getElementById("modal-category");
const modalQuestion = document.getElementById("modal-question");
const modalAnswer = document.getElementById("modal-answer");
const modalId = document.getElementById("modal-id");
const modalUpdated = document.getElementById("modal-updated");

// 資料庫篩選元素
const dropdown = document.getElementById("db-category-dropdown");
const trigger = dropdown.querySelector(".multiselect-trigger");
const triggerText = dropdown.querySelector(".trigger-text");
const checkboxList = document.getElementById("db-checkbox-list");
const btnAll = dropdown.querySelector(".btn-action-all");
const btnNone = dropdown.querySelector(".btn-action-none");

// 資料庫搜尋元素
const dbSearchInput = document.getElementById("db-search-input");
const btnDbSearch = document.getElementById("btn-db-search");
const dbResultsCount = document.getElementById("db-results-count");
const dbResultsList = document.getElementById("db-results-list");

// 新增：欄位搜尋選單元素
const fieldDropdown = document.getElementById("db-field-dropdown");
const fieldTrigger = fieldDropdown.querySelector(".select-trigger");
const fieldTriggerText = fieldDropdown.querySelector(".field-trigger-text");
const fieldOptions = fieldDropdown.querySelectorAll(".select-option");

// 新增：分頁與每頁筆數選擇器元素
const dbPageSizeContainer = document.getElementById("db-page-size-container");
const dbPageSizeSelect = document.getElementById("db-page-size-select");
const dbPagination = document.getElementById("db-pagination");

// 新增：側邊欄與清除歷史 DOM 元素
const sidebar = document.querySelector(".sidebar");
const btnSidebarCollapse = document.getElementById("btn-sidebar-collapse");
const btnSidebarExpand = document.getElementById("btn-sidebar-expand");
const btnClearChat = document.getElementById("btn-clear-chat");

let isHistoryLoading = false;
let allCategories = [];
let selectedCategories = [];
let currentPage = 1;
let currentPageSize = 20;
let currentSearchField = "all";

let sessionId = localStorage.getItem("chatbot_session_id");
if (!sessionId) {
  sessionId = crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2, 15);
  localStorage.setItem("chatbot_session_id", sessionId);
}

/**
 * Adds a message to the chat log with an animation and optional citation tags.
 * @param {string} text 
 * @param {string} role 'user' or 'bot'
 * @param {boolean} isLoading Whether to show a typing indicator
 * @param {object} data The API return payload containing categories, scores, and record_id/reference_ids
 */
function addMessage(text, role, isLoading = false, data = null) {
  const message = document.createElement("div");
  message.className = `message ${role}${isLoading ? " loading" : ""}`;
  
  const textNode = document.createElement("div");
  
  if (role === "bot" && !isLoading) {
    textNode.className = "markdown-body";
    // 1. 將 [#ID] 替換為行內按鈕
    let processedText = text.replace(/\[#(\w+)\]/g, (match, id) => {
      return ` <button class="inline-citation" data-id="${id}" title="查看出處 (項次 ${id})">${id}</button> `;
    });
    
    // 2. 解析 Markdown
    const rawHtml = marked.parse(processedText);
    
    // 3. 安全過濾，允許我們自訂的 data-id 屬性
    const sanitizedHtml = DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['data-id'] });
    textNode.innerHTML = sanitizedHtml;
  } else {
    // 使用者訊息或載入中動畫，使用純文字以策安全
    textNode.style.whiteSpace = "pre-wrap";
    textNode.textContent = text;
  }
  
  message.appendChild(textNode);
  chatLog.appendChild(message);

  // 觸發淡入動畫
  requestAnimationFrame(() => {
    message.classList.add("is-visible");
  });

  // 儲存至對話歷史
  if (!isLoading && !isHistoryLoading) {
    saveMessageToHistory(role, text, data);
  }

  scrollToBottom();
  return message;
}

// 綁定行內標籤點擊事件 (Event Delegation)
chatLog.addEventListener("click", (e) => {
  const btn = e.target.closest(".inline-citation");
  if (btn) {
    const id = btn.dataset.id;
    if (id) {
      openFaqModal(id);
    }
  }
});



function scrollToBottom() {
  chatLog.scrollTo({
    top: chatLog.scrollHeight,
    behavior: "smooth"
  });
}

function setLoading() {
  return addMessage("正在檢索專利資料庫", "bot", true);
}

async function sendMessage(message) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId })
  });

  if (!response.ok) {
    throw new Error("Request failed");
  }

  return response.json();
}

// 監聽聊天表單提交
chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = chatInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  chatInput.value = "";
  chatInput.focus();

  const loadingMessage = setLoading();

  try {
    const data = await sendMessage(text);
    loadingMessage.remove();
    const answer = data.full_answer || data.answer || "抱歉，目前無法取得解答。";
    addMessage(answer, "bot", false, data);
  } catch (error) {
    loadingMessage.remove();
    addMessage("抱歉，連線發生錯誤。請稍後再試。", "bot");
  }
});

// ==========================================================================
// 彈出式視窗 (Faq Modal) 控制邏輯
// ==========================================================================
async function openFaqModal(recordId) {
  try {
    modalCategory.className = "badge badge-category";
    modalCategory.textContent = "載入中...";
    modalQuestion.textContent = "正在讀取專利資料條目...";
    modalAnswer.textContent = "正在連線智慧產權局問答資料庫...";
    modalId.textContent = recordId;
    modalUpdated.textContent = "-";
    
    faqModal.classList.add("is-visible");
    faqModal.setAttribute("aria-hidden", "false");
    
    const response = await fetch(`/api/faq/${recordId}`);
    if (!response.ok) throw new Error("Failed to fetch FAQ detail");
    
    const data = await response.json();
    modalCategory.textContent = data.category;
    modalQuestion.textContent = data.question;
    modalAnswer.textContent = data.answer;
    modalId.textContent = data.record_id;
    modalUpdated.textContent = data.updated || "無紀錄";
  } catch (error) {
    modalCategory.className = "badge badge-id";
    modalCategory.textContent = "錯誤";
    modalQuestion.textContent = "無法取得該條目內容";
    modalAnswer.textContent = "抱歉，讀取資料庫時發生連線錯誤，請稍後再試。";
  }
}

function closeFaqModal() {
  faqModal.classList.remove("is-visible");
  faqModal.setAttribute("aria-hidden", "true");
}

modalClose.addEventListener("click", closeFaqModal);

faqModal.addEventListener("click", (e) => {
  if (e.target === faqModal) {
    closeFaqModal();
  }
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && faqModal.classList.contains("is-visible")) {
    closeFaqModal();
  }
});

// ==========================================================================
// 自訂複選下拉選單與資料庫過濾
// ==========================================================================
async function loadCategories() {
  try {
    const response = await fetch("/api/db/categories");
    if (!response.ok) throw new Error("Failed to fetch categories");
    allCategories = await response.json();
    renderCategoryCheckboxes();
  } catch (error) {
    console.error("Error loading categories:", error);
    checkboxList.innerHTML = '<div style="padding: 10px; color: var(--muted); text-align: center;">無法載入類別</div>';
  }
}

function renderCategoryCheckboxes() {
  checkboxList.innerHTML = "";
  allCategories.forEach((cat, idx) => {
    const label = document.createElement("label");
    label.className = "checkbox-item";
    
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = cat;
    checkbox.id = `cat-chk-${idx}`;
    
    checkbox.addEventListener("change", () => {
      updateSelectedCategories();
    });
    
    const span = document.createElement("span");
    span.textContent = cat;
    
    label.appendChild(checkbox);
    label.appendChild(span);
    checkboxList.appendChild(label);
  });
}

function updateSelectedCategories() {
  const checkedBoxes = checkboxList.querySelectorAll('input[type="checkbox"]:checked');
  selectedCategories = Array.from(checkedBoxes).map(chk => chk.value);
  
  if (selectedCategories.length === 0) {
    triggerText.textContent = "全部類別";
  } else if (selectedCategories.length === allCategories.length) {
    triggerText.textContent = "全部類別 (已全選)";
  } else if (selectedCategories.length <= 2) {
    triggerText.textContent = selectedCategories.join(", ");
  } else {
    triggerText.textContent = `已選擇 ${selectedCategories.length} 個類別`;
  }
}

// 下拉清單展開與收起
trigger.addEventListener("click", (e) => {
  e.stopPropagation();
  dropdown.classList.toggle("active");
  fieldDropdown.classList.remove("active"); // 收起另一個下拉選單
});

// 搜尋欄位下拉選單展開與收起
fieldTrigger.addEventListener("click", (e) => {
  e.stopPropagation();
  fieldDropdown.classList.toggle("active");
  dropdown.classList.remove("active"); // 收起另一個下拉選單
});

// 點擊選項切換欄位
fieldOptions.forEach(opt => {
  opt.addEventListener("click", (e) => {
    e.stopPropagation();
    const value = opt.dataset.value;
    currentSearchField = value;
    fieldTriggerText.textContent = opt.textContent;
    fieldTriggerText.dataset.value = value;
    
    // 更新 active 樣式
    fieldOptions.forEach(o => o.classList.remove("active"));
    opt.classList.add("active");
    
    fieldDropdown.classList.remove("active");
    
    // 當切換欄位時，自動觸發搜尋
    performDbSearch(1);
  });
});

// 核心 UX 功能：點擊下拉清單外部任意位置自動收起面板
document.addEventListener("click", (e) => {
  if (!dropdown.contains(e.target)) {
    dropdown.classList.remove("active");
  }
  if (!fieldDropdown.contains(e.target)) {
    fieldDropdown.classList.remove("active");
  }
});

// 複選快捷按鈕：全選
btnAll.addEventListener("click", (e) => {
  e.stopPropagation();
  const checkboxes = checkboxList.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(chk => chk.checked = true);
  updateSelectedCategories();
});

// 複選快捷按鈕：清除
btnNone.addEventListener("click", (e) => {
  e.stopPropagation();
  const checkboxes = checkboxList.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(chk => chk.checked = false);
  updateSelectedCategories();
});

// ==========================================================================
// 資料庫搜尋與結果渲染
// ==========================================================================
async function performDbSearch(page = 1) {
  currentPage = page;
  const query = dbSearchInput.value.trim();
  const categoriesParam = selectedCategories.join(",");
  
  dbResultsCount.style.display = "block";
  dbResultsCount.textContent = "正在檢索專利資料庫...";
  dbPageSizeContainer.style.display = "none";
  dbPagination.style.display = "none";
  
  dbResultsList.innerHTML = `
    <div class="db-empty-state">
      <div class="message bot loading">正在載入資料</div>
    </div>
  `;
  
  try {
    const url = `/api/db/search?query=${encodeURIComponent(query)}&categories=${encodeURIComponent(categoriesParam)}&page=${currentPage}&pageSize=${currentPageSize}&field=${currentSearchField}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error("Search failed");
    
    const data = await response.json();
    renderDbResults(data);
  } catch (error) {
    dbResultsCount.textContent = "檢索發生錯誤";
    dbResultsList.innerHTML = `
      <div class="db-empty-state">
        <p>連線異常，無法取得資料。請稍後再試。</p>
      </div>
    `;
  }
}

function renderDbResults(data) {
  dbResultsList.innerHTML = "";
  
  if (data.results.length === 0) {
    dbResultsCount.textContent = "未找到匹配的問答條目。";
    dbPageSizeContainer.style.display = "none";
    dbPagination.style.display = "none";
    dbResultsList.innerHTML = `
      <div class="db-empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="icon-empty">
          <circle cx="11" cy="11" r="8"/>
          <path d="M21 21l-4.3-4.3"/>
        </svg>
        <p>沒有找到符合您搜尋條件的專利條目。請嘗試換個關鍵字或調整類別篩選。</p>
      </div>
    `;
    return;
  }
  
  const startNum = (data.page - 1) * data.pageSize + 1;
  const endNum = startNum + data.results.length - 1;
  dbResultsCount.textContent = `共找到 ${data.total} 筆資料，當前顯示第 ${startNum} ~ ${endNum} 筆。`;
  dbPageSizeContainer.style.display = "flex";
  
  data.results.forEach(item => {
    const card = document.createElement("div");
    card.className = "db-card";
    
    card.innerHTML = `
      <div class="db-card-header">
        <div class="db-card-badges">
          <span class="badge badge-id">項次 ${item.record_id}</span>
          <span class="badge badge-category">${item.category}</span>
        </div>
        <span class="db-card-date">${item.updated ? '更新日期：' + item.updated : ''}</span>
      </div>
      <h3 class="db-card-question">${item.question}</h3>
      <div class="db-card-footer">
        <span>查看完整解答</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"></line>
          <polyline points="12 5 19 12 12 19"></polyline>
        </svg>
      </div>
    `;
    
    card.addEventListener("click", () => {
      openFaqModal(item.record_id);
    });
    
    dbResultsList.appendChild(card);
  });
  
  // 渲染分頁
  renderPagination(data);
}

function renderPagination(data) {
  dbPagination.innerHTML = "";
  
  const total = data.total;
  const pageSize = data.pageSize;
  const page = data.page;
  const totalPages = Math.ceil(total / pageSize);
  
  if (totalPages <= 1) {
    dbPagination.style.display = "none";
    return;
  }
  
  dbPagination.style.display = "flex";
  
  // 上一頁按鈕
  const prevBtn = document.createElement("button");
  prevBtn.className = "pag-btn";
  prevBtn.type = "button";
  prevBtn.disabled = page === 1;
  prevBtn.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;">
      <polyline points="15 18 9 12 15 6"></polyline>
    </svg>
  `;
  prevBtn.addEventListener("click", () => {
    performDbSearch(page - 1);
    dbResultsList.scrollTop = 0; // 回到頂部
  });
  dbPagination.appendChild(prevBtn);
  
  // 頁碼生成邏輯 ( delta = 2 )
  const range = [];
  const delta = 2;
  
  for (let i = 1; i <= totalPages; i++) {
    if (i === 1 || i === totalPages || (i >= page - delta && i <= page + delta)) {
      range.push(i);
    }
  }
  
  let l = 0;
  range.forEach(i => {
    if (l > 0) {
      if (i - l === 2) {
        dbPagination.appendChild(createPageBtn(l + 1));
      } else if (i - l > 2) {
        const ellipsis = document.createElement("span");
        ellipsis.className = "pag-ellipsis";
        ellipsis.textContent = "...";
        dbPagination.appendChild(ellipsis);
      }
    }
    dbPagination.appendChild(createPageBtn(i, i === page));
    l = i;
  });
  
  // 下一頁按鈕
  const nextBtn = document.createElement("button");
  nextBtn.className = "pag-btn";
  nextBtn.type = "button";
  nextBtn.disabled = page === totalPages;
  nextBtn.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="width: 14px; height: 14px;">
      <polyline points="9 18 15 12 9 6"></polyline>
    </svg>
  `;
  nextBtn.addEventListener("click", () => {
    performDbSearch(page + 1);
    dbResultsList.scrollTop = 0; // 回到頂部
  });
  dbPagination.appendChild(nextBtn);
}

function createPageBtn(page, isActive = false) {
  const btn = document.createElement("button");
  btn.className = `pag-btn${isActive ? " active" : ""}`;
  btn.type = "button";
  btn.textContent = page;
  if (isActive) {
    btn.disabled = true;
  } else {
    btn.addEventListener("click", () => {
      performDbSearch(page);
      dbResultsList.scrollTop = 0; // 回到頂部
    });
  }
  return btn;
}

// 監聽每頁筆數變更
dbPageSizeSelect.addEventListener("change", () => {
  currentPageSize = parseInt(dbPageSizeSelect.value) || 20;
  performDbSearch(1);
});

btnDbSearch.addEventListener("click", () => performDbSearch(1));
dbSearchInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    performDbSearch(1);
  }
});

// ==========================================================================
// SPA Tab 切換控制
// ==========================================================================
tabChat.addEventListener("click", () => {
  tabChat.classList.add("active");
  tabDb.classList.remove("active");
  chatView.style.display = "flex";
  dbView.style.display = "none";
});

tabDb.addEventListener("click", () => {
  tabDb.classList.add("active");
  tabChat.classList.remove("active");
  chatView.style.display = "none";
  dbView.style.display = "flex";
  
  // 初次切換到資料庫時加載類別列表
  if (allCategories.length === 0) {
    loadCategories();
  }
});

// 移除原本的 Initial greeting，改由 initChat() 統一處理歡迎詞與歷史載入

// ==========================================================================
// 隨機快捷詢問 (Random Prompts) 功能
// ==========================================================================
const quickPromptsContainer = document.getElementById("quick-prompts-container");
const btnRefreshPrompts = document.getElementById("btn-refresh-prompts");

async function loadRandomPrompts() {
  // 顯示骨架屏
  quickPromptsContainer.innerHTML = `
    <div class="prompt-card-skeleton"></div>
    <div class="prompt-card-skeleton"></div>
    <div class="prompt-card-skeleton"></div>
    <div class="prompt-card-skeleton"></div>
  `;
  
  // 加上旋轉動畫
  const refreshIcon = btnRefreshPrompts ? btnRefreshPrompts.querySelector(".icon-refresh") : null;
  if (refreshIcon) {
    refreshIcon.classList.add("spinning");
  }

  try {
    const response = await fetch("/api/faq/random");
    if (!response.ok) throw new Error("Failed to fetch random FAQs");
    const data = await response.json();
    
    // 渲染卡片
    quickPromptsContainer.innerHTML = "";
    data.forEach(item => {
      const card = document.createElement("button");
      card.className = "prompt-card";
      card.type = "button";
      card.dataset.question = item.question;
      card.dataset.id = item.record_id;
      
      card.innerHTML = `
        <span class="prompt-card-category">${item.category}</span>
        <span class="prompt-card-question" title="${item.question}">${item.question}</span>
      `;
      
      quickPromptsContainer.appendChild(card);
    });
  } catch (error) {
    console.error("Error loading random prompts:", error);
    quickPromptsContainer.innerHTML = `
      <div style="padding: 12px; color: #cbd5e1; font-size: 0.85rem; text-align: center;">
        無法載入快捷問題
      </div>
    `;
  } finally {
    // 延遲移除旋轉動畫以確保視覺流暢
    setTimeout(() => {
      if (refreshIcon) {
        refreshIcon.classList.remove("spinning");
      }
    }, 800);
  }
}

// 監聽快捷卡片點擊事件 (事件委派)
if (quickPromptsContainer) {
  quickPromptsContainer.addEventListener("click", (e) => {
    const card = e.target.closest(".prompt-card");
    if (!card) return;
    
    const question = card.dataset.question;
    if (!question) return;
    
    // 切換回對話視圖 (若是當前在資料庫視圖)
    if (dbView.style.display === "flex") {
      tabChat.click();
    }
    
    // 填入問題並送出
    chatInput.value = question;
    // 直接以 submit 事件觸發
    const submitEvent = new Event("submit", { bubbles: true, cancelable: true });
    chatForm.dispatchEvent(submitEvent);
  });
}

// 監聽換一批按鈕
if (btnRefreshPrompts) {
  btnRefreshPrompts.addEventListener("click", () => {
    loadRandomPrompts();
  });
}

// ==========================================================================
// 側邊欄折疊與對話歷史持久化邏輯
// ==========================================================================

function saveMessageToHistory(role, text, data) {
  let history = localStorage.getItem("chatbot_history");
  let messages = [];
  if (history) {
    try {
      messages = JSON.parse(history);
    } catch (e) {
      messages = [];
    }
  }
  messages.push({ role, text, data });
  localStorage.setItem("chatbot_history", JSON.stringify(messages));
}

function initChat() {
  const history = localStorage.getItem("chatbot_history");
  if (history) {
    try {
      const messages = JSON.parse(history);
      if (messages && messages.length > 0) {
        isHistoryLoading = true;
        chatLog.innerHTML = "";
        messages.forEach(msg => {
          addMessage(msg.text, msg.role, false, msg.data);
        });
        isHistoryLoading = false;
        scrollToBottom();
        return;
      }
    } catch (e) {
      console.error("Failed to parse chat history:", e);
      localStorage.removeItem("chatbot_history");
    }
  }
  
  // 若無歷史，顯示預設歡迎詞
  chatLog.innerHTML = "";
  addMessage("您好！我是您的專利行政助理。您可以詢問任何關於專利申請、規費、程序或法律相關的問題。", "bot");
}

function setSidebarCollapsed(collapsed) {
  if (collapsed) {
    sidebar.classList.add("collapsed");
    btnSidebarExpand.style.display = "flex";
    localStorage.setItem("sidebar_collapsed", "true");
  } else {
    sidebar.classList.remove("collapsed");
    btnSidebarExpand.style.display = "none";
    localStorage.setItem("sidebar_collapsed", "false");
  }
}

// 側欄事件監聽
if (btnSidebarCollapse) {
  btnSidebarCollapse.addEventListener("click", () => {
    setSidebarCollapsed(true);
  });
}

if (btnSidebarExpand) {
  btnSidebarExpand.addEventListener("click", () => {
    setSidebarCollapsed(false);
  });
}

// 清除歷史按鈕監聽
if (btnClearChat) {
  btnClearChat.addEventListener("click", async () => {
    if (confirm("確定要清除所有的對話歷史紀錄嗎？")) {
      localStorage.removeItem("chatbot_history");
      if (sessionId) {
        try {
          await fetch("/api/chat/clear", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId })
          });
        } catch (e) {
          console.error("Failed to clear backend session", e);
        }
      }
      sessionId = crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).substring(2, 15);
      localStorage.setItem("chatbot_session_id", sessionId);
      chatLog.innerHTML = "";
      addMessage("您好！我是您的專利行政助理。您可以詢問任何關於專利申請、規費、程序或法律相關的問題。", "bot");
    }
  });
}

function initSidebar() {
  const isCollapsed = localStorage.getItem("sidebar_collapsed") === "true";
  setSidebarCollapsed(isCollapsed);
}

// 頁面載入時初次載入
initSidebar();
initChat();
loadRandomPrompts();
