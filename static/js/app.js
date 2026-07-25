/**
 * Secure Bank - Main Application Script (app.js)
 * Consolidated JavaScript for Login, Register, Customer Management,
 * Deposit, Withdraw, Transfer, Mini Statement, Account Statement, and System Reports.
 */

document.addEventListener("DOMContentLoaded", function () {

  // ==========================================
  // 1. FLASH MESSAGES AUTO-DISMISS
  // ==========================================
  const alerts = document.querySelectorAll(".alert");
  if (alerts.length > 0) {
    setTimeout(function () {
      alerts.forEach(function (alert) {
        alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        alert.style.opacity = "0";
        alert.style.transform = "translateY(-8px)";
        setTimeout(function () {
          alert.remove();
        }, 500);
      });
    }, 5000); // Automatically disappears after 5 seconds
  }

  // ==========================================
  // 2. DYNAMIC PASSWORD VISIBILITY TOGGLE
  // ==========================================
  // Single Field Toggle (login.html)
  const singleToggleBtn = document.getElementById("togglePassword");
  const singlePasswordInput = document.getElementById("password");
  const singleToggleIcon = document.getElementById("toggleIcon");

  if (singleToggleBtn && singlePasswordInput) {
    singleToggleBtn.addEventListener("click", function () {
      const type = singlePasswordInput.getAttribute("type") === "password" ? "text" : "password";
      singlePasswordInput.setAttribute("type", type);
      if (singleToggleIcon) {
        singleToggleIcon.classList.toggle("fa-eye");
        singleToggleIcon.classList.toggle("fa-eye-slash");
      }
    });
  }

  // Multi-Field Toggles (register.html, edit_customer.html)
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
  // 3. DARK MODE TOGGLE & PERSISTENCE
  // ==========================================
  const darkModeBtn = document.getElementById("darkModeBtn");
  const themeIcon = document.getElementById("themeIcon");
  const themeText = document.getElementById("themeText");

  // Check saved theme preference on page load
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
      } else {
        localStorage.setItem("secureBankTheme", "light");
        if (themeIcon) themeIcon.classList.replace("fa-sun", "fa-moon");
        if (themeText) themeText.textContent = "Dark Mode";
      }
    });
  }

  // ==========================================
  // 4. GENERAL FORM VALIDATION & FORMATTING
  // ==========================================
  
  // National Identity Number Input Formatting (Numbers Only, Max 12 Digits)
  const idInput = document.getElementById("aadhaar");
  if (idInput) {
    idInput.addEventListener("input", function () {
      this.value = this.value.replace(/\D/g, "").slice(0, 12);
    });
  }

  // Tax Identifier Formatting (Uppercase, Max 10 Characters)
  const panInput = document.getElementById("pan");
  if (panInput) {
    panInput.addEventListener("input", function () {
      this.value = this.value.toUpperCase().slice(0, 10);
    });
  }

  // Phone Number Formatting (Numbers Only, Max 10 Digits)
  const phoneInput = document.getElementById("phone");
  if (phoneInput) {
    phoneInput.addEventListener("input", function () {
      this.value = this.value.replace(/\D/g, "").slice(0, 10);
    });
  }

  // Password Confirmation Validation (register.html)
  const registerForm = document.getElementById("registerForm");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirmPassword");

  if (registerForm && passwordInput && confirmPasswordInput) {
    registerForm.addEventListener("submit", function (e) {
      if (passwordInput.value !== confirmPasswordInput.value) {
        e.preventDefault();
        alert("Passwords do not match. Please verify your password entry.");
        confirmPasswordInput.focus();
      }
    });
  }

  // ==========================================
  // 5. ACCOUNT & TRANSACTION FORM HANDLERS
  // ==========================================

  // Auto-uppercase all Account Number fields
  const accountInputs = document.querySelectorAll(
    'input[name="account_number"], input[name="sender_account_no"], input[name="receiver_account_no"]'
  );
  accountInputs.forEach(function (input) {
    input.addEventListener("input", function () {
      this.value = this.value.toUpperCase().trim();
    });
  });

  // Amount input formatting (Deposit / Withdraw / Transfer)
  const amountInputs = document.querySelectorAll('input[name="amount"]');
  amountInputs.forEach(function (input) {
    input.addEventListener("input", function () {
      // Remove negative signs if entered
      if (this.value < 0) {
        this.value = Math.abs(this.value);
      }
      // Enforce 2 decimal places if needed
      if (this.value.includes(".")) {
        const parts = this.value.split(".");
        if (parts[1].length > 2) {
          this.value = `${parts[0]}.${parts[1].slice(0, 2)}`;
        }
      }
    });
  });

  // Transfer Page Validation (transfer.html)
  const senderInput = document.getElementById("sender_account_no");
  const receiverInput = document.getElementById("receiver_account_no");
  const transferForm = senderInput ? senderInput.closest("form") : null;

  if (transferForm && senderInput && receiverInput) {
    transferForm.addEventListener("submit", function (e) {
      const senderVal = senderInput.value.trim();
      const receiverVal = receiverInput.value.trim();

      if (senderVal === receiverVal && senderVal !== "") {
        e.preventDefault();
        alert("Sender and Receiver account numbers cannot be identical.");
        receiverInput.focus();
      }
    });
  }

  // Double-Submit Protection on Financial Forms (Deposit, Withdraw, Transfer)
  const financialForms = document.querySelectorAll(
    'form[action*="deposit"], form[action*="withdraw"], form[action*="transfer"]'
  );
  financialForms.forEach(function (form) {
    form.addEventListener("submit", function () {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
      }
    });
  });

  // ==========================================
  // 6. STATEMENT & REPORT DATE RANGE VALIDATIONS
  // ==========================================
  // Account Statement Filter (statement.html)
  const startDateInput = document.getElementById("start_date");
  const endDateInput = document.getElementById("end_date");
  const statementForm = startDateInput ? startDateInput.closest("form") : null;

  if (statementForm && startDateInput && endDateInput) {
    statementForm.addEventListener("submit", function (e) {
      const startDate = startDateInput.value;
      const endDate = endDateInput.value;

      if (startDate && endDate && startDate > endDate) {
        e.preventDefault();
        alert("Start Date cannot be later than End Date.");
        startDateInput.focus();
      }
    });
  }

  // System Reports Filter (reports.html)
  const reportFilterForm = document.getElementById("transactionFilterForm");
  if (reportFilterForm) {
    const reportStartDate = reportFilterForm.querySelector('#start_date');
    const reportEndDate = reportFilterForm.querySelector('#end_date');

    reportFilterForm.addEventListener("submit", function (e) {
      if (reportStartDate && reportEndDate) {
        const startVal = reportStartDate.value;
        const endVal = reportEndDate.value;

        if (startVal && endVal && startVal > endVal) {
          e.preventDefault();
          alert("Filter Error: 'Start Date' cannot be set after 'End Date'.");
          reportStartDate.focus();
        }
      }
    });
  }

  // ==========================================
  // 7. SYSTEM REPORTS TAB SWITCHING (reports.html)
  // ==========================================
  const tabButtons = document.querySelectorAll(".tab-btn");
  const tabPanes = document.querySelectorAll(".tab-pane");

  if (tabButtons.length > 0 && tabPanes.length > 0) {
    tabButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const targetTabId = this.getAttribute("data-tab");

        // Deactivate all buttons & hide all panes
        tabButtons.forEach((btn) => btn.classList.remove("active"));
        tabPanes.forEach((pane) => pane.classList.remove("active"));

        // Activate selected button & pane
        this.classList.add("active");
        const targetPane = document.getElementById(targetTabId);
        if (targetPane) {
          targetPane.classList.add("active");
        }
      });
    });
  }

  // ==========================================
  // 8. GLOBAL CONFIRMATION DIALOGS
  // ==========================================
  const dangerLinks = document.querySelectorAll("a[data-confirm]");
  dangerLinks.forEach(function (link) {
    link.addEventListener("click", function (e) {
      const message = this.getAttribute("data-confirm") || "Are you sure you want to perform this action?";
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

});