// Optional: keep this function if you call it elsewhere
function downloadThankYou() {
    if (window.backend && window.backend.downloadThankYouFile) {
        window.backend.downloadThankYouFile();
    }
}

// Setup WebChannel
new QWebChannel(qt.webChannelTransport, function(channel) {
    window.backend = channel.objects.backend;

    // Attach click handler after backend is ready
    const downloadBtn = document.getElementById("downloadBtn");
    if (downloadBtn) {
        downloadBtn.addEventListener("click", function() {
            if (window.backend && window.backend.downloadThankYouFile) {
                window.backend.downloadThankYouFile();
            }
        });
    }
});
