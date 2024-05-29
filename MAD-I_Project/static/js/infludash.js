function toggle1(){
    element = document.getElementById('banuser');
    element1 = document.getElementById('adreq');
    element2 = document.getElementById('campaignreq');
    element3 = document.getElementById('stats');
    element.style.display = 'block';
    element1.style.display = 'none';
    element2.style.display = 'none';
    element3.style.display = 'none';
}
function toggle2(){
    element = document.getElementById('banuser');
    element1 = document.getElementById('adreq');
    element2 = document.getElementById('campaignreq');
    element3 = document.getElementById('stats');
    element.style.display = 'none';
    element1.style.display = 'block';
    element2.style.display = 'none';
    element3.style.display = 'none';
}
function toggle3(){
    element = document.getElementById('banuser');
    element1 = document.getElementById('adreq');
    element2 = document.getElementById('campaignreq');
    element3 = document.getElementById('stats');
    element.style.display = 'none';
    element1.style.display = 'none';
    element2.style.display = 'block';
    element3.style.display = 'none';
}
function toggle4(){
    element = document.getElementById('banuser');
    element1 = document.getElementById('adreq');
    element2 = document.getElementById('campaignreq');
    element3 = document.getElementById('stats');
    element.style.display = 'none';
    element1.style.display = 'none';
    element2.style.display = 'none';
    element3.style.display = 'block';
}
document.addEventListener("DOMContentLoaded",function(){
    const requests = document.querySelectorAll('.request');
    requests.forEach(request => {
        const header = request.querySelector('.request-header');
        header.addEventListener('click', () => {
            const content = request.querySelector('.request-content');
            const options = request.querySelector('.request-options');
            const isVisible = content.style.display==='block';
            if(content.style.display==='block'){
                content.style.display = 'none';
                options.style.display = 'none';
            }
            else{
                content.style.display = 'block';
                options.style.display = 'block';
            }
        });
    });
});
function change() {
    var type = document.getElementById("type").value;
    var influencerInput = document.getElementById("influencer-input");
    var sponsorInput = document.getElementById("sponsor-input");
    if (type === "influencer") {
        influencerInput.style.display = "block";
        sponsorInput.style.display = "none";
    } else if (type === "sponsor") {
        sponsorInput.style.display = "block";
        influencerInput.style.display = "none";
    } else {
        influencerInput.style.display = "none";
        sponsorInput.style.display = "none";
    }
}