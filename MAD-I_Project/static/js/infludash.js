document.addEventListener("DOMContentLoaded",function(){
    const requests = document.querySelectorAll('.request');
    requests.forEach(request => {
        const header = request.querySelector('.request-header');
        header.addEventListener('click', () => {
            const content = request.querySelector('.request-content');
            const options = request.querySelector('.request-options');
            const isVisible = content.style.display==='block';
            content.style.display = isVisible?'none':'block';
            options.style.display = isVisible?'none':'block';
        });
    });
});
