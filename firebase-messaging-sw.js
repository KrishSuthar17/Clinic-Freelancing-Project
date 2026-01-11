importScripts("https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyCEHTsXR53kbgYEQ2TrlhqMN_2F0Gzs4TM",
  authDomain: "clinic-notifications.firebaseapp.com",
  projectId: "clinic-notifications",
  messagingSenderId: "966949240460",
  appId: "1:966949240460:web:892b509260d0d660fc05a9",
});

const messaging = firebase.messaging();

// 🔔 BACKGROUND NOTIFICATION HANDLER
messaging.onBackgroundMessage(function(payload) {
  console.log("[SW] Background message received:", payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: "/static/images/doctor-hero.jpg", // optional
  };

  self.registration.showNotification(
    notificationTitle,
    notificationOptions
  );
});
