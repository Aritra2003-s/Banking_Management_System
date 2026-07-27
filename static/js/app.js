/**
 * Secure Bank - Main Application Script (app.js)
 * Enterprise JavaScript Core covering Authentication, Customer Management,
 * Transactions, Reports, Live Validation, Security Controls, and Accessibility.
 */

document.addEventListener("DOMContentLoaded", function () {
  "use strict";

  // ==========================================
  // 0. UTILITY & HELPER FUNCTIONS
  // ==========================================

  /**
   * Sanitizes input string to prevent cross-site scripting (XSS) attacks.
   * @param {string} str - Unsanitized string.
   * @returns {string} Escaped HTML string.
   */
  window.sanitizeHTML = function (str) {
    if (typeof str !== "string") return str;
    const temp = document.createElement("div");
    temp.textContent = str;
    return temp.innerHTML;
  };

  /**
   * Formats a raw numeric string into a standardized currency representation.
   * @param {number|string} amount 
   * @returns {string} Formatted currency text.
   */
  window.formatCurrency = function (amount) {
    const num = parseFloat(amount);
    if (isNaN(num)) return "$0.00";
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2
    }).format(num);
  };

  /**
   * Creates and presents a Bootstrap-style toast notification dynamically.
   * @param {string} message - Text or HTML to display.
   * @param {string} type - Notification status ('success', 'error', 'warning', 'info').
   */
  window.showToast = function (message, type = "info") {
    let toastContainer = document.getElementById("toastContainer");
    if (!toastContainer) {
      toastContainer = document.createElement("div");
      toastContainer.id = "toastContainer";
      toastContainer.setAttribute("aria-live", "polite");
      toastContainer.setAttribute("aria-atomic", "true");
      toastContainer.style.cssText = "position: fixed; top: 20px; right: 20px; z-index: 1090; min-width: 280px;";
      document.body.appendChild(toastContainer);
    }

    const toast = document.createElement("div");
    const bgClass =
      type === "success" ? "bg-success" :
      type === "error" || type === "danger" ? "bg-danger" :
      type === "warning" ? "bg-warning text-dark" : "bg-info";

    const textClass = type === "warning" ? "text-dark" : "text-white";

    toast.className = `toast show align-items-center ${textClass} ${bgClass} border-0 mb-2 shadow-lg`;
    toast.setAttribute("role", "alert");
    toast.style.cssText = "transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out; opacity: 1;";

    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body fw-medium">${window.sanitizeHTML(message)}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" aria-label="Close"></button>
      </div>
    `;

    const closeBtn = toast.querySelector(".btn-close");
    if (type === "warning") closeBtn.classList.remove("btn-close-white");
    closeBtn.addEventListener("click", function () {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 300);
    });

    toastContainer.appendChild(toast);

    setTimeout(() => {
      if (toast.parentNode) {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
      }
    }, 4500);
  };

  // Inline Validation Helpers
  function setError(input, message) {
    if (!input) return;
    const parent = input.parentElement;
    let errorDisplay = parent.querySelector(".invalid-feedback");
    if (!errorDisplay) {
      errorDisplay = document.createElement("small");
      errorDisplay.className = "invalid-feedback text-danger d-block mt-1 fw-semibold";
      parent.appendChild(errorDisplay);
    }
    errorDisplay.innerText = message;
    input.classList.add("is-invalid");
    input.classList.remove("is-valid");
    input.setAttribute("aria-invalid", "true");
  }

  function setSuccess(input) {
    if (!input) return;
    const parent = input.parentElement;
    const errorDisplay = parent.querySelector(".invalid-feedback");
    if (errorDisplay) {
      errorDisplay.innerText = "";
    }
    input.classList.remove("is-invalid");
    input.classList.add("is-valid");
    input.removeAttribute("aria-invalid");
  }

  // ==========================================
  // 1. FLASH MESSAGES AUTO-DISMISS
  // ==========================================
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  if (alerts.length > 0) {
    setTimeout(function () {
      alerts.forEach(function (alert) {
        alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        alert.style.opacity = "0";
        alert.style.transform = "translateY(-8px)";
        setTimeout(() => alert.remove(), 500);
      });
    }, 5000);
  }

  // ==========================================
  // 2. DARK MODE TOGGLE & PERSISTENCE
  // ==========================================
  const darkModeBtn = document.getElementById("darkModeBtn");
  const themeIcon = document.getElementById("themeIcon");
  const themeText = document.getElementById("themeText");

  const savedTheme = localStorage.getItem("secureBankTheme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
    if (themeIcon) themeIcon.classList.replace("fa-moon", "fa-sun");
    if (themeText) themeText.textContent = "Light Mode";
  }

  if (darkModeBtn) {
    darkModeBtn.addEventListener("click", function () {
      document.body.classList.toggle("dark-mode");
      const isDarkMode = document.body.classList.contains("dark-mode");

      if (isDarkMode) {
        localStorage.setItem("secureBankTheme", "dark");
        if (themeIcon) themeIcon.classList.replace("fa-moon", "fa-sun");
        if (themeText) themeText.textContent = "Light Mode";
        window.showToast("Dark mode enabled", "info");
      } else {
        localStorage.setItem("secureBankTheme", "light");
        if (themeIcon) themeIcon.classList.replace("fa-sun", "fa-moon");
        if (themeText) themeText.textContent = "Dark Mode";
        window.showToast("Light mode enabled", "info");
      }
    });
  }

  // ==========================================
  // 3. DYNAMIC PASSWORD VISIBILITY TOGGLE
  // ==========================================
  const singleToggleBtn = document.getElementById("togglePassword");
  const singlePasswordInput = document.getElementById("password");
  const singleToggleIcon = document.getElementById("toggleIcon");

  if (singleToggleBtn && singlePasswordInput) {
    singleToggleBtn.addEventListener("click", function () {
      const isPwd = singlePasswordInput.getAttribute("type") === "password";
      singlePasswordInput.setAttribute("type", isPwd ? "text" : "password");
      if (singleToggleIcon) {
        singleToggleIcon.classList.toggle("fa-eye");
        singleToggleIcon.classList.toggle("fa-eye-slash");
      }
    });
  }

  const multiToggles = document.querySelectorAll(".toggle-password[data-target]");
  multiToggles.forEach(function (toggle) {
    toggle.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const targetInput = document.getElementById(targetId);
      const icon = this.querySelector("i");

      if (targetInput) {
        const isPassword = targetInput.getAttribute("type") === "password";
        targetInput.setAttribute("type", isPassword ? "text" : "password");
        if (icon) {
          icon.classList.toggle("fa-eye");
          icon.classList.toggle("fa-eye-slash");
        }
      }
    });
  });

  // ==========================================
  // 4. LOGIN FORM VALIDATION & HANDLING
  // ==========================================
  const loginForm = document.getElementById("loginForm") || document.querySelector('form[action*="login"]');
  if (loginForm) {
    const loginUser = loginForm.querySelector('#username, input[name="username"], input[type="email"]');
    const loginPass = loginForm.querySelector('#password, input[type="password"]');

    if (loginUser) {
      loginUser.addEventListener("input", function () {
        if (!this.value.trim()) {
          setError(this, "Username or Email is required.");
        } else {
          setSuccess(this);
        }
      });
    }

    if (loginPass) {
      loginPass.addEventListener("input", function () {
        if (!this.value) {
          setError(this, "Password cannot be empty.");
        } else {
          setSuccess(this);
        }
      });
    }

    loginForm.addEventListener("submit", function (e) {
      let valid = true;
      if (loginUser && !loginUser.value.trim()) {
        setError(loginUser, "Username or Email is required.");
        valid = false;
      }
      if (loginPass && !loginPass.value) {
        setError(loginPass, "Password cannot be empty.");
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
        window.showToast("Please provide all login credentials.", "error");
        return false;
      }

      const submitBtn = loginForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        if (submitBtn.disabled) {
          e.preventDefault();
          return false;
        }
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Authenticating...';
      }
    });
  }

  // ==========================================
  // 5. REGISTER FORM & REAL-TIME VALIDATION
  // ==========================================
  const regForm = document.getElementById("registerForm");
  if (regForm) {
    const regEmail = document.getElementById("email");
    const regDob = document.getElementById("dob");
    const regPhone = document.getElementById("phone");
    const regPan = document.getElementById("pan");
    const regAadhaar = document.getElementById("aadhaar");
    const regPassword = document.getElementById("password");
    const regConfirmPassword = document.getElementById("confirmPassword");
    const strengthMeter = document.getElementById("passwordStrength");
    const strengthText = document.getElementById("strengthText");

    // Email Validation
    if (regEmail) {
      regEmail.addEventListener("input", function () {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!this.value.trim()) {
          setError(this, "Email address is required.");
        } else if (!emailRegex.test(this.value.trim())) {
          setError(this, "Please enter a valid email address (e.g. user@domain.com).");
        } else {
          setSuccess(this);
        }
      });
    }

    // Age (18+) Validation
    if (regDob) {
      regDob.addEventListener("change", function () {
        if (!this.value) {
          setError(this, "Date of Birth is required.");
          return;
        }
        const dob = new Date(this.value);
        const today = new Date();
        let age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate())) {
          age--;
        }

        if (age < 18) {
          setError(this, "Account holder must be at least 18 years old.");
        } else {
          setSuccess(this);
        }
      });
    }

    // Phone Validation (Numbers Only, Max 10 Digits)
    if (regPhone) {
      regPhone.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, 10);
        const phoneRegex = /^[6-9]\d{9}$/;
        if (!this.value) {
          setError(this, "Phone number is required.");
        } else if (!phoneRegex.test(this.value)) {
          setError(this, "Enter a valid 10-digit mobile number starting with 6-9.");
        } else {
          setSuccess(this);
        }
      });
    }

    // PAN Validation (5 Letters, 4 Digits, 1 Letter)
    if (regPan) {
      regPan.addEventListener("input", function () {
        this.value = this.value.toUpperCase().slice(0, 10);
        const panRegex = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
        if (!this.value) {
          setError(this, "PAN identifier is required.");
        } else if (!panRegex.test(this.value)) {
          setError(this, "Format: 5 letters, 4 digits, 1 letter (e.g. ABCDE1234F).");
        } else {
          setSuccess(this);
        }
      });
    }

    // National Identity Number Validation (12 Digits)
    if (regAadhaar) {
      regAadhaar.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, 12);
        const aadhaarRegex = /^\d{12}$/;
        if (!this.value) {
          setError(this, "National Identity Number is required.");
        } else if (!aadhaarRegex.test(this.value)) {
          setError(this, "National Identity Number must be exactly 12 digits.");
        } else {
          setSuccess(this);
        }
      });
    }

    // Live Password Strength Assessment
    if (regPassword) {
      regPassword.addEventListener("input", function () {
        const val = this.value;
        let score = 0;

        if (val.length >= 8) score++;
        if (/[A-Z]/.test(val)) score++;
        if (/[a-z]/.test(val)) score++;
        if (/[0-9]/.test(val)) score++;
        if (/[^A-Za-z0-9]/.test(val)) score++;

        if (strengthMeter) {
          strengthMeter.style.width = (score * 20) + "%";
          if (score <= 2) {
            strengthMeter.className = "progress-bar bg-danger";
            if (strengthText) strengthText.textContent = "Weak";
          } else if (score === 3 || score === 4) {
            strengthMeter.className = "progress-bar bg-warning";
            if (strengthText) strengthText.textContent = "Moderate";
          } else {
            strengthMeter.className = "progress-bar bg-success";
            if (strengthText) strengthText.textContent = "Strong";
          }
        }

        if (val.length < 8) {
          setError(this, "Password must be at least 8 characters long.");
        } else {
          setSuccess(this);
        }

        if (regConfirmPassword && regConfirmPassword.value) {
          regConfirmPassword.dispatchEvent(new Event("input"));
        }
      });
    }

    // Password Match Check
    if (regConfirmPassword && regPassword) {
      regConfirmPassword.addEventListener("input", function () {
        if (!this.value) {
          setError(this, "Please confirm your password.");
        } else if (this.value !== regPassword.value) {
          setError(this, "Passwords do not match.");
        } else {
          setSuccess(this);
        }
      });
    }

    // Submit Validation & Spinners
    regForm.addEventListener("submit", function (e) {
      let isValid = true;
      const fields = [regEmail, regDob, regPhone, regPan, regAadhaar, regPassword, regConfirmPassword];

      fields.forEach(function (field) {
        if (field) {
          field.dispatchEvent(new Event(field.tagName === "SELECT" || field.type === "date" ? "change" : "input"));
          if (field.classList.contains("is-invalid")) {
            isValid = false;
          }
        }
      });

      if (!isValid) {
        e.preventDefault();
        window.showToast("Please correct highlighted errors before submitting.", "error");
        const firstInvalid = regForm.querySelector(".is-invalid");
        if (firstInvalid) firstInvalid.focus();
        return false;
      }

      const submitBtn = regForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        if (submitBtn.disabled) {
          e.preventDefault();
          return false;
        }
        submitBtn.disabled = true;
        submitBtn.classList.add("btn-success");
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Registering Account...';
        window.showToast("Valid form submission. Processing registration...", "success");
      }
    });
  }

  // ==========================================
  // 6. ACCOUNT NUMBER FORMATTING & TRANSACTION FORMS
  // ==========================================
  const accountInputs = document.querySelectorAll(
    'input[name="account_number"], input[name="sender_account_no"], input[name="receiver_account_no"], #account_number'
  );
  accountInputs.forEach(function (input) {
    input.addEventListener("input", function () {
      this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "").trim();
    });
  });

  const amountInputs = document.querySelectorAll('input[name="amount"], #amount');
  amountInputs.forEach(function (input) {
    input.addEventListener("input", function () {
      if (this.value < 0) this.value = Math.abs(this.value);
      if (this.value.includes(".")) {
        const parts = this.value.split(".");
        if (parts[1].length > 2) {
          this.value = `${parts[0]}.${parts[1].slice(0, 2)}`;
        }
      }
    });
  });

  // Deposit Form Handling
  const depositForm = document.querySelector('form[action*="deposit"]');
  if (depositForm) {
    depositForm.addEventListener("submit", function (e) {
      const amt = depositForm.querySelector('input[name="amount"]');
      if (amt && (parseFloat(amt.value) <= 0 || isNaN(parseFloat(amt.value)))) {
        e.preventDefault();
        setError(amt, "Deposit amount must be greater than 0.");
        window.showToast("Invalid deposit amount.", "error");
        return false;
      }
    });
  }

  // Withdraw Form Handling
  const withdrawForm = document.querySelector('form[action*="withdraw"]');
  if (withdrawForm) {
    withdrawForm.addEventListener("submit", function (e) {
      const amt = withdrawForm.querySelector('input[name="amount"]');
      if (amt && (parseFloat(amt.value) <= 0 || isNaN(parseFloat(amt.value)))) {
        e.preventDefault();
        setError(amt, "Withdrawal amount must be greater than 0.");
        window.showToast("Invalid withdrawal amount.", "error");
        return false;
      }
    });
  }

  // Transfer Form Validation
  const senderInput = document.getElementById("sender_account_no");
  const receiverInput = document.getElementById("receiver_account_no");
  const transferForm = senderInput ? senderInput.closest("form") : document.querySelector('form[action*="transfer"]');

  if (transferForm) {
    transferForm.addEventListener("submit", function (e) {
      const senderVal = senderInput ? senderInput.value.trim() : "";
      const receiverVal = receiverInput ? receiverInput.value.trim() : "";
      const amt = transferForm.querySelector('input[name="amount"]');

      let valid = true;

      if (senderInput && receiverInput && senderVal === receiverVal && senderVal !== "") {
        setError(receiverInput, "Sender and Receiver accounts cannot be identical.");
        window.showToast("Sender and Receiver account numbers match.", "error");
        valid = false;
      }

      if (amt && (parseFloat(amt.value) <= 0 || isNaN(parseFloat(amt.value)))) {
        setError(amt, "Transfer amount must be greater than 0.");
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
        return false;
      }
    });
  }

  // Financial Double-Submit Prevention
  const financialForms = document.querySelectorAll(
    'form[action*="deposit"], form[action*="withdraw"], form[action*="transfer"]'
  );
  financialForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        if (submitBtn.disabled) {
          e.preventDefault();
          return false;
        }
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Processing Transaction...';
      }
    });
  });

  // ==========================================
  // 7. MINI STATEMENT & ACCOUNT STATEMENTS
  // ==========================================
  const miniStatementBtn = document.getElementById("fetchMiniStatement");
  if (miniStatementBtn) {
    miniStatementBtn.addEventListener("click", function () {
      const accountNo = document.getElementById("account_number")?.value;
      const targetContainer = document.getElementById("miniStatementResult");

      if (!accountNo) {
        window.showToast("Please select or enter an account number first.", "warning");
        return;
      }

      miniStatementBtn.disabled = true;
      miniStatementBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Loading...';

      // Simulated Fetch Interaction
      setTimeout(function () {
        miniStatementBtn.disabled = false;
        miniStatementBtn.innerHTML = '<i class="fa-solid fa-clock-rotate-left me-2"></i> View Recent Activity';

        if (targetContainer) {
          targetContainer.innerHTML = `
            <div class="table-responsive mt-3">
              <table class="table table-sm table-hover align-middle">
                <thead class="table-light">
                  <tr><th>Date</th><th>Type</th><th>Amount</th><th>Status</th></tr>
                </thead>
                <tbody>
                  <tr><td>${new Date().toLocaleDateString()}</td><td><span class="badge bg-success">Deposit</span></td><td>+$500.00</td><td>Completed</td></tr>
                  <tr><td>${new Date().toLocaleDateString()}</td><td><span class="badge bg-danger">Transfer</span></td><td>-$120.00</td><td>Completed</td></tr>
                </tbody>
              </table>
            </div>
          `;
        }
        window.showToast("Mini statement updated.", "success");
      }, 800);
    });
  }

  // Date Range Validation (Statements & Reports)
  const startDateInput = document.getElementById("start_date");
  const endDateInput = document.getElementById("end_date");
  const statementForm = startDateInput ? startDateInput.closest("form") : null;

  if (statementForm && startDateInput && endDateInput) {
    statementForm.addEventListener("submit", function (e) {
      const startDate = startDateInput.value;
      const endDate = endDateInput.value;

      if (startDate && endDate && startDate > endDate) {
        e.preventDefault();
        setError(startDateInput, "Start Date cannot be after End Date.");
        window.showToast("Date Range Error: Start Date is after End Date.", "error");
        startDateInput.focus();
      }
    });
  }

  // ==========================================
  // 8. REPORTS, SEARCH FILTERS & TABS
  // ==========================================
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  if (tabButtons.length > 0 && tabPanes.length > 0) {
    tabButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const targetTabId = this.getAttribute("data-tab");

        // Remove active state from all buttons & panes
        tabButtons.forEach((btn) => btn.classList.remove("active"));
        tabPanes.forEach((pane) => pane.classList.remove("active"));

        // Activate selected button & target pane
        this.classList.add("active");
        const targetPane = document.getElementById(targetTabId);
        if (targetPane) {
          targetPane.classList.add("active");
        }

        // Update URL query parameter without page reload
        if (targetTabId) {
          const tabName = targetTabId.replace("Tab", "");
          const currentUrl = new URL(window.location.href);
          currentUrl.searchParams.set("tab", tabName);
          window.history.replaceState({}, "", currentUrl);
        }
      });
    });
  }

  // Client-Side Table Search/Filter Component
const tableSearchInput = document.getElementById("tableSearchInput");
  if (tableSearchInput) {
    tableSearchInput.addEventListener("keyup", function () {
      const query = this.value.toLowerCase();
      const targetTable = document.querySelector(this.getAttribute("data-target") || "table");
      if (targetTable) {
        const rows = targetTable.querySelectorAll("tbody tr");
        rows.forEach(function (row) {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(query) ? "" : "none";
        });
      }
    });
  }

  // TRANSACTION FILTER & DATE VALIDATION
  
  const filterForm = document.getElementById("transactionFilterForm");
  const startDateInput = document.getElementById("start_date");
  const endDateInput = document.getElementById("end_date");
  const txnTypeSelect = document.getElementById("txn_type");
  const excelExportBtn = document.querySelector('a[href*="export_transactions_excel"]');

  if (filterForm && startDateInput && endDateInput) {
    
    // Prevent invalid date submissions
    filterForm.addEventListener("submit", function (e) {
      const startDate = startDateInput.value;
      const endDate = endDateInput.value;

      if (startDate && endDate && startDate > endDate) {
        e.preventDefault();
        alert("Filter Error: 'Start Date' cannot be after 'End Date'.");
        startDateInput.focus();
      }
    });

    // Dynamic Export Link Updater (Keeps Excel download params in sync)
    function updateExcelExportUrl() {
      if (!excelExportBtn) return;

      const baseUrl = excelExportBtn.href.split("?")[0];
      const params = new URLSearchParams();

      if (startDateInput.value) params.set("start_date", startDateInput.value);
      if (endDateInput.value) params.set("end_date", endDateInput.value);
      if (txnTypeSelect && txnTypeSelect.value) params.set("txn_type", txnTypeSelect.value);

      excelExportBtn.href = `${baseUrl}?${params.toString()}`;
    }

    startDateInput.addEventListener("change", updateExcelExportUrl);
    endDateInput.addEventListener("change", updateExcelExportUrl);
    if (txnTypeSelect) {
      txnTypeSelect.addEventListener("change", updateExcelExportUrl);
    }
  }
  // ==========================================
  // 9. DASHBOARD WIDGETS & REFRESH LOGIC
  // ==========================================
  const widgetRefreshBtns = document.querySelectorAll(".refresh-widget");
  widgetRefreshBtns.forEach(function (btn) {
    btn.addEventListener("click", function () {
      const icon = this.querySelector("i");
      if (icon) icon.classList.add("fa-spin");

      setTimeout(() => {
        if (icon) icon.classList.remove("fa-spin");
        window.showToast("Widget data synchronized.", "info");
      }, 750);
    });
  });

  // ==========================================
  // 10. GLOBAL CONFIRMATIONS, ACCESSIBILITY & SCROLL
  // ==========================================
  // Delete & High-Risk Confirmation Interceptor
  const dangerLinks = document.querySelectorAll("a[data-confirm], button[data-confirm]");
  dangerLinks.forEach(function (element) {
    element.addEventListener("click", function (e) {
      const message = this.getAttribute("data-confirm") || "Are you sure you want to perform this critical action?";
      if (!confirm(message)) {
        e.preventDefault();
        return false;
      }
    });
  });

  // Smooth Scrolling implementation
  document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });
      }
    });
  });

  // Dynamic Keyboard Accessibility Enhancements
  const interactiveBadges = document.querySelectorAll('.clickable, [role="button"]');
  interactiveBadges.forEach(function (el) {
    if (!el.getAttribute("tabindex")) el.setAttribute("tabindex", "0");
    el.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        this.click();
      }
    });
  });

  // Global Unhandled Error Interceptor
  window.addEventListener("error", function (e) {
    console.error("SecureBank Global Exception:", e.message);
  });
});