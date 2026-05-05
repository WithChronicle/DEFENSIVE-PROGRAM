let otpGlobal;

// kirim OTP
function kirimOTP() {
  let email = document.getElementById("email").value;

  // DEFENSIVE PROGRAMMING
  if (email === "") {
    alert("Email tidak boleh kosong!");
    return;
  }

  if (!email.includes("@")) {
    alert("Email tidak valid!");
    return;
  }

  otpGlobal = Math.floor(100000 + Math.random() * 900000);

  // simpan sementara (biar pindah halaman tetap ada)
  localStorage.setItem("otp", otpGlobal);

  alert("OTP kamu: " + otpGlobal);

  window.location.href = "verifikasi.html";
}

// verifikasi OTP
function verifikasiOTP() {
  let otpInput = document.getElementById("otpInput").value;
  let otp = localStorage.getItem("otp");

  if (otpInput === "") {
    alert("OTP tidak boleh kosong!");
    return;
  }

  if (otpInput.length != 6) {
    alert("OTP harus 6 digit!");
    return;
  }

  if (otpInput == otp) {
    alert("Login berhasil!");
    window.location.href = "dashboard.html";
  } else {
    alert("OTP salah!");
  }
}
function showPage(id) {
  let pages = document.querySelectorAll(".content");

  pages.forEach(p => p.classList.remove("active"));

  document.getElementById(id).classList.add("active");
}