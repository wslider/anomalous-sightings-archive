import { navBarLinks, updateFooter } from "./utils.js";

// ────────────────────────────────────────────────
// Greeting & Time
// ────────────────────────────────────────────────

const monthNames = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const createGreetingStr = (year, month, day, hour, minsPadded, amPm) => {
  return `${year} ${month} ${day} ${hour}:${minsPadded} ${amPm} local time 📍`;
};

function updateLocalTimeGreeting() {
  const now = new Date();
  const year = now.getFullYear();
  const month = monthNames[now.getMonth()];
  const day = now.getDate().toString().padStart(2, "0");
  let hour = now.getHours();
  const minsPadded = now.getMinutes().toString().padStart(2, "0");
  const amPm = hour >= 12 ? "PM" : "AM";
  hour = hour % 12 || 12; // 12-hour format (0 → 12)

  const greetingText = createGreetingStr(year, month, day, hour, minsPadded, amPm);

  const el = document.getElementById("localTimeGreeting");
  if (el) {
    el.textContent = greetingText;
  } else {
    console.warn("Element #localTimeGreeting not found");
  }
}

// ────────────────────────────────────────────────
// Initialization
// ────────────────────────────────────────────────

function init() {


  // Footer
  updateFooter();
  setInterval(updateFooter, 3600000); // 1 hour

  navBarLinks();

}

// Initialize when DOM is ready

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}