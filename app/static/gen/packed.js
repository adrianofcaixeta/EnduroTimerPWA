document.addEventListener('DOMContentLoaded', () => {
    const downloadButton = document.getElementById('downloadButton');
    const startButton = document.getElementById('startButton');
    const pauseButton = document.getElementById('pauseButton');
    const timerDisplay = document.getElementById('timer');
    const dataDisplay = document.getElementById('dataDisplay');

    let isRunning = false;
    let time = 0;
    let interval;

    function checkExistingPDF() {
        fetch('/check-pdf')
            .then(response => response.json())
            .then(data => {
                if (data.exists) {
                    displayPDF(data.path);
                    startButton.disabled = false;
                    downloadButton.disabled = true;
                    downloadButton.textContent = 'Rota do Enduro Baixada';
                }
            });
    }

    checkExistingPDF();

    downloadButton.addEventListener('click', () => {
        downloadButton.disabled = true;
        downloadButton.textContent = 'Baixando...';

        fetch('/download-pdf')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displayPDF(data.path);
                    startButton.disabled = false;
                    downloadButton.textContent = 'Rota do Enduro Baixada';
                    downloadButton.disabled = true;
                } else {
                    alert('Erro ao baixar o PDF: ' + data.error);
                    downloadButton.textContent = 'Tentar Novamente';
                    downloadButton.disabled = false;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Erro ao baixar o arquivo');
                downloadButton.textContent = 'Tentar Novamente';
                downloadButton.disabled = false;
            });
    });

    startButton.addEventListener('click', () => {
        if (!isRunning) {
            isRunning = true;
            startButton.disabled = true;
            interval = setInterval(updateTimer, 1000);
        }
    });

    pauseButton.addEventListener('click', () => {
        if (isRunning) {
            isRunning = false;
            clearInterval(interval);
            alert(`Tempo total: ${timerDisplay.textContent}`);
        }
    });

    function updateTimer() {
        time++;
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function displayPDF(path) {
        dataDisplay.innerHTML = `<iframe src="${path}" width="100%" height="600px" id="pdfFrame"></iframe>`;
        
        const iframe = document.getElementById('pdfFrame');
        iframe.onload = () => {
            iframe.contentWindow.addEventListener('scroll', () => {
                const scrollPosition = iframe.contentWindow.scrollY;
                const scrollHeight = iframe.contentDocument.documentElement.scrollHeight;
                const clientHeight = iframe.contentDocument.documentElement.clientHeight;
                
                if (scrollPosition + clientHeight >= scrollHeight - 100) {
                    pauseButton.style.display = 'block';
                }
            });
        };
    }

    // PWA Installation
    let deferredPrompt;

    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        showInstallPromotion();
    });

    function showInstallPromotion() {
        const installBanner = document.getElementById('installBanner');
        const installButton = document.getElementById('installButton');
        
        installBanner.style.display = 'block';
        
        installButton.addEventListener('click', async () => {
            installBanner.style.display = 'none';
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to the install prompt: ${outcome}`);
            deferredPrompt = null;
        });
    }

    window.addEventListener('appinstalled', (evt) => {
        document.getElementById('installBanner').style.display = 'none';
        console.log('INSTALL: Success');
    });
});